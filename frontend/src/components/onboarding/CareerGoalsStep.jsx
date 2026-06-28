import { useStudentProfile } from "@/context/StudentProfileContext";
import { CAREER_GOALS } from "@/constants/studentOptions";
import { cn } from "@/lib/utils";

export default function CareerGoalsStep() {
  const { profile, updateProfile } = useStudentProfile();

  const toggleGoal = (goal) => {
    const isSelected = profile.career_goals.includes(goal);
    updateProfile({
      career_goals: isSelected
        ? profile.career_goals.filter((g) => g !== goal)
        : [...profile.career_goals, goal],
    });
  };

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-foreground">What's your career goal?</h2>
        <p className="text-sm text-muted-foreground">Select one or more.</p>
      </div>

      <div className="flex flex-wrap gap-2">
        {CAREER_GOALS.map((goal) => (
          <button
            key={goal}
            type="button"
            onClick={() => toggleGoal(goal)}
            className={cn(
              "rounded-full border px-4 py-2 text-sm transition-colors",
              profile.career_goals.includes(goal)
                ? "border-primary bg-primary text-primary-foreground"
                : "border-input text-muted-foreground hover:border-primary/50"
            )}
          >
            {goal}
          </button>
        ))}
      </div>
    </div>
  );
}
