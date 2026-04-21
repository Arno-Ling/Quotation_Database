import { Modal } from 'antd';
import { useState, useEffect } from 'react';

interface PDFPreviewModalProps {
  visible: boolean;
  onClose: () => void;
  pdfUrl: string;
  title: string;
}

function PDFPreviewModal({ visible, onClose, pdfUrl, title }: PDFPreviewModalProps) {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (visible) {
      setLoading(true);
    }
  }, [visible]);

  const handleIframeLoad = () => {
    setLoading(false);
  };

  return (
    <Modal
      title={`PDF预览 - ${title}`}
      open={visible}
      onCancel={onClose}
      footer={null}
      width="90%"
      style={{ top: 20 }}
      bodyStyle={{ height: 'calc(100vh - 200px)', padding: 0 }}
    >
      {loading && (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100%' 
        }}>
          <div>加载中...</div>
        </div>
      )}
      <iframe
        src={pdfUrl}
        style={{
          width: '100%',
          height: '100%',
          border: 'none',
          display: loading ? 'none' : 'block'
        }}
        title="PDF预览"
        onLoad={handleIframeLoad}
      />
    </Modal>
  );
}

export default PDFPreviewModal;
