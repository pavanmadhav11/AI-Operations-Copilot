import { useState } from "react";

import ChatSidebar from "../../components/chat/ChatSidebar";
import ChatWindow from "../../components/chat/ChatWindow";
import ChatInput from "../../components/chat/ChatInput";

import { sendMessage } from "../../services/chatService";
import useChatStore from "../../store/chatStore";

export default function Chat() {
  const [loading, setLoading] = useState(false);

  const {
    chats,
    activeChatId,
    addMessage,
  } = useChatStore();

  const activeChat = chats.find(
    (chat) => chat.id === activeChatId
  );

  async function handleSend(text) {
    const userMessage = {
      id: Date.now(),
      role: "user",
      content: text,
    };

    addMessage(activeChatId, userMessage);

    setLoading(true);

    const aiMessage = await sendMessage(text);

    addMessage(activeChatId, aiMessage);

    setLoading(false);
  }

  return (
    <div className="flex h-[calc(100vh-64px)]">

      <ChatSidebar />

      <div className="flex flex-col flex-1">

        <ChatWindow
          messages={activeChat.messages}
          loading={loading}
        />

        <ChatInput onSend={handleSend} />

      </div>

    </div>
  );
}