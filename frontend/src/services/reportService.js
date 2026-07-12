import api from "../api/api";

async function download(url, filename) {
  const response = await api.get(url, {
    responseType: "blob",
  });

  const blob = new Blob([response.data]);

  const link = document.createElement("a");

  link.href = window.URL.createObjectURL(blob);

  link.download = filename;

  link.click();
}

export const downloadDashboardReport = () =>
  download(
    "/reports/dashboard",
    "dashboard_report.pdf"
  );

export const downloadChatReport = () =>
  download(
    "/reports/chat",
    "chat_report.pdf"
  );

export const downloadDocumentReport = () =>
  download(
    "/reports/documents",
    "documents_report.pdf"
  );

export const downloadSQLReport = () =>
  download(
    "/reports/sql",
    "sql_report.pdf"
  );