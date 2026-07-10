const dashboardStats = {
  users: 1284,
  documents: 8450,
  aiRequests: 42813,
  storage: "72 GB",
};

const recentActivities = [
  "Contract uploaded",
  "AI generated report",
  "SQL query executed",
  "Forecast completed",
  "Email summarized",
];

const recentDocuments = [
  "Invoice.pdf",
  "Report.xlsx",
  "Meeting.pdf",
  "Budget.xlsx",
  "Shipment.pdf",
];

export function getDashboardStats() {
  return Promise.resolve(dashboardStats);
}

export function getRecentActivities() {
  return Promise.resolve(recentActivities);
}

export function getRecentDocuments() {
  return Promise.resolve(recentDocuments);
}