import { createBrowserRouter } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import Dashboard from "../pages/dashboard/Dashboard";

import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";
import ForgotPassword from "../pages/auth/ForgotPassword";

import Chat from "../pages/chat/Chat";
import SQLGenerator from "../pages/sql/SQLGenerator";

import NotFound from "../pages/NotFound";

import ProtectedRoute from "./ProtectedRoute";

export const router = createBrowserRouter([
  // -------------------------
  // Authentication
  // -------------------------
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/register",
    element: <Register />,
  },
  {
    path: "/forgot-password",
    element: <ForgotPassword />,
  },

  // -------------------------
  // Protected Routes
  // -------------------------
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),

    children: [
      {
        index: true,
        element: <Dashboard />,
      },

      {
        path: "chat",
        element: <Chat />,
      },

      {
        path: "sql",
        element: <SQLGenerator />,
      },

      // Future Modules
      {
        path: "pdf",
        element: <h1 className="text-3xl p-10">PDF Analyzer</h1>,
      },

      {
        path: "excel",
        element: <h1 className="text-3xl p-10">Excel Analyzer</h1>,
      },

      {
        path: "analytics",
        element: <h1 className="text-3xl p-10">Analytics</h1>,
      },

      {
        path: "reports",
        element: <h1 className="text-3xl p-10">Reports</h1>,
      },

      {
        path: "settings",
        element: <h1 className="text-3xl p-10">Settings</h1>,
      },
    ],
  },

  // -------------------------
  // 404
  // -------------------------
  {
    path: "*",
    element: <NotFound />,
  },
]);