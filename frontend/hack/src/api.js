import axios from "axios";

// Create an axios instance with default settings
const api = axios.create({
  baseURL: "http://localhost:8000", // Django API base URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Add the JWT token to every request's Authorization header (if it exists)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
