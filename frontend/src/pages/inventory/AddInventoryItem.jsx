import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { addInventoryItem, getWarehouses } from "../../services/inventoryService";

const emptyForm = {
  name: "",
  category: "",
  price: "",
  quantity: "",
  reorder_level: "",
  warehouse_id: "",
  average_daily_demand: "",
  supplier_lead_time_days: "",
};

export default function AddInventoryItem() {
  const [form, setForm] = useState(emptyForm);
  const [warehouses, setWarehouses] = useState([]);
  const [saving, setSaving] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    getWarehouses()
      .then((data) => {
        setWarehouses(data);
        if (data.length) setForm((current) => ({ ...current, warehouse_id: String(data[0].id) }));
      })
      .catch(() => toast.error("Could not load warehouses."));
  }, []);

  function updateField(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    try {
      await addInventoryItem({
        ...form,
        price: Number(form.price),
        quantity: Number(form.quantity),
        reorder_level: Number(form.reorder_level),
        warehouse_id: Number(form.warehouse_id),
        average_daily_demand: Number(form.average_daily_demand),
        supplier_lead_time_days: Number(form.supplier_lead_time_days),
      });
      toast.success("Inventory item added.");
      navigate("/inventory");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not add the item.");
    } finally {
      setSaving(false);
    }
  }

  const fields = [
    ["name", "Product name", "text"],
    ["category", "Category", "text"],
    ["price", "Price", "number"],
    ["quantity", "Starting quantity", "number"],
    ["reorder_level", "Reorder level", "number"],
    ["average_daily_demand", "Average daily demand", "number"],
    ["supplier_lead_time_days", "Supplier lead time in days", "number"],
  ];

  return (
    <main className="p-8">
      <h1 className="mb-2 text-3xl font-bold">Add inventory item</h1>
      <p className="mb-6 text-slate-600">Add a product and its starting stock at a warehouse.</p>
      <p className="mb-4 text-sm text-slate-500">Enter 0 for average daily demand or supplier lead time if you do not know the value.</p>
      <form className="max-w-xl space-y-4 rounded-lg bg-white p-6 shadow" onSubmit={submit}>
        {fields.map(([name, label, type]) => (
          <label className="block" key={name}>
            <span className="mb-1 block font-medium">{label}</span>
            <input
              className="w-full rounded border border-slate-300 p-3"
              min={type === "number" ? "0" : undefined}
              name={name}
              onChange={updateField}
              required
              step={name === "price" ? "0.01" : type === "number" ? "1" : undefined}
              type={type}
              value={form[name]}
            />
          </label>
        ))}
        <label className="block">
          <span className="mb-1 block font-medium">Warehouse</span>
          <select className="w-full rounded border border-slate-300 p-3" name="warehouse_id" onChange={updateField} required value={form.warehouse_id}>
            {warehouses.map((warehouse) => (
              <option key={warehouse.id} value={warehouse.id}>{warehouse.name} — {warehouse.city}</option>
            ))}
          </select>
        </label>
        <button className="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white disabled:opacity-50" disabled={saving || !warehouses.length}>
          {saving ? "Saving..." : "Add item"}
        </button>
      </form>
    </main>
  );
}
