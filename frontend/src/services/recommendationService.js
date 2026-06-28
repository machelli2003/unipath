import api from "./apiClient";

export async function getRecommendations(assessmentId) {
  const { data } = await api.post("/recommend", { assessment_id: assessmentId });
  return data;
}
