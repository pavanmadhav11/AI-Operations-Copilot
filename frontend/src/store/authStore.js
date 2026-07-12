import { create } from "zustand";

import {
  login as loginAPI,
  getCurrentUser,
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

    // Save JWT
    localStorage.setItem(
      "token",
      data.access_token
    );

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
        token: localStorage.getItem("token"),
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
    localStorage.removeItem("token");

    set({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  },
}));

export default useAuthStore;