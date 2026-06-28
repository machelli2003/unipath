import api from "./apiClient";

export async function submitAssessment({ mode, subjects, isSimulation = false }) {
  const { data } = await api.post("/assess", {
    mode,
    subjects,
    is_simulation: isSimulation,
  });
  return data;
}
