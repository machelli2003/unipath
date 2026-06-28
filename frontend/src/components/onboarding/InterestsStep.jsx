import { useStudentProfile } from "@/context/StudentProfileContext";
import { INTERESTS } from "@/constants/studentOptions";
import { cn } from "@/lib/utils";

export default function InterestsStep() {
  const { profile, updateProfile } = useStudentProfile();

  const toggleInterest = (interest) => {
    const isSelected = profile.interests.includes(interest);
    updateProfile({
      interests: isSelected
        ? profile.interests.filter((i) => i !== interest)
        : [...profile.interests, interest],
    });
  };

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-foreground">What are you interested in?</h2>
        <p className="text-sm text-muted-foreground">Select all that apply.</p>
      </div>

      <div className="flex flex-wrap gap-2">
        {INTERESTS.map((interest) => (
          <button
            key={interest}
            type="button"
            onClick={() => toggleInterest(interest)}
            className={cn(
              "rounded-full border px-4 py-2 text-sm transition-colors",
              profile.interests.includes(interest)
                ? "border-primary bg-primary text-primary-foreground"
                : "border-input text-muted-foreground hover:border-primary/50"
            )}
          >
            {interest}
          </button>
        ))}
      </div>
    </div>
  );
}
