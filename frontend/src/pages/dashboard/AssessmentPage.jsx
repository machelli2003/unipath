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

  // Check which required fields are missing
  const getMissingFields = () => {
    const missing = [];
    if (!profile.interests || profile.interests.length === 0) missing.push("Interests");
    if (!profile.skills || profile.skills.length === 0) missing.push("Skills");
    if (!profile.career_goals || profile.career_goals.length === 0) missing.push("Career Goals");
    return missing;
  };

  const missingFields = getMissingFields();

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

      {missingFields.length > 0 && (
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4">
          <p className="text-sm font-semibold text-yellow-900">Complete your profile first</p>
          <p className="mt-1 text-sm text-yellow-800">
            You need to fill in: {missingFields.join(", ")}
          </p>
          <button
            onClick={() => navigate("/onboarding")}
            className="mt-2 text-sm font-medium text-yellow-700 underline hover:text-yellow-900"
          >
            Go back to onboarding →
          </button>
        </div>
      )}

      {error && <p className="text-sm text-destructive">{error}</p>}

      <button
        onClick={handleRunAssessment}
        disabled={isSubmitting || profile.subjects.length === 0 || missingFields.length > 0}
        className="w-full rounded-md bg-primary py-2.5 text-sm font-medium text-primary-foreground disabled:opacity-60"
      >
        {isSubmitting ? "Calculating..." : "Get my recommendations"}
      </button>
    </div>
  );
}
