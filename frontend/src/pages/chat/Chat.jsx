import { useEffect, useRef, useState } from "react";

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
    clearMessages,
  } = useChatStore();

  const { currentSession } = useSessionStore();
  const [error, setError] = useState("");
  const activeSessionId = useRef(currentSession?.id);

  useEffect(() => {
    let active = true;
    activeSessionId.current = currentSession?.id;
    clearMessages();
    setError("");
    setLoading(false);
    if (!currentSession) {
      return () => {
        active = false;
      };
    }

    async function loadSessionHistory() {
      try {
        const history = await getHistory(currentSession.id);
        if (active) setMessages(history);
      } catch (err) {
        if (active) setError(err.response?.data?.detail || "I couldn't load this conversation. Please try again.");
      }
    }

    loadSessionHistory();
    return () => {
      active = false;
    };
  }, [currentSession?.id]);

  async function handleSend(text) {
    if (!currentSession || loading) return;
    const sessionId = currentSession.id;

    const userMessage = {
      id: Date.now(),
      role: "user",
      message: text,
    };

    addMessage(userMessage);
    setError("");
    setLoading(true);

    try {
      const response = await sendMessage(
        sessionId,
        text
      );

      if (activeSessionId.current === sessionId) {
        addMessage({
          id: Date.now() + 1,
          role: "assistant",
          message: response.response,
        });
      }
    } catch (err) {
      if (activeSessionId.current === sessionId) {
        setError(err.response?.data?.detail || "I couldn't answer that. Try asking in a different way.");
      }
    } finally {
      if (activeSessionId.current === sessionId) setLoading(false);
    }
  }

  return (
    <div className="flex h-[calc(100vh-64px)]">

      <ChatSidebar />

      <div className="flex flex-col flex-1">

        <ChatWindow
          messages={messages}
          loading={loading}
        />

        {error && <p className="border-t border-rose-200 bg-rose-50 px-5 py-3 text-sm text-rose-800">{error}</p>}

        <ChatInput
          onSend={handleSend}
          loading={loading}
          hasSession={Boolean(currentSession)}
        />

      </div>

    </div>
  );
}
