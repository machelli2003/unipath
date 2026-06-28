import { Link } from "react-router-dom";
import { FiBarChart2, FiShield, FiChevronRight } from "react-icons/fi";
import PublicHeader from "@/components/common/PublicHeader";
import PageHero from "@/components/common/PageHero";

const CUT_OFF_UNIS = [
  { name: "UG Legon", range: "8–12", note: "Top programmes like Medicine and Pharmacy." },
  { name: "KNUST", range: "6–18", note: "Competitive engineering and science courses." },
  { name: "UCC", range: "8–20", note: "Strong options in education, business, and health." },
  { name: "UDS", range: "18–36", note: "Flexible ranges for many programmes." },
  { name: "UPSA", range: "12–28", note: "Best for business, accounting, and law." },
  { name: "GCTU", range: "10–25", note: "Strong ICT and technology programmes." },
];

const FAQS = [
  {
    question: "Do cut-offs change every year?",
    answer: "Yes, they are influenced by applicant volume, programme demand, and available spaces each year.",
  },
  {
    question: "Can I still apply with a higher aggregate?",
    answer: "Yes, especially to private universities and less competitive programmes where cut-off points are higher.",
  },
  {
    question: "Which universities are good backup options?",
    answer: "UDS, UEW, and many private institutions offer more flexible ranges while still providing quality programmes.",
  },
];

export default function CutOffPointsPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <PublicHeader />

      <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 space-y-10">
        <div className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <nav className="flex flex-wrap items-center gap-2 text-sm text-slate-500">
              <Link to="/" className="hover:text-slate-900">Home</Link>
              <span className="text-slate-300">/</span>
              <span className="font-semibold text-slate-900">Cut-Off Points</span>
            </nav>
            <Link
              to="/"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
            >
              🎓 Click here to check which university you qualify for
            </Link>
          </div>
        </div>

        <PageHero
          badge="Understand the minimum aggregates you need for admission"
          title="University Cut-Off Points in Ghana"
          description="Know the minimum aggregate score you need before applying. Compare cut-off points for UG Legon, KNUST, UCC, UDS, and more."
        />

        <section className="grid gap-6 xl:grid-cols-2">
          <div className="rounded-[2rem] border border-slate-200 bg-card p-8 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-3xl bg-primary/10 text-primary">
                <FiShield className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-foreground">Understanding Cut-Off Points</h2>
                <p className="mt-2 text-sm text-muted-foreground">
                  A cut-off point is the maximum aggregate score a university will accept for a programme. Lower scores are better.
                </p>
              </div>
            </div>
            <ul className="mt-6 space-y-3 text-sm text-muted-foreground">
              <li>Use your best 6 subjects, including Core English, Core Maths, and relevant electives.</li>
              <li>The cut-off depends on the programme's demand and the number of qualified applicants.</li>
              <li>Private universities often have more flexible aggregates than public universities.</li>
            </ul>
          </div>

          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-3xl bg-primary/10 text-primary">
                <FiBarChart2 className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-foreground">Cut-Off Points by University</h2>
                <p className="mt-2 text-sm text-muted-foreground">
                  These ranges reflect recent admission cycles and help you plan your applications.
                </p>
              </div>
            </div>
            <div className="mt-6 grid gap-4">
              {CUT_OFF_UNIS.map((item) => (
                <div key={item.name} className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="font-semibold text-foreground">{item.name}</p>
                      <p className="text-sm text-muted-foreground">{item.note}</p>
                    </div>
                    <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
                      {item.range}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-semibold text-foreground">Tips for Meeting Cut-Off Points</h2>
            <ul className="mt-6 space-y-4 text-sm text-muted-foreground">
              <li>Practice more and improve your NOVDEC scores if you need a lower aggregate.</li>
              <li>Apply to a mix of ambitious and safe programmes across public and private universities.</li>
              <li>Review the programme combination requirements carefully before you submit your application.</li>
              <li>Focus on the strongest subjects for your chosen programme.</li>
            </ul>
            <div className="mt-8 rounded-3xl border border-slate-200 bg-slate-50 p-6">
              <p className="text-sm font-semibold text-foreground">See which programmes fit your grades.</p>
              <p className="mt-2 text-sm text-muted-foreground">
                If your dream programme is too competitive, find related options with slightly higher cut-off points.
              </p>
            </div>
          </div>

          <aside className="space-y-6 rounded-[2rem] border border-slate-200 bg-card p-6 shadow-sm">
            <div className="rounded-3xl bg-primary/5 p-5 text-sm text-primary">
              <p className="font-semibold">When to explore backup options</p>
              <p className="mt-2 text-primary/90">
                Don't rely on a single application. Choose 2–3 universities with different cut-off ranges.
              </p>
            </div>
            <div className="space-y-4">
              <p className="text-lg font-semibold text-foreground">Frequently Asked Questions</p>
              {FAQS.map((item) => (
                <div key={item.question}>
                  <p className="font-semibold text-foreground">{item.question}</p>
                  <p className="mt-2 text-sm text-muted-foreground">{item.answer}</p>
                </div>
              ))}
            </div>
            <Link
              to="/admission-requirements"
              className="inline-flex w-full items-center justify-center rounded-full bg-primary px-4 py-3 text-sm font-semibold text-white transition hover:bg-primary/90"
            >
              View admission requirements
            </Link>
          </aside>
        </section>
      </main>
    </div>
  );
}
