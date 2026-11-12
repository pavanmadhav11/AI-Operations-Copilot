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
import Inventory from "../pages/inventory/Inventory";
import AddInventoryItem from "../pages/inventory/AddInventoryItem";
import UserRoles from "../pages/admin/UserRoles";
import Transfers from "../pages/inventory/Transfers";
import Batches from "../pages/inventory/Batches";
import ActionHistory from "../pages/inventory/ActionHistory";
import Warehouses from "../pages/inventory/Warehouses";
import Procurement from "../pages/inventory/Procurement";

export const router = createBrowserRouter([
  { path: "/login", element: <Login /> },
  { path: "/register", element: <Register /> },
  { path: "/forgot-password", element: <ForgotPassword /> },
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <Dashboard /> },
      { path: "chat", element: <Chat /> },
      { path: "sql", element: <SQLGenerator /> },
      { path: "pdf", element: <PDFAnalyzer /> },
      { path: "excel", element: <ExcelAnalyzer /> },
      { path: "settings", element: <Settings /> },
      {
        path: "analytics",
        element: (
          <ProtectedRoute roles={["admin"]}>
            <Analytics />
          </ProtectedRoute>
        ),
      },
      { path: "reports", element: <Reports /> },
      { path: "inventory", element: <Inventory /> },
      { path: "inventory/batches", element: <Batches /> },
      {
        path: "inventory/add",
        element: (
          <ProtectedRoute roles={["admin", "manager"]}>
            <AddInventoryItem />
          </ProtectedRoute>
        ),
      },
      {
        path: "inventory/transfers",
        element: (
          <ProtectedRoute roles={["admin", "manager"]}>
            <Transfers />
          </ProtectedRoute>
        ),
      },
      {
        path: "inventory/warehouses",
        element: (
          <ProtectedRoute roles={["admin", "manager"]}>
            <Warehouses />
          </ProtectedRoute>
        ),
      },
      {
        path: "inventory/actions",
        element: (
          <ProtectedRoute roles={["admin", "manager"]}>
            <ActionHistory />
          </ProtectedRoute>
        ),
      },
      {
        path: "procurement",
        element: (
          <ProtectedRoute roles={["admin", "manager"]}>
            <Procurement />
          </ProtectedRoute>
        ),
      },
      {
        path: "users",
        element: (
          <ProtectedRoute roles={["admin"]}>
            <UserRoles />
          </ProtectedRoute>
        ),
      },
    ],
  },
  { path: "*", element: <NotFound /> },
]);
