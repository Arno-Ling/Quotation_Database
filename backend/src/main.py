"""
FastAPI应用主入口
"""

from fastapi import FastAPI, HTTPException, Query, Path as PathParam, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List
import time
import sys
import os
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models.part import Part
from models.query import LogicOperator, QueryRequest, QueryResponse
from core.database_loader import DatabaseLoader
from core.validator import DataValidator
from core.query_engine import QueryEngine
from core.pdf_resolver import PDFResolver, PathFormat
from core.index_manager import IndexManager
from core.serializer import Serializer, ExportFormat

# 创建FastAPI应用
app = FastAPI(
    title="模具零件数据库查询系统 API",
    description="提供模具零件数据查询、浏览和管理功能",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
query_engine: Optional[QueryEngine] = None
pdf_resolver: Optional[PDFResolver] = None
index_manager: Optional[IndexManager] = None
database_loaded: bool = False


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    global query_engine, pdf_resolver, index_manager, database_loaded
    
    print("=" * 60)
    print("正在启动模具零件数据库查询系统...")
    print("=" * 60)
    
    try:
        # 数据库路径
        database_path = "../Database"
        
        # 初始化数据库加载器
        validator = DataValidator()
        loader = DatabaseLoader(database_path, validator)
        
        # 加载数据库
        print("\n正在加载数据库...")
        stats = loader.load_database()
        print(f"✓ 数据库加载完成: {stats.success_count} 个零件")
        
        # 初始化各模块
        index_manager = loader.get_index_manager()
        query_engine = QueryEngine(index_manager)
        pdf_resolver = PDFResolver(database_path, index_manager)
        
        database_loaded = True
        
        print("\n✓ 系统启动成功！")
        print(f"✓ API文档: http://localhost:8000/api/docs")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 启动失败: {e}")
        database_loaded = False


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "模具零件数据库查询系统 API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy" if database_loaded else "unhealthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "database_loaded": database_loaded,
        "total_parts": len(index_manager.parts) if index_manager else 0
    }


@app.get("/api/parts", response_model=QueryResponse)
async def query_parts(
    catalog_type: Optional[str] = Query(None, description="型号代码"),
    additional_code: Optional[str] = Query(None, description="附加代码"),
    item_name: Optional[str] = Query(None, description="零件名称关键词"),
    category: Optional[str] = Query(None, description="零件类别"),
    logic: str = Query("AND", pattern="^(AND|OR)$", description="逻辑运算符"),
    case_sensitive: bool = Query(False, description="是否大小写敏感"),
    use_regex: bool = Query(False, description="是否使用正则表达式"),
    limit: int = Query(100, ge=1, le=1000, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="结果偏移量")
):
    """
    查询零件列表
    
    支持多条件组合查询，可以按型号代码、附加代码、零件名称、类别进行查询。
    """
    if not database_loaded:
        raise HTTPException(status_code=503, detail="数据库未加载")
    
    try:
        # 构建查询参数
        catalog_types = [catalog_type] if catalog_type else None
        additional_codes = [additional_code] if additional_code else None
        
        # 执行查询
        response = query_engine.execute_query(
            catalog_types=catalog_types,
            additional_codes=additional_codes,
            item_name=item_name,
            part_category=category,
            logic=LogicOperator(logic),
            case_sensitive=case_sensitive,
            use_regex=use_regex,
            limit=limit,
            offset=offset
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/parts/{part_id}", response_model=Part)
async def get_part(part_id: str = PathParam(..., description="零件ID")):
    """获取单个零件详情"""
    if not database_loaded:
        raise HTTPException(status_code=503, detail="数据库未加载")
    
    part = index_manager.get_part(part_id)
    if not part:
        raise HTTPException(status_code=404, detail=f"零件不存在: {part_id}")
    
    return part


@app.get("/api/parts/{part_id}/pdf")
async def get_part_pdf(
    part_id: str = PathParam(..., description="零件ID"),
    format: str = Query("absolute", pattern="^(absolute|relative|url)$", description="路径格式"),
    download: bool = Query(False, description="是否直接下载文件")
):
    """
    获取零件PDF文件
    
    - format=absolute: 返回绝对路径
    - format=relative: 返回相对路径
    - format=url: 返回file:// URL
    - download=true: 直接下载PDF文件
    """
    if not database_loaded:
        raise HTTPException(status_code=503, detail="数据库未加载")
    
    pdf_path = pdf_resolver.get_pdf_path(part_id, PathFormat(format))
    
    if not pdf_path:
        raise HTTPException(status_code=404, detail=f"PDF文件不存在: {part_id}")
    
    if download:
        # 直接返回PDF文件
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=Path(pdf_path).name
        )
    else:
        # 返回PDF路径信息
        pdf_info = pdf_resolver.get_pdf_info(part_id)
        return pdf_info


@app.get("/api/categories")
async def get_categories():
    """获取所有类别"""
    if not database_loaded:
        raise HTTPException(status_code=503, detail="数据库未加载")
    
    categories = query_engine.get_all_categories()
    return {
        "total_categories": len(categories),
        "categories": categories
    }


@app.get("/api/categories/{category}/parts", response_model=QueryResponse)
async def get_category_parts(
    category: str = PathParam(..., description="类别名称"),
    limit: int = Query(100, ge=1, le=1000, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="结果偏移量")
):
    """获取指定类别的所有零件"""
    if not database_loaded:
        raise HTTPException(status_code=503, detail="数据库未加载")
    
    start_time = time.time()
    
    results = query_engine.get_parts_by_category(category)
    if not results:
        raise HTTPException(status_code=404, detail=f"类别不存在: {category}")
    
    # 分页
    total = len(results)
    paginated_results = results[offset:offset + limit]
    query_time_ms = (time.time() - start_time) * 1000
    
    return QueryResponse(
        total=total,
        limit=limit,
        offset=offset,
        results=paginated_results,
        truncated=total > limit,
        query_time_ms=query_time_ms
    )


@app.get("/api/statistics")
async def get_statistics():
    """获取统计信息"""
    if not database_loaded:
        raise HTTPException(status_code=503, detail="数据库未加载")
    
    # 索引统计
    index_stats = index_manager.get_statistics()
    
    # PDF统计
    pdf_stats = pdf_resolver.get_statistics()
    
    # 类别统计
    categories = query_engine.get_all_categories()
    category_distribution = {cat["name"]: cat["count"] for cat in categories}
    
    return {
        "total_parts": index_stats["total_parts"],
        "total_categories": index_stats["total_categories"],
        "total_catalog_types": index_stats["total_catalog_types"],
        "total_additional_codes": index_stats["total_additional_codes"],
        "pdf_coverage": {
            "pdfs_found": pdf_stats["pdfs_found"],
            "pdfs_missing": pdf_stats["pdfs_missing"],
            "coverage_percentage": pdf_stats["coverage_percentage"]
        },
        "category_distribution": category_distribution,
        "database_health": {
            "status": "healthy",
            "database_loaded": database_loaded
        }
    }


@app.get("/api/export")
async def export_data(
    format: str = Query("json", pattern="^(json|csv|excel)$", description="导出格式: json, csv, excel"),
    catalog_type: Optional[str] = Query(None, description="型号代码"),
    additional_code: Optional[str] = Query(None, description="附加代码"),
    item_name: Optional[str] = Query(None, description="零件名称关键词"),
    category: Optional[str] = Query(None, description="零件类别"),
    logic: str = Query("AND", pattern="^(AND|OR)$", description="逻辑运算符"),
    case_sensitive: bool = Query(False, description="是否大小写敏感"),
    use_regex: bool = Query(False, description="是否使用正则表达式"),
    limit: int = Query(1000, ge=1, le=10000, description="导出数量限制")
):
    """
    导出查询结果
    
    支持JSON、CSV、Excel格式导出。
    可以使用与查询端点相同的过滤参数。
    """
    if not database_loaded:
        raise HTTPException(status_code=503, detail="数据库未加载")
    
    try:
        # 验证导出格式
        if not ExportFormat.is_valid(format):
            raise HTTPException(status_code=400, detail=f"不支持的导出格式: {format}")
        
        # 执行查询
        catalog_types = [catalog_type] if catalog_type else None
        additional_codes = [additional_code] if additional_code else None
        
        # 如果没有任何查询条件，返回所有零件
        if not any([catalog_types, additional_codes, item_name, category]):
            # 获取所有零件
            all_parts = list(index_manager.parts.values())
            parts = all_parts[:limit]  # 应用限制
        else:
            # 执行查询
            response = query_engine.execute_query(
                catalog_types=catalog_types,
                additional_codes=additional_codes,
                item_name=item_name,
                part_category=category,
                logic=LogicOperator(logic),
                case_sensitive=case_sensitive,
                use_regex=use_regex,
                limit=limit,
                offset=0
            )
            
            # response是字典，获取results列表
            parts = response["results"]
        
        if not parts:
            raise HTTPException(status_code=404, detail="没有找到匹配的数据")
        
        # 添加PDF路径信息
        for part in parts:
            if not part.pdf_path:
                pdf_path = pdf_resolver.get_pdf_path(part.part_id, PathFormat.RELATIVE)
                if pdf_path:
                    part.pdf_path = pdf_path
        
        # 根据格式序列化数据
        format_lower = format.lower()
        
        if format_lower == ExportFormat.JSON:
            content = Serializer.to_json(parts)
            media_type = ExportFormat.get_content_type(format_lower)
            filename = f"parts_export_{int(time.time())}.json"
            
            return Response(
                content=content,
                media_type=media_type,
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )
        
        elif format_lower == ExportFormat.CSV:
            content = Serializer.to_csv(parts)
            media_type = ExportFormat.get_content_type(format_lower)
            filename = f"parts_export_{int(time.time())}.csv"
            
            return Response(
                content=content,
                media_type=media_type,
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )
        
        elif format_lower == ExportFormat.EXCEL:
            content = Serializer.to_excel(parts)
            media_type = ExportFormat.get_content_type(format_lower)
            filename = f"parts_export_{int(time.time())}.xlsx"
            
            return Response(
                content=content,
                media_type=media_type,
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url)
            }
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """通用异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "detail": str(exc),
                "path": str(request.url)
            }
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
