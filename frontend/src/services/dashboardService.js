import api from "../api/api";

export async function getDashboardStats() {
  const response = await api.get("/dashboard");
  return response.data;
}

export async function getActivityChart() {
  const response = await api.get("/dashboard/activity");
  return response.data;
}

export async function getRecentActivity() {
  const response = await api.get("/dashboard/recent-activity");
  return response.data;
}

export async function getRecentDocuments() {
  const response = await api.get("/dashboard/recent-documents");
  return response.data;
}