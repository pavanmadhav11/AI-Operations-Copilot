const activities = [
  "📄 Contract uploaded",
  "🤖 AI generated report",
  "📊 SQL query executed",
  "📈 Forecast completed",
  "📧 Email summarized",
];

export default function RecentActivity() {
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
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}