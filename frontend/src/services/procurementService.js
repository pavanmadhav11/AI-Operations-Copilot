import api from "../api/api";

export async function getPurchaseOrders() {
  const response = await api.get("/procurement/orders");
  return response.data;
}

export async function createPurchaseOrderDraft(fileId, recommendation) {
  const response = await api.post(`/procurement/quotes/${fileId}/draft`, recommendation);
  return response.data;
}

export async function extractPurchaseQuote(fileId) {
  const response = await api.post(`/procurement/quotes/${fileId}/extract`);
  return response.data;
}
