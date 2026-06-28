import { useStudentProfile } from "@/context/StudentProfileContext";
import { STUDENT_MODES } from "@/constants/studentOptions";
import { cn } from "@/lib/utils";

export default function ModeSelectStep() {
  const { profile, updateProfile } = useStudentProfile();

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-foreground">How are you tracking your grades?</h2>
        <p className="text-sm text-muted-foreground">
          This determines how we ask for your academic information.
        </p>
      </div>

      <div className="grid gap-3">
        {STUDENT_MODES.map((mode) => (
          <button
            key={mode.value}
            type="button"
            onClick={() => updateProfile({ mode: mode.value })}
            className={cn(
              "rounded-md border px-4 py-3 text-left text-sm transition-colors",
              profile.mode === mode.value
                ? "border-primary bg-primary/10 text-foreground"
                : "border-input text-muted-foreground hover:border-primary/50"
            )}
          >
            {mode.label}
          </button>
        ))}
      </div>
    </div>
  );
}
