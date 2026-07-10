import api from "../api/api";

export async function register(data) {
  const response = await api.post("/auth/register", data);
  return response.data;
}

export async function login(data) {
  const response = await api.post("/auth/login", data);

  localStorage.setItem(
    "token",
    response.data.access_token
  );

  return response.data;
}

export async function getCurrentUser() {
  const response = await api.get("/auth/me");
  return response.data;
}

export function logout() {
  localStorage.removeItem("token");
}