import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import useAuthStore from "../../store/authStore";
import { Bell } from "lucide-react";
import { getNotifications, markNotificationRead } from "../../services/notificationService";

export default function Navbar() {
  const navigate = useNavigate();

  const { user, logout } = useAuthStore();

  const [open, setOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);

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

  useEffect(() => {
    loadNotifications();
    const timer = setInterval(loadNotifications, 60000);
    return () => clearInterval(timer);
  }, []);

  async function loadNotifications() {
    try {
      setNotifications(await getNotifications());
    } catch {
      setNotifications([]);
    }
  }

  async function openNotification(notification) {
    try {
      if (!notification.is_read) await markNotificationRead(notification.id);
      setNotifications((current) => current.map((item) => item.id === notification.id ? { ...item, is_read: true } : item));
      setNotificationsOpen(false);
      navigate(notification.link);
    } catch {
      await loadNotifications();
    }
  }

  const unreadCount = notifications.filter((notification) => !notification.is_read).length;

  function handleLogout() {
    logout();

    navigate("/login");
  }

  return (
    <header className="bg-white dark:bg-slate-800 shadow h-16 px-8 flex justify-between items-center">

      <input
        type="text"
        placeholder="Search..."
        className="w-96 border rounded-lg px-4 py-2 dark:bg-slate-700 dark:text-white dark:border-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <div className="flex items-center gap-6">

        <div className="relative">
          <button className="relative rounded p-2 hover:bg-slate-100" onClick={() => { setNotificationsOpen((value) => !value); loadNotifications(); }} aria-label="Notifications">
            <Bell size={22} />
            {unreadCount > 0 && <span className="absolute -right-1 -top-1 rounded-full bg-red-600 px-1.5 text-xs text-white">{unreadCount}</span>}
          </button>
          {notificationsOpen && (
            <div className="absolute right-0 top-12 z-50 max-h-96 w-96 overflow-y-auto rounded-xl border bg-white shadow-xl">
              <div className="border-b p-4 font-semibold">Notifications</div>
              {notifications.length === 0 ? <p className="p-5 text-sm text-slate-500">No current alerts.</p> : notifications.map((notification) => (
                <button className={`block w-full border-b p-4 text-left hover:bg-slate-50 ${notification.is_read ? "" : "bg-blue-50"}`} key={notification.id} onClick={() => openNotification(notification)}>
                  <span className="block font-medium">{notification.title}</span>
                  <span className="mt-1 block text-sm text-slate-600">{notification.message}</span>
                </button>
              ))}
            </div>
          )}
        </div>

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
