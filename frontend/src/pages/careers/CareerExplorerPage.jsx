import { useEffect, useState } from "react";

import { listCareers, getCareer } from "@/services/careerService";

export default function CareerExplorerPage() {
  const [careers, setCareers] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    listCareers().then(setCareers);
  }, []);

  const handleSelect = async (name) => {
    const detail = await getCareer(name);
    setSelected(detail);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <div className="space-y-2 lg:col-span-1">
        <h1 className="text-xl font-bold text-foreground">Career Explorer</h1>
        <p className="text-sm text-muted-foreground">
          Start from a career goal and see which courses lead there.
        </p>
        <div className="mt-3 space-y-1">
          {careers.map((career) => (
            <button
              key={career.name}
              onClick={() => handleSelect(career.name)}
              className="w-full rounded-md border border-border bg-card px-3 py-2 text-left text-sm text-foreground hover:border-primary/50"
            >
              {career.name}
            </button>
          ))}
        </div>
      </div>

      <div className="lg:col-span-2">
        {selected ? (
          <div className="rounded-lg border border-border bg-card p-5">
            <h2 className="text-lg font-semibold text-foreground">{selected.name}</h2>
            <p className="mt-2 text-sm text-muted-foreground">{selected.description}</p>

            <h3 className="mt-4 text-sm font-semibold text-foreground">Related Courses</h3>
            <ul className="mt-2 space-y-1">
              {selected.related_courses_detail?.map((c) => (
                <li key={c.name} className="text-sm text-muted-foreground">
                  {c.name}
                </li>
              ))}
            </ul>

            <h3 className="mt-4 text-sm font-semibold text-foreground">Required Skills</h3>
            <div className="mt-2 flex flex-wrap gap-2">
              {selected.required_skills?.map((s) => (
                <span key={s} className="rounded-full bg-secondary px-3 py-1 text-xs text-secondary-foreground">
                  {s}
                </span>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">Select a career to explore.</p>
        )}
      </div>
    </div>
  );
}
