"""
PDF解析器 - 定位和返回PDF文件路径
"""

from pathlib import Path
from typing import Optional, Tuple, List, Dict
from enum import Enum
import sys
import os
from urllib.parse import quote
from urllib.request import pathname2url

# 添加父目录到路径以支持导入
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.part import Part
from src.core.index_manager import IndexManager


class PathFormat(str, Enum):
    """路径格式枚举"""
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    URL = "url"


class PDFResolver:
    """
    PDF解析器 - 负责定位和返回PDF文件路径
    """
    
    def __init__(self, database_path: str, index_manager: IndexManager):
        """
        初始化PDF解析器
        
        Args:
            database_path: 数据库根目录路径
            index_manager: 索引管理器
        """
        self.database_path = Path(database_path).resolve()
        self.index = index_manager
    
    def get_pdf_path(
        self,
        part_id: str,
        format: PathFormat = PathFormat.ABSOLUTE
    ) -> Optional[str]:
        """
        获取零件PDF文件路径
        
        Args:
            part_id: 零件ID
            format: 路径格式
            
        Returns:
            Optional[str]: PDF文件路径，文件不存在返回None
        """
        # 获取零件信息
        part = self.index.get_part(part_id)
        if not part:
            return None
        
        # 解析PDF位置
        pdf_path, is_paged = self.resolve_pdf_location(part)
        if not pdf_path:
            return None
        
        # 验证文件存在
        if not self.verify_pdf_exists(pdf_path):
            return None
        
        # 转换为指定格式
        return self._format_path(pdf_path, format)
    
    def resolve_pdf_location(self, part: Part) -> Tuple[Optional[Path], bool]:
        """
        解析PDF文件位置
        
        Args:
            part: 零件对象
            
        Returns:
            Tuple[Optional[Path], bool]: (PDF路径, 是否为分页PDF)
        """
        category = part.part_category
        item_name = part.item_name
        source_file = part.source_file
        
        # 策略1: 尝试分页PDF - 使用item_name作为文件名 (优先)
        paged_pdf = self.database_path / category / "output_pdf" / f"{item_name}.pdf"
        if paged_pdf.exists() and paged_pdf.is_file():
            return paged_pdf, True
        
        # 策略2: 尝试分页PDF - 使用source_file作为文件名
        if source_file:
            paged_pdf_alt = self.database_path / category / "output_pdf" / source_file
            if paged_pdf_alt.exists() and paged_pdf_alt.is_file():
                return paged_pdf_alt, True
        
        # 策略3: 尝试源PDF
        source_pdf = self.database_path / category / f"{category}.pdf"
        if source_pdf.exists() and source_pdf.is_file():
            return source_pdf, False
        
        # 策略4: 尝试其他可能的位置
        # 有时source_file可能包含完整路径信息
        if source_file:
            alternative_pdf = self.database_path / category / source_file
            if alternative_pdf.exists() and alternative_pdf.is_file():
                return alternative_pdf, True
        
        return None, False
    
    def verify_pdf_exists(self, pdf_path: Path) -> bool:
        """
        验证PDF文件是否存在
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            bool: 文件是否存在
        """
        return pdf_path.exists() and pdf_path.is_file()
    
    def get_missing_pdfs(self) -> List[Dict[str, str]]:
        """
        获取所有缺失PDF的零件列表
        
        Returns:
            List[Dict]: 缺失PDF信息列表
        """
        missing = []
        
        for part_id, part in self.index.parts.items():
            pdf_path, _ = self.resolve_pdf_location(part)
            
            if not pdf_path or not self.verify_pdf_exists(pdf_path):
                missing.append({
                    "part_id": part_id,
                    "item_name": part.item_name,
                    "part_category": part.part_category,
                    "source_file": part.source_file,
                    "expected_path": str(self.database_path / part.part_category / "output_pdf" / part.source_file)
                })
        
        return missing
    
    def get_pdf_info(self, part_id: str) -> Optional[Dict]:
        """
        获取PDF文件的详细信息
        
        Args:
            part_id: 零件ID
            
        Returns:
            Optional[Dict]: PDF信息字典
        """
        part = self.index.get_part(part_id)
        if not part:
            return None
        
        pdf_path, is_paged = self.resolve_pdf_location(part)
        exists = pdf_path and self.verify_pdf_exists(pdf_path)
        
        info = {
            "part_id": part_id,
            "item_name": part.item_name,
            "part_category": part.part_category,
            "source_file": part.source_file,
            "pdf_exists": exists,
            "is_paged_pdf": is_paged if exists else None,
            "pdf_path_absolute": str(pdf_path) if pdf_path else None,
            "pdf_path_relative": str(pdf_path.relative_to(self.database_path.parent)) if pdf_path else None,
        }
        
        if exists and pdf_path:
            # 添加文件大小信息
            info["file_size_bytes"] = pdf_path.stat().st_size
            info["file_size_mb"] = round(pdf_path.stat().st_size / (1024 * 1024), 2)
        
        return info
    
    def get_statistics(self) -> Dict:
        """
        获取PDF文件统计信息
        
        Returns:
            Dict: 统计信息
        """
        total_parts = len(self.index.parts)
        missing_pdfs = self.get_missing_pdfs()
        
        # 统计分页PDF和源PDF
        paged_count = 0
        source_count = 0
        
        for part in self.index.parts.values():
            pdf_path, is_paged = self.resolve_pdf_location(part)
            if pdf_path and self.verify_pdf_exists(pdf_path):
                if is_paged:
                    paged_count += 1
                else:
                    source_count += 1
        
        return {
            "total_parts": total_parts,
            "pdfs_found": paged_count + source_count,
            "pdfs_missing": len(missing_pdfs),
            "paged_pdfs": paged_count,
            "source_pdfs": source_count,
            "coverage_percentage": round((paged_count + source_count) / total_parts * 100, 2) if total_parts > 0 else 0
        }
    
    def _format_path(self, pdf_path: Path, format: PathFormat) -> str:
        """
        将路径转换为指定格式
        
        Args:
            pdf_path: PDF文件路径
            format: 目标格式
            
        Returns:
            str: 格式化后的路径
        """
        if format == PathFormat.ABSOLUTE:
            return str(pdf_path.resolve())
        
        elif format == PathFormat.RELATIVE:
            try:
                # 相对于项目根目录（database_path的父目录）
                return str(pdf_path.relative_to(self.database_path.parent))
            except ValueError:
                # 如果无法计算相对路径，返回绝对路径
                return str(pdf_path.resolve())
        
        elif format == PathFormat.URL:
            # 转换为file:// URL
            abs_path = pdf_path.resolve()
            # 在Windows上需要特殊处理
            if os.name == 'nt':
                # Windows: file:///C:/path/to/file.pdf
                url_path = pathname2url(str(abs_path))
                return f"file:///{url_path}"
            else:
                # Unix: file:///path/to/file.pdf
                return f"file://{abs_path}"
        
        return str(pdf_path)
    
    def batch_get_pdf_paths(
        self,
        part_ids: List[str],
        format: PathFormat = PathFormat.ABSOLUTE
    ) -> Dict[str, Optional[str]]:
        """
        批量获取PDF路径
        
        Args:
            part_ids: 零件ID列表
            format: 路径格式
            
        Returns:
            Dict[str, Optional[str]]: 零件ID -> PDF路径的映射
        """
        result = {}
        for part_id in part_ids:
            result[part_id] = self.get_pdf_path(part_id, format)
        return result
