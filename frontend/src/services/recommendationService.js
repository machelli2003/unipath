import api from "./apiClient";

export async function getRecommendations(assessmentId) {
  const { data } = await api.post("/api/v2/recommend", { assessment_id: assessmentId });
  return data;
}

export async function getLatestRecommendations() {
  const { data } = await api.get("/api/v2/recommend/latest");
  return data;
}
