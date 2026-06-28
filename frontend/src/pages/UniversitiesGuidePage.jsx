import { Link } from "react-router-dom";
import { FiAward, FiChevronRight, FiCompass } from "react-icons/fi";
import PublicHeader from "@/components/common/PublicHeader";
import PageHero from "@/components/common/PageHero";

const UNIVERSITY_LIST = [
  {
    rank: "#1",
    name: "University of Ghana (UG)",
    location: "Legon, Accra",
    founded: "1948",
    description: "Ghana's oldest and largest university, consistently ranked #1 nationally and among the top 10 in Africa.",
    programmes: ["Medicine & Health Sciences", "Law", "Business Administration", "Arts & Social Sciences"],
  },
  {
    rank: "#2",
    name: "Kwame Nkrumah University of Science & Technology (KNUST)",
    location: "Kumasi",
    founded: "1952",
    description: "The premier science and technology university in West Africa, known for producing top engineers and doctors.",
    programmes: ["Engineering", "Architecture", "Pharmacy", "Computer Science", "Medicine"],
  },
  {
    rank: "#3",
    name: "University of Cape Coast (UCC)",
    location: "Cape Coast",
    founded: "1962",
    description: "Leading institution for teacher education, with a beautiful coastal campus and growing research output.",
    programmes: ["Education", "Agriculture", "Health Sciences", "Business"],
  },
  {
    rank: "#4",
    name: "Ashesi University",
    location: "Berekuso, Eastern Region",
    founded: "2002",
    description: "Top-ranked private university, known for innovation, ethics-focused education, and high graduate employability.",
    programmes: ["Computer Science", "Business Administration", "Engineering", "Liberal Arts"],
  },
  {
    rank: "#5",
    name: "University for Development Studies (UDS)",
    location: "Tamale",
    founded: "1992",
    description: "Community-based learning approach, strong medical school, and commitment to northern Ghana development.",
    programmes: ["Medicine", "Agriculture", "Development Studies", "Public Health"],
  },
  {
    rank: "#6",
    name: "University of Professional Studies, Accra (UPSA)",
    location: "Accra",
    founded: "1965",
    description: "Top choice for business and professional studies, with strong industry connections and career placement.",
    programmes: ["Accounting", "Banking & Finance", "Marketing", "Law"],
  },
  {
    rank: "#7",
    name: "Ghana Communication Technology University (GCTU)",
    location: "Accra",
    founded: "2005",
    description: "Specialized in ICT education, producing graduates ready for Ghana's growing tech sector.",
    programmes: ["Information Technology", "Telecommunications", "Multimedia", "Cyber Security"],
  },
  {
    rank: "#8",
    name: "University of Mines and Technology (UMaT)",
    location: "Tarkwa",
    founded: "2004",
    description: "The only university in Ghana dedicated to mining and mineral technology education.",
    programmes: ["Mining Engineering", "Geological Engineering", "Environmental Science"],
  },
];

const TIPS = [
  {
    title: "Match Your Strengths",
    description: "Choose a university known for the programme you're passionate about, not just its overall ranking.",
  },
  {
    title: "Consider Location",
    description: "Think about proximity to home, cost of living, and campus environment (urban vs. rural).",
  },
  {
    title: "Check Your Eligibility",
    description: "Ensure your WASSCE aggregate and subject combination meet the requirements before applying.",
  },
  {
    title: "Explore Financial Aid",
    description: "Many universities offer scholarships, bursaries, and work-study options. Research these early.",
  },
];

const FAQS = [
  {
    question: "What is the best university in Ghana?",
    answer: "The University of Ghana (Legon) is consistently ranked #1 in Ghana and among the top 10 in Africa. KNUST follows closely, especially for science and engineering programmes.",
  },
  {
    question: "Which university is best for Engineering in Ghana?",
    answer: "KNUST is the premier engineering university in Ghana, offering Mechanical, Electrical, Computer, Civil, and Chemical Engineering.",
  },
  {
    question: "What is the best private university in Ghana?",
    answer: "Ashesi University is widely regarded as the best private university in Ghana, known for innovation, ethics-focused education, and high graduate employability.",
  },
  {
    question: "How many accredited universities are in Ghana?",
    answer: "Ghana has over 15 accredited public universities and numerous private institutions. All must be accredited by the National Accreditation Board (NAB) to award recognized degrees.",
  },
  {
    question: "Which university is easiest to get into in Ghana?",
    answer: "Universities like UDS, UEW, and some private institutions have more flexible aggregate requirements (up to 36), while still offering strong programmes.",
  },
];

export default function UniversitiesGuidePage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <PublicHeader />

      <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8 space-y-10">
        <div className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <nav className="flex flex-wrap items-center gap-2 text-sm text-slate-500">
              <Link to="/" className="hover:text-slate-900">Home</Link>
              <span className="text-slate-300">/</span>
              <span className="font-semibold text-slate-900">Best Universities in Ghana</span>
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
          badge="University rankings, programmes, and admission insight"
          title="Best Universities in Ghana 2026"
          description="A comprehensive guide to Ghana's top universities — what makes them stand out, their strongest programmes, and how to get admitted."
        />

        <section className="grid gap-6 xl:grid-cols-2">
          {UNIVERSITY_LIST.slice(0, 4).map((university) => (
            <div key={university.name} className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
              <div className="flex items-center justify-between gap-3">
                <span className="rounded-3xl bg-primary/10 px-4 py-2 text-sm font-semibold text-primary">{university.rank}</span>
                <div className="text-right text-sm text-slate-500">
                  <p>{university.location}</p>
                  <p>Founded {university.founded}</p>
                </div>
              </div>
              <h2 className="mt-6 text-xl font-semibold text-foreground">{university.name}</h2>
              <p className="mt-3 text-sm leading-7 text-muted-foreground">{university.description}</p>
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {university.programmes.map((program) => (
                  <div key={program} className="rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
                    {program}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          {UNIVERSITY_LIST.slice(4).map((university) => (
            <div key={university.name} className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
              <div className="flex items-center justify-between gap-3">
                <span className="rounded-3xl bg-primary/10 px-4 py-2 text-sm font-semibold text-primary">{university.rank}</span>
                <div className="text-right text-sm text-slate-500">
                  <p>{university.location}</p>
                  <p>Founded {university.founded}</p>
                </div>
              </div>
              <h2 className="mt-6 text-xl font-semibold text-foreground">{university.name}</h2>
              <p className="mt-3 text-sm leading-7 text-muted-foreground">{university.description}</p>
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {university.programmes.map((program) => (
                  <div key={program} className="rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
                    {program}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </section>

        <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-primary">How to Choose</p>
              <h2 className="mt-3 text-3xl font-semibold text-foreground">How to Choose the Right University</h2>
            </div>
            <p className="max-w-2xl text-sm leading-7 text-muted-foreground">
              Use your grades, programme preference, location, and future goals to find the best-fit university.
            </p>
          </div>
          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            {TIPS.map((tip) => (
              <div key={tip.title} className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
                <h3 className="font-semibold text-foreground">{tip.title}</h3>
                <p className="mt-3 text-sm text-muted-foreground">{tip.description}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-[2rem] border border-slate-200 bg-card p-8 shadow-sm">
          <div className="space-y-4">
            <h2 className="text-3xl font-semibold text-foreground">Frequently Asked Questions</h2>
            <p className="max-w-2xl text-sm text-muted-foreground">
              Answers to the most common questions students ask when choosing universities in Ghana.
            </p>
          </div>
          <div className="mt-8 grid gap-4">
            {FAQS.map((item) => (
              <div key={item.question} className="rounded-3xl border border-slate-200 bg-white p-6">
                <h3 className="font-semibold text-foreground">{item.question}</h3>
                <p className="mt-3 text-sm text-muted-foreground">{item.answer}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
