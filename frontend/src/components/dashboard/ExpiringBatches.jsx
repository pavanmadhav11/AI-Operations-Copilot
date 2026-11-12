import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";
import { getExpiringBatches } from "../../services/inventoryService";

export default function ExpiringBatches() {
  const [batches, setBatches] = useState([]);

  useEffect(() => {
    getExpiringBatches(30)
      .then(setBatches)
      .catch(() => toast.error("Could not load expiry alerts."));
  }, []);

  return (
    <section className="rounded-xl border border-orange-200 bg-white p-6 shadow">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Expiry alerts</h2>
          <p className="text-sm text-slate-600">Lots expiring within 30 days</p>
        </div>
        <Link className="text-sm font-semibold text-blue-700" to="/inventory/batches">View batches</Link>
      </div>
      {batches.length === 0 ? (
        <p className="text-emerald-700">No batches are close to expiration.</p>
      ) : (
        <div className="space-y-3">
          {batches.slice(0, 5).map((batch) => (
            <div className="flex items-center justify-between gap-3 border-b pb-3" key={batch.id}>
              <div>
                <p className="font-medium">{batch.product_name} · Lot {batch.lot_code}</p>
                <p className="text-sm text-slate-500">{batch.warehouse_name} · {batch.quantity} units</p>
              </div>
              <span className={`shrink-0 text-sm font-semibold ${batch.days_until_expiration < 0 ? "text-red-700" : "text-orange-700"}`}>
                {batch.days_until_expiration < 0 ? "Expired" : `${batch.days_until_expiration} days`}
              </span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
