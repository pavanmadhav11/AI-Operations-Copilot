import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const loginUser = async (data) => {
  const response = await api.post("/auth/login", data);
  return response.data;
};

export const registerUser = async (data) => {
  const response = await api.post("/auth/register", data);
  return response.data;
};

export default api;