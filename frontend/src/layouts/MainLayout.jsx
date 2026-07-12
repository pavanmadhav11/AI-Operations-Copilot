import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import { Outlet } from "react-router-dom";

function MainLayout() {
  return (
    <div className="flex min-h-screen bg-gray-100 dark:bg-slate-900 transition-colors duration-300">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <main className="p-8 bg-gray-100 dark:bg-slate-900 text-black dark:text-white min-h-screen transition-colors duration-300">
          <Outlet />
        </main>

      </div>

    </div>
  );
}

export default MainLayout;