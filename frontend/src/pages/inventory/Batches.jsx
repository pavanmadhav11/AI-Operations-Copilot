import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { addStockBatch, getExpiringBatches, getInventory, getWarehouses, writeOffExpiredBatch } from "../../services/inventoryService";
import useAuthStore from "../../store/authStore";

export default function Batches() {
  const [batches, setBatches] = useState([]);
  const [items, setItems] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [form, setForm] = useState({ product_id: "", warehouse_id: "", lot_code: "", quantity: "", expiration_date: "" });
  const [saving, setSaving] = useState(false);
  const user = useAuthStore((state) => state.user);
  const canAdd = user && ["admin", "manager"].includes(user.role);

  async function load() {
    try {
      const [batchList, inventory, warehouseList] = await Promise.all([
        getExpiringBatches(60),
        getInventory(),
        canAdd ? getWarehouses() : Promise.resolve([]),
      ]);
      setBatches(batchList);
      setItems(inventory);
      setWarehouses(warehouseList);
    } catch {
      toast.error("Could not load batch information.");
    }
  }

  useEffect(() => {
    load();
  }, [user?.role]);

  function updateField(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    try {
      await addStockBatch({
        ...form,
        product_id: Number(form.product_id),
        warehouse_id: Number(form.warehouse_id),
        quantity: Number(form.quantity),
      });
      toast.success("Batch received and stock updated.");
      setForm({ ...form, lot_code: "", quantity: "", expiration_date: "" });
      await load();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not add batch.");
    } finally {
      setSaving(false);
    }
  }

  async function writeOff(batch) {
    if (!window.confirm(`Write off ${batch.quantity} expired units from lot ${batch.lot_code}?`)) return;
    try {
      await writeOffExpiredBatch(batch.id);
      toast.success("Expired stock written off and recorded.");
      await load();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not write off this batch.");
    }
  }

  const products = [...new Map(items.map((item) => [item.product_id, item])).values()];

  return (
    <main className="p-8">
      <h1 className="mb-2 text-3xl font-bold">Expiry and batches</h1>
      <p className="mb-6 text-slate-600">Track lot quantities and see products approaching their expiration date.</p>

      {canAdd && (
        <form className="mb-8 grid max-w-4xl grid-cols-1 gap-4 rounded-lg bg-white p-6 shadow md:grid-cols-2" onSubmit={submit}>
          <label className="block"><span className="mb-1 block font-medium">Product</span><select className="w-full rounded border p-3" name="product_id" onChange={updateField} required value={form.product_id}><option value="">Choose product</option>{products.map((item) => <option key={item.product_id} value={item.product_id}>{item.product_name}</option>)}</select></label>
          <label className="block"><span className="mb-1 block font-medium">Warehouse</span><select className="w-full rounded border p-3" name="warehouse_id" onChange={updateField} required value={form.warehouse_id}><option value="">Choose warehouse</option>{warehouses.map((warehouse) => <option key={warehouse.id} value={warehouse.id}>{warehouse.name}</option>)}</select></label>
          <label className="block"><span className="mb-1 block font-medium">Lot code</span><input className="w-full rounded border p-3" name="lot_code" onChange={updateField} required value={form.lot_code} /></label>
          <label className="block"><span className="mb-1 block font-medium">Quantity received</span><input className="w-full rounded border p-3" min="1" name="quantity" onChange={updateField} required type="number" value={form.quantity} /></label>
          <label className="block"><span className="mb-1 block font-medium">Expiration date</span><input className="w-full rounded border p-3" name="expiration_date" onChange={updateField} required type="date" value={form.expiration_date} /></label>
          <div className="flex items-end"><button className="rounded bg-blue-700 px-5 py-3 text-white disabled:opacity-50" disabled={saving}>{saving ? "Saving..." : "Receive batch"}</button></div>
        </form>
      )}

      <section className="overflow-x-auto rounded-lg bg-white shadow">
        <h2 className="p-5 text-xl font-semibold">Expiring in the next 60 days</h2>
        {batches.length === 0 ? <p className="px-5 pb-5 text-emerald-700">No batches are approaching expiration.</p> : (
          <table className="w-full text-left">
            <thead className="bg-slate-100"><tr>{["Product", "Warehouse", "Lot", "Quantity", "Expiration", "Status", ...(canAdd ? ["Action"] : [])].map((heading) => <th className="p-3" key={heading}>{heading}</th>)}</tr></thead>
            <tbody>{batches.map((batch) => <tr className="border-t" key={batch.id}>
              <td className="p-3">{batch.product_name}</td><td className="p-3">{batch.warehouse_name}</td><td className="p-3">{batch.lot_code}</td><td className="p-3">{batch.quantity}</td><td className="p-3">{batch.expiration_date}</td>
              <td className={`p-3 font-semibold ${batch.days_until_expiration < 0 ? "text-red-700" : "text-amber-700"}`}>{batch.days_until_expiration < 0 ? "Expired" : `${batch.days_until_expiration} days left`}</td>
              {canAdd && <td className="p-3">{batch.days_until_expiration < 0 && batch.quantity > 0 && <button className="rounded bg-red-700 px-3 py-2 text-sm text-white" onClick={() => writeOff(batch)}>Write off</button>}</td>}
            </tr>)}</tbody>
          </table>
        )}
      </section>
    </main>
  );
}
