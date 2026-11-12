import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";
import { getInventory, getStockMovements } from "../../services/inventoryService";
import useAuthStore from "../../store/authStore";

export default function Inventory() {
  const PAGE_SIZE = 25;
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingMoreItems, setLoadingMoreItems] = useState(false);
  const [hasMoreItems, setHasMoreItems] = useState(true);
  const [movements, setMovements] = useState([]);
  const [loadingMoreMovements, setLoadingMoreMovements] = useState(false);
  const [hasMoreMovements, setHasMoreMovements] = useState(true);
  const user = useAuthStore((state) => state.user);
  const canAddItems = user && ["admin", "manager"].includes(user.role);

  useEffect(() => {
    getInventory({ limit: PAGE_SIZE, offset: 0 })
      .then((data) => {
        setItems(data);
        setHasMoreItems(data.length === PAGE_SIZE);
      })
      .catch(() => toast.error("Could not load inventory."))
      .finally(() => setLoading(false));
    getStockMovements({ limit: PAGE_SIZE, offset: 0 })
      .then((data) => {
        setMovements(data);
        setHasMoreMovements(data.length === PAGE_SIZE);
      })
      .catch(() => toast.error("Could not load stock history."));
  }, []);

  async function loadMoreItems() {
    setLoadingMoreItems(true);
    try {
      const data = await getInventory({ limit: PAGE_SIZE, offset: items.length });
      setItems((current) => [...current, ...data]);
      setHasMoreItems(data.length === PAGE_SIZE);
    } catch {
      toast.error("Could not load more inventory.");
    } finally {
      setLoadingMoreItems(false);
    }
  }

  async function loadMoreMovements() {
    setLoadingMoreMovements(true);
    try {
      const data = await getStockMovements({ limit: PAGE_SIZE, offset: movements.length });
      setMovements((current) => [...current, ...data]);
      setHasMoreMovements(data.length === PAGE_SIZE);
    } catch {
      toast.error("Could not load more stock history.");
    } finally {
      setLoadingMoreMovements(false);
    }
  }

  return (
    <main className="p-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Inventory</h1>
          <p className="mt-2 text-slate-600">View current stock by product and warehouse.</p>
        </div>
        {canAddItems && (
          <Link className="rounded-lg bg-blue-600 px-4 py-3 text-white" to="/inventory/add">
            Add inventory item
          </Link>
        )}
      </div>

      {loading ? (
        <p>Loading inventory...</p>
      ) : items.length === 0 ? (
        <p className="rounded-lg bg-white p-6 shadow">There are no inventory items yet.</p>
      ) : (
        <div className="overflow-x-auto rounded-lg bg-white shadow">
          <table className="w-full text-left">
            <thead className="bg-slate-100">
              <tr>
                {["ID", "Product", "Category", "Warehouse", "Quantity", "Reorder level", "Demand / day", "Lead time", "Stockout estimate", "Price"].map((heading) => (
                  <th className="p-4" key={heading}>{heading}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr className="border-t" key={item.id}>
                  <td className="p-4">{item.id}</td>
                  <td className="p-4">{item.product_name}</td>
                  <td className="p-4">{item.category}</td>
                  <td className="p-4">{item.warehouse_name}</td>
                  <td className="p-4">{item.quantity}</td>
                  <td className="p-4">{item.reorder_level}</td>
                  <td className="p-4">{item.average_daily_demand}</td>
                  <td className="p-4">{item.supplier_lead_time_days} days</td>
                  <td className="p-4">{item.days_until_stockout == null ? "Not set" : `${item.days_until_stockout} days`}</td>
                  <td className="p-4">${Number(item.price).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {hasMoreItems && (
            <div className="border-t p-4 text-center">
              <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 disabled:opacity-60" onClick={loadMoreItems} disabled={loadingMoreItems}>
                {loadingMoreItems ? "Loading..." : "Load more inventory"}
              </button>
            </div>
          )}
        </div>
      )}

      <section className="mt-8 rounded-lg bg-white p-6 shadow">
        <h2 className="mb-4 text-xl font-semibold">Stock movement history</h2>
          {movements.length === 0 ? <p className="text-slate-500">No stock movements recorded yet.</p> : (
          <div className="space-y-3">
            {movements.map((movement) => (
              <div className="flex flex-wrap justify-between gap-2 border-b pb-3" key={movement.id}>
                <div>
                  <p className="font-medium">{movement.product_name} · {movement.warehouse_name}</p>
                  <p className="text-sm text-slate-500">{movement.movement_type}: {movement.reason}</p>
                </div>
                <p className="text-sm">{movement.quantity_before} → {movement.quantity_after}</p>
              </div>
            ))}
            {hasMoreMovements && (
              <button className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 disabled:opacity-60" onClick={loadMoreMovements} disabled={loadingMoreMovements}>
                {loadingMoreMovements ? "Loading..." : "Load more stock history"}
              </button>
            )}
          </div>
        )}
      </section>
    </main>
  );
}
