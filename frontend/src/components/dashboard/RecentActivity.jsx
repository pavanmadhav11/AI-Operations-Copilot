import { useEffect, useState } from "react";

import {
  getRecentActivity,
} from "../../services/dashboardService";

export default function RecentActivity() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    loadActivities();
  }, []);

  async function loadActivities() {
    try {
      const data = await getRecentActivity();
      setActivities(data);
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-xl font-semibold mb-5">
        Recent Activity
      </h2>

      <div className="space-y-4">
        {activities.map((item, index) => (
          <div
            key={index}
            className="border-b pb-3"
          >
            {item.text}
          </div>
        ))}
      </div>
    </div>
  );
}