export default function SQLResult({ sql }) {

  if (!sql) return null;

  return (
    <div className="bg-white rounded-xl shadow p-6 mt-6">

      <h2 className="font-bold mb-4">
        Generated SQL
      </h2>

      <pre className="bg-slate-900 text-green-400 p-5 rounded-lg overflow-x-auto">
        {sql}
      </pre>

    </div>
  );
}