import {
  Users,
  FileText,
  Activity,
  Database,
} from "lucide-react";

const icons = {
  users: Users,
  documents: FileText,
  ai: Activity,
  storage: Database,
};

export default function StatCard({
  title,
  value,
  type,
  color,
}) {
  const Icon = icons[type] || FileText;

  return (
    <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition duration-300">
      <div className="flex justify-between items-center">
        <div>
          <p className="text-gray-500 text-sm">
            {title}
          </p>

          <h2
            className={`text-3xl font-bold mt-2 ${color}`}
          >
            {value}
          </h2>
        </div>

        <div className="rounded-full bg-slate-100 p-4">
          <Icon
            size={30}
            className={color}
          />
        </div>
      </div>
    </div>
  );
}