import { useState } from "react";

const examples = [
  "Show items below reorder level",
  "Show Arabica Coffee at North Warehouse",
  "Set inventory ID 4 quantity to 20",
];

export default function SQLInput({ onGenerate, loading }) {
  const [question, setQuestion] = useState("");

  function handleSubmit() {
    if (!question.trim()) return;

    onGenerate(question);
  }

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <label htmlFor="stock-question" className="block text-sm font-semibold text-slate-900">
        What would you like to know or change?
      </label>
      <textarea
        id="stock-question"
        rows={4}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="For example, show Arabica Coffee stock at North Warehouse"
        className="mt-2 w-full rounded-xl border border-slate-300 p-4 text-sm text-slate-900 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
        aria-describedby="stock-question-help"
      />
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <span id="stock-question-help" className="mr-1 text-xs font-medium text-slate-500">Try an example</span>
        {examples.map((example) => (
          <button
            key={example}
            type="button"
            onClick={() => setQuestion(example)}
            className="rounded-full border border-slate-200 px-3 py-1.5 text-xs text-slate-600 transition hover:border-blue-300 hover:bg-blue-50 hover:text-blue-700"
          >
            {example}
          </button>
        ))}
      </div>
      <button
        onClick={handleSubmit}
        disabled={loading || !question.trim()}
        className="mt-5 rounded-xl bg-blue-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-slate-300"
      >
        {loading ? "Checking inventory…" : "Run request"}
      </button>
      <p className="mt-3 text-xs text-slate-500">Product and warehouse names can contain small spelling mistakes. Stock changes always need your confirmation.</p>
    </section>
  );
}
