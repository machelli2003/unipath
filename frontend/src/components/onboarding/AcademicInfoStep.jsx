import { useStudentProfile } from "@/context/StudentProfileContext";
import { WASSCE_GRADES, COMMON_WASSCE_SUBJECTS } from "@/constants/studentOptions";

export default function AcademicInfoStep() {
  const { profile, updateProfile } = useStudentProfile();

  const addSubject = () => {
    updateProfile({
      subjects: [...profile.subjects, { subject_name: COMMON_WASSCE_SUBJECTS[0], grade: "C6" }],
    });
  };

  const updateSubject = (index, key, value) => {
    const next = [...profile.subjects];
    next[index] = { ...next[index], [key]: value };
    updateProfile({ subjects: next });
  };

  const removeSubject = (index) => {
    updateProfile({ subjects: profile.subjects.filter((_, i) => i !== index) });
  };

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-lg font-semibold text-foreground">Academic information</h2>
        <p className="text-sm text-muted-foreground">
          {profile.mode === "awaiting_results"
            ? "Enter your mock grades or rate your subject strengths."
            : "Enter your WASSCE subjects and grades."}
        </p>
      </div>

      <div>
        <label className="text-sm font-medium text-foreground">SHS Program</label>
        <input
          type="text"
          placeholder="e.g. General Science"
          value={profile.shs_program}
          onChange={(e) => updateProfile({ shs_program: e.target.value })}
          className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-foreground">Subjects &amp; Grades</label>
        {profile.subjects.map((subj, index) => (
          <div key={index} className="flex gap-2">
            <select
              value={subj.subject_name}
              onChange={(e) => updateSubject(index, "subject_name", e.target.value)}
              className="flex-1 rounded-md border border-input bg-background px-3 py-2 text-sm"
            >
              {COMMON_WASSCE_SUBJECTS.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
            <select
              value={subj.grade}
              onChange={(e) => updateSubject(index, "grade", e.target.value)}
              className="w-24 rounded-md border border-input bg-background px-3 py-2 text-sm"
            >
              {WASSCE_GRADES.map((g) => (
                <option key={g} value={g}>
                  {g}
                </option>
              ))}
            </select>
            <button
              type="button"
              onClick={() => removeSubject(index)}
              className="rounded-md border border-input px-3 text-sm text-destructive"
            >
              Remove
            </button>
          </div>
        ))}

        <button
          type="button"
          onClick={addSubject}
          className="text-sm font-medium text-primary"
        >
          + Add subject
        </button>
      </div>
    </div>
  );
}
