import api from "./api";

export const sendMessage = async (
    sessionId,
    message,
) => {

    const response = await api.post("/chat", {
        session_id: sessionId,
        message,
    });

    return response.data;
};

export const getHistory = async (
    sessionId,
) => {

    const response = await api.get(
        `/chat/${sessionId}/history`
    );

    return response.data;
};