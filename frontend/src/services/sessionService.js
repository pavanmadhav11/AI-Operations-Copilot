import api from "../api/api";

export const getSessions = async () => {
  const response = await api.get("/chat/sessions");
  return response.data;
};

export const createSession = async () => {
  const response = await api.post("/chat/sessions", {
    title: "New Chat",
  });

  return response.data;
};

export const deleteSession = async (id) => {
  await api.delete(`/chat/sessions/${id}`);
};