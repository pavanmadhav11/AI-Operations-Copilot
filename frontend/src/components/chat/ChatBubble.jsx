import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { FileText } from "lucide-react";

export default function ChatBubble({ message }) {
  const isUser = message.role === "user";

  const text = message.message || message.content || "";
  const citationMarker = "\n\nSources: ";
  const citationIndex = text.lastIndexOf(citationMarker);
  const answerText = citationIndex >= 0 ? text.slice(0, citationIndex) : text;
  const citations = citationIndex >= 0 ? text.slice(citationIndex + citationMarker.length).split("; ") : [];
  const sqlBlock = answerText.match(/```sql\s*([\s\S]*?)```/i);
  const visibleAnswer = sqlBlock ? answerText.replace(sqlBlock[0], "").trim() : answerText;

  const copyMessage = () => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className={`flex items-end gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-700 text-sm font-semibold text-white">
          AI
        </div>
      )}

      <div
        className={`max-w-3xl rounded-2xl px-5 py-4 ${
          isUser
            ? "rounded-br-md bg-blue-700 text-white"
            : "rounded-bl-md border border-slate-200 bg-white shadow-sm"
        }`}
      >
        <ReactMarkdown
          components={{
            table({ children }) {
              return <div className="my-3 overflow-x-auto rounded-lg border border-slate-200"><table className="min-w-full divide-y divide-slate-200 text-sm">{children}</table></div>;
            },
            thead({ children }) {
              return <thead className="bg-slate-100 text-left text-slate-700">{children}</thead>;
            },
            th({ children }) {
              return <th className="whitespace-nowrap px-3 py-2 font-semibold">{children}</th>;
            },
            td({ children }) {
              return <td className="whitespace-nowrap border-t border-slate-100 px-3 py-2">{children}</td>;
            },
            p({ children }) {
              return <p className="mb-2 last:mb-0 leading-7">{children}</p>;
            },
            ul({ children }) {
              return <ul className="mb-3 list-disc space-y-1 pl-5 last:mb-0">{children}</ul>;
            },
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
          {visibleAnswer}
        </ReactMarkdown>

        {sqlBlock && (
          <details className="mt-3 rounded-lg border border-slate-200 bg-slate-50 p-3">
            <summary className="cursor-pointer text-sm font-medium text-slate-700">How I got this answer</summary>
            <SyntaxHighlighter style={oneDark} language="sql" PreTag="div" className="mt-3 rounded-lg">
              {sqlBlock[1].trim()}
            </SyntaxHighlighter>
          </details>
        )}

        {citations.length > 0 && (
          <div className="mt-4 rounded-lg border border-blue-100 bg-blue-50 p-3 text-sm text-slate-700">
            <p className="mb-2 flex items-center gap-2 font-semibold text-blue-900"><FileText size={16} />Answer sources</p>
            <ul className="space-y-1.5">
              {citations.map((citation) => <li className="flex items-start gap-2" key={citation}><span className="mt-0.5 text-blue-700">•</span><span>{citation}</span></li>)}
            </ul>
            <p className="mt-2 text-xs text-slate-500">These are the uploaded document sections used for this answer.</p>
          </div>
        )}

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
