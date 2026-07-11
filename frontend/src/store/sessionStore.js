import { create } from "zustand";

const useSessionStore = create((set) => ({
  sessions: [],
  currentSession: null,

  setSessions: (sessions) =>
    set({
      sessions,
    }),

  setCurrentSession: (session) =>
    set({
      currentSession: session,
    }),

  addSession: (session) =>
    set((state) => ({
      sessions: [session, ...state.sessions],
      currentSession: session,
    })),
}));

export default useSessionStore;