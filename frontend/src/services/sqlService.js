import api from "../api/api";

export async function generateSQL(question) {
  const response = await api.post("/sql", {
    question,
  });

  return response.data;
}