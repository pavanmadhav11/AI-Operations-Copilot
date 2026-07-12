import api from "../api/api";

export async function getPDFs(sessionId) {
  const response = await api.get(
    `/upload?session_id=${sessionId}`
  );

  return response.data.filter(
    (file) =>
      file.file_type === "application/pdf"
  );
}