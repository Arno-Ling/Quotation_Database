import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu, Typography } from 'antd';
import {
  HomeOutlined,
  SearchOutlined,
  FolderOutlined,
  BarChartOutlined,
} from '@ant-design/icons';
import HomePage from './pages/HomePage';
import PartDetailPage from './pages/PartDetailPage';
import CategoriesPage from './pages/CategoriesPage';
import CategoryPartsPage from './pages/CategoryPartsPage';
import StatisticsPage from './pages/StatisticsPage';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

function App() {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ display: 'flex', alignItems: 'center', background: '#001529' }}>
          <Title level={3} style={{ color: 'white', margin: '0 24px 0 0' }}>
            模具零件数据库
          </Title>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['home']}
            style={{ flex: 1, minWidth: 0 }}
          >
            <Menu.Item key="home" icon={<HomeOutlined />}>
              <Link to="/">首页</Link>
            </Menu.Item>
            <Menu.Item key="search" icon={<SearchOutlined />}>
              <Link to="/">搜索</Link>
            </Menu.Item>
            <Menu.Item key="categories" icon={<FolderOutlined />}>
              <Link to="/categories">类别浏览</Link>
            </Menu.Item>
            <Menu.Item key="statistics" icon={<BarChartOutlined />}>
              <Link to="/statistics">统计信息</Link>
            </Menu.Item>
          </Menu>
        </Header>

        <Content style={{ padding: '24px 50px' }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/parts/:partId" element={<PartDetailPage />} />
            <Route path="/categories" element={<CategoriesPage />} />
            <Route path="/categories/:category" element={<CategoryPartsPage />} />
            <Route path="/statistics" element={<StatisticsPage />} />
          </Routes>
        </Content>

        <Footer style={{ textAlign: 'center' }}>
          模具零件数据库查询系统 ©2026
        </Footer>
      </Layout>
    </Router>
  );
}

export default App;
