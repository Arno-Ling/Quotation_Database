"""
查询引擎 - 执行各类查询操作
"""

from typing import List, Set, Optional
import time
import re
import sys
import os

# 添加父目录到路径以支持导入
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.part import Part
from src.models.query import LogicOperator
from src.core.index_manager import IndexManager


class QueryEngine:
    """
    查询引擎 - 提供各种查询功能
    """
    
    def __init__(self, index_manager: IndexManager):
        """
        初始化查询引擎
        
        Args:
            index_manager: 索引管理器
        """
        self.index = index_manager
    
    def query_by_catalog_type(self, catalog_type: str, case_sensitive: bool = False) -> List[Part]:
        """
        根据型号代码查询零件
        
        Args:
            catalog_type: 型号代码
            case_sensitive: 是否大小写敏感
            
        Returns:
            List[Part]: 零件列表
        """
        part_ids = self.index.lookup_by_catalog(catalog_type, case_sensitive)
        return self._resolve_parts(part_ids)
    
    def query_by_additional_code(self, additional_code: str, case_sensitive: bool = False) -> List[Part]:
        """
        根据附加代码查询零件
        
        Args:
            additional_code: 附加代码
            case_sensitive: 是否大小写敏感
            
        Returns:
            List[Part]: 零件列表
        """
        part_ids = self.index.lookup_by_additional(additional_code, case_sensitive)
        return self._resolve_parts(part_ids)
    
    def query_by_item_name(self, keyword: str, use_regex: bool = False) -> List[Part]:
        """
        根据零件名称查询
        
        Args:
            keyword: 搜索关键词
            use_regex: 是否使用正则表达式
            
        Returns:
            List[Part]: 零件列表
        """
        if use_regex:
            # 使用正则表达式搜索
            pattern = re.compile(keyword)
            part_ids = set()
            for part_id, part in self.index.parts.items():
                if pattern.search(part.item_name):
                    part_ids.add(part_id)
        else:
            # 简单的子字符串搜索
            part_ids = self.index.search_by_name(keyword)
        
        return self._resolve_parts(part_ids)
    
    def query_combined(
        self,
        catalog_types: Optional[List[str]] = None,
        additional_codes: Optional[List[str]] = None,
        item_name: Optional[str] = None,
        part_category: Optional[str] = None,
        logic: LogicOperator = LogicOperator.AND,
        case_sensitive: bool = False,
        use_regex: bool = False
    ) -> List[Part]:
        """
        组合查询
        
        Args:
            catalog_types: 型号代码列表
            additional_codes: 附加代码列表
            item_name: 零件名称关键词
            part_category: 零件类别
            logic: 逻辑运算符（AND/OR）
            case_sensitive: 是否大小写敏感
            use_regex: 是否使用正则表达式（用于名称搜索）
            
        Returns:
            List[Part]: 零件列表
        """
        result_sets = []
        
        # 收集所有查询条件的结果集
        if catalog_types:
            for catalog_type in catalog_types:
                part_ids = self.index.lookup_by_catalog(catalog_type, case_sensitive)
                result_sets.append(part_ids)
        
        if additional_codes:
            for additional_code in additional_codes:
                part_ids = self.index.lookup_by_additional(additional_code, case_sensitive)
                result_sets.append(part_ids)
        
        if item_name:
            if use_regex:
                pattern = re.compile(item_name)
                part_ids = set()
                for part_id, part in self.index.parts.items():
                    if pattern.search(part.item_name):
                        part_ids.add(part_id)
            else:
                part_ids = self.index.search_by_name(item_name)
            result_sets.append(part_ids)
        
        if part_category:
            part_ids = self.index.lookup_by_category(part_category)
            result_sets.append(part_ids)
        
        # 如果没有任何查询条件，返回空列表
        if not result_sets:
            return []
        
        # 应用逻辑运算符
        final_ids = self._apply_logic(result_sets, logic)
        
        return self._resolve_parts(final_ids)
    
    def get_parts_by_category(self, category: str) -> List[Part]:
        """
        获取指定类别的所有零件
        
        Args:
            category: 零件类别
            
        Returns:
            List[Part]: 零件列表
        """
        part_ids = self.index.lookup_by_category(category)
        return self._resolve_parts(part_ids)
    
    def get_all_categories(self) -> List[dict]:
        """
        获取所有类别及其统计信息
        
        Returns:
            List[dict]: 类别信息列表，包含名称和零件数量
        """
        categories = self.index.get_all_categories()
        result = []
        
        for category in categories:
            part_ids = self.index.lookup_by_category(category)
            result.append({
                "name": category,
                "count": len(part_ids),
                "description": f"{category}零件"
            })
        
        return result
    
    def _apply_logic(self, sets: List[Set[str]], logic: LogicOperator) -> Set[str]:
        """
        应用逻辑运算符到多个集合
        
        Args:
            sets: 零件ID集合列表
            logic: 逻辑运算符
            
        Returns:
            Set[str]: 运算结果集合
        """
        if not sets:
            return set()
        
        if logic == LogicOperator.AND:
            # AND逻辑：取交集
            result = sets[0]
            for s in sets[1:]:
                result = result & s
            return result
        else:
            # OR逻辑：取并集
            result = set()
            for s in sets:
                result = result | s
            return result
    
    def _resolve_parts(self, part_ids: Set[str]) -> List[Part]:
        """
        将零件ID集合解析为零件对象列表
        
        Args:
            part_ids: 零件ID集合
            
        Returns:
            List[Part]: 零件列表
        """
        parts = []
        for part_id in part_ids:
            part = self.index.get_part(part_id)
            if part:
                parts.append(part)
        return parts
    
    def execute_query(
        self,
        catalog_types: Optional[List[str]] = None,
        additional_codes: Optional[List[str]] = None,
        item_name: Optional[str] = None,
        part_category: Optional[str] = None,
        logic: LogicOperator = LogicOperator.AND,
        case_sensitive: bool = False,
        use_regex: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> dict:
        """
        执行查询并返回格式化的结果
        
        Args:
            catalog_types: 型号代码列表
            additional_codes: 附加代码列表
            item_name: 零件名称关键词
            part_category: 零件类别
            logic: 逻辑运算符
            case_sensitive: 是否大小写敏感
            use_regex: 是否使用正则表达式
            limit: 结果数量限制
            offset: 结果偏移量
            
        Returns:
            dict: 查询响应字典
        """
        start_time = time.time()
        
        # 执行查询
        results = self.query_combined(
            catalog_types=catalog_types,
            additional_codes=additional_codes,
            item_name=item_name,
            part_category=part_category,
            logic=logic,
            case_sensitive=case_sensitive,
            use_regex=use_regex
        )
        
        # 分页
        total = len(results)
        truncated = total > limit
        paginated_results = results[offset:offset + limit]
        
        query_time_ms = (time.time() - start_time) * 1000
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "results": paginated_results,
            "truncated": truncated,
            "query_time_ms": query_time_ms
        }
