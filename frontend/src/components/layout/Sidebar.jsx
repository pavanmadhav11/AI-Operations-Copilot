import { NavLink } from "react-router-dom";
import { useEffect } from "react";

import {
  createSession,
  getSessions,
} from "../../services/sessionService";

import useSessionStore from "../../store/sessionStore";

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
  const {
    sessions,
    currentSession,
    setSessions,
    setCurrentSession,
    addSession,
  } = useSessionStore();

  useEffect(() => {
    loadSessions();
  }, []);

  async function loadSessions() {
    try {
      const data = await getSessions();

      setSessions(data);

      if (data.length > 0) {
        setCurrentSession(data[0]);
      }
    } catch (err) {
      toast.error(
        err.response?.data?.detail ||
        "Something went wrong."
      );
    }
  }

  async function handleNewChat() {
    try {
      const session = await createSession();

      addSession(session);
    } catch (err) {
      toast.error(
      err.response?.data?.detail ||
      "Something went wrong."
    );
    }
  }

  return (
    <aside className="bg-slate-900 dark:bg-black text-white w-72 min-h-screen flex flex-col transition-colors">

      <div className="text-2xl font-bold p-6 border-b border-slate-700">
        AI Copilot
      </div>

      <nav className="p-5">

        {menu.map((item) => (

          <NavLink
            key={item.name}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              `block rounded-lg px-4 py-3 mb-2 transition-all ${
                isActive
                  ? "bg-blue-600 text-white font-semibold"
                  : "hover:bg-slate-700"
              }`
            }
          >
            {item.name}
          </NavLink>

        ))}

      </nav>

      <div className="px-5 mt-2">

        <button
          onClick={handleNewChat}
          className="w-full bg-blue-600 hover:bg-blue-700 rounded-lg py-2 transition"
        >
          + New Chat
        </button>

      </div>

      <div className="flex-1 overflow-y-auto p-5">

        <h3 className="text-sm text-slate-400 mb-3">
          Chat Sessions
        </h3>

        {sessions.map((session) => (

          <button
            key={session.id}
            onClick={() => setCurrentSession(session)}
            className={`w-full text-left p-3 rounded-lg mb-2 transition ${
              currentSession?.id === session.id
                ? "bg-slate-700"
                : "hover:bg-slate-800"
            }`}
          >
            {session.title}
          </button>

        ))}

      </div>

    </aside>
  );
}