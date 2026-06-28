import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { listCourses } from "@/services/courseService";

export default function CourseListPage() {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    listCourses()
      .then((data) => setCourses(data.items))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold text-foreground">Courses</h1>

      {isLoading ? (
        <p className="text-sm text-muted-foreground">Loading...</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {courses.map((course) => (
            <Link
              key={course._id}
              to={`/courses/${encodeURIComponent(course.name)}`}
              className="rounded-lg border border-border bg-card p-4 hover:border-primary/50"
            >
              <h3 className="text-sm font-semibold text-foreground">{course.name}</h3>
              <p className="mt-1 line-clamp-2 text-xs text-muted-foreground">
                {course.description}
              </p>
              <span className="mt-2 inline-block rounded-full bg-secondary px-2 py-0.5 text-xs text-secondary-foreground">
                {course.difficulty_level}
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
