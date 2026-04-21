"""
数据序列化器模块
支持JSON、CSV、Excel格式的数据导出
"""

import csv
import json
from typing import List, Optional
from io import StringIO, BytesIO
from pathlib import Path

from models.part import Part


class Serializer:
    """数据序列化器"""
    
    @staticmethod
    def to_json(parts: List[Part], indent: int = 2) -> str:
        """
        将零件列表序列化为JSON字符串
        
        Args:
            parts: 零件列表
            indent: JSON缩进空格数
            
        Returns:
            JSON字符串
        """
        data = [part.dict() for part in parts]
        return json.dumps(data, ensure_ascii=False, indent=indent)
    
    @staticmethod
    def to_csv(parts: List[Part]) -> str:
        """
        将零件列表序列化为CSV字符串
        
        Args:
            parts: 零件列表
            
        Returns:
            CSV字符串
        """
        if not parts:
            return ""
        
        output = StringIO()
        writer = csv.writer(output)
        
        # 写入表头
        headers = [
            "part_id",
            "item_name", 
            "part_category",
            "catalog_types",
            "additional_codes",
            "source_file",
            "pdf_path"
        ]
        writer.writerow(headers)
        
        # 写入数据行
        for part in parts:
            row = [
                part.part_id,
                part.item_name,
                part.part_category,
                ",".join(part.catalog_types) if part.catalog_types else "",
                ",".join(part.additional_codes) if part.additional_codes else "",
                part.source_file,
                part.pdf_path or ""
            ]
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def to_excel(parts: List[Part]) -> bytes:
        """
        将零件列表序列化为Excel文件（xlsx格式）
        
        Args:
            parts: 零件列表
            
        Returns:
            Excel文件的字节数据
        """
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, Alignment
        except ImportError:
            raise ImportError("需要安装openpyxl库: pip install openpyxl")
        
        # 创建工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = "零件数据"
        
        # 设置表头
        headers = [
            "零件ID",
            "零件名称",
            "零件类别",
            "型号代码",
            "附加代码",
            "源文件",
            "PDF路径"
        ]
        ws.append(headers)
        
        # 设置表头样式
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        # 写入数据
        for part in parts:
            row = [
                part.part_id,
                part.item_name,
                part.part_category,
                ", ".join(part.catalog_types) if part.catalog_types else "",
                ", ".join(part.additional_codes) if part.additional_codes else "",
                part.source_file,
                part.pdf_path or ""
            ]
            ws.append(row)
        
        # 自动调整列宽
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)  # 最大宽度50
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # 保存到字节流
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return output.getvalue()


class ExportFormat:
    """导出格式枚举"""
    JSON = "json"
    CSV = "csv"
    EXCEL = "excel"
    
    @classmethod
    def is_valid(cls, format: str) -> bool:
        """验证格式是否有效"""
        return format.lower() in [cls.JSON, cls.CSV, cls.EXCEL]
    
    @classmethod
    def get_content_type(cls, format: str) -> str:
        """获取Content-Type"""
        content_types = {
            cls.JSON: "application/json",
            cls.CSV: "text/csv",
            cls.EXCEL: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }
        return content_types.get(format.lower(), "application/octet-stream")
    
    @classmethod
    def get_file_extension(cls, format: str) -> str:
        """获取文件扩展名"""
        extensions = {
            cls.JSON: ".json",
            cls.CSV: ".csv",
            cls.EXCEL: ".xlsx"
        }
        return extensions.get(format.lower(), ".txt")
