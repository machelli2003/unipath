import { useState } from "react";
import { FiDownload } from "react-icons/fi";

export default function ReportsPage() {
  const [reportType, setReportType] = useState("recommendation_summary");

  return (
    <div className="max-w-lg space-y-6">
      <div>
        <h1 className="text-xl font-bold text-foreground">Reports</h1>
        <p className="text-sm text-muted-foreground">
          Generate a PDF report of your recommendations or career roadmap. Premium feature.
        </p>
      </div>

      <div className="rounded-lg border border-border bg-card p-5 space-y-4">
        <label className="text-sm font-medium text-foreground">Report type</label>
        <select
          value={reportType}
          onChange={(e) => setReportType(e.target.value)}
          className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
        >
          <option value="recommendation_summary">Recommendation Summary</option>
          <option value="career_roadmap">Career Roadmap</option>
          <option value="full_report">Full Report</option>
        </select>

        <button className="flex w-full items-center justify-center gap-2 rounded-md bg-primary py-2 text-sm font-medium text-primary-foreground">
          <FiDownload className="h-4 w-4" />
          Generate report
        </button>
      </div>
    </div>
  );
}
