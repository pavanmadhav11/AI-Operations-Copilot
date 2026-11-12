import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import toast from "react-hot-toast";
import { getInventory, getWarehouses, previewTransfer } from "../../services/inventoryService";
import { confirmStockAction, rejectStockAction } from "../../services/sqlService";

export default function Transfers() {
  const [searchParams] = useSearchParams();
  const [items, setItems] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [sourceId, setSourceId] = useState(searchParams.get("source") || "");
  const [destinationId, setDestinationId] = useState(searchParams.get("destination") || "");
  const [quantity, setQuantity] = useState(searchParams.get("quantity") || "1");
  const [preview, setPreview] = useState(null);

  useEffect(() => {
    Promise.all([getInventory(), getWarehouses()])
      .then(([inventory, warehouseList]) => {
        setItems(inventory);
        setWarehouses(warehouseList);
      })
      .catch(() => toast.error("Could not load inventory or warehouses."));
  }, []);

  const source = items.find((item) => String(item.id) === String(sourceId));

  async function createPreview(event) {
    event.preventDefault();
    try {
      const data = await previewTransfer({
        source_inventory_id: Number(sourceId),
        destination_warehouse_id: Number(destinationId),
        quantity: Number(quantity),
        recommendation_inventory_id: searchParams.get("recommendation_inventory_id") ? Number(searchParams.get("recommendation_inventory_id")) : null,
        recommended_quantity: searchParams.get("recommended_quantity") ? Number(searchParams.get("recommended_quantity")) : null,
      });
      setPreview(data);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not prepare transfer.");
    }
  }

  async function confirm() {
    try {
      await confirmStockAction(preview.action_id);
      toast.success("Transfer completed and recorded.");
      setPreview(null);
      const refreshed = await getInventory();
      setItems(refreshed);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not confirm transfer.");
    }
  }

  async function cancel() {
    try {
      await rejectStockAction(preview.action_id);
      toast.success("Transfer cancelled.");
      setPreview(null);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not cancel transfer.");
    }
  }

  return (
    <main className="p-8">
      <h1 className="mb-2 text-3xl font-bold">Warehouse transfer</h1>
      <p className="mb-6 text-slate-600">Preview a transfer from a warehouse with surplus stock to another warehouse.</p>
      <form className="max-w-2xl space-y-4 rounded-lg bg-white p-6 shadow" onSubmit={createPreview}>
        <label className="block">
          <span className="mb-1 block font-medium">Source product and warehouse</span>
          <select className="w-full rounded border p-3" onChange={(event) => setSourceId(event.target.value)} required value={sourceId}>
            <option value="">Choose stock</option>
            {items.map((item) => <option key={item.id} value={item.id}>{item.product_name} · {item.warehouse_name} · {item.quantity} available</option>)}
          </select>
        </label>
        <label className="block">
          <span className="mb-1 block font-medium">Destination warehouse</span>
          <select className="w-full rounded border p-3" onChange={(event) => setDestinationId(event.target.value)} required value={destinationId}>
            <option value="">Choose destination</option>
            {warehouses.filter((warehouse) => warehouse.id !== source?.warehouse_id).map((warehouse) => (
              <option key={warehouse.id} value={warehouse.id}>{warehouse.name} · {warehouse.city}</option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="mb-1 block font-medium">Quantity to transfer</span>
          <input className="w-full rounded border p-3" min="1" max={source?.quantity} onChange={(event) => setQuantity(event.target.value)} required type="number" value={quantity} />
        </label>
        <button className="rounded bg-blue-700 px-5 py-3 text-white">Preview transfer</button>
      </form>

      {preview && (
        <section className="mt-6 max-w-2xl rounded-lg border border-amber-300 bg-amber-50 p-6">
          <h2 className="text-xl font-semibold">Confirm transfer</h2>
          <p className="mt-3">{preview.quantity} × {preview.product_name}</p>
          <p>From {preview.source_warehouse} to {preview.destination_warehouse}</p>
          <p className="mt-3 text-sm text-slate-600">Both warehouse quantities will be updated and added to movement history.</p>
          <div className="mt-5 flex gap-3">
            <button className="rounded bg-blue-700 px-4 py-2 text-white" onClick={confirm}>Confirm transfer</button>
            <button className="rounded border px-4 py-2" onClick={cancel}>Cancel</button>
          </div>
        </section>
      )}
    </main>
  );
}
