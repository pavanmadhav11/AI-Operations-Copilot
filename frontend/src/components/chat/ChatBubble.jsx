import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

export default function ChatBubble({ message }) {
  const isUser = message.role === "user";

  const text = message.message || message.content || "";

  const copyMessage = () => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div
      className={`flex gap-4 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && (
        <div className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
          AI
        </div>
      )}

      <div
        className={`max-w-3xl rounded-2xl px-5 py-4 ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white shadow"
        }`}
      >
        <ReactMarkdown
          components={{
            code({ inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || "");

              return !inline && match ? (
                <SyntaxHighlighter
                  style={oneDark}
                  language={match[1]}
                  PreTag="div"
                  {...props}
                >
                  {String(children).replace(/\n$/, "")}
                </SyntaxHighlighter>
              ) : (
                <code className="bg-gray-200 px-1 rounded">
                  {children}
                </code>
              );
            },
          }}
        >
          {text}
        </ReactMarkdown>

        {!isUser && (
          <button
            onClick={copyMessage}
            className="mt-4 text-sm text-blue-600 hover:underline"
          >
            Copy
          </button>
        )}
      </div>

      {isUser && (
        <div className="w-10 h-10 rounded-full bg-gray-700 text-white flex items-center justify-center font-bold">
          U
        </div>
      )}
    </div>
  );
}