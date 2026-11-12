import api from "../api/api";

export async function getInventory({ limit, offset = 0 } = {}) {
  const params = limit ? { limit, offset } : undefined;
  const response = await api.get("/inventory", { params });
  return response.data;
}

export async function getWarehouses() {
  const response = await api.get("/inventory/warehouses");
  return response.data;
}

export async function addWarehouse(warehouse) {
  const response = await api.post("/inventory/warehouses", warehouse);
  return response.data;
}

export async function addInventoryItem(item) {
  const response = await api.post("/inventory", item);
  return response.data;
}

export async function getStockMovements({ limit = 25, offset = 0 } = {}) {
  const response = await api.get("/inventory/movements", { params: { limit, offset } });
  return response.data;
}

export async function getStockActions() {
  const response = await api.get("/inventory/actions");
  return response.data;
}

export async function previewTransfer(transfer) {
  const response = await api.post("/inventory/transfers/preview", transfer);
  return response.data;
}

export async function getExpiringBatches(days = 30) {
  const response = await api.get(`/inventory/batches/expiring?days=${days}`);
  return response.data;
}

export async function addStockBatch(batch) {
  const response = await api.post("/inventory/batches", batch);
  return response.data;
}

export async function writeOffExpiredBatch(batchId) {
  const response = await api.post(`/inventory/batches/${batchId}/write-off`);
  return response.data;
}

export async function getRecommendationMetrics() {
  const response = await api.get("/recommendations/metrics");
  return response.data;
}

export async function sendRecommendationFeedback(feedback) {
  const response = await api.post("/recommendations/feedback", feedback);
  return response.data;
}
