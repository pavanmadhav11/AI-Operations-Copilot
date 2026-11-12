import api from "../api/api";

export async function generateSQL(question) {
  const response = await api.post("/sql", {
    question,
  });

  return response.data;
}

export async function confirmStockAction(actionId) {
  const response = await api.post(`/inventory/actions/${actionId}/confirm`);
  return response.data;
}

export async function rejectStockAction(actionId) {
  const response = await api.post(`/inventory/actions/${actionId}/reject`);
  return response.data;
}
