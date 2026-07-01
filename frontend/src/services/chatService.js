import api from "./apiClient";

export async function sendChatMessage(message, sessionId = null) {
  const { data } = await api.post("/api/chat", { message, session_id: sessionId });
  return data;
}

export async function getChatHistory() {
  const { data } = await api.get("/api/chat/history");
  return data;
}
