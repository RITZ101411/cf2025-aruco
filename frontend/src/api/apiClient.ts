import axios from "axios";
import type { AxiosInstance } from "axios";
import type { User } from "../types/User";

const apiUrl = "/api";

const api: AxiosInstance = axios.create({
    baseURL: apiUrl,
    headers: {
        "Content-Type": "application/json",
    },
    withCredentials: true,
});

//POST
export async function postRequest<T>(endpoint: string, body: unknown, token?: string): Promise<T> {
    const res = await api.post(endpoint, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    return res.data;
}

//GET
export async function getRequest<T>(endpoint: string, token?: string): Promise<T> {
    const res = await api.get(endpoint, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    return res.data;
}

export async function getUsers(): Promise<User[]> {
    return await getRequest<User[]>("/get-users");
}

export const init = async (): Promise<User> => {
    const res = await axios.get("/api/init");
    return res.data;
  };