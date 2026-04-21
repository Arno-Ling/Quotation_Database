"""
数据验证器
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path


class DataValidator:
    """
    数据验证器 - 验证JSON数据的完整性和正确性
    """
    
    REQUIRED_FIELDS = ["item_name", "catalog_types", "source_file"]
    
    def validate_json_data(self, data: Dict, file_path: Path) -> Tuple[bool, Optional[str]]:
        """
        验证JSON数据
        
        Args:
            data: JSON数据字典
            file_path: 文件路径（用于错误报告）
            
        Returns:
            Tuple[bool, Optional[str]]: (是否通过验证, 错误信息)
        """
        # 检查必需字段
        missing_fields = []
        for field in self.REQUIRED_FIELDS:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # 检查字段类型
        if not isinstance(data.get("catalog_types"), list):
            return False, "Field 'catalog_types' must be a list"
        
        if "additional_codes" in data and not isinstance(data["additional_codes"], list):
            return False, "Field 'additional_codes' must be a list"
        
        # 检查字段值
        if not data.get("item_name"):
            return False, "Field 'item_name' cannot be empty"
        
        if not data.get("source_file"):
            return False, "Field 'source_file' cannot be empty"
        
        return True, None
    
    def validate_part_data(self, data: Dict, file_path: Path) -> bool:
        """
        验证零件数据完整性（简化版本，用于向后兼容）
        
        Args:
            data: JSON数据字典
            file_path: 文件路径
            
        Returns:
            bool: 验证是否通过
        """
        is_valid, _ = self.validate_json_data(data, file_path)
        return is_valid
