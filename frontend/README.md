# 模具零件数据库查询系统 - 前端

React + TypeScript + Ant Design 前端应用

## 技术栈

- **React 18** - UI框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Ant Design** - UI组件库
- **React Router** - 路由管理
- **Axios** - HTTP客户端

## 项目结构

```
frontend/
├── src/
│   ├── pages/              # 页面组件
│   │   ├── HomePage.tsx           # 首页/搜索页
│   │   ├── PartDetailPage.tsx     # 零件详情页
│   │   ├── CategoriesPage.tsx     # 类别浏览页
│   │   ├── CategoryPartsPage.tsx  # 类别零件列表页
│   │   └── StatisticsPage.tsx     # 统计信息页
│   ├── services/           # API服务
│   │   └── api.ts                 # API客户端
│   ├── types/              # TypeScript类型定义
│   │   └── index.ts
│   ├── App.tsx             # 主应用组件
│   ├── main.tsx            # 入口文件
│   ├── App.css             # 应用样式
│   └── index.css           # 全局样式
├── index.html              # HTML模板
├── package.json            # 依赖配置
├── tsconfig.json           # TypeScript配置
└── vite.config.ts          # Vite配置

```

## 功能特性

### 1. 首页/搜索页 (`/`)
- 多条件搜索（型号代码、附加代码、零件名称、类别）
- 搜索结果表格展示
- 分页功能
- 导出功能（JSON、CSV、Excel）
- 查询性能统计

### 2. 零件详情页 (`/parts/:partId`)
- 零件完整信息展示
- PDF文档信息
- PDF下载功能
- 返回导航

### 3. 类别浏览页 (`/categories`)
- 所有类别网格展示
- 类别搜索过滤
- 零件数量统计
- 点击进入类别详情

### 4. 类别零件列表页 (`/categories/:category`)
- 类别下所有零件列表
- 分页浏览
- 快速查看详情

### 5. 统计信息页 (`/statistics`)
- 总览统计（零件数、类别数、代码数）
- PDF覆盖率可视化
- 数据库健康状态
- 类别分布图表

## 开发指南

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问: http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## API配置

前端通过Vite代理连接后端API：

```typescript
// vite.config.ts
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

确保后端API服务运行在 `http://localhost:8000`

## 环境要求

- Node.js >= 16
- npm >= 8

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 开发注意事项

1. **类型安全**: 所有API响应都有TypeScript类型定义
2. **错误处理**: API客户端包含请求/响应拦截器
3. **响应式设计**: 使用Ant Design Grid系统适配不同屏幕
4. **国际化**: 已配置中文语言包

## API客户端使用示例

```typescript
import apiClient from './services/api';

// 查询零件
const response = await apiClient.queryParts({
  catalog_type: 'SJ',
  limit: 20,
  offset: 0
});

// 获取零件详情
const part = await apiClient.getPart('凸模_顶料型凸模');

// 获取类别
const categories = await apiClient.getCategories();

// 导出数据
apiClient.downloadExport('excel', { catalog_type: 'SJ' });
```

## 常见问题

### 1. 端口冲突
如果3000端口被占用，修改 `vite.config.ts` 中的端口号

### 2. API连接失败
确保后端服务运行在 http://localhost:8000

### 3. 依赖安装失败
尝试清除缓存: `npm cache clean --force`

## 许可证

MIT
