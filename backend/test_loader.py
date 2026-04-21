"""
数据库加载器测试脚本
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.core.database_loader import DatabaseLoader
from src.core.validator import DataValidator


def main():
    """主测试函数"""
    print("=" * 60)
    print("模具零件数据库加载器测试")
    print("=" * 60)
    
    # 数据库路径（相对于项目根目录）
    database_path = "../Database"
    
    # 检查路径是否存在
    db_path = Path(database_path)
    if not db_path.exists():
        print(f"错误: 数据库路径不存在: {db_path.absolute()}")
        print("请确保Database目录在项目根目录下")
        return
    
    # 创建加载器
    validator = DataValidator()
    loader = DatabaseLoader(database_path, validator)
    
    # 加载数据库
    stats = loader.load_database()
    
    # 显示详细统计
    print("\n" + "=" * 60)
    print("加载统计")
    print("=" * 60)
    print(f"总文件数: {stats.total_files}")
    print(f"成功加载: {stats.success_count}")
    print(f"加载失败: {stats.error_count}")
    print(f"总耗时: {stats.total_time_ms:.2f} ms")
    print(f"平均耗时: {stats.total_time_ms / max(stats.total_files, 1):.2f} ms/文件")
    
    # 显示错误信息（如果有）
    if stats.errors:
        print(f"\n错误详情（前10个）:")
        for i, error in enumerate(stats.errors[:10], 1):
            print(f"{i}. {error['file']}")
            print(f"   错误: {error['error']}")
    
    # 显示索引统计
    index_stats = loader.index_manager.get_statistics()
    print("\n" + "=" * 60)
    print("索引统计")
    print("=" * 60)
    print(f"总零件数: {index_stats['total_parts']}")
    print(f"类别数: {index_stats['total_categories']}")
    print(f"型号代码数: {index_stats['total_catalog_types']}")
    print(f"附加代码数: {index_stats['total_additional_codes']}")
    
    # 显示所有类别
    categories = loader.index_manager.get_all_categories()
    print(f"\n所有类别 ({len(categories)}):")
    for category in categories:
        count = len(loader.index_manager.lookup_by_category(category))
        print(f"  - {category}: {count} 个零件")
    
    # 测试查询功能
    print("\n" + "=" * 60)
    print("查询功能测试")
    print("=" * 60)
    
    # 测试型号代码查询
    test_catalog = "SJ"
    results = loader.index_manager.lookup_by_catalog(test_catalog)
    print(f"\n查询型号代码 '{test_catalog}': 找到 {len(results)} 个零件")
    if results:
        # 显示前3个结果
        for i, part_id in enumerate(list(results)[:3], 1):
            part = loader.index_manager.get_part(part_id)
            if part:
                print(f"{i}. {part.item_name} ({part.part_category})")
    
    # 测试名称搜索
    test_keyword = "凸模"
    results = loader.index_manager.search_by_name(test_keyword)
    print(f"\n搜索名称包含 '{test_keyword}': 找到 {len(results)} 个零件")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
