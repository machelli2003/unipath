import api from "./apiClient";

export async function compareItems(type, names) {
  const { data } = await api.post("/api/compare", { type, names });
  return data;
}
