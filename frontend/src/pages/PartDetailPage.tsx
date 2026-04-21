import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Descriptions,
  Tag,
  Button,
  Space,
  message,
  Spin,
  Alert,
} from 'antd';
import {
  ArrowLeftOutlined,
  FilePdfOutlined,
  DownloadOutlined,
  EyeOutlined,
} from '@ant-design/icons';
import apiClient from '../services/api';
import PDFPreviewModal from '../components/PDFPreviewModal';
import type { Part, PDFInfo } from '../types';

function PartDetailPage() {
  const { partId } = useParams<{ partId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [part, setPart] = useState<Part | null>(null);
  const [pdfInfo, setPdfInfo] = useState<PDFInfo | null>(null);
  const [error, setError] = useState<string>('');
  const [previewVisible, setPreviewVisible] = useState(false);

  useEffect(() => {
    if (partId) {
      loadPartDetail(decodeURIComponent(partId));
    }
  }, [partId]);

  const loadPartDetail = async (id: string) => {
    setLoading(true);
    setError('');
    
    try {
      // 加载零件详情
      const partData = await apiClient.getPart(id);
      setPart(partData);

      // 加载PDF信息
      try {
        const pdfData = await apiClient.getPDFInfo(id);
        setPdfInfo(pdfData);
      } catch (pdfError) {
        console.warn('PDF信息加载失败:', pdfError);
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.error?.message || err.message || '加载失败';
      setError(errorMsg);
      message.error('加载零件详情失败: ' + errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (partId) {
      const url = apiClient.getPDFDownloadURL(decodeURIComponent(partId));
      window.open(url, '_blank');
      message.success('正在下载PDF文件...');
    }
  };

  const handlePreviewPDF = () => {
    setPreviewVisible(true);
  };

  const handleClosePreview = () => {
    setPreviewVisible(false);
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px' }}>
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  if (error || !part) {
    return (
      <div style={{ padding: '24px' }}>
        <Alert
          message="加载失败"
          description={error || '未找到零件信息'}
          type="error"
          showIcon
        />
        <Button
          type="primary"
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate(-1)}
          style={{ marginTop: 16 }}
        >
          返回
        </Button>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* 返回按钮 */}
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate(-1)}
        >
          返回
        </Button>

        {/* 零件基本信息 */}
        <Card title="零件信息" bordered={false}>
          <Descriptions column={2} bordered>
            <Descriptions.Item label="零件ID" span={2}>
              {part.part_id}
            </Descriptions.Item>
            <Descriptions.Item label="零件名称" span={2}>
              <strong style={{ fontSize: '16px' }}>{part.item_name}</strong>
            </Descriptions.Item>
            <Descriptions.Item label="零件类别">
              <Tag color="purple">{part.part_category}</Tag>
            </Descriptions.Item>
            <Descriptions.Item label="源文件">
              {part.source_file}
            </Descriptions.Item>
            <Descriptions.Item label="型号代码" span={2}>
              <Space wrap>
                {part.catalog_types.map((type) => (
                  <Tag key={type} color="blue">
                    {type}
                  </Tag>
                ))}
              </Space>
            </Descriptions.Item>
            <Descriptions.Item label="附加代码" span={2}>
              <Space wrap>
                {part.additional_codes.map((code) => (
                  <Tag key={code} color="green">
                    {code}
                  </Tag>
                ))}
              </Space>
            </Descriptions.Item>
          </Descriptions>
        </Card>

        {/* PDF信息 */}
        {pdfInfo && (
          <Card
            title="PDF文档信息"
            bordered={false}
            extra={
              pdfInfo.pdf_exists && (
                <Space>
                  <Button
                    icon={<EyeOutlined />}
                    onClick={handlePreviewPDF}
                  >
                    预览PDF
                  </Button>
                  <Button
                    type="primary"
                    icon={<DownloadOutlined />}
                    onClick={handleDownloadPDF}
                  >
                    下载PDF
                  </Button>
                </Space>
              )
            }
          >
            <Descriptions column={2} bordered>
              <Descriptions.Item label="PDF状态">
                {pdfInfo.pdf_exists ? (
                  <Tag color="success" icon={<FilePdfOutlined />}>
                    文件存在
                  </Tag>
                ) : (
                  <Tag color="error">文件不存在</Tag>
                )}
              </Descriptions.Item>
              <Descriptions.Item label="文件大小">
                {pdfInfo.file_size_mb.toFixed(2)} MB
              </Descriptions.Item>
              <Descriptions.Item label="PDF类型">
                {pdfInfo.is_paged_pdf ? '分页PDF' : '源PDF'}
              </Descriptions.Item>
              <Descriptions.Item label="相对路径" span={2}>
                <code>{pdfInfo.pdf_path_relative}</code>
              </Descriptions.Item>
              <Descriptions.Item label="绝对路径" span={2}>
                <code style={{ fontSize: '12px' }}>
                  {pdfInfo.pdf_path_absolute}
                </code>
              </Descriptions.Item>
            </Descriptions>
          </Card>
        )}

        {/* PDF预览Modal */}
        {partId && pdfInfo?.pdf_exists && (
          <PDFPreviewModal
            visible={previewVisible}
            onClose={handleClosePreview}
            pdfUrl={apiClient.getPDFPreviewURL(decodeURIComponent(partId))}
            title={part?.item_name || ''}
          />
        )}
      </Space>
    </div>
  );
}

export default PartDetailPage;
