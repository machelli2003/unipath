import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useStudentProfile } from "@/context/StudentProfileContext";
import { submitAssessment } from "@/services/assessmentService";
import { getRecommendations } from "@/services/recommendationService";

export default function AssessmentPage() {
  const { profile } = useStudentProfile();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleRunAssessment = async () => {
    setError("");
    setIsSubmitting(true);
    try {
      const assessment = await submitAssessment({
        mode: profile.mode,
        subjects: profile.subjects,
      });
      const recommendations = await getRecommendations(assessment.assessment_id);
      navigate("/recommendations", { state: { recommendations } });
    } catch (err) {
      setError(err.response?.data?.error || "Could not run assessment. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mx-auto max-w-lg space-y-6 py-10">
      <div>
        <h1 className="text-xl font-bold text-foreground">Review your information</h1>
        <p className="text-sm text-muted-foreground">
          We&apos;ll convert your grades and run them against our course database.
        </p>
      </div>

      <div className="rounded-lg border border-border bg-card p-5">
        <h2 className="text-sm font-semibold text-foreground">Subjects</h2>
        <ul className="mt-2 space-y-1">
          {profile.subjects.map((s, i) => (
            <li key={i} className="flex justify-between text-sm text-muted-foreground">
              <span>{s.subject_name}</span>
              <span className="font-medium text-foreground">{s.grade}</span>
            </li>
          ))}
        </ul>
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      <button
        onClick={handleRunAssessment}
        disabled={isSubmitting || profile.subjects.length === 0}
        className="w-full rounded-md bg-primary py-2.5 text-sm font-medium text-primary-foreground disabled:opacity-60"
      >
        {isSubmitting ? "Calculating..." : "Get my recommendations"}
      </button>
    </div>
  );
}
