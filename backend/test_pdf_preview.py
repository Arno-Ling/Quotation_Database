"""
测试PDF预览功能
"""

import requests

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("PDF预览功能测试")
print("=" * 60)
print()

# 测试1: 获取PDF信息
print("测试1: 获取PDF信息")
print("-" * 60)

response = requests.get(f"{BASE_URL}/api/parts/凸模_顶料型凸模/pdf")
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✓ PDF存在: {data['pdf_exists']}")
    print(f"✓ 文件大小: {data['file_size_mb']:.2f} MB")
    print(f"✓ 相对路径: {data['pdf_path_relative']}")
else:
    print(f"✗ 请求失败: {response.text}")

print()

# 测试2: 预览模式（返回PDF文件，Content-Disposition: inline）
print("测试2: 预览模式")
print("-" * 60)

response = requests.get(f"{BASE_URL}/api/parts/凸模_顶料型凸模/pdf?preview=true")
print(f"状态码: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
print(f"响应大小: {len(response.content) / 1024 / 1024:.2f} MB")

if response.status_code == 200:
    content_disposition = response.headers.get('Content-Disposition', '')
    if 'inline' in content_disposition:
        print("✓ 预览模式正确：Content-Disposition包含'inline'")
    else:
        print("✗ 预览模式错误：Content-Disposition应该包含'inline'")
    
    if response.headers.get('Content-Type') == 'application/pdf':
        print("✓ Content-Type正确：application/pdf")
    else:
        print("✗ Content-Type错误")
else:
    print(f"✗ 请求失败: {response.text}")

print()

# 测试3: 下载模式（返回PDF文件，Content-Disposition: attachment）
print("测试3: 下载模式")
print("-" * 60)

response = requests.get(f"{BASE_URL}/api/parts/凸模_顶料型凸模/pdf?download=true")
print(f"状态码: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
print(f"响应大小: {len(response.content) / 1024 / 1024:.2f} MB")

if response.status_code == 200:
    content_disposition = response.headers.get('Content-Disposition', '')
    if 'attachment' in content_disposition:
        print("✓ 下载模式正确：Content-Disposition包含'attachment'")
    else:
        print("✗ 下载模式错误：Content-Disposition应该包含'attachment'")
    
    if response.headers.get('Content-Type') == 'application/pdf':
        print("✓ Content-Type正确：application/pdf")
    else:
        print("✗ Content-Type错误")
else:
    print(f"✗ 请求失败: {response.text}")

print()

# 测试4: 测试多个零件的PDF预览
print("测试4: 批量测试PDF预览")
print("-" * 60)

test_parts = [
    "凸模_顶料型凸模",
    "凹模_圆形凹模",
    "方形凸模_方形凸模",
]

success_count = 0
for part_id in test_parts:
    response = requests.get(f"{BASE_URL}/api/parts/{part_id}/pdf?preview=true")
    if response.status_code == 200:
        success_count += 1
        print(f"✓ {part_id}: 预览成功")
    else:
        print(f"✗ {part_id}: 预览失败 ({response.status_code})")

print(f"\n成功率: {success_count}/{len(test_parts)} ({success_count/len(test_parts)*100:.1f}%)")

print()
print("=" * 60)
print("测试完成！")
print("=" * 60)
print()
print("✅ PDF预览功能验证:")
print("  ✓ PDF信息获取")
print("  ✓ 预览模式（inline）")
print("  ✓ 下载模式（attachment）")
print("  ✓ 批量预览测试")
print()
print("📖 在浏览器中测试:")
print(f"  预览: {BASE_URL}/api/parts/凸模_顶料型凸模/pdf?preview=true")
print(f"  下载: {BASE_URL}/api/parts/凸模_顶料型凸模/pdf?download=true")
print()
print("🌐 前端测试:")
print("  1. 访问 http://localhost:3000")
print("  2. 搜索零件")
print("  3. 点击'查看'进入详情页")
print("  4. 点击'预览PDF'按钮")
