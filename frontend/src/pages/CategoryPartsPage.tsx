import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Table,
  Button,
  Tag,
  message,
  Spin,
  Pagination,
  Space,
} from 'antd';
import { ArrowLeftOutlined, EyeOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import apiClient from '../services/api';
import type { Part } from '../types';

function CategoryPartsPage() {
  const { category } = useParams<{ category: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [parts, setParts] = useState<Part[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  useEffect(() => {
    if (category) {
      loadCategoryParts(decodeURIComponent(category), 1, pageSize);
    }
  }, [category]);

  const loadCategoryParts = async (cat: string, page: number, size: number) => {
    setLoading(true);
    try {
      const response = await apiClient.getCategoryParts(cat, size, (page - 1) * size);
      setParts(response.results);
      setTotal(response.total);
      setCurrentPage(page);
      setPageSize(size);
    } catch (error: any) {
      message.error('加载失败: ' + (error.response?.data?.error?.message || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page: number, size: number) => {
    if (category) {
      loadCategoryParts(decodeURIComponent(category), page, size);
    }
  };

  const handleViewDetail = (partId: string) => {
    navigate(`/parts/${encodeURIComponent(partId)}`);
  };

  const columns: ColumnsType<Part> = [
    {
      title: '零件名称',
      dataIndex: 'item_name',
      key: 'item_name',
      width: 250,
      ellipsis: true,
    },
    {
      title: '型号代码',
      dataIndex: 'catalog_types',
      key: 'catalog_types',
      width: 200,
      render: (types: string[]) => (
        <>
          {types.slice(0, 3).map((type) => (
            <Tag key={type} color="blue">
              {type}
            </Tag>
          ))}
          {types.length > 3 && <Tag>+{types.length - 3}</Tag>}
        </>
      ),
    },
    {
      title: '附加代码',
      dataIndex: 'additional_codes',
      key: 'additional_codes',
      width: 200,
      render: (codes: string[]) => (
        <>
          {codes.slice(0, 3).map((code) => (
            <Tag key={code} color="green">
              {code}
            </Tag>
          ))}
          {codes.length > 3 && <Tag>+{codes.length - 3}</Tag>}
        </>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      render: (_, record) => (
        <Button
          type="link"
          icon={<EyeOutlined />}
          onClick={() => handleViewDetail(record.part_id)}
        >
          查看
        </Button>
      ),
    },
  ];

  if (loading && parts.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '100px' }}>
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/categories')}
        >
          返回类别列表
        </Button>

        <Card
          title={`类别: ${category ? decodeURIComponent(category) : ''}`}
          extra={<span>共 {total} 个零件</span>}
        >
          <Table
            columns={columns}
            dataSource={parts}
            rowKey="part_id"
            loading={loading}
            pagination={false}
            scroll={{ x: 750 }}
          />

          {total > 0 && (
            <Pagination
              current={currentPage}
              pageSize={pageSize}
              total={total}
              onChange={handlePageChange}
              showSizeChanger
              showQuickJumper
              showTotal={(total) => `共 ${total} 条`}
              style={{ marginTop: 16, textAlign: 'right' }}
            />
          )}
        </Card>
      </Space>
    </div>
  );
}

export default CategoryPartsPage;
