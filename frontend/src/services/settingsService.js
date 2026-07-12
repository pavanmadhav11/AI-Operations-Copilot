import api from "../api/api";

export async function getProfile() {
  const response = await api.get("/settings/profile");
  return response.data;
}

export async function updateProfile(data) {
  const response = await api.put(
    "/settings/profile",
    data
  );

  return response.data;
}

export async function changePassword(data) {
  const response = await api.put(
    "/settings/password",
    data
  );

  return response.data;
}