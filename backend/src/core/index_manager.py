"""
索引管理器 - 使用多级哈希表实现O(1)查询
"""

from typing import Dict, Set, List, Optional
from collections import defaultdict
import sys
import os

# 添加父目录到路径以支持导入
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.part import Part


class IndexManager:
    """
    索引管理器 - 维护多级哈希表索引以实现高效查询
    """
    
    def __init__(self):
        """初始化索引结构"""
        # 主索引：part_id -> Part对象
        self.parts: Dict[str, Part] = {}
        
        # 型号代码索引：catalog_type -> Set[part_id]
        self.catalog_index: Dict[str, Set[str]] = defaultdict(set)
        
        # 附加代码索引：additional_code -> Set[part_id]
        self.additional_index: Dict[str, Set[str]] = defaultdict(set)
        
        # 类别索引：category -> Set[part_id]
        self.category_index: Dict[str, Set[str]] = defaultdict(set)
        
        # 名称索引：用于模糊搜索（倒排索引）
        self.name_index: Dict[str, Set[str]] = defaultdict(set)
    
    def add_part(self, part: Part) -> None:
        """
        添加零件到索引
        
        Args:
            part: 零件对象
        """
        # 主索引
        self.parts[part.part_id] = part
        
        # 型号代码索引（支持大小写不敏感）
        for catalog in part.catalog_types:
            self.catalog_index[catalog.upper()].add(part.part_id)
            self.catalog_index[catalog.lower()].add(part.part_id)
            self.catalog_index[catalog].add(part.part_id)  # 保留原始大小写
        
        # 附加代码索引（支持大小写不敏感）
        for code in part.additional_codes:
            self.additional_index[code.upper()].add(part.part_id)
            self.additional_index[code.lower()].add(part.part_id)
            self.additional_index[code].add(part.part_id)  # 保留原始大小写
        
        # 类别索引
        self.category_index[part.part_category].add(part.part_id)
        
        # 名称倒排索引（分词）
        for token in self._tokenize(part.item_name):
            self.name_index[token].add(part.part_id)
    
    def remove_part(self, part_id: str) -> bool:
        """
        从索引中移除零件
        
        Args:
            part_id: 零件ID
            
        Returns:
            bool: 是否成功移除
        """
        if part_id not in self.parts:
            return False
        
        part = self.parts[part_id]
        
        # 从型号代码索引移除
        for catalog in part.catalog_types:
            self.catalog_index[catalog.upper()].discard(part_id)
            self.catalog_index[catalog.lower()].discard(part_id)
            self.catalog_index[catalog].discard(part_id)
        
        # 从附加代码索引移除
        for code in part.additional_codes:
            self.additional_index[code.upper()].discard(part_id)
            self.additional_index[code.lower()].discard(part_id)
            self.additional_index[code].discard(part_id)
        
        # 从类别索引移除
        self.category_index[part.part_category].discard(part_id)
        
        # 从名称索引移除
        for token in self._tokenize(part.item_name):
            self.name_index[token].discard(part_id)
        
        # 从主索引移除
        del self.parts[part_id]
        
        return True
    
    def get_part(self, part_id: str) -> Optional[Part]:
        """
        根据ID获取零件
        
        Args:
            part_id: 零件ID
            
        Returns:
            Optional[Part]: 零件对象或None
        """
        return self.parts.get(part_id)
    
    def lookup_by_catalog(self, catalog_type: str, case_sensitive: bool = False) -> Set[str]:
        """
        根据型号代码查询零件ID集合
        
        Args:
            catalog_type: 型号代码
            case_sensitive: 是否大小写敏感
            
        Returns:
            Set[str]: 零件ID集合
        """
        if case_sensitive:
            return self.catalog_index.get(catalog_type, set()).copy()
        else:
            # 大小写不敏感：合并大写和小写的结果
            upper_results = self.catalog_index.get(catalog_type.upper(), set())
            lower_results = self.catalog_index.get(catalog_type.lower(), set())
            return upper_results | lower_results
    
    def lookup_by_additional(self, additional_code: str, case_sensitive: bool = False) -> Set[str]:
        """
        根据附加代码查询零件ID集合
        
        Args:
            additional_code: 附加代码
            case_sensitive: 是否大小写敏感
            
        Returns:
            Set[str]: 零件ID集合
        """
        if case_sensitive:
            return self.additional_index.get(additional_code, set()).copy()
        else:
            upper_results = self.additional_index.get(additional_code.upper(), set())
            lower_results = self.additional_index.get(additional_code.lower(), set())
            return upper_results | lower_results
    
    def lookup_by_category(self, category: str) -> Set[str]:
        """
        根据类别查询零件ID集合
        
        Args:
            category: 零件类别
            
        Returns:
            Set[str]: 零件ID集合
        """
        return self.category_index.get(category, set()).copy()
    
    def search_by_name(self, keyword: str) -> Set[str]:
        """
        根据名称关键词搜索零件ID集合
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            Set[str]: 零件ID集合
        """
        # 简单实现：查找包含关键词的所有零件
        results = set()
        for part_id, part in self.parts.items():
            if keyword in part.item_name:
                results.add(part_id)
        return results
    
    def get_all_categories(self) -> List[str]:
        """
        获取所有类别列表
        
        Returns:
            List[str]: 类别列表
        """
        return sorted(self.category_index.keys())
    
    def get_statistics(self) -> Dict[str, int]:
        """
        获取索引统计信息
        
        Returns:
            Dict[str, int]: 统计信息字典
        """
        return {
            "total_parts": len(self.parts),
            "total_categories": len(self.category_index),
            "total_catalog_types": len([k for k in self.catalog_index.keys() if self.catalog_index[k]]),
            "total_additional_codes": len([k for k in self.additional_index.keys() if self.additional_index[k]]),
        }
    
    def _tokenize(self, text: str) -> List[str]:
        """
        分词（简单实现：按字符分割）
        
        Args:
            text: 文本
            
        Returns:
            List[str]: 词元列表
        """
        # 简单实现：每个字符作为一个token
        return list(text)
