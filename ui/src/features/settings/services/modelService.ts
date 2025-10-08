import { apiClient } from "../../../core/api/apiClient";

export async function getAvailableModels(): Promise<string[]> {
  const res = await apiClient.get("/models");
  return res.data;
}

export async function getCurrentModel(projectPath: string): Promise<{ embedding_model: string }> {
  const res = await apiClient.get(`/projects/model?project_path=${encodeURIComponent(projectPath)}`);
  return res.data;
}

export async function setProjectModel(projectPath: string, model: string, autoReindex = false): Promise<any> {
  const res = await apiClient.post(`/projects/model/change?project_path=${encodeURIComponent(projectPath)}`, {
    model,
    auto_reindex: autoReindex
  });
  return res.data;
}
