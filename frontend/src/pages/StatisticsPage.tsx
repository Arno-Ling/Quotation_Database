import { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, message, Spin, Progress, List } from 'antd';
import {
  DatabaseOutlined,
  FolderOutlined,
  TagsOutlined,
  FilePdfOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';
import apiClient from '../services/api';
import type { Statistics } from '../types';

function StatisticsPage() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<Statistics | null>(null);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    setLoading(true);
    try {
      const data = await apiClient.getStatistics();
      setStats(data);
    } catch (error: any) {
      message.error('加载统计信息失败: ' + (error.response?.data?.error?.message || error.message));
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px' }}>
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  if (!stats) {
    return (
      <div style={{ padding: '24px' }}>
        <Card>
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            无法加载统计信息
          </div>
        </Card>
      </div>
    );
  }

  // 获取前10个类别
  const topCategories = Object.entries(stats.category_distribution)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10);

  return (
    <div style={{ padding: '24px' }}>
      <Row gutter={[16, 16]}>
        {/* 总览统计 */}
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="总零件数"
              value={stats.total_parts}
              prefix={<DatabaseOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="总类别数"
              value={stats.total_categories}
              prefix={<FolderOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="型号代码数"
              value={stats.total_catalog_types}
              prefix={<TagsOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="附加代码数"
              value={stats.total_additional_codes}
              prefix={<TagsOutlined />}
              valueStyle={{ color: '#eb2f96' }}
            />
          </Card>
        </Col>

        {/* PDF覆盖率 */}
        <Col xs={24} md={12}>
          <Card title="PDF文档覆盖率">
            <Progress
              type="circle"
              percent={stats.pdf_coverage.coverage_percentage}
              format={(percent) => `${percent}%`}
              strokeColor={{
                '0%': '#108ee9',
                '100%': '#87d068',
              }}
              style={{ display: 'flex', justifyContent: 'center' }}
            />
            <Row gutter={16} style={{ marginTop: 24 }}>
              <Col span={12}>
                <Statistic
                  title="已找到"
                  value={stats.pdf_coverage.pdfs_found}
                  prefix={<FilePdfOutlined />}
                  valueStyle={{ color: '#52c41a' }}
                />
              </Col>
              <Col span={12}>
                <Statistic
                  title="缺失"
                  value={stats.pdf_coverage.pdfs_missing}
                  valueStyle={{ color: '#ff4d4f' }}
                />
              </Col>
            </Row>
          </Card>
        </Col>

        {/* 数据库健康状态 */}
        <Col xs={24} md={12}>
          <Card title="数据库状态">
            <div style={{ textAlign: 'center', padding: '40px 0' }}>
              <CheckCircleOutlined
                style={{
                  fontSize: 80,
                  color: stats.database_health.database_loaded ? '#52c41a' : '#ff4d4f',
                }}
              />
              <div style={{ marginTop: 16, fontSize: 18 }}>
                {stats.database_health.status === 'healthy' ? '运行正常' : '异常'}
              </div>
              <div style={{ marginTop: 8, color: '#999' }}>
                数据库{stats.database_health.database_loaded ? '已加载' : '未加载'}
              </div>
            </div>
          </Card>
        </Col>

        {/* 类别分布 - 前10 */}
        <Col xs={24}>
          <Card title="类别分布 (前10)">
            <List
              grid={{
                gutter: 16,
                xs: 1,
                sm: 2,
                md: 3,
                lg: 4,
                xl: 5,
              }}
              dataSource={topCategories}
              renderItem={([name, count]) => (
                <List.Item>
                  <Card size="small">
                    <Statistic
                      title={name}
                      value={count}
                      valueStyle={{ fontSize: 20 }}
                    />
                  </Card>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default StatisticsPage;
