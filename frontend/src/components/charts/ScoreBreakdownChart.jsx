import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const COMPONENT_LABELS = {
  academic_fit: "Academic",
  interest_fit: "Interest",
  skills_fit: "Skills",
  career_fit: "Career",
};

const COMPONENT_MAX = {
  academic_fit: 40,
  interest_fit: 25,
  skills_fit: 20,
  career_fit: 15,
};

const BAR_COLORS = ["#0d6e5f", "#2a9d8f", "#e9c46a", "#e76f51"];

export default function ScoreBreakdownChart({ breakdown }) {
  const data = Object.entries(breakdown).map(([key, value]) => ({
    name: COMPONENT_LABELS[key] || key,
    value,
    max: COMPONENT_MAX[key] || 100,
  }));

  return (
    <ResponsiveContainer width="100%" height={160}>
      <BarChart data={data} layout="vertical" margin={{ left: 8, right: 16 }}>
        <XAxis type="number" hide domain={[0, 40]} />
        <YAxis type="category" dataKey="name" width={70} tick={{ fontSize: 12 }} />
        <Tooltip
          formatter={(value, _name, item) => [`${value} / ${item.payload.max}`, "Score"]}
        />
        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
          {data.map((_, index) => (
            <Cell key={index} fill={BAR_COLORS[index % BAR_COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
