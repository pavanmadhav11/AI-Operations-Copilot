import api from "../api/api";

export async function uploadExcel(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/excel/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export async function getExcels() {
  const response = await api.get("/excel");

  return response.data;
}

export async function deleteExcel(id) {
  const response = await api.delete(
    `/excel/${id}`
  );

  return response.data;
}