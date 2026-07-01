import api from "./apiClient";

export async function listCourses(page = 1, perPage = 20) {
  const { data } = await api.get("/api/courses", { params: { page, per_page: perPage } });
  return data;
}

export async function getCourse(name) {
  const { data } = await api.get(`/api/courses/${encodeURIComponent(name)}`);
  return data;
}
