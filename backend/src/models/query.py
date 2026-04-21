"""
查询相关的数据模型
"""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class LogicOperator(str, Enum):
    """逻辑运算符"""
    AND = "AND"
    OR = "OR"


class QueryRequest(BaseModel):
    """
    查询请求模型
    
    Attributes:
        catalog_types: 型号代码列表
        additional_codes: 附加代码列表
        item_name: 零件名称关键词
        part_category: 零件类别
        logic: 逻辑运算符（AND/OR）
        case_sensitive: 是否大小写敏感
        use_regex: 是否使用正则表达式（用于名称搜索）
        limit: 结果数量限制
        offset: 结果偏移量
    """
    catalog_types: Optional[List[str]] = Field(None, description="型号代码列表")
    additional_codes: Optional[List[str]] = Field(None, description="附加代码列表")
    item_name: Optional[str] = Field(None, description="零件名称关键词")
    part_category: Optional[str] = Field(None, description="零件类别")
    logic: LogicOperator = Field(LogicOperator.AND, description="逻辑运算符")
    case_sensitive: bool = Field(False, description="是否大小写敏感")
    use_regex: bool = Field(False, description="是否使用正则表达式")
    limit: int = Field(100, ge=1, le=1000, description="结果数量限制")
    offset: int = Field(0, ge=0, description="结果偏移量")


class QueryResponse(BaseModel):
    """
    查询响应模型
    
    Attributes:
        total: 总结果数
        limit: 返回数量限制
        offset: 结果偏移量
        results: 零件列表
        truncated: 结果是否被截断
        query_time_ms: 查询耗时（毫秒）
    """
    total: int = Field(..., description="总结果数")
    limit: int = Field(..., description="返回数量限制")
    offset: int = Field(..., description="结果偏移量")
    results: List = Field(..., description="零件列表")  # List[Part]
    truncated: bool = Field(False, description="结果是否被截断")
    query_time_ms: float = Field(..., description="查询耗时（毫秒）")
