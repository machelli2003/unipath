import { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";

import CourseRecommendationCard from "@/components/recommendations/CourseRecommendationCard";
import { getLatestRecommendations } from "@/services/recommendationService";

export default function RecommendationResultsPage() {
  const location = useLocation();
  const [recommendations, setRecommendations] = useState(location.state?.recommendations ?? null);
  const [loading, setLoading] = useState(!location.state?.recommendations);
  const [error, setError] = useState("");

  useEffect(() => {
    if (location.state?.recommendations) return;

    const loadRecommendations = async () => {
      try {
        setLoading(true);
        const data = await getLatestRecommendations();
        setRecommendations(data);
      } catch (err) {
        setError(err.response?.data?.error || "Could not load recommendations.");
      } finally {
        setLoading(false);
      }
    };

    loadRecommendations();
  }, [location.state?.recommendations]);

  if (loading) {
    return <div className="py-10 text-sm text-muted-foreground">Loading your recommendations…</div>;
  }

  if (!recommendations || !Array.isArray(recommendations.top_courses) || recommendations.top_courses.length === 0) {
    return (
      <div className="mx-auto max-w-md py-16 text-center">
        <h1 className="text-lg font-semibold text-foreground">No recommendations yet</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Complete an assessment first to see your personalized course matches.
        </p>
        {error ? <p className="mt-2 text-sm text-destructive">{error}</p> : null}
        <Link
          to="/onboarding"
          className="mt-4 inline-block rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground"
        >
          Start assessment
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-foreground">Your top course matches</h1>
        <p className="text-sm text-muted-foreground">
          Ranked by Academic Fit (40%), Interest Fit (25%), Skills Fit (20%), Career Fit (15%).
        </p>
      </div>

      <div className="space-y-4">
        {recommendations.top_courses.map((result, index) => (
          <CourseRecommendationCard key={result.course_id || result.course_name} result={result} rank={index + 1} />
        ))}
      </div>
    </div>
  );
}
