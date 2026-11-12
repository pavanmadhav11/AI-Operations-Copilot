import { useState } from "react";
import toast from "react-hot-toast";
import SQLInput from "../../components/sql/SQLInput";
import SQLResult from "../../components/sql/SQLResult";
import SQLTable from "../../components/sql/SQLTable";
import { confirmStockAction, generateSQL, rejectStockAction } from "../../services/sqlService";
import useAuthStore from "../../store/authStore";

export default function SQLGenerator() {
  const [loading, setLoading] = useState(false);
  const [sql, setSql] = useState("");
  const [rows, setRows] = useState([]);
  const [pendingAction, setPendingAction] = useState(null);
  const user = useAuthStore((state) => state.user);
  const canChangeStock = user && ["admin", "manager"].includes(user.role);

  async function handleGenerate(question) {
    setLoading(true);
    setPendingAction(null);
    try {
      const response = await generateSQL(question);
      if (!response.success) {
        toast.error(response.message);
      } else {
        setSql(response.sql);
        if (response.confirmation_required) {
          setRows([]);
          setPendingAction(response.result);
        } else {
          setRows(Array.isArray(response.result) ? response.result : []);
        }
      }
    } catch {
      toast.error("Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  async function confirmAction() {
    try {
      await confirmStockAction(pendingAction.action_id);
      toast.success("Stock change confirmed and saved.");
      setPendingAction(null);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not confirm the stock change.");
    }
  }

  async function cancelAction() {
    try {
      await rejectStockAction(pendingAction.action_id);
      toast.success("Stock change cancelled.");
      setPendingAction(null);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not cancel the stock change.");
    }
  }

  return (
    <div className="p-8">
      <h1 className="mb-2 text-3xl font-bold">Stock Assistant</h1>
      <p className="mb-6 text-slate-600">
        Ask a stock question in plain language. Employees can view stock. Managers and admins can preview a quantity change before confirming it.
      </p>
      <SQLInput onGenerate={handleGenerate} loading={loading} />
      <SQLResult sql={sql} />
      <SQLTable rows={rows} />
      {pendingAction && canChangeStock && (
        <section className="mt-6 max-w-2xl rounded-xl border border-amber-300 bg-amber-50 p-6">
          <h2 className="text-xl font-semibold text-slate-900">Review stock change</h2>
          <p className="mt-1 text-sm text-slate-600">Check the item and quantity before saving this adjustment.</p>
          <dl className="mt-4 grid grid-cols-1 gap-3 rounded-lg border border-amber-200 bg-white p-4 sm:grid-cols-2">
            <div><dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Item</dt><dd className="mt-1 font-semibold text-slate-900">{pendingAction.product_name}</dd></div>
            <div><dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Warehouse</dt><dd className="mt-1 font-semibold text-slate-900">{pendingAction.warehouse_name}</dd></div>
            <div><dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Current quantity</dt><dd className="mt-1 text-slate-900">{pendingAction.quantity_before} units</dd></div>
            <div><dt className="text-xs font-medium uppercase tracking-wide text-slate-500">After change</dt><dd className="mt-1 text-lg font-bold text-blue-800">{pendingAction.quantity_after} units</dd></div>
            <div className="sm:col-span-2"><dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Your request</dt><dd className="mt-1 text-slate-700">{pendingAction.request_text}</dd></div>
          </dl>
          <p className="mt-3 text-sm text-slate-600">The stock is updated only after you confirm. The change is added to movement history.</p>
          <div className="mt-5 flex gap-3">
            <button className="rounded bg-blue-700 px-4 py-2 text-white" onClick={confirmAction}>Confirm change</button>
            <button className="rounded border border-slate-400 px-4 py-2" onClick={cancelAction}>Cancel</button>
          </div>
        </section>
      )}
    </div>
  );
}
