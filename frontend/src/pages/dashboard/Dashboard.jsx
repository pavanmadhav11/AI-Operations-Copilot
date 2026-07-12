import { useEffect, useState } from "react";

import WelcomeBanner from "../../components/dashboard/WelcomeBanner";
import StatCard from "../../components/dashboard/StatCard";
import ActivityChart from "../../components/dashboard/ActivityChart";
import RecentActivity from "../../components/dashboard/RecentActivity";
import RecentDocuments from "../../components/dashboard/RecentDocuments";
import LoadingSpinner from "../../components/common/LoadingSpinner";

import { getDashboardStats } from "../../services/dashboardService";

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const data = await getDashboardStats();
      setStats(data);
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  if (!stats) {
    return <LoadingSpinner />;
  }

  return (
    <div className="space-y-8">

      <WelcomeBanner />

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        <StatCard
          title="Users"
          value={stats.users}
          type="users"
          color="text-blue-600"
        />

        <StatCard
          title="Documents"
          value={stats.documents}
          type="documents"
          color="text-green-600"
        />

        <StatCard
          title="AI Requests"
          value={stats.aiRequests}
          type="ai"
          color="text-purple-600"
        />

        <StatCard
          title="Storage"
          value={stats.storage}
          type="storage"
          color="text-red-600"
        />

      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

        <div className="xl:col-span-2">
          <ActivityChart />
        </div>

        <RecentActivity />

      </div>

      <RecentDocuments />

    </div>
  );
}