import api from "../api/api";

export async function getNotifications() {
  const response = await api.get("/notifications");
  return response.data;
}

export async function markNotificationRead(notificationId) {
  const response = await api.post(`/notifications/${notificationId}/read`);
  return response.data;
}
