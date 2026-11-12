import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { getStockActions } from "../../services/inventoryService";
import { confirmStockAction, rejectStockAction } from "../../services/sqlService";

export default function ActionHistory() {
  const [actions, setActions] = useState([]);

  async function loadActions() {
    try {
      const data = await getStockActions();
      setActions(data);
    } catch {
      toast.error("Could not load action history.");
    }
  }

  useEffect(() => {
    loadActions();
  }, []);

  async function updateAction(action, decision) {
    try {
      if (decision === "confirm") {
        await confirmStockAction(action.id);
      } else {
        await rejectStockAction(action.id);
      }
      toast.success(decision === "confirm" ? "Action confirmed." : "Action rejected.");
      await loadActions();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not update this action.");
    }
  }

  return (
    <main className="p-8">
      <h1 className="mb-2 text-3xl font-bold">Stock action history</h1>
      <p className="mb-6 text-slate-600">Review the natural-language request, generated plan, and final status.</p>
      {actions.length === 0 ? <div className="rounded-lg bg-white p-6 shadow">No stock actions have been requested.</div> : (
        <div className="space-y-4">
          {actions.map((action) => (
            <article className="rounded-lg bg-white p-5 shadow" key={action.id}>
              <div className="flex flex-wrap justify-between gap-2">
                <p className="font-semibold">{action.action_type.replaceAll("_", " ")}</p>
                <span className={`rounded px-2 py-1 text-sm ${action.status === "confirmed" ? "bg-emerald-100 text-emerald-800" : action.status === "pending" ? "bg-amber-100 text-amber-800" : "bg-slate-100 text-slate-700"}`}>{action.status}</span>
              </div>
              <p className="mt-3">Request: {action.request_text}</p>
              <p className="mt-2 break-all rounded bg-slate-50 p-3 font-mono text-sm">{action.generated_sql}</p>
              <p className="mt-2 text-sm text-slate-500">{action.user_email} · {new Date(action.created_at).toLocaleString()}</p>
              {action.reviewed_at && <p className="mt-1 text-sm text-slate-500">Reviewed by {action.reviewed_by_email} · {new Date(action.reviewed_at).toLocaleString()}</p>}
              {action.status === "pending" && (
                <div className="mt-4 flex gap-3">
                  <button className="rounded bg-blue-700 px-4 py-2 text-white" onClick={() => updateAction(action, "confirm")}>Confirm</button>
                  <button className="rounded border px-4 py-2" onClick={() => updateAction(action, "reject")}>Reject</button>
                </div>
              )}
            </article>
          ))}
        </div>
      )}
    </main>
  );
}
