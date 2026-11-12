import api from "../api/api";

export async function getUsers() {
  const response = await api.get("/auth/users");
  return response.data;
}

export async function updateUserRole(userId, role) {
  const response = await api.put(`/auth/users/${userId}/role`, { role });
  return response.data;
}
