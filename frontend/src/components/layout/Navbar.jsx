import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import useAuthStore from "../../store/authStore";

export default function Navbar() {
  const navigate = useNavigate();

  const { user, logout } = useAuthStore();

  const [open, setOpen] = useState(false);

  const menuRef = useRef(null);

  const initials = user?.name
    ? user.name
        .split(" ")
        .map((word) => word[0])
        .join("")
        .toUpperCase()
        .slice(0, 2)
    : "U";

  useEffect(() => {
    function handleClickOutside(event) {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target)
      ) {
        setOpen(false);
      }
    }

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () =>
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
  }, []);

  function handleLogout() {
    logout();

    navigate("/login");
  }

  return (
    <header className="bg-white dark:bg-slate-800 shadow h-16 px-8 flex justify-between items-center">

      {/* Search */}

      <input
        type="text"
        placeholder="Search..."
        className="w-96 border rounded-lg px-4 py-2 dark:bg-slate-700 dark:text-white dark:border-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      {/* Right */}

      <div className="flex items-center gap-6">

        <button className="text-xl hover:scale-110 transition">
          🔔
        </button>

        <div
          className="relative"
          ref={menuRef}
        >

          <button
            onClick={() => setOpen(!open)}
            className="flex items-center gap-3"
          >

            <div className="text-right">

              <p className="font-semibold text-gray-800 dark:text-white">
                {user?.name || "User"}
              </p>

              <p className="text-xs text-gray-500">
                {user?.email}
              </p>

            </div>

            <div className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">

              {initials}

            </div>

          </button>

          {open && (
            <div className="absolute right-0 mt-3 w-56 bg-white dark:bg-slate-800 rounded-xl shadow-lg border dark:border-slate-700 overflow-hidden z-50">

              <button
                onClick={() => {
                  navigate("/settings");
                  setOpen(false);
                }}
                className="w-full text-left px-5 py-3 hover:bg-gray-100 dark:hover:bg-slate-700"
              >
                ⚙ Settings
              </button>

              <button
                onClick={() => {
                  navigate("/reports");
                  setOpen(false);
                }}
                className="w-full text-left px-5 py-3 hover:bg-gray-100 dark:hover:bg-slate-700"
              >
                📄 Reports
              </button>

              <hr />

              <button
                onClick={handleLogout}
                className="w-full text-left px-5 py-3 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
              >
                🚪 Logout
              </button>

            </div>
          )}

        </div>

      </div>

    </header>
  );
}