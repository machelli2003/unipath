import { Link } from "react-router-dom";
import { FiClipboard, FiLayers, FiChevronRight } from "react-icons/fi";
import PublicHeader from "@/components/common/PublicHeader";
import PageHero from "@/components/common/PageHero";

const UNIVERSITY_REQUIREMENTS = [
  {
    name: "University of Ghana (UG)",
    location: "Legon, Accra",
    aggregate: "6–24",
    points: [
      "Credit passes (A1–C6) in Core English, Core Mathematics, and Integrated Science or Social Studies.",
      "Three relevant elective subjects with credit passes.",
      "Specific subject requirements vary by faculty (e.g. Sciences need Elective Maths).",
      "Medicine requires aggregate 6–10 with distinctions in science subjects.",
    ],
  },
  {
    name: "Kwame Nkrumah University of Science & Technology (KNUST)",
    location: "Kumasi",
    aggregate: "6–24",
    points: [
      "Credit passes in three core subjects and three elective subjects.",
      "Engineering programmes require Elective Mathematics and Physics.",
      "Health sciences require Biology, Chemistry, and Physics/Elective Maths.",
      "Art programmes accept passes in relevant creative arts subjects.",
    ],
  },
  {
    name: "University of Cape Coast (UCC)",
    location: "Cape Coast",
    aggregate: "6–30",
    points: [
      "Credit passes in Core English and Core Mathematics are required for all programmes.",
      "Education programmes may accept slightly higher aggregates.",
      "Science programmes require relevant science electives.",
      "Popular for B.Ed programmes with flexible requirements.",
    ],
  },
  {
    name: "University for Development Studies (UDS)",
    location: "Tamale",
    aggregate: "6–36",
    points: [
      "Generally more flexible aggregate requirements.",
      "Strong focus on development-oriented and agricultural programmes.",
      "Medical programmes still require competitive aggregates (6–15).",
      "Accepts students from all SHS programme tracks.",
    ],
  },
  {
    name: "Ashesi University",
    location: "Berekuso, Eastern Region",
    aggregate: "Varies",
    points: [
      "Private university with a holistic admissions process.",
      "WASSCE results are considered with entrance exam and interview.",
      "Strong emphasis on leadership, ethics, and innovation.",
      "Scholarship programmes are available for qualified students.",
    ],
  },
];

const FAQS = [
  {
    question: "What are the basic requirements for university admission in Ghana?",
    answer: "You need a valid WASSCE or NOVDEC certificate with credit passes (A1–C6) in Core English, Core Mathematics, and either Integrated Science or Social Studies, plus 3 relevant elective subjects.",
  },
  {
    question: "Do all universities in Ghana have the same requirements?",
    answer: "No. While the basic WASSCE requirement is universal, each university sets its own aggregate cut-off points and specific subject requirements for each programme.",
  },
  {
    question: "Can I apply with NOVDEC results?",
    answer: "Yes. All public universities and most private universities in Ghana accept NOVDEC results alongside WASSCE results.",
  },
  {
    question: "What if I don't meet the requirements for any university?",
    answer: "You can resit subjects through NOVDEC to improve grades, apply for diploma or certificate programmes, or consider distance learning options.",
  },
  {
    question: "How do I know which electives I need for a programme?",
    answer: "Each programme has specific elective requirements. For example, Engineering needs Elective Maths and Physics, while Medicine needs Biology and Chemistry.",
  },
];

export default function RequirementsPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <PublicHeader />

      <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 space-y-10">
        <div className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <nav className="flex flex-wrap items-center gap-2 text-sm text-slate-500">
              <Link to="/" className="hover:text-slate-900">Home</Link>
              <span className="text-slate-300">/</span>
              <span className="font-semibold text-slate-900">Admission Requirements</span>
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
          badge="The admission rules every Ghanaian university expects"
          title="University Admission Requirements in Ghana"
          description="A comprehensive breakdown of what each major Ghanaian university requires — from aggregate scores to subject combinations."
        />

        <section className="grid gap-6 xl:grid-cols-2">
          <div className="rounded-[2rem] border border-slate-200 bg-card p-8 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-3xl bg-primary/10 text-primary">
                <FiClipboard className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-foreground">General Requirements for All Universities</h2>
                <p className="mt-2 text-sm text-muted-foreground">
                  You need a valid WASSCE or NOVDEC certificate with credit passes in English, Maths, and relevant electives.
                </p>
              </div>
            </div>
            <ul className="mt-6 space-y-3 text-sm text-muted-foreground">
              <li>Valid WASSCE or NOVDEC certificate from WAEC.</li>
              <li>Credit passes in Core English and Core Mathematics.</li>
              <li>Credit pass in either Integrated Science or Social Studies.</li>
              <li>Three relevant elective subjects with credit passes.</li>
              <li>Aggregate within the university's cut-off point.</li>
            </ul>
          </div>

          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-3xl bg-primary/10 text-primary">
                <FiLayers className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-foreground">Requirements by University</h2>
                <p className="mt-2 text-sm text-muted-foreground">
                  Each university sets programme-specific requirements, especially for medicine, engineering, and law.
                </p>
              </div>
            </div>
            <div className="mt-6 space-y-4">
              {UNIVERSITY_REQUIREMENTS.map((item) => (
                <div key={item.name} className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <h3 className="font-semibold text-foreground">{item.name}</h3>
                      <p className="text-sm text-muted-foreground">{item.location}</p>
                    </div>
                    <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">Aggregate: {item.aggregate}</span>
                  </div>
                  <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
                    {item.points.map((point) => (
                      <li key={point} className="flex items-start gap-2">
                        <span className="mt-1 text-primary">→</span>
                        <span>{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-semibold text-foreground">What You Need to Apply</h2>
            <div className="mt-6 space-y-4 text-sm text-muted-foreground">
              <p>Strong core grades, the correct elective combination, and an aggregate that meets your chosen programme's cut-off are the foundations for admission.</p>
              <p>Private universities may also require interviews or entrance exams in addition to WASSCE/NOVDEC results.</p>
              <p>You can resit subjects through NOVDEC to improve your scores and increase your chance of meeting the required aggregate.</p>
            </div>
          </div>

          <aside className="space-y-6 rounded-[2rem] border border-slate-200 bg-card p-6 shadow-sm">
            <div className="rounded-3xl bg-primary/5 p-5 text-sm text-primary">
              <p className="font-semibold">Can I use NOVDEC results?</p>
              <p className="mt-2 text-sm text-primary/90">Yes, most public and private universities in Ghana accept NOVDEC results the same way as WASSCE certificates.</p>
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
              to="/best-universities"
              className="inline-flex w-full items-center justify-center rounded-full bg-primary px-4 py-3 text-sm font-semibold text-white transition hover:bg-primary/90"
            >
              Explore top universities
            </Link>
          </aside>
        </section>
      </main>
    </div>
  );
}
