import { useState } from "react";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");

  function handleSend() {
    if (!text.trim()) return;

    onSend(text);

    setText("");
  }

  return (
    <div className="flex gap-3 p-5 border-t bg-white">

      <textarea
        rows={2}
        value={text}
        placeholder="Ask anything..."
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
            }
        }}
        className="flex-1 border rounded-lg p-3 resize-none"
      />

      <button
        onClick={handleSend}
        className="bg-blue-600 text-white px-6 rounded-lg"
      >
        Send
      </button>

    </div>
  );
}