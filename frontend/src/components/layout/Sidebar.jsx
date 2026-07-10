import { Link } from "react-router-dom";

const menu = [
  { name: "Dashboard", path: "/" },
  { name: "AI Chat", path: "/chat" },
  { name: "SQL Generator", path: "/sql" },
  { name: "PDF Analyzer", path: "/pdf" },
  { name: "Excel Analyzer", path: "/excel" },
  { name: "Analytics", path: "/analytics" },
  { name: "Reports", path: "/reports" },
  { name: "Settings", path: "/settings" },
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
            key={item.name}
            to={item.path}
            className="block rounded-lg px-4 py-3 hover:bg-slate-700 mb-2"
          >
            {item.name}
          </Link>
        ))}

      </nav>

    </aside>
  );
}