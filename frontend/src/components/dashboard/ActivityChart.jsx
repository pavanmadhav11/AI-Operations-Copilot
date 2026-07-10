import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

const data = [
  { day: "Mon", requests: 120 },
  { day: "Tue", requests: 240 },
  { day: "Wed", requests: 180 },
  { day: "Thu", requests: 320 },
  { day: "Fri", requests: 280 },
  { day: "Sat", requests: 390 },
  { day: "Sun", requests: 450 },
];

export default function ActivityChart() {
  return (
    <div className="bg-white rounded-xl shadow p-6 h-96">
      <h2 className="text-xl font-semibold mb-5">
        AI Requests
      </h2>

      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="day" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="requests"
            stroke="#2563eb"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}