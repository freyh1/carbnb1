import {Car} from "@/types/car"
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function fetchFromAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  return res.json();
}


export async function getCars() {
  return fetchFromAPI<Car[]>("/cars/");
}


export async function getCarById(id: string | number) {
  return fetchFromAPI<Car>(`/cars/${id}/`);
}
