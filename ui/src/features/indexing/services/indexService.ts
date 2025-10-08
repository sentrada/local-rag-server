import { apiClient } from "../../../core/api/apiClient";

export interface IndexRequest {
  project_path: string;
  file_extensions?: string[];
  model?: string;
  force_reindex?: boolean;
}

export interface IndexResponse {
  status: string;
  message: string;
  project_path: string;
  file_extensions: string[];
  embedding_model: string;
  total_projects: number;
}

export async function indexProject(request: IndexRequest): Promise<IndexResponse> {
  const res = await apiClient.post("/index", request);
  return res.data;
}

export async function reindexProject(projectPath: string, model?: string): Promise<IndexResponse> {
  const res = await apiClient.post("/index", {
    project_path: projectPath,
    force_reindex: true,
    model
  });
  return res.data;
}
