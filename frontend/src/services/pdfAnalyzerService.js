import api from "../api/api";

export async function uploadPDF(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/pdf/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export async function getPDFs() {
  const response = await api.get("/pdf");

  return response.data;
}

export async function deletePDF(id) {
  await api.delete(`/pdf/${id}`);
}