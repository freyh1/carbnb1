const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

function getCookie(name: string): string | undefined {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? decodeURIComponent(match[2]) : undefined;
}
export async function fetchFromAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const csrfToken = getCookie("csrftoken");

  const defaultHeaders: HeadersInit = {
    "Content-Type": "application/json",
    ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
  };

  const res = await fetch(`${endpoint}`, {
    ...options,
    credentials: "include", 
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  if (res.status === 204) {
    return {} as T;
  }

  return res.json();
}


export const api = {
  // 🔐 Auth-related
  auth: {
    login: `${API_BASE}/login/`,
    logout: `${API_BASE}/logout/`,
    signup: `${API_BASE}/signup/`,
    profile: `${API_BASE}/profile/`,
    confirmEmail: (key: string) => `${API_BASE}/confirm-email/${key}/`,
    restAuth: {
      base: `${API_BASE}/api/auth/`,
      registration: `${API_BASE}/api/auth/registration/`,
    },
    accounts: `${API_BASE}/api/accounts/`,
  },

  // 👤 User API
  users: {
    base: `${API_BASE}/api/users/`,
    me: `${API_BASE}/api/users/?me=true`,
  },

  // 🚘 Car API
  cars: {
    base: `${API_BASE}/api/cars/`,
    detail: (id: number) => `${API_BASE}/api/cars/${id}/`,
    book: (id: number) => `${API_BASE}/api/cars/${id}/book/`,
    mine: `${API_BASE}/api/cars/mine/`,
    bookings: (id: number) => `${API_BASE}/api/cars/${id}/bookings/`,
  },

  // 📷 Car Images
  carImages: `${API_BASE}/api/car-images/`,

  // 💬 Reviews
  reviews: `${API_BASE}/api/reviews/`,

  // 📅 Bookings
  bookings: {
    base: `${API_BASE}/api/bookings/`,
    mine: `${API_BASE}/api/bookings/mine/`,
    confirm: (id: number) => `${API_BASE}/api/bookings/${id}/confirm/`,
    reject: (id: number) => `${API_BASE}/api/bookings/${id}/reject/`,
  },

  // 📬 Contact form
  contact: `${API_BASE}/api/contact/`,

  // 🏠 Static or route-related
  home: `${API_BASE}/`,
  myCars: `${API_BASE}/my-cars`,
  createCar: `${API_BASE}/create-car`,
  carDetailPage: (carId: number) => `${API_BASE}/cars/${carId}/`,
  bookCarPage: (carId: number) => `${API_BASE}/cars/${carId}/book/`,
  myBookingsPage: `${API_BASE}/my-bookings/`,
  profilePage: `${API_BASE}/profile/`,
};
