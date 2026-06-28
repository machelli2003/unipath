import { useState } from "react";

import { useStudentProfile } from "@/context/StudentProfileContext";
import { runSimulation } from "@/services/simulationService";
import { WASSCE_GRADES } from "@/constants/studentOptions";
import CourseRecommendationCard from "@/components/recommendations/CourseRecommendationCard";

export default function WhatIfSimulatorPage() {
  const { profile } = useStudentProfile();
  const [subjects, setSubjects] = useState(profile.subjects);
  const [results, setResults] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  const updateGrade = (index, grade) => {
    const next = [...subjects];
    next[index] = { ...next[index], grade };
    setSubjects(next);
  };

  const handleRun = async () => {
    setIsRunning(true);
    try {
      const data = await runSimulation({ mode: "awaiting_results", subjects });
      setResults(data);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-foreground">What-If Simulator</h1>
        <p className="text-sm text-muted-foreground">
          Adjust your grades to see how your course matches would change. Premium feature —
          results here are hypothetical and not saved to your profile.
        </p>
      </div>

      <div className="rounded-lg border border-border bg-card p-5">
        <h2 className="text-sm font-semibold text-foreground">Adjust grades</h2>
        <div className="mt-3 space-y-2">
          {subjects.map((s, i) => (
            <div key={i} className="flex items-center justify-between gap-3">
              <span className="text-sm text-foreground">{s.subject_name}</span>
              <select
                value={s.grade}
                onChange={(e) => updateGrade(i, e.target.value)}
                className="rounded-md border border-input bg-background px-2 py-1 text-sm"
              >
                {WASSCE_GRADES.map((g) => (
                  <option key={g} value={g}>
                    {g}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>

        <button
          onClick={handleRun}
          disabled={isRunning}
          className="mt-4 w-full rounded-md bg-primary py-2 text-sm font-medium text-primary-foreground disabled:opacity-60"
        >
          {isRunning ? "Calculating..." : "Run simulation"}
        </button>
      </div>

      {results && (
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Simulated aggregate: <span className="font-medium text-foreground">{results.simulated_aggregate}</span>
          </p>
          {results.results.map((result, index) => (
            <CourseRecommendationCard key={result.course_name} result={result} rank={index + 1} />
          ))}
        </div>
      )}
    </div>
  );
}
