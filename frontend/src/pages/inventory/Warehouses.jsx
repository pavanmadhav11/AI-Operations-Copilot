import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { addWarehouse, getWarehouses } from "../../services/inventoryService";

export default function Warehouses() {
  const [warehouses, setWarehouses] = useState([]);
  const [form, setForm] = useState({ name: "", city: "", manager: "" });

  async function loadWarehouses() {
    try {
      setWarehouses(await getWarehouses());
    } catch {
      toast.error("Could not load warehouses.");
    }
  }

  useEffect(() => {
    loadWarehouses();
  }, []);

  async function submit(event) {
    event.preventDefault();
    try {
      await addWarehouse(form);
      toast.success("Warehouse added.");
      setForm({ name: "", city: "", manager: "" });
      await loadWarehouses();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not add warehouse.");
    }
  }

  function update(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  return (
    <main className="p-8">
      <h1 className="mb-2 text-3xl font-bold">Warehouses</h1>
      <p className="mb-6 text-slate-600">Set up warehouse locations for inventory and transfers.</p>
      <form className="mb-8 grid max-w-3xl grid-cols-1 gap-4 rounded-lg bg-white p-6 shadow md:grid-cols-3" onSubmit={submit}>
        {[["name", "Warehouse name"], ["city", "City"], ["manager", "Manager name"]].map(([name, label]) => (
          <label className="block" key={name}>
            <span className="mb-1 block font-medium">{label}</span>
            <input className="w-full rounded border p-3" name={name} onChange={update} required={name !== "manager"} value={form[name]} />
          </label>
        ))}
        <button className="rounded bg-blue-700 px-5 py-3 text-white md:col-span-3 md:justify-self-start">Add warehouse</button>
      </form>
      <section className="max-w-3xl space-y-3">
        {warehouses.map((warehouse) => (
          <article className="rounded-lg bg-white p-5 shadow" key={warehouse.id}>
            <p className="font-semibold">{warehouse.name}</p>
            <p className="text-sm text-slate-600">{warehouse.city} · {warehouse.manager || "No manager assigned"}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
