import api from "./apiClient";

export async function runSimulation({ mode, subjects }) {
  const { data } = await api.post("/simulate", { mode, subjects });
  return data;
}
