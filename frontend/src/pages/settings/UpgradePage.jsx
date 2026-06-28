import { useNavigate } from "react-router-dom";
import { FiCheck } from "react-icons/fi";

const PREMIUM_FEATURES = [
  "AI chat advisor",
  "What-if grade simulator",
  "Downloadable PDF reports",
  "Unlimited course & university comparisons",
  "Career roadmap planning",
];

export default function UpgradePage() {
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-md space-y-6 py-10 text-center">
      <h1 className="text-xl font-bold text-foreground">This feature needs Premium</h1>
      <p className="text-sm text-muted-foreground">
        Upgrade to unlock the full UniPath Ghana toolkit.
      </p>

      <div className="rounded-lg border border-border bg-card p-5 text-left">
        <ul className="space-y-2">
          {PREMIUM_FEATURES.map((feature) => (
            <li key={feature} className="flex items-center gap-2 text-sm text-foreground">
              <FiCheck className="h-4 w-4 text-primary" />
              {feature}
            </li>
          ))}
        </ul>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => navigate(-1)}
          className="flex-1 rounded-md border border-input py-2 text-sm font-medium"
        >
          Go back
        </button>
        <button className="flex-1 rounded-md bg-accent py-2 text-sm font-medium text-accent-foreground">
          Upgrade now
        </button>
      </div>
    </div>
  );
}
