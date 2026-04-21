"""
测试PDF路径解析是否正确
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("PDF路径解析测试")
print("=" * 60)
print()

# 测试不同类别的零件
test_cases = [
    {
        "category": "材料导向·顶料相关零件",
        "search_params": {"category": "材料导向·顶料相关零件", "limit": 1}
    },
    {
        "category": "凸模",
        "search_params": {"catalog_type": "SJ", "limit": 1}
    },
    {
        "category": "方形凸模",
        "search_params": {"category": "方形凸模", "limit": 1}
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"测试 {i}: {test_case['category']}")
    print("-" * 60)
    
    # 查询零件
    response = requests.get(f"{BASE_URL}/api/parts", params=test_case['search_params'])
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            part = data['results'][0]
            part_id = part['part_id']
            item_name = part['item_name']
            
            print(f"零件ID: {part_id}")
            print(f"零件名称: {item_name}")
            print(f"类别: {part['part_category']}")
            print()
            
            # 获取PDF信息
            pdf_response = requests.get(f"{BASE_URL}/api/parts/{part_id}/pdf")
            if pdf_response.status_code == 200:
                pdf_info = pdf_response.json()
                print(f"✓ PDF存在: {pdf_info['pdf_exists']}")
                print(f"✓ 是否分页PDF: {pdf_info['is_paged_pdf']}")
                print(f"✓ 绝对路径: {pdf_info['pdf_path_absolute']}")
                print(f"✓ 相对路径: {pdf_info['pdf_path_relative']}")
                print(f"✓ 文件大小: {pdf_info['file_size_mb']:.2f} MB")
                
                # 验证路径是否正确
                abs_path = pdf_info['pdf_path_absolute']
                if pdf_info['is_paged_pdf']:
                    # 分页PDF应该在output_pdf目录下，文件名应该是item_name
                    expected_filename = f"{item_name}.pdf"
                    if expected_filename in abs_path and "output_pdf" in abs_path:
                        print(f"✓ 路径正确：分页PDF使用item_name作为文件名")
                    else:
                        print(f"✗ 路径可能不正确")
                        print(f"  期望文件名: {expected_filename}")
                else:
                    # 源PDF应该在类别根目录下
                    if f"{part['part_category']}.pdf" in abs_path:
                        print(f"✓ 路径正确：源PDF在类别根目录")
                    else:
                        print(f"✗ 路径可能不正确")
            else:
                print(f"✗ 获取PDF信息失败: {pdf_response.status_code}")
        else:
            print("✗ 未找到零件")
    else:
        print(f"✗ 查询失败: {response.status_code}")
    
    print()

print("=" * 60)
print("测试完成！")
print("=" * 60)
print()
print("📝 说明:")
print("  - 分页PDF应该在: Database/{类别}/output_pdf/{零件名称}.pdf")
print("  - 源PDF应该在: Database/{类别}/{类别}.pdf")
print()
print("🔍 如果路径不正确，请检查:")
print("  1. JSON文件中的source_file字段")
print("  2. output_pdf目录下的实际文件名")
print("  3. PDF解析器的resolve_pdf_location方法")
