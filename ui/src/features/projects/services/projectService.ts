import { apiClient } from "../../../core/api/apiClient";

export interface Project {
  path: string;
  name: string;
  indexed_files: number;
  total_chunks: number;
  is_current: boolean;
}

export interface ProjectStats {
  project_root: string;
  indexed_files: number;
  total_chunks: number;
  vector_db_size: string;
  embedding_model: string;
  is_current: boolean;
  all_projects: string[];
}

export async function listProjects(): Promise<{
  total_projects: number;
  current_project: string | null;
  projects: Project[];
}> {
  const res = await apiClient.get("/projects");
  return res.data;
}

export async function switchProject(projectPath: string): Promise<{
  status: string;
  current_project: string;
  message: string;
}> {
  const res = await apiClient.post("/switch", { project_path: projectPath });
  return res.data;
}

export async function getProjectStats(projectPath?: string): Promise<ProjectStats> {
  const params = projectPath ? { project_path: projectPath } : {};
  const res = await apiClient.get("/stats", { params });
  return res.data;
}

export async function clearProject(projectPath?: string): Promise<{
  status: string;
  message: string;
}> {
  const params = projectPath ? { project_path: projectPath } : {};
  const res = await apiClient.delete("/clear", { params });
  return res.data;
}
