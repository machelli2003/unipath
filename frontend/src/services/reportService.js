import api from "./apiClient";

export async function generateReport(recommendationId, reportType = "recommendation_summary") {
  const { data } = await api.post("/report", {
    recommendation_id: recommendationId,
    report_type: reportType,
  });
  return data;
}

export function getReportDownloadUrl(reportId) {
  return `/api/report/${reportId}/download`;
}
