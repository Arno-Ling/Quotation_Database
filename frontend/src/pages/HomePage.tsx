import { useState } from 'react';
import {
  Input,
  Select,
  Button,
  Table,
  Space,
  Card,
  message,
  Tag,
  Pagination,
  Dropdown,
  MenuProps,
} from 'antd';
import { SearchOutlined, DownloadOutlined, EyeOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import type { ColumnsType } from 'antd/es/table';
import apiClient from '../services/api';
import type { Part, QueryParams, ExportFormat } from '../types';

const { Option } = Select;

function HomePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [searchType, setSearchType] = useState<string>('catalog_type');
  const [searchValue, setSearchValue] = useState<string>('');
  const [results, setResults] = useState<Part[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [queryTime, setQueryTime] = useState<number>(0);

  // 执行搜索
  const handleSearch = async (page: number = 1, size: number = pageSize) => {
    if (!searchValue.trim()) {
      message.warning('请输入搜索关键词');
      return;
    }

    setLoading(true);
    try {
      const params: QueryParams = {
        limit: size,
        offset: (page - 1) * size,
      };

      // 根据搜索类型设置参数
      if (searchType === 'catalog_type') {
        params.catalog_type = searchValue;
      } else if (searchType === 'additional_code') {
        params.additional_code = searchValue;
      } else if (searchType === 'item_name') {
        params.item_name = searchValue;
      } else if (searchType === 'category') {
        params.category = searchValue;
      }

      const response = await apiClient.queryParts(params);
      setResults(response.results);
      setTotal(response.total);
      setCurrentPage(page);
      setPageSize(size);
      setQueryTime(response.query_time_ms);

      message.success(`找到 ${response.total} 个零件，查询耗时 ${response.query_time_ms.toFixed(2)}ms`);
    } catch (error: any) {
      message.error('查询失败: ' + (error.response?.data?.error?.message || error.message));
    } finally {
      setLoading(false);
    }
  };

  // 分页变化
  const handlePageChange = (page: number, size: number) => {
    handleSearch(page, size);
  };

  // 查看详情
  const handleViewDetail = (partId: string) => {
    navigate(`/parts/${encodeURIComponent(partId)}`);
  };

  // 导出菜单
  const exportMenuItems: MenuProps['items'] = [
    {
      key: 'json',
      label: '导出为 JSON',
      onClick: () => handleExport('json'),
    },
    {
      key: 'csv',
      label: '导出为 CSV',
      onClick: () => handleExport('csv'),
    },
    {
      key: 'excel',
      label: '导出为 Excel',
      onClick: () => handleExport('excel'),
    },
  ];

  // 导出数据
  const handleExport = (format: ExportFormat) => {
    if (!searchValue.trim()) {
      message.warning('请先执行搜索');
      return;
    }

    const params: QueryParams = { limit: 10000 };
    
    if (searchType === 'catalog_type') {
      params.catalog_type = searchValue;
    } else if (searchType === 'additional_code') {
      params.additional_code = searchValue;
    } else if (searchType === 'item_name') {
      params.item_name = searchValue;
    } else if (searchType === 'category') {
      params.category = searchValue;
    }

    apiClient.downloadExport(format, params);
    message.success(`正在导出为 ${format.toUpperCase()} 格式...`);
  };

  // 表格列定义
  const columns: ColumnsType<Part> = [
    {
      title: '零件名称',
      dataIndex: 'item_name',
      key: 'item_name',
      width: 250,
      ellipsis: true,
    },
    {
      title: '类别',
      dataIndex: 'part_category',
      key: 'part_category',
      width: 150,
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

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          {/* 搜索栏 */}
          <Space.Compact style={{ width: '100%' }}>
            <Select
              value={searchType}
              onChange={setSearchType}
              style={{ width: 150 }}
            >
              <Option value="catalog_type">型号代码</Option>
              <Option value="additional_code">附加代码</Option>
              <Option value="item_name">零件名称</Option>
              <Option value="category">零件类别</Option>
            </Select>
            <Input
              placeholder="请输入搜索关键词"
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              onPressEnter={() => handleSearch()}
              style={{ flex: 1 }}
            />
            <Button
              type="primary"
              icon={<SearchOutlined />}
              onClick={() => handleSearch()}
              loading={loading}
            >
              搜索
            </Button>
          </Space.Compact>

          {/* 结果统计和导出 */}
          {results.length > 0 && (
            <Space style={{ justifyContent: 'space-between', width: '100%' }}>
              <span>
                找到 <strong>{total}</strong> 个零件，查询耗时{' '}
                <strong>{queryTime.toFixed(2)}ms</strong>
              </span>
              <Dropdown menu={{ items: exportMenuItems }} placement="bottomRight">
                <Button icon={<DownloadOutlined />}>导出数据</Button>
              </Dropdown>
            </Space>
          )}

          {/* 结果表格 */}
          <Table
            columns={columns}
            dataSource={results}
            rowKey="part_id"
            loading={loading}
            pagination={false}
            scroll={{ x: 900 }}
          />

          {/* 分页 */}
          {total > 0 && (
            <Pagination
              current={currentPage}
              pageSize={pageSize}
              total={total}
              onChange={handlePageChange}
              showSizeChanger
              showQuickJumper
              showTotal={(total) => `共 ${total} 条`}
              style={{ textAlign: 'right' }}
            />
          )}
        </Space>
      </Card>
    </div>
  );
}

export default HomePage;
