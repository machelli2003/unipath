import { Link } from "react-router-dom";
import { FiArrowRight, FiTarget, FiSliders, FiBookOpen } from "react-icons/fi";

import { useAuth } from "@/context/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-foreground">
          Welcome back, {user?.full_name?.split(" ")[0] || "there"}
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Here&apos;s where things stand with your university path.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <DashboardCard
          icon={FiTarget}
          title="Get Recommendations"
          description="See which courses fit you best based on your latest assessment."
          to="/recommendations"
        />
        <DashboardCard
          icon={FiSliders}
          title="What-If Simulator"
          description="See how different grades would change your results."
          to="/simulator"
        />
        <DashboardCard
          icon={FiBookOpen}
          title="Explore Courses"
          description="Browse the full course and university knowledge base."
          to="/courses"
        />
      </div>
    </div>
  );
}

function DashboardCard({ icon: Icon, title, description, to }) {
  return (
    <Link
      to={to}
      className="group flex flex-col justify-between rounded-lg border border-border bg-card p-5 transition-colors hover:border-primary/50"
    >
      <div>
        <Icon className="h-6 w-6 text-primary" />
        <h3 className="mt-3 text-sm font-semibold text-foreground">{title}</h3>
        <p className="mt-1 text-sm text-muted-foreground">{description}</p>
      </div>
      <div className="mt-4 flex items-center text-sm font-medium text-primary">
        Go
        <FiArrowRight className="ml-1 h-4 w-4 transition-transform group-hover:translate-x-1" />
      </div>
    </Link>
  );
}
