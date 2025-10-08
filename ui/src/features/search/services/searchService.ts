import { apiClient } from "../../../core/api/apiClient";

export interface QueryRequest {
  query: string;
  max_results?: number;
  include_metadata?: boolean;
  project_path?: string;
}

export interface QueryResponse {
  optimized_prompt: string;
  context_chunks: number;
  token_count: number;
  metadata?: {
    project_root: string;
    queried_project: string;
    indexed_files: number;
    total_chunks: number;
    embedding_model: string;
    available_projects: string[];
  };
}

export async function queryRAG(request: QueryRequest): Promise<QueryResponse> {
  const res = await apiClient.post("/query", request);
  return res.data;
}

export async function getHealth(): Promise<{
  status: string;
  version: string;
  indexed_projects: number;
  current_project: string | null;
  projects: string[];
  vector_db_status: string;
}> {
  const res = await apiClient.get("/health");
  return res.data;
}
