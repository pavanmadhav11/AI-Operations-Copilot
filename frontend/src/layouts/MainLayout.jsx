import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import { Outlet } from "react-router-dom";

function MainLayout() {
  return (
    <div className="flex">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <main className="p-8">

          <Outlet />

        </main>

      </div>

    </div>
  );
}

export default MainLayout;