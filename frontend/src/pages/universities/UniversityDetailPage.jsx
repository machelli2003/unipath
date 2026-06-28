import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { getUniversity } from "@/services/universityService";

export default function UniversityDetailPage() {
  const { name } = useParams();
  const [university, setUniversity] = useState(null);

  useEffect(() => {
    getUniversity(name).then(setUniversity);
  }, [name]);

  if (!university) return <p className="text-sm text-muted-foreground">Loading...</p>;

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">{university.name}</h1>
        <p className="mt-1 text-sm text-muted-foreground">{university.location}</p>
        <p className="mt-3 text-sm text-muted-foreground">{university.overview}</p>
      </div>

      <div className="rounded-lg border border-border bg-card p-5">
        <h2 className="text-sm font-semibold text-foreground">Faculties &amp; Programs</h2>
        <div className="mt-3 space-y-4">
          {university.faculties?.map((faculty, i) => (
            <div key={i}>
              <h3 className="text-sm font-medium text-foreground">{faculty.name}</h3>
              <ul className="mt-1 ml-4 space-y-1">
                {faculty.departments?.map((dept, j) => (
                  <li key={j} className="text-sm text-muted-foreground">
                    {dept.name}: {dept.programs?.join(", ")}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-lg border border-border bg-card p-5">
        <h2 className="text-sm font-semibold text-foreground">General Admission Requirements</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          {university.general_admission_requirements}
        </p>
      </div>
    </div>
  );
}
