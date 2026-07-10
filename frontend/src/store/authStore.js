import { create } from "zustand";
import {
  login as loginAPI,
  getCurrentUser,
  logout as logoutAPI,
} from "../services/authService";

const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem("token"),
  isAuthenticated: !!localStorage.getItem("token"),

  login: async (email, password) => {
    const data = await loginAPI({
      email,
      password,
    });

    const user = await getCurrentUser();

    set({
      user,
      token: data.access_token,
      isAuthenticated: true,
    });
  },

  loadUser: async () => {
    try {
      const user = await getCurrentUser();

      set({
        user,
        isAuthenticated: true,
      });
    } catch {
      localStorage.removeItem("token");

      set({
        user: null,
        token: null,
        isAuthenticated: false,
      });
    }
  },

  logout: () => {
    logoutAPI();

    set({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  },
}));

export default useAuthStore;