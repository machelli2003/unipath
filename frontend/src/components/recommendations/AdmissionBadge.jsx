import { cn } from "@/lib/utils";

const CATEGORY_STYLES = {
  "Safe Choice": "bg-safe/15 text-safe border-safe/30",
  "Competitive Choice": "bg-competitive/15 text-competitive border-competitive/30",
  "Reach Choice": "bg-reach/15 text-reach border-reach/30",
};

const CATEGORY_EMOJI = {
  "Safe Choice": "🟢",
  "Competitive Choice": "🟡",
  "Reach Choice": "🔴",
};

export default function AdmissionBadge({ category }) {
  if (!category) {
    return (
      <span className="inline-flex items-center rounded-full border border-border bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground">
        No cut-off data
      </span>
    );
  }

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-medium",
        CATEGORY_STYLES[category]
      )}
    >
      {CATEGORY_EMOJI[category]} {category}
    </span>
  );
}
