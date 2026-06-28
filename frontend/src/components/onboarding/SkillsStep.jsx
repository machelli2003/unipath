import { useStudentProfile } from "@/context/StudentProfileContext";
import { SKILLS } from "@/constants/studentOptions";

export default function SkillsStep() {
  const { profile, updateProfile } = useStudentProfile();

  const getRating = (skillName) => {
    const found = profile.skills.find((s) => s.skill_name === skillName);
    return found ? found.rating : 3;
  };

  const setRating = (skillName, rating) => {
    const existingIndex = profile.skills.findIndex((s) => s.skill_name === skillName);
    const next = [...profile.skills];
    if (existingIndex >= 0) {
      next[existingIndex] = { skill_name: skillName, rating };
    } else {
      next.push({ skill_name: skillName, rating });
    }
    updateProfile({ skills: next });
  };

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-lg font-semibold text-foreground">Rate your skills</h2>
        <p className="text-sm text-muted-foreground">1 = weakest, 5 = strongest.</p>
      </div>

      <div className="space-y-4">
        {SKILLS.map((skill) => (
          <div key={skill}>
            <div className="flex justify-between text-sm">
              <span className="text-foreground">{skill}</span>
              <span className="text-muted-foreground">{getRating(skill)}/5</span>
            </div>
            <input
              type="range"
              min={1}
              max={5}
              value={getRating(skill)}
              onChange={(e) => setRating(skill, Number(e.target.value))}
              className="mt-1 w-full accent-primary"
            />
          </div>
        ))}
      </div>
    </div>
  );
}
