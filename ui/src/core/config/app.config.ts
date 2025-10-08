export const appConfig = {
  apiBaseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  apiTimeout: 30000,
  enableWebSocket: false,
};
