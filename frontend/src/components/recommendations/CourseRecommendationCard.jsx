import { useState } from "react";
import { FiChevronDown, FiChevronUp } from "react-icons/fi";

import AdmissionBadge from "./AdmissionBadge";
import ScoreBreakdownChart from "@/components/charts/ScoreBreakdownChart";

export default function CourseRecommendationCard({ result, rank }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="rounded-lg border border-border bg-card p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-medium text-muted-foreground">#{rank}</span>
            <h3 className="text-base font-semibold text-foreground">{result.course_name}</h3>
          </div>
          <p className="mt-1 text-2xl font-bold text-primary">{result.match_score}%</p>
        </div>
        <AdmissionBadge category={result.admission?.category} />
      </div>

      <ul className="mt-4 space-y-1">
        {result.explanation_points.map((point, i) => (
          <li key={i} className="text-sm text-muted-foreground">
            • {point}
          </li>
        ))}
      </ul>

      <button
        onClick={() => setExpanded((e) => !e)}
        className="mt-3 flex items-center gap-1 text-sm font-medium text-primary"
      >
        {expanded ? "Hide breakdown" : "Show score breakdown"}
        {expanded ? <FiChevronUp /> : <FiChevronDown />}
      </button>

      {expanded && (
        <div className="mt-3">
          <ScoreBreakdownChart breakdown={result.score_breakdown} />
        </div>
      )}
    </div>
  );
}
