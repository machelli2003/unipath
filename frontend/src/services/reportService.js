import api from "./apiClient";

export async function generateReport(reportType = "recommendation_summary") {
  const { data } = await api.post("/api/v2/report/generate");
  return data;
}

export function getReportDownloadUrl(reportId) {
  return `/api/v2/report/${reportId}/download`;
}
