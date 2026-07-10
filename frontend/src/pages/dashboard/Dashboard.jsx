import { useEffect, useState } from "react";

import WelcomeBanner from "../../components/dashboard/WelcomeBanner";
import StatCard from "../../components/dashboard/StatCard";
import ActivityChart from "../../components/dashboard/ActivityChart";
import RecentActivity from "../../components/dashboard/RecentActivity";
import RecentDocuments from "../../components/dashboard/RecentDocuments";

import {
  getDashboardStats,
} from "../../services/dashboardService";

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    async function loadDashboard() {
      const data = await getDashboardStats();
      setStats(data);
    }

    loadDashboard();
  }, []);

  if (!stats) {
    return (
      <div className="text-center mt-20 text-xl">
        Loading Dashboard...
      </div>
    );
  }

  return (
    <div className="space-y-8">

      <WelcomeBanner />

      <div className="grid grid-cols-4 gap-6">

        <StatCard
          title="Users"
          value={stats.users}
          icon="👥"
          color="text-blue-600"
        />

        <StatCard
          title="Documents"
          value={stats.documents}
          icon="📄"
          color="text-green-600"
        />

        <StatCard
          title="AI Requests"
          value={stats.aiRequests}
          icon="🤖"
          color="text-purple-600"
        />

        <StatCard
          title="Storage"
          value={stats.storage}
          icon="💾"
          color="text-red-600"
        />

      </div>

      <div className="grid grid-cols-3 gap-6">

        <div className="col-span-2">
          <ActivityChart />
        </div>

        <RecentActivity />

      </div>

      <RecentDocuments />

    </div>
  );
}