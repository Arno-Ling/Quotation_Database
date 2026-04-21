"""
零件数据模型
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from dataclasses import dataclass


class Part(BaseModel):
    """
    零件数据模型
    
    Attributes:
        part_id: 唯一标识符，格式：{category}_{item_name}
        item_name: 零件名称
        part_category: 零件类别
        catalog_types: 型号代码列表
        additional_codes: 附加代码列表
        source_file: 源PDF文件名
        pdf_path: PDF文件完整路径（可选）
    """
    part_id: str = Field(..., description="唯一标识符")
    item_name: str = Field(..., description="零件名称")
    part_category: str = Field(..., description="零件类别")
    catalog_types: List[str] = Field(default_factory=list, description="型号代码列表")
    additional_codes: List[str] = Field(default_factory=list, description="附加代码列表")
    source_file: str = Field(..., description="源PDF文件名")
    pdf_path: Optional[str] = Field(None, description="PDF文件完整路径")
    
    class Config:
        json_schema_extra = {
            "example": {
                "part_id": "凸模_顶料型凸模",
                "item_name": "顶料型凸模",
                "part_category": "凸模",
                "catalog_types": ["SJ", "SJV", "PJ", "PJV"],
                "additional_codes": ["PC", "WC"],
                "source_file": "第8页.pdf",
                "pdf_path": "Database/凸模/output_pdf/第8页.pdf"
            }
        }


@dataclass
class LoadStatistics:
    """
    数据加载统计信息
    
    Attributes:
        total_files: 总文件数
        success_count: 成功加载数量
        error_count: 失败数量
        total_time_ms: 总耗时（毫秒）
        errors: 错误列表
    """
    total_files: int
    success_count: int
    error_count: int
    total_time_ms: float
    errors: List[Dict[str, str]]
    
    def __str__(self) -> str:
        return (
            f"LoadStatistics(total={self.total_files}, "
            f"success={self.success_count}, "
            f"errors={self.error_count}, "
            f"time={self.total_time_ms:.2f}ms)"
        )
