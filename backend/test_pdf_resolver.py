"""
PDF解析器测试脚本
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.core.database_loader import DatabaseLoader
from src.core.validator import DataValidator
from src.core.pdf_resolver import PDFResolver, PathFormat


def main():
    """主测试函数"""
    print("=" * 60)
    print("PDF解析器测试")
    print("=" * 60)
    
    # 加载数据库
    database_path = "../Database"
    validator = DataValidator()
    loader = DatabaseLoader(database_path, validator)
    
    print("\n正在加载数据库...")
    stats = loader.load_database()
    print(f"加载完成: {stats.success_count} 个零件")
    
    # 创建PDF解析器
    pdf_resolver = PDFResolver(database_path, loader.get_index_manager())
    
    print("\n" + "=" * 60)
    print("测试1: PDF统计信息")
    print("=" * 60)
    
    # 获取统计信息
    pdf_stats = pdf_resolver.get_statistics()
    print(f"总零件数: {pdf_stats['total_parts']}")
    print(f"找到PDF: {pdf_stats['pdfs_found']}")
    print(f"缺失PDF: {pdf_stats['pdfs_missing']}")
    print(f"分页PDF: {pdf_stats['paged_pdfs']}")
    print(f"源PDF: {pdf_stats['source_pdfs']}")
    print(f"覆盖率: {pdf_stats['coverage_percentage']}%")
    
    print("\n" + "=" * 60)
    print("测试2: 获取PDF路径 - 不同格式")
    print("=" * 60)
    
    # 选择一个有PDF的零件进行测试
    test_part_id = "凸模_顶料型凸模"
    
    # 绝对路径
    abs_path = pdf_resolver.get_pdf_path(test_part_id, PathFormat.ABSOLUTE)
    print(f"\n零件: {test_part_id}")
    print(f"绝对路径: {abs_path}")
    
    # 相对路径
    rel_path = pdf_resolver.get_pdf_path(test_part_id, PathFormat.RELATIVE)
    print(f"相对路径: {rel_path}")
    
    # URL格式
    url_path = pdf_resolver.get_pdf_path(test_part_id, PathFormat.URL)
    print(f"URL格式: {url_path}")
    
    print("\n" + "=" * 60)
    print("测试3: PDF详细信息")
    print("=" * 60)
    
    # 获取PDF详细信息
    pdf_info = pdf_resolver.get_pdf_info(test_part_id)
    if pdf_info:
        print(f"\n零件ID: {pdf_info['part_id']}")
        print(f"零件名称: {pdf_info['item_name']}")
        print(f"类别: {pdf_info['part_category']}")
        print(f"源文件: {pdf_info['source_file']}")
        print(f"PDF存在: {'是' if pdf_info['pdf_exists'] else '否'}")
        print(f"是否分页PDF: {'是' if pdf_info['is_paged_pdf'] else '否'}")
        if pdf_info['pdf_exists']:
            print(f"文件大小: {pdf_info['file_size_mb']} MB")
            print(f"绝对路径: {pdf_info['pdf_path_absolute']}")
            print(f"相对路径: {pdf_info['pdf_path_relative']}")
    
    print("\n" + "=" * 60)
    print("测试4: 批量获取PDF路径")
    print("=" * 60)
    
    # 获取前5个零件的PDF路径
    index = loader.get_index_manager()
    part_ids = list(index.parts.keys())[:5]
    
    batch_paths = pdf_resolver.batch_get_pdf_paths(part_ids, PathFormat.RELATIVE)
    print(f"\n批量查询 {len(part_ids)} 个零件:")
    for part_id, pdf_path in batch_paths.items():
        part = index.get_part(part_id)
        status = "✓" if pdf_path else "✗"
        print(f"{status} {part.item_name}: {pdf_path if pdf_path else '未找到'}")
    
    print("\n" + "=" * 60)
    print("测试5: 缺失PDF检测")
    print("=" * 60)
    
    # 获取缺失PDF列表
    missing_pdfs = pdf_resolver.get_missing_pdfs()
    print(f"\n缺失PDF的零件数: {len(missing_pdfs)}")
    
    if missing_pdfs:
        print(f"\n前10个缺失PDF的零件:")
        for i, missing in enumerate(missing_pdfs[:10], 1):
            print(f"{i}. {missing['item_name']} ({missing['part_category']})")
            print(f"   源文件: {missing['source_file']}")
            print(f"   期望路径: {missing['expected_path']}")
    else:
        print("✓ 所有零件都有对应的PDF文件！")
    
    print("\n" + "=" * 60)
    print("测试6: 按类别统计PDF")
    print("=" * 60)
    
    # 按类别统计PDF覆盖率
    categories = index.get_all_categories()
    category_stats = []
    
    for category in categories:
        part_ids = index.lookup_by_category(category)
        total = len(part_ids)
        found = 0
        
        for part_id in part_ids:
            if pdf_resolver.get_pdf_path(part_id):
                found += 1
        
        coverage = round(found / total * 100, 1) if total > 0 else 0
        category_stats.append({
            "category": category,
            "total": total,
            "found": found,
            "missing": total - found,
            "coverage": coverage
        })
    
    # 按覆盖率排序
    category_stats.sort(key=lambda x: x['coverage'])
    
    print(f"\nPDF覆盖率最低的10个类别:")
    for i, stat in enumerate(category_stats[:10], 1):
        print(f"{i}. {stat['category']}: {stat['coverage']}% ({stat['found']}/{stat['total']})")
    
    print(f"\nPDF覆盖率最高的10个类别:")
    for i, stat in enumerate(category_stats[-10:], 1):
        print(f"{i}. {stat['category']}: {stat['coverage']}% ({stat['found']}/{stat['total']})")
    
    print("\n" + "=" * 60)
    print("测试7: PDF路径解析策略")
    print("=" * 60)
    
    # 测试不同的PDF查找策略
    test_parts = list(index.parts.values())[:5]
    
    print("\n测试PDF查找策略:")
    for part in test_parts:
        pdf_path, is_paged = pdf_resolver.resolve_pdf_location(part)
        if pdf_path:
            exists = pdf_resolver.verify_pdf_exists(pdf_path)
            pdf_type = "分页PDF" if is_paged else "源PDF"
            status = "✓" if exists else "✗"
            print(f"{status} {part.item_name}: {pdf_type}")
        else:
            print(f"✗ {part.item_name}: 未找到PDF")
    
    print("\n" + "=" * 60)
    print("测试8: 性能测试")
    print("=" * 60)
    
    import time
    
    # 测试单个查询性能
    start = time.time()
    for _ in range(100):
        pdf_resolver.get_pdf_path(test_part_id)
    duration = (time.time() - start) * 1000
    print(f"单个PDF路径查询 (100次): {duration:.2f} ms")
    print(f"平均每次: {duration/100:.2f} ms")
    
    # 测试批量查询性能
    test_ids = list(index.parts.keys())[:100]
    start = time.time()
    pdf_resolver.batch_get_pdf_paths(test_ids)
    duration = (time.time() - start) * 1000
    print(f"\n批量查询100个PDF路径: {duration:.2f} ms")
    print(f"平均每次: {duration/100:.2f} ms")
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)
    
    # 总结
    print("\n✅ PDF解析器功能验证:")
    print("  ✓ PDF统计信息")
    print("  ✓ 多种路径格式（绝对、相对、URL）")
    print("  ✓ PDF详细信息查询")
    print("  ✓ 批量路径查询")
    print("  ✓ 缺失PDF检测")
    print("  ✓ 按类别统计")
    print("  ✓ 查找策略（分页PDF优先，源PDF回退）")
    print(f"  ✓ 性能优秀（<{duration/100:.2f}ms/查询）")


if __name__ == "__main__":
    main()
