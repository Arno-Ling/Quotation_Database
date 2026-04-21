# 模具零件数据库查询系统

一个功能完整的模具零件数据库管理和查询系统，提供高性能的零件检索、PDF文档管理和数据导出功能。

## 📋 项目概述

本系统旨在为模具零件数据提供高效的查询、浏览和管理功能。系统采用前后端分离架构，后端使用Python FastAPI构建RESTful API，前端使用React + TypeScript + Ant Design构建现代化Web界面。

### 核心功能

- 🔍 **多条件查询**: 支持按型号代码、附加代码、零件名称、类别等多种条件查询
- 📊 **数据统计**: 实时统计零件数量、类别分布、PDF覆盖率等信息
- 📁 **类别浏览**: 按类别组织和浏览零件数据
- 📄 **PDF管理**: 自动关联和管理零件PDF文档，支持在线预览和下载
- 👁️ **PDF预览**: 无需下载即可在浏览器中预览PDF文档
- 📤 **数据导出**: 支持JSON、CSV、Excel三种格式的数据导出
- ⚡ **高性能**: 使用多级哈希索引，查询响应时间<100ms
- 🎨 **现代化UI**: 响应式设计，支持桌面和移动设备

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端 (React)                          │
│  - 搜索界面  - 详情页面  - 类别浏览  - 统计图表        │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/REST API
┌─────────────────────▼───────────────────────────────────┐
│                  后端 (FastAPI)                          │
│  - RESTful API  - 查询引擎  - PDF解析  - 数据导出      │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              数据层 (JSON + PDF)                         │
│  - 626个零件  - 32个类别  - 100% PDF覆盖               │
└─────────────────────────────────────────────────────────┘
```

## 📊 数据统计

- **总零件数**: 626个
- **总类别数**: 32个
- **型号代码数**: 13,182个
- **附加代码数**: 1,054个
- **PDF覆盖率**: 100%
- **查询性能**: <0.02ms/查询

## 🚀 快速开始

### 环境要求

**后端**:
- Python 3.9+
- pip

**前端**:
- Node.js 16+
- npm 8+

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repository-url>
cd system
```

#### 2. 启动后端

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动API服务器
python src/main.py
```

后端服务将运行在: http://localhost:8000

#### 3. 启动前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将运行在: http://localhost:3000

#### 4. 访问应用

打开浏览器访问: http://localhost:3000

## 📖 使用指南

### 搜索零件

1. 在首页选择搜索类型（型号代码、附加代码、零件名称、类别）
2. 输入搜索关键词
3. 点击"搜索"按钮
4. 查看搜索结果，支持分页浏览

### 查看零件详情

1. 在搜索结果中点击"查看"按钮
2. 查看零件完整信息
3. 查看PDF文档信息
4. 点击"预览PDF"按钮在线预览文档（无需下载）
5. 点击"下载PDF"按钮下载文档到本地

### 浏览类别

1. 点击顶部导航栏的"类别浏览"
2. 查看所有类别网格
3. 点击任意类别查看该类别下的所有零件

### 导出数据

1. 执行搜索查询
2. 点击"导出数据"按钮
3. 选择导出格式（JSON、CSV、Excel）
4. 文件将自动下载

### 查看统计信息

1. 点击顶部导航栏的"统计信息"
2. 查看系统总览统计
3. 查看PDF覆盖率
4. 查看类别分布

## 🔧 API文档

### 访问API文档

启动后端服务后，访问: http://localhost:8000/api/docs

### 主要API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/parts` | GET | 查询零件列表 |
| `/api/parts/{part_id}` | GET | 获取零件详情 |
| `/api/parts/{part_id}/pdf` | GET | 获取PDF信息/预览/下载 |
| `/api/categories` | GET | 获取所有类别 |
| `/api/categories/{category}/parts` | GET | 获取类别零件 |
| `/api/statistics` | GET | 获取统计信息 |
| `/api/export` | GET | 导出数据 |

### API使用示例

```bash
# 健康检查
curl http://localhost:8000/api/health

# 查询零件
curl "http://localhost:8000/api/parts?catalog_type=SJ&limit=10"

# 获取零件详情
curl "http://localhost:8000/api/parts/凸模_顶料型凸模"

# 预览PDF（在浏览器中打开）
curl "http://localhost:8000/api/parts/凸模_顶料型凸模/pdf?preview=true"

# 下载PDF
curl "http://localhost:8000/api/parts/凸模_顶料型凸模/pdf?download=true" -o part.pdf

# 导出数据
curl "http://localhost:8000/api/export?format=json&catalog_type=SJ" -o parts.json
```

## 📁 项目结构

```
system/
├── backend/                    # 后端代码
│   ├── src/
│   │   ├── api/               # API路由
│   │   ├── core/              # 核心模块
│   │   │   ├── database_loader.py    # 数据库加载器
│   │   │   ├── index_manager.py      # 索引管理器
│   │   │   ├── query_engine.py       # 查询引擎
│   │   │   ├── pdf_resolver.py       # PDF解析器
│   │   │   ├── validator.py          # 数据验证器
│   │   │   └── serializer.py         # 数据序列化器
│   │   ├── models/            # 数据模型
│   │   │   ├── part.py               # 零件模型
│   │   │   └── query.py              # 查询模型
│   │   └── main.py            # FastAPI应用入口
│   ├── requirements.txt       # Python依赖
│   └── test_*.py             # 测试文件
│
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── pages/            # 页面组件
│   │   │   ├── HomePage.tsx           # 首页/搜索页
│   │   │   ├── PartDetailPage.tsx     # 零件详情页
│   │   │   ├── CategoriesPage.tsx     # 类别浏览页
│   │   │   ├── CategoryPartsPage.tsx  # 类别零件列表
│   │   │   └── StatisticsPage.tsx     # 统计信息页
│   │   ├── services/         # API服务
│   │   │   └── api.ts                 # API客户端
│   │   ├── types/            # TypeScript类型
│   │   │   └── index.ts
│   │   ├── App.tsx           # 主应用组件
│   │   └── main.tsx          # 入口文件
│   ├── package.json          # npm依赖
│   └── vite.config.ts        # Vite配置
│
├── Database/                  # 数据库文件
│   ├── 凸模/
│   ├── 凹模/
│   └── ...                   # 32个类别
│
└── README.md                 # 项目文档
```

## 🛠️ 技术栈

### 后端

- **框架**: FastAPI 0.104+
- **语言**: Python 3.9+
- **数据验证**: Pydantic 2.0+
- **HTTP服务器**: Uvicorn
- **导出功能**: openpyxl (Excel), csv (CSV)

### 前端

- **框架**: React 18
- **语言**: TypeScript 5
- **构建工具**: Vite 5
- **UI组件**: Ant Design 5
- **路由**: React Router 6
- **HTTP客户端**: Axios 1.6

### 数据结构

- **存储格式**: JSON + PDF
- **索引结构**: 多级哈希表
- **查询复杂度**: O(1)

## 🎯 核心特性详解

### 1. 高性能查询引擎

- **多级哈希索引**: 按型号代码、附加代码、类别、名称建立索引
- **O(1)查询复杂度**: 平均查询时间<0.02ms
- **组合查询**: 支持AND/OR逻辑运算
- **模糊搜索**: 支持名称模糊匹配和正则表达式

### 2. PDF文档管理

- **自动关联**: 自动关联零件与PDF文档
- **智能定位**: 优先分页PDF，回退到源PDF
- **多种路径格式**: 支持绝对路径、相对路径、file:// URL
- **在线预览**: 支持浏览器内PDF预览，无需下载
- **批量下载**: 支持批量导出PDF路径

### 3. 数据导出

- **多格式支持**: JSON、CSV、Excel
- **过滤导出**: 支持按查询条件导出
- **大数据量**: 支持最多10,000条记录导出
- **自动格式化**: Excel自动调整列宽、表头加粗

### 4. 数据验证

- **必需字段验证**: 确保关键字段存在
- **类型验证**: 验证字段类型正确性
- **错误处理**: 详细的错误信息和日志

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| 数据库加载时间 | ~270ms (626个零件) |
| 单次查询时间 | <0.02ms |
| API响应时间 | ~2秒 (含网络) |
| PDF解析时间 | 0.31ms/查询 |
| 并发支持 | 100+ 并发请求 |
| 内存占用 | <100MB |

## 🔒 安全性

- **输入验证**: 所有API输入都经过Pydantic验证
- **SQL注入防护**: 不使用SQL数据库，无SQL注入风险
- **XSS防护**: 前端使用React自动转义
- **CORS配置**: 可配置允许的源
- **错误处理**: 统一的错误处理和日志记录

## 🧪 测试

### 后端测试

```bash
cd backend

# 测试数据库加载
python test_loader.py

# 测试查询引擎
python test_query_engine.py

# 测试PDF解析
python test_pdf_resolver.py

# 测试API接口
python test_api.py

# 测试导出功能
python test_export.py
```

### 测试覆盖

- ✅ 数据库加载测试
- ✅ 查询引擎测试
- ✅ PDF解析测试
- ✅ API端点测试
- ✅ 导出功能测试

## 🐛 故障排除

### 后端问题

**问题**: 数据库加载失败
```bash
# 检查Database目录是否存在
ls Database/

# 检查JSON文件格式
python -m json.tool Database/凸模/output_json/凸模.json
```

**问题**: API启动失败
```bash
# 检查端口是否被占用
netstat -ano | findstr :8000

# 检查Python版本
python --version  # 需要3.9+
```

### 前端问题

**问题**: 依赖安装失败
```bash
# 清除npm缓存
npm cache clean --force

# 重新安装
npm install
```

**问题**: API连接失败
```bash
# 检查后端是否运行
curl http://localhost:8000/api/health

# 检查代理配置
cat frontend/vite.config.ts
```

## 📝 开发指南

### 添加新的查询条件

1. 在 `backend/src/models/query.py` 添加新字段
2. 在 `backend/src/core/query_engine.py` 实现查询逻辑
3. 在 `backend/src/main.py` 添加API参数
4. 在 `frontend/src/types/index.ts` 添加类型定义
5. 在 `frontend/src/pages/HomePage.tsx` 添加UI控件

### 添加新的导出格式

1. 在 `backend/src/core/serializer.py` 实现序列化方法
2. 在 `ExportFormat` 类添加新格式
3. 在 `backend/src/main.py` 的导出端点添加处理逻辑
4. 在前端添加导出选项

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License

## 👥 作者

项目开发团队

## 🙏 致谢

- FastAPI - 现代化的Python Web框架
- React - 用户界面库
- Ant Design - 企业级UI组件库
- Vite - 下一代前端构建工具

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 查看 [PDF预览功能指南](PDF_PREVIEW_GUIDE.md)

---

**最后更新**: 2026-04-21  
**版本**: v1.1.0 - 新增PDF在线预览功能
