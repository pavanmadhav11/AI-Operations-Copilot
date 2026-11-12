import { useState } from "react";
import { Send } from "lucide-react";
import FileUpload from "./FileUpload";

export default function ChatInput({ onSend, loading, hasSession }) {
  const [text, setText] = useState("");

  function handleSend() {
    if (loading || !text.trim()) return;

    onSend(text.trim());

    setText("");
  }

  return (
    <div className="border-t bg-white px-4 py-3 sm:px-6">
      <div className="mx-auto flex max-w-4xl items-end gap-2 rounded-2xl border border-slate-300 bg-white p-2 shadow-sm focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100">
        <FileUpload />
        <textarea
          rows={1}
          value={text}
          placeholder={hasSession ? "Ask about stock, warehouses, or your documents..." : "Create a chat to start asking questions..."}
          disabled={loading || !hasSession}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              handleSend();
            }
          }}
          className="max-h-32 min-h-11 flex-1 resize-y border-0 bg-transparent p-3 outline-none focus:ring-0"
          aria-label="Message"
        />
        <button
          onClick={handleSend}
          disabled={loading || !hasSession || !text.trim()}
          className="flex h-11 items-center gap-2 rounded-xl bg-blue-700 px-4 text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-slate-300"
          aria-label="Send message"
        >
          <Send size={17} />
          <span className="hidden sm:inline">Send</span>
        </button>
      </div>
      <p className="mx-auto mt-2 max-w-4xl text-xs text-slate-500">Press Enter to send · Shift + Enter for a new line</p>
    </div>
  );
}
