import { useEffect, useRef } from "react";

import ChatBubble from "./ChatBubble";
import TypingIndicator from "./TypingIndicator";

export default function ChatWindow({
  messages,
  loading,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div className="flex-1 overflow-y-auto bg-slate-50 px-4 py-6 sm:px-8">

      {messages.length === 0 ? (
        <div className="flex h-full justify-center items-center">
          <div className="text-center">

            <h1 className="text-4xl font-bold">
              AI Operations Copilot
            </h1>

            <p className="mt-4 text-gray-500">
              Start a conversation...
            </p>

          </div>
        </div>
      ) : (
        <>
          <div className="mx-auto max-w-4xl space-y-6">

            {messages.map((message) => (
              <ChatBubble
                key={message.id}
                message={message}
              />
            ))}

            {loading && <TypingIndicator />}

          </div>

          <div ref={bottomRef} />
        </>
      )}

    </div>
  );
}
