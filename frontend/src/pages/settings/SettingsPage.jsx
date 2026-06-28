import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";

export default function SettingsPage() {
  const { user, isPremium } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="max-w-lg space-y-6">
      <h1 className="text-xl font-bold text-foreground">Settings</h1>

      <div className="rounded-lg border border-border bg-card p-5 space-y-3">
        <h2 className="text-sm font-semibold text-foreground">Account</h2>
        <p className="text-sm text-muted-foreground">{user?.full_name}</p>
        <p className="text-sm text-muted-foreground">{user?.email}</p>
      </div>

      <div className="rounded-lg border border-border bg-card p-5 flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-foreground">Appearance</h2>
          <p className="text-sm text-muted-foreground">Toggle dark/light mode</p>
        </div>
        <button
          onClick={toggleTheme}
          className="rounded-md border border-input px-3 py-1.5 text-sm"
        >
          {theme === "dark" ? "Switch to light" : "Switch to dark"}
        </button>
      </div>

      <div id="upgrade" className="rounded-lg border border-border bg-card p-5">
        <h2 className="text-sm font-semibold text-foreground">Subscription</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          You are on the {isPremium ? "Premium" : "Free"} plan.
        </p>
        {!isPremium && (
          <button className="mt-3 rounded-md bg-accent px-4 py-2 text-sm font-medium text-accent-foreground">
            Upgrade to Premium
          </button>
        )}
      </div>
    </div>
  );
}
