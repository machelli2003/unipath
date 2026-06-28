import { useState } from "react";

import { compareItems } from "@/services/comparisonService";

export default function ComparisonPage() {
  const [type, setType] = useState("course");
  const [namesInput, setNamesInput] = useState("");
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  const handleCompare = async () => {
    setError("");
    const names = namesInput.split(",").map((n) => n.trim()).filter(Boolean);
    try {
      const data = await compareItems(type, names);
      setItems(data.items);
    } catch (err) {
      setError(err.response?.data?.error || "Comparison failed.");
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-foreground">Compare</h1>
        <p className="text-sm text-muted-foreground">
          Compare courses or universities side by side.
        </p>
      </div>

      <div className="flex flex-wrap gap-3">
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="rounded-md border border-input bg-background px-3 py-2 text-sm"
        >
          <option value="course">Courses</option>
          <option value="university">Universities</option>
        </select>
        <input
          type="text"
          placeholder="Names, comma separated"
          value={namesInput}
          onChange={(e) => setNamesInput(e.target.value)}
          className="flex-1 rounded-md border border-input bg-background px-3 py-2 text-sm"
        />
        <button
          onClick={handleCompare}
          className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground"
        >
          Compare
        </button>
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <div key={item._id || item.name} className="rounded-lg border border-border bg-card p-4">
            <h3 className="text-sm font-semibold text-foreground">{item.name}</h3>
            <pre className="mt-2 whitespace-pre-wrap text-xs text-muted-foreground">
              {JSON.stringify(item, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
}
