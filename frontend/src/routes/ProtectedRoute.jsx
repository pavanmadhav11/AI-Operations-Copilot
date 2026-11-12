import { Navigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

export default function ProtectedRoute({ children, roles }) {
  const { token, user, isLoading } = useAuthStore();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (isLoading || !user) {
    return <div className="p-8">Loading account...</div>;
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
