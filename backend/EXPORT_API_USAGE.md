# 导出API使用指南

## 概述

导出API允许您将查询结果导出为JSON、CSV或Excel格式。支持与查询端点相同的过滤参数。

## API端点

```
GET /api/export
```

## 参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| format | string | 否 | json | 导出格式：json, csv, excel |
| catalog_type | string | 否 | - | 型号代码 |
| additional_code | string | 否 | - | 附加代码 |
| item_name | string | 否 | - | 零件名称关键词 |
| category | string | 否 | - | 零件类别 |
| logic | string | 否 | AND | 逻辑运算符：AND, OR |
| case_sensitive | boolean | 否 | false | 是否大小写敏感 |
| use_regex | boolean | 否 | false | 是否使用正则表达式 |
| limit | integer | 否 | 1000 | 导出数量限制（1-10000） |

## 使用示例

### 1. 导出JSON格式

```bash
# 导出型号代码为SJ的零件
curl "http://localhost:8000/api/export?format=json&catalog_type=SJ&limit=5" -o parts.json

# 导出所有零件
curl "http://localhost:8000/api/export?format=json&limit=10000" -o all_parts.json
```

### 2. 导出CSV格式

```bash
# 导出附加代码为PC的零件
curl "http://localhost:8000/api/export?format=csv&additional_code=PC&limit=10" -o parts.csv

# 导出特定类别
curl "http://localhost:8000/api/export?format=csv&category=凸模&limit=100" -o parts_category.csv
```

### 3. 导出Excel格式

```bash
# 导出名称包含"顶料"的零件
curl "http://localhost:8000/api/export?format=excel&item_name=顶料&limit=50" -o parts.xlsx

# 导出所有零件到Excel
curl "http://localhost:8000/api/export?format=excel&limit=10000" -o all_parts.xlsx
```

### 4. Python示例

```python
import requests

# 导出JSON格式
response = requests.get(
    "http://localhost:8000/api/export",
    params={
        "format": "json",
        "catalog_type": "SJ",
        "limit": 5
    }
)

if response.status_code == 200:
    with open("parts.json", "wb") as f:
        f.write(response.content)
    print("导出成功！")

# 导出Excel格式
response = requests.get(
    "http://localhost:8000/api/export",
    params={
        "format": "excel",
        "category": "凸模",
        "limit": 100
    }
)

if response.status_code == 200:
    with open("parts.xlsx", "wb") as f:
        f.write(response.content)
    print("导出成功！")
```

### 5. JavaScript/Fetch示例

```javascript
// 导出CSV格式
fetch('http://localhost:8000/api/export?format=csv&additional_code=PC&limit=10')
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'parts.csv';
    a.click();
  });

// 导出Excel格式
fetch('http://localhost:8000/api/export?format=excel&category=凸模&limit=100')
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'parts.xlsx';
    a.click();
  });
```

## 导出格式说明

### JSON格式
- Content-Type: `application/json`
- 文件扩展名: `.json`
- 特点：完整的数据结构，易于程序处理
- 示例：
```json
[
  {
    "part_id": "凸模_顶料型凸模",
    "item_name": "顶料型凸模",
    "part_category": "凸模",
    "catalog_types": ["SJ", "SJV", "PJ"],
    "additional_codes": ["PC", "WC", "BC"],
    "source_file": "第8页.pdf",
    "pdf_path": "Database\\凸模\\凸模.pdf"
  }
]
```

### CSV格式
- Content-Type: `text/csv`
- 文件扩展名: `.csv`
- 特点：表格格式，易于Excel打开，列表字段用逗号分隔
- 列：part_id, item_name, part_category, catalog_types, additional_codes, source_file, pdf_path

### Excel格式
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- 文件扩展名: `.xlsx`
- 特点：原生Excel格式，支持格式化，列宽自动调整
- 工作表名称：零件数据
- 表头：零件ID, 零件名称, 零件类别, 型号代码, 附加代码, 源文件, PDF路径

## 错误处理

### 400 Bad Request
```json
{
  "error": {
    "code": 400,
    "message": "不支持的导出格式: xml"
  }
}
```

### 404 Not Found
```json
{
  "error": {
    "code": 404,
    "message": "没有找到匹配的数据"
  }
}
```

### 503 Service Unavailable
```json
{
  "error": {
    "code": 503,
    "message": "数据库未加载"
  }
}
```

## 性能建议

1. **限制导出数量**：使用`limit`参数控制导出数量，避免一次导出过多数据
2. **使用过滤条件**：通过查询参数过滤数据，只导出需要的零件
3. **选择合适的格式**：
   - JSON：程序处理
   - CSV：简单表格，文件较小
   - Excel：需要格式化和人工查看

## 注意事项

1. 导出的数据包含PDF相对路径
2. 最大导出数量限制为10000条
3. 文件名自动生成，格式为：`parts_export_{timestamp}.{ext}`
4. 所有导出都会自动触发浏览器下载（Content-Disposition: attachment）
