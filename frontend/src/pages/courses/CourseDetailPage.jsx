import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { getCourse } from "@/services/courseService";

export default function CourseDetailPage() {
  const { name } = useParams();
  const [course, setCourse] = useState(null);

  useEffect(() => {
    getCourse(name).then(setCourse);
  }, [name]);

  if (!course) return <p className="text-sm text-muted-foreground">Loading...</p>;

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">{course.name}</h1>
        <p className="mt-1 text-sm text-muted-foreground">{course.description}</p>
      </div>

      <Section title="Required Subjects">
        <ul className="space-y-1">
          {course.required_subjects?.map((s, i) => (
            <li key={i} className="text-sm text-muted-foreground">
              {s.subject_name} — minimum {s.minimum_grade} {s.is_core === "yes" && "(core)"}
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Career Paths">
        <div className="flex flex-wrap gap-2">
          {course.career_paths?.map((c) => (
            <span key={c} className="rounded-full bg-secondary px-3 py-1 text-xs text-secondary-foreground">
              {c}
            </span>
          ))}
        </div>
      </Section>

      <Section title="Offered At">
        <ul className="space-y-1">
          {course.offered_at_universities?.map((u) => (
            <li key={u} className="text-sm text-muted-foreground">
              {u}
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Historical Cut-offs">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-muted-foreground">
              <th className="py-1">University</th>
              <th className="py-1">Year</th>
              <th className="py-1">Cut-off Aggregate</th>
            </tr>
          </thead>
          <tbody>
            {course.historical_cutoffs?.map((c, i) => (
              <tr key={i} className="border-t border-border">
                <td className="py-1.5 text-foreground">{c.university_name}</td>
                <td className="py-1.5 text-muted-foreground">{c.year}</td>
                <td className="py-1.5 text-muted-foreground">{c.cut_off_aggregate}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className="rounded-lg border border-border bg-card p-5">
      <h2 className="text-sm font-semibold text-foreground">{title}</h2>
      <div className="mt-3">{children}</div>
    </div>
  );
}
