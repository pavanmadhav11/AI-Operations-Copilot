import api from "../api/api";

export async function uploadFile(sessionId, file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    `/upload?session_id=${sessionId}`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export async function getFiles(sessionId) {
  const response = await api.get(
    `/upload?session_id=${sessionId}`
  );

  return response.data;
}

export async function deleteFile(id) {
  const response = await api.delete(
    `/upload/${id}`
  );

  return response.data;
}