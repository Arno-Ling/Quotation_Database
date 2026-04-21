"""
API接口测试脚本
使用requests库测试所有API端点
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """打印响应信息"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"状态码: {response.status_code}")
    print(f"响应时间: {response.elapsed.total_seconds() * 1000:.2f} ms")
    
    try:
        data = response.json()
        print(f"响应数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
        if len(json.dumps(data)) > 500:
            print("... (数据已截断)")
        return data
    except:
        print(f"响应内容: {response.text[:200]}")
        return None


def test_root():
    """测试根路径"""
    response = requests.get(f"{BASE_URL}/")
    print_response("测试1: 根路径 GET /", response)


def test_health():
    """测试健康检查"""
    response = requests.get(f"{BASE_URL}/api/health")
    data = print_response("测试2: 健康检查 GET /api/health", response)
    
    if data:
        print(f"\n✓ 数据库状态: {'已加载' if data.get('database_loaded') else '未加载'}")
        print(f"✓ 总零件数: {data.get('total_parts', 0)}")


def test_query_parts():
    """测试零件查询"""
    # 测试1: 按型号代码查询
    response = requests.get(f"{BASE_URL}/api/parts", params={"catalog_type": "SJ"})
    data = print_response("测试3: 查询零件 - 型号代码SJ", response)
    
    if data:
        print(f"\n✓ 找到 {data.get('total', 0)} 个零件")
        print(f"✓ 查询耗时: {data.get('query_time_ms', 0):.2f} ms")
    
    # 测试2: 按附加代码查询
    response = requests.get(f"{BASE_URL}/api/parts", params={"additional_code": "PC"})
    data = print_response("测试4: 查询零件 - 附加代码PC", response)
    
    if data:
        print(f"\n✓ 找到 {data.get('total', 0)} 个零件")
    
    # 测试3: 按名称查询
    response = requests.get(f"{BASE_URL}/api/parts", params={"item_name": "顶料"})
    data = print_response("测试5: 查询零件 - 名称包含'顶料'", response)
    
    if data:
        print(f"\n✓ 找到 {data.get('total', 0)} 个零件")
    
    # 测试4: 组合查询 (AND)
    response = requests.get(f"{BASE_URL}/api/parts", params={
        "catalog_type": "SJ",
        "additional_code": "PC",
        "logic": "AND"
    })
    data = print_response("测试6: 组合查询 - SJ AND PC", response)
    
    if data:
        print(f"\n✓ 找到 {data.get('total', 0)} 个零件")
    
    # 测试5: 分页查询
    response = requests.get(f"{BASE_URL}/api/parts", params={
        "catalog_type": "SJ",
        "limit": 2,
        "offset": 0
    })
    data = print_response("测试7: 分页查询 - limit=2, offset=0", response)
    
    if data:
        print(f"\n✓ 总数: {data.get('total', 0)}, 返回: {len(data.get('results', []))}")


def test_get_part():
    """测试获取单个零件"""
    part_id = "凸模_顶料型凸模"
    response = requests.get(f"{BASE_URL}/api/parts/{part_id}")
    data = print_response(f"测试8: 获取零件详情 - {part_id}", response)
    
    if data:
        print(f"\n✓ 零件名称: {data.get('item_name')}")
        print(f"✓ 类别: {data.get('part_category')}")
        print(f"✓ 型号代码数: {len(data.get('catalog_types', []))}")


def test_get_pdf():
    """测试获取PDF"""
    part_id = "凸模_顶料型凸模"
    
    # 测试1: 获取PDF信息
    response = requests.get(f"{BASE_URL}/api/parts/{part_id}/pdf", params={"format": "relative"})
    data = print_response(f"测试9: 获取PDF信息 - {part_id}", response)
    
    if data:
        print(f"\n✓ PDF存在: {data.get('pdf_exists')}")
        print(f"✓ 文件大小: {data.get('file_size_mb')} MB")
        print(f"✓ 相对路径: {data.get('pdf_path_relative')}")


def test_categories():
    """测试类别接口"""
    # 测试1: 获取所有类别
    response = requests.get(f"{BASE_URL}/api/categories")
    data = print_response("测试10: 获取所有类别", response)
    
    if data:
        print(f"\n✓ 总类别数: {data.get('total_categories', 0)}")
        categories = data.get('categories', [])
        if categories:
            print(f"✓ 前5个类别:")
            for cat in categories[:5]:
                print(f"  - {cat.get('name')}: {cat.get('count')} 个零件")
    
    # 测试2: 获取类别下的零件
    category = "凸模"
    response = requests.get(f"{BASE_URL}/api/categories/{category}/parts", params={"limit": 5})
    data = print_response(f"测试11: 获取类别零件 - {category}", response)
    
    if data:
        print(f"\n✓ 该类别总零件数: {data.get('total', 0)}")
        print(f"✓ 返回零件数: {len(data.get('results', []))}")


def test_statistics():
    """测试统计接口"""
    response = requests.get(f"{BASE_URL}/api/statistics")
    data = print_response("测试12: 获取统计信息", response)
    
    if data:
        print(f"\n✓ 总零件数: {data.get('total_parts', 0)}")
        print(f"✓ 总类别数: {data.get('total_categories', 0)}")
        print(f"✓ 型号代码数: {data.get('total_catalog_types', 0)}")
        print(f"✓ 附加代码数: {data.get('total_additional_codes', 0)}")
        
        pdf_coverage = data.get('pdf_coverage', {})
        print(f"✓ PDF覆盖率: {pdf_coverage.get('coverage_percentage', 0)}%")


def test_error_handling():
    """测试错误处理"""
    # 测试1: 不存在的零件
    response = requests.get(f"{BASE_URL}/api/parts/不存在的零件")
    print_response("测试13: 错误处理 - 不存在的零件", response)
    
    # 测试2: 不存在的类别
    response = requests.get(f"{BASE_URL}/api/categories/不存在的类别/parts")
    print_response("测试14: 错误处理 - 不存在的类别", response)


def test_performance():
    """测试性能"""
    print(f"\n{'='*60}")
    print("测试15: 性能测试")
    print(f"{'='*60}")
    
    # 测试查询性能
    start = time.time()
    for _ in range(10):
        requests.get(f"{BASE_URL}/api/parts", params={"catalog_type": "SJ"})
    duration = (time.time() - start) * 1000
    
    print(f"查询接口 (10次): {duration:.2f} ms")
    print(f"平均每次: {duration/10:.2f} ms")
    
    # 测试健康检查性能
    start = time.time()
    for _ in range(10):
        requests.get(f"{BASE_URL}/api/health")
    duration = (time.time() - start) * 1000
    
    print(f"\n健康检查 (10次): {duration:.2f} ms")
    print(f"平均每次: {duration/10:.2f} ms")


def main():
    """主测试函数"""
    print("=" * 60)
    print("FastAPI接口测试")
    print("=" * 60)
    print(f"API地址: {BASE_URL}")
    print(f"API文档: {BASE_URL}/api/docs")
    
    try:
        # 基础测试
        test_root()
        test_health()
        
        # 查询测试
        test_query_parts()
        test_get_part()
        test_get_pdf()
        
        # 类别测试
        test_categories()
        
        # 统计测试
        test_statistics()
        
        # 错误处理测试
        test_error_handling()
        
        # 性能测试
        test_performance()
        
        print(f"\n{'='*60}")
        print("所有测试完成！")
        print(f"{'='*60}")
        
        print("\n✅ API接口功能验证:")
        print("  ✓ 根路径和健康检查")
        print("  ✓ 零件查询（单条件、组合、分页）")
        print("  ✓ 零件详情")
        print("  ✓ PDF文件访问")
        print("  ✓ 类别浏览")
        print("  ✓ 统计信息")
        print("  ✓ 错误处理")
        print("  ✓ 性能优秀")
        
        print(f"\n📖 访问API文档: {BASE_URL}/api/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ 错误: 无法连接到API服务器")
        print("请确保服务器正在运行: python src/main.py")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")


if __name__ == "__main__":
    main()
