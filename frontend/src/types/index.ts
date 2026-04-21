/**
 * 零件数据类型
 */
export interface Part {
  part_id: string;
  item_name: string;
  part_category: string;
  catalog_types: string[];
  additional_codes: string[];
  source_file: string;
  pdf_path?: string;
}

/**
 * 查询请求参数
 */
export interface QueryParams {
  catalog_type?: string;
  additional_code?: string;
  item_name?: string;
  category?: string;
  logic?: 'AND' | 'OR';
  case_sensitive?: boolean;
  use_regex?: boolean;
  limit?: number;
  offset?: number;
}

/**
 * 查询响应
 */
export interface QueryResponse {
  total: number;
  limit: number;
  offset: number;
  results: Part[];
  truncated: boolean;
  query_time_ms: number;
}

/**
 * 类别信息
 */
export interface Category {
  name: string;
  count: number;
  description: string;
}

/**
 * 类别响应
 */
export interface CategoriesResponse {
  total_categories: number;
  categories: Category[];
}

/**
 * PDF信息
 */
export interface PDFInfo {
  part_id: string;
  item_name: string;
  part_category: string;
  source_file: string;
  pdf_exists: boolean;
  is_paged_pdf: boolean;
  pdf_path_absolute: string;
  pdf_path_relative: string;
  file_size_bytes: number;
  file_size_mb: number;
}

/**
 * 统计信息
 */
export interface Statistics {
  total_parts: number;
  total_categories: number;
  total_catalog_types: number;
  total_additional_codes: number;
  pdf_coverage: {
    pdfs_found: number;
    pdfs_missing: number;
    coverage_percentage: number;
  };
  category_distribution: Record<string, number>;
  database_health: {
    status: string;
    database_loaded: boolean;
  };
}

/**
 * 健康检查响应
 */
export interface HealthResponse {
  status: string;
  timestamp: number;
  version: string;
  database_loaded: boolean;
  total_parts: number;
}

/**
 * 导出格式
 */
export type ExportFormat = 'json' | 'csv' | 'excel';
