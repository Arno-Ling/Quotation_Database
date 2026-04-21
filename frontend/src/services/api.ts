import axios, { AxiosInstance } from 'axios';
import type {
  Part,
  QueryParams,
  QueryResponse,
  CategoriesResponse,
  PDFInfo,
  Statistics,
  HealthResponse,
  ExportFormat
} from '../types';

/**
 * API客户端类
 */
class APIClient {
  private client: AxiosInstance;

  constructor(baseURL: string = '/api') {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        console.log('API Request:', config.method?.toUpperCase(), config.url);
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器
    this.client.interceptors.response.use(
      (response) => {
        console.log('API Response:', response.status, response.config.url);
        return response;
      },
      (error) => {
        console.error('API Error:', error.response?.status, error.message);
        return Promise.reject(error);
      }
    );
  }

  /**
   * 健康检查
   */
  async health(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/health');
    return response.data;
  }

  /**
   * 查询零件
   */
  async queryParts(params: QueryParams): Promise<QueryResponse> {
    const response = await this.client.get<QueryResponse>('/parts', { params });
    return response.data;
  }

  /**
   * 获取零件详情
   */
  async getPart(partId: string): Promise<Part> {
    const response = await this.client.get<Part>(`/parts/${encodeURIComponent(partId)}`);
    return response.data;
  }

  /**
   * 获取PDF信息
   */
  async getPDFInfo(partId: string): Promise<PDFInfo> {
    const response = await this.client.get<PDFInfo>(
      `/parts/${encodeURIComponent(partId)}/pdf`,
      { params: { format: 'absolute' } }
    );
    return response.data;
  }

  /**
   * 下载PDF文件
   */
  getPDFDownloadURL(partId: string): string {
    return `/api/parts/${encodeURIComponent(partId)}/pdf?download=true`;
  }

  /**
   * 获取所有类别
   */
  async getCategories(): Promise<CategoriesResponse> {
    const response = await this.client.get<CategoriesResponse>('/categories');
    return response.data;
  }

  /**
   * 获取类别下的零件
   */
  async getCategoryParts(
    category: string,
    limit: number = 100,
    offset: number = 0
  ): Promise<QueryResponse> {
    const response = await this.client.get<QueryResponse>(
      `/categories/${encodeURIComponent(category)}/parts`,
      { params: { limit, offset } }
    );
    return response.data;
  }

  /**
   * 获取统计信息
   */
  async getStatistics(): Promise<Statistics> {
    const response = await this.client.get<Statistics>('/statistics');
    return response.data;
  }

  /**
   * 导出数据
   */
  getExportURL(format: ExportFormat, params: QueryParams): string {
    const queryParams = new URLSearchParams();
    queryParams.append('format', format);
    
    if (params.catalog_type) queryParams.append('catalog_type', params.catalog_type);
    if (params.additional_code) queryParams.append('additional_code', params.additional_code);
    if (params.item_name) queryParams.append('item_name', params.item_name);
    if (params.category) queryParams.append('category', params.category);
    if (params.logic) queryParams.append('logic', params.logic);
    if (params.case_sensitive !== undefined) queryParams.append('case_sensitive', String(params.case_sensitive));
    if (params.use_regex !== undefined) queryParams.append('use_regex', String(params.use_regex));
    if (params.limit) queryParams.append('limit', String(params.limit));

    return `/api/export?${queryParams.toString()}`;
  }

  /**
   * 触发导出下载
   */
  downloadExport(format: ExportFormat, params: QueryParams): void {
    const url = this.getExportURL(format, params);
    window.open(url, '_blank');
  }
}

// 创建单例实例
const apiClient = new APIClient();

export default apiClient;
