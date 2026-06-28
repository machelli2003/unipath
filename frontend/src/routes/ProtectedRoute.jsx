import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

export default function ProtectedRoute({ children, requirePremium = false }) {
  const { isAuthenticated, isPremium, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return null; // could render a spinner here

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requirePremium && !isPremium) {
    return <Navigate to="/settings/upgrade" replace />;
  }

  return children;
}
