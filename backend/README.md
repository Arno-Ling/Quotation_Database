# 模具零件数据库查询系统 - 后端

## 项目结构

```
backend/
├── src/
│   ├── models/          # 数据模型
│   │   ├── part.py      # Part和LoadStatistics模型
│   │   └── __init__.py
│   ├── core/            # 核心业务逻辑
│   │   ├── database_loader.py   # 数据库加载器
│   │   ├── index_manager.py     # 索引管理器
│   │   ├── validator.py         # 数据验证器
│   │   └── __init__.py
│   └── __init__.py
├── tests/               # 测试代码（待添加）
├── test_loader.py       # 数据库加载器测试脚本
├── requirements.txt     # Python依赖
└── README.md           # 本文件
```

## 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 运行测试

测试数据库加载器：

```bash
cd backend
python test_loader.py
```

## 已实现功能

### 1. 数据模型 (models/part.py)
- `Part`: 零件数据模型，包含所有必需字段
- `LoadStatistics`: 加载统计信息

### 2. 数据验证器 (core/validator.py)
- 验证必需字段存在性
- 验证字段类型
- 提供详细的错误信息

### 3. 索引管理器 (core/index_manager.py)
- 多级哈希表索引（O(1)查询复杂度）
- 支持按型号代码、附加代码、类别、名称查询
- 支持大小写不敏感查询
- 提供统计信息

### 4. 数据库加载器 (core/database_loader.py)
- 自动扫描Database目录
- 解析所有JSON文件
- 构建索引
- 错误处理和统计
- PDF路径解析

## 使用示例

```python
from src.core.database_loader import DatabaseLoader
from src.core.validator import DataValidator

# 创建加载器
validator = DataValidator()
loader = DatabaseLoader("../Database", validator)

# 加载数据库
stats = loader.load_database()
print(f"加载完成: {stats}")

# 获取索引管理器
index = loader.get_index_manager()

# 查询型号代码
results = index.lookup_by_catalog("SJ")
print(f"找到 {len(results)} 个零件")

# 获取零件详情
for part_id in list(results)[:5]:
    part = index.get_part(part_id)
    print(f"- {part.item_name} ({part.part_category})")

# 获取所有类别
categories = index.get_all_categories()
print(f"类别: {categories}")

# 获取统计信息
stats = index.get_statistics()
print(f"统计: {stats}")
```

## 性能特点

- **O(1)查询复杂度**: 使用哈希表索引
- **大小写不敏感**: 自动处理大小写变体
- **容错设计**: 单个文件失败不影响整体加载
- **详细统计**: 提供加载时间、成功/失败数量等信息

## 下一步

- [ ] 添加日志系统
- [ ] 添加配置文件支持
- [ ] 实现并行加载
- [ ] 添加单元测试
- [ ] 实现查询引擎
- [ ] 实现PDF解析器
- [ ] 实现缓存管理器
- [ ] 实现FastAPI接口
