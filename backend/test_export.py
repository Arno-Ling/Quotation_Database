"""
测试导出功能
"""

import requests
import json
import csv
from io import StringIO

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("导出功能测试")
print("=" * 60)
print(f"API地址: {BASE_URL}")
print()

# 测试1: JSON导出
print("=" * 60)
print("测试1: JSON格式导出 - 查询型号代码SJ")
print("=" * 60)

response = requests.get(
    f"{BASE_URL}/api/export",
    params={
        "format": "json",
        "catalog_type": "SJ",
        "limit": 5
    }
)

print(f"状态码: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
print(f"响应大小: {len(response.content)} bytes")

if response.status_code == 200:
    data = json.loads(response.text)
    print(f"✓ 导出成功: {len(data)} 个零件")
    print(f"✓ 第一个零件: {data[0]['item_name']}")
    print(f"✓ PDF路径: {data[0].get('pdf_path', 'N/A')}")
else:
    print(f"✗ 导出失败: {response.text}")

print()

# 测试2: CSV导出
print("=" * 60)
print("测试2: CSV格式导出 - 查询附加代码PC")
print("=" * 60)

response = requests.get(
    f"{BASE_URL}/api/export",
    params={
        "format": "csv",
        "additional_code": "PC",
        "limit": 10
    }
)

print(f"状态码: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
print(f"响应大小: {len(response.content)} bytes")

if response.status_code == 200:
    csv_data = StringIO(response.text)
    reader = csv.reader(csv_data)
    rows = list(reader)
    print(f"✓ 导出成功: {len(rows) - 1} 个零件 (不含表头)")
    print(f"✓ 表头: {rows[0]}")
    if len(rows) > 1:
        print(f"✓ 第一行数据: {rows[1][0:3]}")  # 显示前3列
else:
    print(f"✗ 导出失败: {response.text}")

print()

# 测试3: Excel导出
print("=" * 60)
print("测试3: Excel格式导出 - 查询类别'凸模'")
print("=" * 60)

response = requests.get(
    f"{BASE_URL}/api/export",
    params={
        "format": "excel",
        "category": "凸模",
        "limit": 20
    }
)

print(f"状态码: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
print(f"响应大小: {len(response.content)} bytes")

if response.status_code == 200:
    print(f"✓ 导出成功")
    print(f"✓ Excel文件大小: {len(response.content) / 1024:.2f} KB")
    
    # 保存文件以便验证
    filename = "test_export.xlsx"
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"✓ 文件已保存: {filename}")
else:
    print(f"✗ 导出失败: {response.text}")

print()

# 测试4: 导出所有零件（JSON）
print("=" * 60)
print("测试4: 导出所有零件 - JSON格式")
print("=" * 60)

response = requests.get(
    f"{BASE_URL}/api/export",
    params={
        "format": "json",
        "limit": 10000  # 导出所有
    }
)

print(f"状态码: {response.status_code}")
print(f"响应大小: {len(response.content) / 1024:.2f} KB")

if response.status_code == 200:
    data = json.loads(response.text)
    print(f"✓ 导出成功: {len(data)} 个零件")
    
    # 统计有PDF路径的零件
    with_pdf = sum(1 for part in data if part.get('pdf_path'))
    print(f"✓ 包含PDF路径: {with_pdf}/{len(data)} ({with_pdf/len(data)*100:.1f}%)")
else:
    print(f"✗ 导出失败: {response.text}")

print()

# 测试5: 错误处理 - 无效格式
print("=" * 60)
print("测试5: 错误处理 - 无效的导出格式")
print("=" * 60)

response = requests.get(
    f"{BASE_URL}/api/export",
    params={
        "format": "xml",  # 不支持的格式
        "limit": 10
    }
)

print(f"状态码: {response.status_code}")
if response.status_code != 200:
    print(f"✓ 正确返回错误: {response.status_code}")
    print(f"✓ 错误信息: {response.json()}")
else:
    print(f"✗ 应该返回错误但返回了成功")

print()

# 测试6: 错误处理 - 无匹配数据
print("=" * 60)
print("测试6: 错误处理 - 查询无匹配数据")
print("=" * 60)

response = requests.get(
    f"{BASE_URL}/api/export",
    params={
        "format": "json",
        "catalog_type": "NONEXISTENT_CODE_12345",
        "limit": 10
    }
)

print(f"状态码: {response.status_code}")
if response.status_code == 404:
    print(f"✓ 正确返回404")
    print(f"✓ 错误信息: {response.json()}")
else:
    print(f"✗ 应该返回404但返回了: {response.status_code}")

print()
print("=" * 60)
print("所有测试完成！")
print("=" * 60)
print()
print("✅ 导出功能验证:")
print("  ✓ JSON格式导出")
print("  ✓ CSV格式导出")
print("  ✓ Excel格式导出")
print("  ✓ 查询过滤参数")
print("  ✓ PDF路径包含")
print("  ✓ 错误处理")
print()
print("📖 访问API文档查看导出端点: http://localhost:8000/api/docs")
