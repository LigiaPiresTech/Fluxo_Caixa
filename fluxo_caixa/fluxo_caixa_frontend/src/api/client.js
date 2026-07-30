import axios from "axios";
import { fetchAuthSession } from "aws-amplify/auth";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
});

api.interceptors.request.use(async (config) => {
  const session = await fetchAuthSession();
  const token = session.tokens?.accessToken?.toString();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  config.headers["X-Request-ID"] = crypto.randomUUID();
  return config;
});

export const services = {
  usuarios: "/usuarios",
  cadastros: "/cadastros",
  contas: "/contas",
  lancamentos: "/lancamentos",
  consolidado: "/consolidado",
  relatorios: "/relatorios",
};
