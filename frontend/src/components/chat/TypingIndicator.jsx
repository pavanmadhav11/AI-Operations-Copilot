export default function TypingIndicator() {
  return (
    <div className="flex items-start gap-3" role="status" aria-live="polite">
      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-700 text-sm font-semibold text-white">AI</div>
      <div className="rounded-2xl rounded-tl-md bg-white px-5 py-4 shadow-sm">
        <div className="flex gap-2">
          <span className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></span>
          <span
            className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"
            style={{ animationDelay: "0.2s" }}
          ></span>
          <span
            className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"
            style={{ animationDelay: "0.4s" }}
          ></span>
        </div>
        <p className="mt-2 text-xs text-slate-500">Thinking...</p>
      </div>
    </div>
  );
}
