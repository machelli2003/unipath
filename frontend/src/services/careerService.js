import api from "./apiClient";

export async function listCareers() {
  const { data } = await api.get("/careers");
  return data;
}

export async function getCareer(name) {
  const { data } = await api.get(`/careers/${encodeURIComponent(name)}`);
  return data;
}
