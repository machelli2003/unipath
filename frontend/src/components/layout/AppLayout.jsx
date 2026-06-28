import { Outlet, NavLink } from "react-router-dom";
import {
  FiHome,
  FiBarChart2,
  FiBookOpen,
  FiUsers,
  FiCompass,
  FiSliders,
  FiFileText,
  FiSettings,
  FiSun,
  FiMoon,
  FiLogOut,
} from "react-icons/fi";

import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: FiHome },
  { to: "/recommendations", label: "Recommendations", icon: FiBarChart2 },
  { to: "/courses", label: "Courses", icon: FiBookOpen },
  { to: "/universities", label: "Universities", icon: FiUsers },
  { to: "/careers", label: "Career Explorer", icon: FiCompass },
  { to: "/simulator", label: "What-If Simulator", icon: FiSliders },
  { to: "/reports", label: "Reports", icon: FiFileText },
  { to: "/settings", label: "Settings", icon: FiSettings },
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="flex min-h-screen bg-background">
      <aside className="hidden w-60 shrink-0 border-r border-border bg-card md:flex md:flex-col">
        <div className="px-5 py-6">
          <span className="text-lg font-bold text-foreground">UniPath Ghana</span>
        </div>

        <nav className="flex-1 space-y-1 px-3">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                )
              }
            >
              <Icon className="h-4 w-4" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-border p-3">
          <button
            onClick={toggleTheme}
            className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-secondary"
          >
            {theme === "dark" ? <FiSun className="h-4 w-4" /> : <FiMoon className="h-4 w-4" />}
            {theme === "dark" ? "Light mode" : "Dark mode"}
          </button>
          <button
            onClick={logout}
            className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-secondary"
          >
            <FiLogOut className="h-4 w-4" />
            Log out
          </button>
        </div>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex h-14 items-center justify-between border-b border-border bg-card px-4 md:px-6">
          <span className="text-sm font-medium text-muted-foreground md:hidden">UniPath Ghana</span>
          <div className="ml-auto flex items-center gap-3">
            <span className="text-sm text-foreground">{user?.full_name}</span>
            <span
              className={cn(
                "rounded-full px-2 py-0.5 text-xs font-medium",
                user?.subscription_tier === "premium"
                  ? "bg-accent text-accent-foreground"
                  : "bg-secondary text-secondary-foreground"
              )}
            >
              {user?.subscription_tier === "premium" ? "Premium" : "Free"}
            </span>
          </div>
        </header>

        <main className="flex-1 p-4 md:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
