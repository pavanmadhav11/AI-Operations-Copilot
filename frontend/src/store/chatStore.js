import { create } from "zustand";

const useChatStore = create((set) => ({
  chats: [
    {
      id: 1,
      title: "New Chat",
      messages: [],
    },
  ],

  activeChatId: 1,

  createChat: () =>
    set((state) => {
      const newChat = {
        id: Date.now(),
        title: "New Chat",
        messages: [],
      };

      return {
        chats: [...state.chats, newChat],
        activeChatId: newChat.id,
      };
    }),

  setActiveChat: (id) =>
    set({
      activeChatId: id,
    }),

  addMessage: (chatId, message) =>
    set((state) => ({
      chats: state.chats.map((chat) =>
        chat.id === chatId
          ? {
              ...chat,
              messages: [...chat.messages, message],
            }
          : chat
      ),
    })),

  renameChat: (id, title) =>
    set((state) => ({
      chats: state.chats.map((chat) =>
        chat.id === id ? { ...chat, title } : chat
      ),
    })),

  deleteChat: (id) =>
    set((state) => {
        const updated = state.chats.filter((chat) => chat.id !== id);

        if (updated.length === 0) {
        const newChat = {
            id: Date.now(),
            title: "New Chat",
            messages: [],
        };

        return {
            chats: [newChat],
            activeChatId: newChat.id,
        };
        }

        return {
        chats: updated,
        activeChatId: updated[0].id,
        };
    }),
}));

export default useChatStore;