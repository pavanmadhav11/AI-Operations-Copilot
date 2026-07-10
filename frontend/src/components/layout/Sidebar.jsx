import { Link } from "react-router-dom";

const menu = [
  "Dashboard",
  "AI Chat",
  "SQL Generator",
  "PDF Analyzer",
  "Excel Analyzer",
  "Analytics",
  "Forecasting",
  "Reports",
  "Workflow",
  "Admin",
  "Settings",
];

export default function Sidebar() {
  return (
    <aside className="bg-slate-900 text-white w-72 min-h-screen">

      <div className="text-2xl font-bold p-6 border-b border-slate-700">
        AI Copilot
      </div>

      <nav className="p-5">

        {menu.map((item) => (

          <Link
            key={item}
            to="/"
            className="block rounded-lg px-4 py-3 hover:bg-slate-700 mb-2"
          >
            {item}
          </Link>

        ))}

      </nav>

    </aside>
  );
}