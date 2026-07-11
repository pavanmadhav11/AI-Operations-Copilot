import { useState } from "react";

export default function SQLInput({ onGenerate, loading }) {
  const [question, setQuestion] = useState("");

  function handleSubmit() {
    if (!question.trim()) return;

    onGenerate(question);
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">

      <textarea
        rows={4}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask about your database..."
        className="border rounded-lg w-full p-3"
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-4 bg-blue-600 text-white px-6 py-3 rounded-lg"
      >
        {loading ? "Generating..." : "Generate SQL"}
      </button>

    </div>
  );
}