import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-3 bg-background px-4 text-center">
      <h1 className="text-4xl font-bold text-foreground">404</h1>
      <p className="text-sm text-muted-foreground">This page doesn&apos;t exist.</p>
      <Link to="/dashboard" className="text-sm font-medium text-primary">
        Back to dashboard
      </Link>
    </div>
  );
}
