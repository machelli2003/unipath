import api from "./apiClient";

export async function compareItems(type, names) {
  const { data } = await api.post("/compare", { type, names });
  return data;
}
