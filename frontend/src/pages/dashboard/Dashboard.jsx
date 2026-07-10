import WelcomeBanner from "../../components/dashboard/WelcomeBanner";
import StatCard from "../../components/dashboard/StatCard";

export default function Dashboard() {
  return (
    <div className="space-y-8">

      <WelcomeBanner />

      <div className="grid grid-cols-4 gap-6">

        <StatCard
          title="Users"
          value="1,284"
          icon="👥"
          color="text-blue-600"
        />

        <StatCard
          title="Documents"
          value="8,450"
          icon="📄"
          color="text-green-600"
        />

        <StatCard
          title="AI Requests"
          value="42,813"
          icon="🤖"
          color="text-purple-600"
        />

        <StatCard
          title="Storage"
          value="72 GB"
          icon="💾"
          color="text-red-600"
        />

      </div>

      <div className="bg-white rounded-xl shadow-md p-6">

        <h2 className="text-xl font-bold mb-4">
          Dashboard Overview
        </h2>

        <p className="text-gray-600">
          This dashboard will display charts, AI analytics, recent
          activities, uploaded documents, and operational insights.
        </p>

      </div>

    </div>
  );
}