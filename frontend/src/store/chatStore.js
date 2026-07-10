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
}));

export default useChatStore;