export default function SQLResult({ sql }) {

  if (!sql) return null;
  const isUpdate = /^UPDATE\b/i.test(sql.trim());

  return (
    <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="font-semibold text-slate-900">Request details</h2>
          <p className="mt-1 text-sm text-slate-500">The assistant translated your request into a safe inventory query.</p>
        </div>
        <span className={`rounded-full px-3 py-1 text-xs font-semibold ${isUpdate ? "bg-amber-100 text-amber-800" : "bg-emerald-100 text-emerald-800"}`}>
          {isUpdate ? "Stock change preview" : "Read only"}
        </span>
      </div>
      <pre className="overflow-x-auto rounded-xl bg-slate-950 p-4 text-sm leading-6 text-emerald-300">
        {sql}
      </pre>
    </section>
  );
}
