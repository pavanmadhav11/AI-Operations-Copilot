import { create } from "zustand";
import { login as loginAPI, getCurrentUser } from "../services/authService";

const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem("token"),
  isAuthenticated: !!localStorage.getItem("token"),
  isLoading: !!localStorage.getItem("token"),

  login: async (email, password) => {
    const data = await loginAPI({ email, password });
    localStorage.setItem("token", data.access_token);
    const user = await getCurrentUser();
    set({ user, token: data.access_token, isAuthenticated: true, isLoading: false });
  },

  loadUser: async () => {
    try {
      const user = await getCurrentUser();
      set({ user, token: localStorage.getItem("token"), isAuthenticated: true, isLoading: false });
    } catch {
      localStorage.removeItem("token");
      set({ user: null, token: null, isAuthenticated: false, isLoading: false });
    }
  },

  logout: () => {
    localStorage.removeItem("token");
    set({ user: null, token: null, isAuthenticated: false, isLoading: false });
  },
}));

export default useAuthStore;
