import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import { getAnalytics } from "../../services/analyticsService";

export default function Analytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  async function loadAnalytics() {
    try {
      const response = await getAnalytics();
      setData(response);
    } catch (err) {
     toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  if (!data) {
    return (
      <div className="text-center mt-20 text-xl">
        Loading Analytics...
      </div>
    );
  }

  const pieData = [
    {
      name: "PDF",
      value: data.pdfs,
    },
    {
      name: "Excel",
      value: data.excels,
    },
  ];

  return (
    <div className="space-y-8">

      <h1 className="text-3xl font-bold">
        Analytics
      </h1>

      <div className="grid grid-cols-4 gap-6">

        <Card
          title="Users"
          value={data.users}
          icon="👥"
        />

        <Card
          title="Sessions"
          value={data.sessions}
          icon="💬"
        />

        <Card
          title="Documents"
          value={data.documents}
          icon="📄"
        />

        <Card
          title="Storage"
          value={data.storage}
          icon="💾"
        />

      </div>

      <div className="grid grid-cols-2 gap-6">

        <div className="bg-white rounded-xl shadow p-6 h-96">

          <h2 className="text-xl font-semibold mb-5">
            Uploads Per Day
          </h2>

          <ResponsiveContainer
            width="100%"
            height="90%"
          >
            <LineChart data={data.chart}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="date" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="uploads"
                stroke="#16a34a"
                strokeWidth={3}
              />

            </LineChart>
          </ResponsiveContainer>

        </div>

        <div className="bg-white rounded-xl shadow p-6 h-96">

          <h2 className="text-xl font-semibold mb-5">
            Documents
          </h2>

          <ResponsiveContainer
            width="100%"
            height="90%"
          >
            <PieChart>

              <Pie
                data={pieData}
                dataKey="value"
                outerRadius={120}
                label
              >
                <Cell fill="#2563eb" />

                <Cell fill="#16a34a" />
              </Pie>

              <Tooltip />

            </PieChart>
          </ResponsiveContainer>

        </div>

      </div>

      <div className="grid grid-cols-3 gap-6">

        <Card
          title="PDF Files"
          value={data.pdfs}
          icon="📕"
        />

        <Card
          title="Excel Files"
          value={data.excels}
          icon="📗"
        />

        <Card
          title="AI Requests"
          value={data.ai_requests}
          icon="🤖"
        />

      </div>

    </div>
  );
}

function Card({
  title,
  value,
  icon,
}) {
  return (
    <div className="bg-white rounded-xl shadow p-6">

      <div className="flex justify-between items-center">

        <div>

          <p className="text-gray-500">
            {title}
          </p>

          <h2 className="text-3xl font-bold mt-3">
            {value}
          </h2>

        </div>

        <div className="text-4xl">
          {icon}
        </div>

      </div>

    </div>
  );
}