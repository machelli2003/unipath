import { useState } from "react";
import { FiDownload } from "react-icons/fi";

import { generateReport } from "@/services/reportService";

export default function ReportsPage() {
  const [reportType, setReportType] = useState("recommendation_summary");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    setLoading(true);
    setError("");
    setMessage("");

    try {
      const data = await generateReport(reportType);
      setMessage(data.message || "Report generated successfully.");
    } catch (err) {
      setError(err.response?.data?.error || "Could not generate report.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-lg space-y-6">
      <div>
        <h1 className="text-xl font-bold text-foreground">Reports</h1>
        <p className="text-sm text-muted-foreground">
          Generate a plain-text report of your latest recommendation results.
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

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-md bg-primary py-2 text-sm font-medium text-primary-foreground disabled:opacity-60"
        >
          <FiDownload className="h-4 w-4" />
          {loading ? "Generating..." : "Generate report"}
        </button>

        {message ? <p className="text-sm text-green-600">{message}</p> : null}
        {error ? <p className="text-sm text-destructive">{error}</p> : null}
      </div>
    </div>
  );
}
