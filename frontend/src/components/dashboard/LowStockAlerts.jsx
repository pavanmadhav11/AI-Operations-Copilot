import { useEffect, useState } from "react";
import { AlertTriangle, ArrowUpRight, Clock3 } from "lucide-react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";
import { getLowStockInventory } from "../../services/dashboardService";
import useAuthStore from "../../store/authStore";
import { sendRecommendationFeedback } from "../../services/inventoryService";

const VISIBLE_ITEMS = 5;
const ROW_HEIGHT = 112;

export default function LowStockAlerts() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const user = useAuthStore((state) => state.user);
  const canTransfer = user && ["admin", "manager"].includes(user.role);

  useEffect(() => {
    getLowStockInventory()
      .then(setItems)
      .catch(() => toast.error("Could not load low stock alerts."))
      .finally(() => setLoading(false));
  }, []);

  const scrolling = items.length > VISIBLE_ITEMS;
  const displayItems = scrolling ? [...items, ...items] : items;

  async function sendFeedback(item, recommendationType, accepted) {
    try {
      await sendRecommendationFeedback({
        inventory_id: item.id,
        recommendation_type: recommendationType,
        recommended_quantity: recommendationType === "transfer" ? item.recommended_transfer_quantity : item.recommended_order_quantity,
        accepted,
        note: accepted ? "Accepted from dashboard" : "Marked not useful from dashboard",
      });
      toast.success("Thanks, your feedback was recorded.");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Could not save feedback.");
    }
  }

  return (
    <section className="overflow-hidden rounded-xl border border-amber-200 bg-white shadow">
      <div className="flex items-center justify-between border-b border-amber-100 bg-amber-50 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="rounded-full bg-amber-100 p-2 text-amber-700">
            <AlertTriangle size={21} />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Low stock alerts</h2>
            <p className="text-sm text-slate-600">Items where current stock is below the reorder level</p>
          </div>
        </div>
        <Link className="flex items-center gap-1 text-sm font-medium text-blue-700" to="/inventory">
          View inventory <ArrowUpRight size={16} />
        </Link>
      </div>

      {loading ? (
        <div className="flex items-center justify-center text-slate-500" style={{ height: `${VISIBLE_ITEMS * ROW_HEIGHT}px` }}>Loading stock alerts...</div>
      ) : items.length === 0 ? (
        <div className="flex h-24 items-center px-6 text-emerald-700">All inventory is at or above its reorder level.</div>
      ) : (
      <div className="overflow-hidden" style={{ height: `${VISIBLE_ITEMS * ROW_HEIGHT}px` }} aria-label="Low stock items" role="region">
          <div
            className={scrolling ? "low-stock-track" : ""}
            style={scrolling ? { animationDuration: `${items.length * 3}s` } : undefined}
          >
            {displayItems.map((item, index) => (
              <div className="flex h-[112px] items-center justify-between gap-4 border-b border-slate-100 px-6" key={`${item.id}-${index}`} aria-hidden={scrolling && index >= items.length}>
                <div className="min-w-0">
                  <p className="truncate font-semibold text-slate-900">{item.product_name}</p>
                  <p className="text-sm text-slate-500">{item.warehouse_name} · Inventory ID {item.id}</p>
                  <p className="mt-1 truncate text-xs text-slate-600">{item.recommended_action}</p>
                </div>
                <div className="ml-4 flex shrink-0 items-center gap-4">
                  <div className="text-right">
                    <p className="text-sm font-semibold text-amber-800">{item.quantity} in stock · reorder at {item.reorder_level}</p>
                    <p className="text-xs text-slate-600">Short by {Math.max(0, item.reorder_level - item.quantity)} units</p>
                    <p className="mt-1 inline-flex items-center justify-end gap-1 text-xs text-slate-500">
                      <Clock3 size={13} />
                      {item.days_until_stockout == null ? "Add daily demand for stockout estimate" : `About ${item.days_until_stockout} days of stock`}
                    </p>
                    <p className="text-xs text-slate-500">Suggested: transfer {item.recommended_transfer_quantity} · reorder {item.recommended_order_quantity}</p>
                    {canTransfer && item.suggested_transfer_source && item.recommended_transfer_quantity > 0 && (
                      <Link
                        className="text-sm font-semibold text-blue-700"
                        to={`/inventory/transfers?source=${item.suggested_transfer_source.inventory_id}&destination=${item.warehouse_id}&quantity=${item.recommended_transfer_quantity}&recommendation_inventory_id=${item.id}&recommended_quantity=${item.recommended_transfer_quantity}`}
                      >
                        Preview transfer from {item.suggested_transfer_source.warehouse_name}
                      </Link>
                    )}
                    {canTransfer && item.recommended_order_quantity > 0 && (
                      <Link className="block text-sm font-semibold text-blue-700" to={`/procurement?inventory_id=${item.id}&quantity=${item.recommended_order_quantity}`}>
                        Prepare reorder draft
                      </Link>
                    )}
                    {canTransfer && (
                      <div className="mt-1 flex justify-end gap-3">
                        {item.recommended_transfer_quantity > 0 && <button className="text-xs text-slate-500 hover:underline" onClick={() => sendFeedback(item, "transfer", false)}>Transfer not useful</button>}
                        {item.recommended_order_quantity > 0 && <button className="text-xs text-slate-500 hover:underline" onClick={() => sendFeedback(item, "reorder", false)}>Reorder not useful</button>}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
