import { useLocation, Link } from "react-router-dom";

import CourseRecommendationCard from "@/components/recommendations/CourseRecommendationCard";

export default function RecommendationResultsPage() {
  const location = useLocation();
  const recommendations = location.state?.recommendations;

  if (!recommendations) {
    return (
      <div className="mx-auto max-w-md py-16 text-center">
        <h1 className="text-lg font-semibold text-foreground">No recommendations yet</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Complete an assessment first to see your personalized course matches.
        </p>
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
        {recommendations.results.map((result, index) => (
          <CourseRecommendationCard key={result.course_name} result={result} rank={index + 1} />
        ))}
      </div>
    </div>
  );
}
