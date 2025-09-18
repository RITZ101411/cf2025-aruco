import axios from "axios";
import type { AxiosInstance } from "axios";
import type { User } from "../types/User";

const apiUrl = "/api";

const api: AxiosInstance = axios.create({
  baseURL: apiUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

//POST
export async function postRequest<T>(endpoint: string, body: any, token?: string): Promise<T> {
  const res = await api.post(endpoint, body, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  return res.data;
}

export async function getUsers(): Promise<User[]> {
  const res = await api.get<User[]>("/get-users");
  return res.data;
}