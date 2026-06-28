import api from "./apiClient";

export async function listUniversities(page = 1, perPage = 20) {
  const { data } = await api.get("/universities", { params: { page, per_page: perPage } });
  return data;
}

export async function getUniversity(name) {
  const { data } = await api.get(`/universities/${encodeURIComponent(name)}`);
  return data;
}
