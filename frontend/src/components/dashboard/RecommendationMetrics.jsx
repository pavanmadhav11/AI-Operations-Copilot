import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import useAuthStore from "../../store/authStore";
import { getRecommendationMetrics } from "../../services/inventoryService";

export default function RecommendationMetrics() {
  const [metrics, setMetrics] = useState(null);
  const user = useAuthStore((state) => state.user);
  const canView = user && ["admin", "manager"].includes(user.role);

  useEffect(() => {
    if (!canView) return;
    getRecommendationMetrics()
      .then(setMetrics)
      .catch(() => toast.error("Could not load recommendation results."));
  }, [canView]);

  if (!canView || !metrics) return null;

  const cards = [
    ["Feedback received", metrics.total_feedback],
    ["Accepted", `${metrics.acceptance_rate}%`],
    ["Purchase drafts", metrics.purchase_order_drafts],
    ["Expired units written off", metrics.expired_units_written_off],
  ];

  return (
    <section className="rounded-xl bg-white p-6 shadow">
      <h2 className="mb-4 text-xl font-semibold">Recommendation outcomes</h2>
      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
        {cards.map(([label, value]) => <div className="rounded-lg bg-slate-50 p-4" key={label}><p className="text-sm text-slate-600">{label}</p><p className="mt-1 text-2xl font-bold">{value}</p></div>)}
      </div>
      <p className="mt-4 text-sm text-slate-500">Accepted: {metrics.accepted} · Marked not useful: {metrics.rejected}</p>
    </section>
  );
}
