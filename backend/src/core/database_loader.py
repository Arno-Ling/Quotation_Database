"""
数据库加载器 - 扫描和加载所有零件数据
"""

from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
import time
import sys
import os

# 添加父目录到路径以支持导入
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.part import Part, LoadStatistics
from src.core.index_manager import IndexManager
from src.core.validator import DataValidator


class DatabaseLoader:
    """
    数据库加载器 - 负责扫描和加载所有零件数据
    """
    
    def __init__(self, database_path: str, validator: Optional[DataValidator] = None):
        """
        初始化数据库加载器
        
        Args:
            database_path: 数据库根目录路径
            validator: 数据验证器（可选）
        """
        self.database_path = Path(database_path)
        self.validator = validator or DataValidator()
        self.index_manager = IndexManager()
        self.parts: Dict[str, Part] = {}
    
    def load_database(self) -> LoadStatistics:
        """
        加载整个数据库
        
        Returns:
            LoadStatistics: 加载统计信息
        """
        start_time = time.time()
        
        print(f"开始加载数据库: {self.database_path}")
        
        # 扫描所有类别目录
        categories = self.scan_categories()
        print(f"发现 {len(categories)} 个类别目录")
        
        total_files = 0
        success_count = 0
        all_errors = []
        
        # 遍历每个类别
        for category_path in categories:
            category_name = category_path.name
            print(f"正在加载类别: {category_name}")
            
            parts, errors = self.load_category(category_path)
            
            total_files += len(parts) + len(errors)
            success_count += len(parts)
            all_errors.extend(errors)
            
            # 将零件添加到索引
            for part in parts:
                self.index_manager.add_part(part)
                self.parts[part.part_id] = part
            
            print(f"  - 成功: {len(parts)}, 失败: {len(errors)}")
        
        total_time_ms = (time.time() - start_time) * 1000
        
        stats = LoadStatistics(
            total_files=total_files,
            success_count=success_count,
            error_count=len(all_errors),
            total_time_ms=total_time_ms,
            errors=all_errors
        )
        
        print(f"\n加载完成: {stats}")
        print(f"索引统计: {self.index_manager.get_statistics()}")
        
        return stats
    
    def scan_categories(self) -> List[Path]:
        """
        扫描所有零件类别目录
        
        Returns:
            List[Path]: 类别目录路径列表
        """
        if not self.database_path.exists():
            print(f"警告: 数据库路径不存在: {self.database_path}")
            return []
        
        categories = []
        for item in self.database_path.iterdir():
            if item.is_dir():
                # 检查是否包含output_json目录
                json_dir = item / "output_json"
                if json_dir.exists() and json_dir.is_dir():
                    categories.append(item)
        
        return sorted(categories)
    
    def load_category(self, category_path: Path) -> Tuple[List[Part], List[Dict]]:
        """
        加载单个类别的所有零件
        
        Args:
            category_path: 类别目录路径
            
        Returns:
            Tuple[List[Part], List[Dict]]: (成功加载的零件列表, 错误列表)
        """
        category_name = category_path.name
        json_dir = category_path / "output_json"
        
        parts = []
        errors = []
        
        if not json_dir.exists():
            return parts, errors
        
        # 遍历所有JSON文件
        for json_file in json_dir.glob("*.json"):
            try:
                part = self.parse_json_file(json_file, category_name)
                if part:
                    parts.append(part)
            except Exception as e:
                error_info = {
                    "file": str(json_file),
                    "error": str(e),
                    "type": type(e).__name__
                }
                errors.append(error_info)
        
        return parts, errors
    
    def parse_json_file(self, json_path: Path, category: str) -> Optional[Part]:
        """
        解析单个JSON文件
        
        Args:
            json_path: JSON文件路径
            category: 零件类别
            
        Returns:
            Optional[Part]: 解析成功返回Part对象，失败返回None
        """
        try:
            # 读取JSON文件
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证数据
            is_valid, error_msg = self.validator.validate_json_data(data, json_path)
            if not is_valid:
                raise ValueError(f"数据验证失败: {error_msg}")
            
            # 生成part_id
            item_name = data["item_name"]
            part_id = f"{category}_{item_name}"
            
            # 解析PDF路径
            pdf_path = self._resolve_pdf_path(category, data.get("source_file", ""))
            
            # 创建Part对象
            part = Part(
                part_id=part_id,
                item_name=item_name,
                part_category=category,
                catalog_types=data.get("catalog_types", []),
                additional_codes=data.get("additional_codes", []),
                source_file=data.get("source_file", ""),
                pdf_path=pdf_path
            )
            
            return part
            
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析错误: {e}")
        except Exception as e:
            raise
    
    def _resolve_pdf_path(self, category: str, source_file: str) -> Optional[str]:
        """
        解析PDF文件路径
        
        Args:
            category: 类别名称
            source_file: 源文件名（如"第8页.pdf"）
            
        Returns:
            Optional[str]: PDF文件路径
        """
        if not source_file:
            return None
        
        # 尝试output_pdf目录
        pdf_path = self.database_path / category / "output_pdf" / source_file
        if pdf_path.exists():
            return str(pdf_path)
        
        # 尝试根目录的PDF文件
        root_pdf = self.database_path / category / f"{category}.pdf"
        if root_pdf.exists():
            return str(root_pdf)
        
        return None
    
    def get_index_manager(self) -> IndexManager:
        """
        获取索引管理器
        
        Returns:
            IndexManager: 索引管理器实例
        """
        return self.index_manager
    
    def get_all_parts(self) -> Dict[str, Part]:
        """
        获取所有零件
        
        Returns:
            Dict[str, Part]: 零件字典
        """
        return self.parts
