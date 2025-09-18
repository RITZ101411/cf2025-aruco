import axios from "axios";

import type { Post } from "../types/Post"

const api = axios.create({
  baseURL: "http://0.0.0.0:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Post一覧取得
export const getPosts = async (): Promise<Post[]> => {
  const res = await api.get<Post[]>("/posts");
  return res.data;
};

// Post単体取得
export const getPost = async (id: number): Promise<Post> => {
  const res = await api.get<Post>(`/posts/${id}`);
  return res.data;
};

// Post作成
export const createPost = async (post: Omit<Post, "id">): Promise<Post> => {
  const res = await api.post<Post>("/posts", post);
  return res.data;
};

// Post更新
export const updatePost = async (id: number, post: Partial<Post>): Promise<Post> => {
  const res = await api.put<Post>(`/posts/${id}`, post);
  return res.data;
};

// Post削除
export const deletePost = async (id: number): Promise<void> => {
  await api.delete(`/posts/${id}`);
};