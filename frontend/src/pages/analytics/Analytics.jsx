import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { Activity, Database, FileSpreadsheet, FileText, MessageSquare, UsersRound } from "lucide-react";
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
          icon={UsersRound}
        />

        <Card
          title="Sessions"
          value={data.sessions}
          icon={MessageSquare}
        />

        <Card
          title="Documents"
          value={data.documents}
          icon={FileText}
        />

        <Card
          title="Storage"
          value={data.storage}
          icon={Database}
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
          icon={FileText}
        />

        <Card
          title="Excel Files"
          value={data.excels}
          icon={FileSpreadsheet}
        />

        <Card
          title="AI Requests"
          value={data.ai_requests}
          icon={Activity}
        />

      </div>

    </div>
  );
}

function Card({ title, value, icon: Icon }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm text-slate-500">{title}</p>
          <h2 className="mt-2 text-2xl font-semibold text-slate-900">{value}</h2>
        </div>
        <div className="flex h-10 w-10 items-center justify-center rounded-md bg-slate-100 text-slate-600">
          <Icon size={19} strokeWidth={1.75} aria-hidden="true" />
        </div>
      </div>
    </div>
  );
}