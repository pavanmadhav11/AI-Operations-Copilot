import { useEffect, useState } from "react";

import ChatSidebar from "../../components/chat/ChatSidebar";
import ChatWindow from "../../components/chat/ChatWindow";
import ChatInput from "../../components/chat/ChatInput";

import {
  sendMessage,
  getHistory,
} from "../../services/chatService";

import useChatStore from "../../store/chatStore";
import useSessionStore from "../../store/sessionStore";

export default function Chat() {
  const [loading, setLoading] = useState(false);

  const {
    messages,
    setMessages,
    addMessage,
  } = useChatStore();

  const { currentSession } = useSessionStore();

  useEffect(() => {
    if (currentSession) {
      loadHistory();
    }
  }, [currentSession]);

  async function loadHistory() {
    try {
      const history = await getHistory(currentSession.id);
      setMessages(history);
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  async function handleSend(text) {
    if (!currentSession) return;

    const userMessage = {
      id: Date.now(),
      role: "user",
      message: text,
    };

    addMessage(userMessage);

    setLoading(true);

    try {
      const response = await sendMessage(
        currentSession.id,
        text
      );

      addMessage({
        id: Date.now() + 1,
        role: "assistant",
        message: response.response,
      });

    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
        "Something went wrong."
    );
    }

    setLoading(false);
  }

  return (
    <div className="flex h-[calc(100vh-64px)]">

      <ChatSidebar />

      <div className="flex flex-col flex-1">

        <ChatWindow
          messages={messages}
          loading={loading}
        />

        <ChatInput
          onSend={handleSend}
        />

      </div>

    </div>
  );
}