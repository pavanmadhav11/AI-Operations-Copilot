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
import Reports from "../pages/reports/Reports";
import Settings from "../pages/settings/Settings";
import PDFAnalyzer from "../pages/pdf/PDFAnalyzer";
import ExcelAnalyzer from "../pages/excel/ExcelAnalyzer";
import Analytics from "../pages/analytics/Analytics";

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
        element: <PDFAnalyzer />,
      },

      {
        path: "excel",
        element: <ExcelAnalyzer />,
      },

      {
        path: "settings",
        element: <Settings />,
      },
      {
        path: "analytics",
        element: <Analytics />,
      },
      {
        path: "reports",
        element: <Reports />,
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