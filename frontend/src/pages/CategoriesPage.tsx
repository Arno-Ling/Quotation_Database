import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, List, Badge, message, Spin, Input } from 'antd';
import { FolderOutlined, SearchOutlined } from '@ant-design/icons';
import apiClient from '../services/api';
import type { Category } from '../types';

const { Search } = Input;

function CategoriesPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState<Category[]>([]);
  const [filteredCategories, setFilteredCategories] = useState<Category[]>([]);
  const [searchText, setSearchText] = useState('');

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    // 过滤类别
    if (searchText) {
      const filtered = categories.filter((cat) =>
        cat.name.toLowerCase().includes(searchText.toLowerCase())
      );
      setFilteredCategories(filtered);
    } else {
      setFilteredCategories(categories);
    }
  }, [searchText, categories]);

  const loadCategories = async () => {
    setLoading(true);
    try {
      const response = await apiClient.getCategories();
      setCategories(response.categories);
      setFilteredCategories(response.categories);
    } catch (error: any) {
      message.error('加载类别失败: ' + (error.response?.data?.error?.message || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryClick = (categoryName: string) => {
    navigate(`/categories/${encodeURIComponent(categoryName)}`);
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px' }}>
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card
        title={
          <span>
            <FolderOutlined style={{ marginRight: 8 }} />
            零件类别浏览
          </span>
        }
        extra={<span>共 {categories.length} 个类别</span>}
      >
        {/* 搜索框 */}
        <Search
          placeholder="搜索类别名称"
          prefix={<SearchOutlined />}
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          style={{ marginBottom: 16 }}
          allowClear
        />

        {/* 类别列表 */}
        <List
          grid={{
            gutter: 16,
            xs: 1,
            sm: 2,
            md: 3,
            lg: 4,
            xl: 4,
            xxl: 6,
          }}
          dataSource={filteredCategories}
          renderItem={(category) => (
            <List.Item>
              <Card
                hoverable
                onClick={() => handleCategoryClick(category.name)}
                style={{ textAlign: 'center' }}
              >
                <FolderOutlined style={{ fontSize: 48, color: '#1890ff', marginBottom: 16 }} />
                <div style={{ fontSize: 16, fontWeight: 'bold', marginBottom: 8 }}>
                  {category.name}
                </div>
                <Badge
                  count={category.count}
                  showZero
                  style={{ backgroundColor: '#52c41a' }}
                />
                <div style={{ marginTop: 4, color: '#999', fontSize: 12 }}>
                  个零件
                </div>
              </Card>
            </List.Item>
          )}
        />

        {filteredCategories.length === 0 && (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            未找到匹配的类别
          </div>
        )}
      </Card>
    </div>
  );
}

export default CategoriesPage;
