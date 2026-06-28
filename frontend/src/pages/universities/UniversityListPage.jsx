import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { listUniversities } from "@/services/universityService";

export default function UniversityListPage() {
  const [universities, setUniversities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    listUniversities()
      .then((data) => setUniversities(data.items))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold text-foreground">Universities</h1>

      {isLoading ? (
        <p className="text-sm text-muted-foreground">Loading...</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {universities.map((u) => (
            <Link
              key={u._id}
              to={`/universities/${encodeURIComponent(u.name)}`}
              className="rounded-lg border border-border bg-card p-4 hover:border-primary/50"
            >
              <h3 className="text-sm font-semibold text-foreground">{u.short_name || u.name}</h3>
              <p className="mt-1 text-xs text-muted-foreground">{u.location}</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
