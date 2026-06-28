import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  headers: { "Content-Type": "application/json" },
});

// Attach JWT access token to every outgoing request, if present.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("unipath_access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401, clear stale auth state so the app can redirect to login.
// (Token refresh flow can be added here later using the refresh_token.)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("unipath_access_token");
      localStorage.removeItem("unipath_refresh_token");
      localStorage.removeItem("unipath_user");
    }
    return Promise.reject(error);
  }
);

export default api;
