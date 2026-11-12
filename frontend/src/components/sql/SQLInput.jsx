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
        placeholder="Example: show stock below reorder level, or set inventory ID 4 quantity to 20"
        className="border rounded-lg w-full p-3"
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-4 bg-blue-600 text-white px-6 py-3 rounded-lg"
      >
        {loading ? "Working..." : "Ask Stock Assistant"}
      </button>

    </div>
  );
}
