import { Link } from "react-router-dom";
import { FiCheckCircle, FiCompass, FiClock, FiSearch, FiChevronDown, FiShield } from "react-icons/fi";
import { useAuth } from "@/context/AuthContext";
import PublicHeader from "@/components/common/PublicHeader";
import PageHero from "@/components/common/PageHero";

const COVERED_UNIVERSITIES = [
  "UG", "KNUST", "UCC", "UDS", "UPSA", "Ashesi", "GCTU", "UMaT",
];

const WHY_CARDS = [
  {
    title: "Instant Results",
    description: "Get your admission chances in seconds without guesswork.",
  },
  {
    title: "20+ Universities",
    description: "Covers all major public and private universities across Ghana.",
  },
  {
    title: "Trusted & Accurate",
    description: "Built with admission data and updated for each cycle.",
  },
];

const TESTIMONIALS = [
  {
    quote: "I wasn't sure if my grades were good enough for KNUST. Ghana Uni Checker showed me exactly where I stood — I got admitted!",
    name: "Kwame A.",
    details: "BSc Computer Science, KNUST",
  },
  {
    quote: "Checked my eligibility in under a minute. The results were spot on. Saved me from applying to programmes I didn't qualify for.",
    name: "Ama D.",
    details: "BA Economics, UG",
  },
  {
    quote: "Very easy to use. I entered my WASSCE grades and instantly knew which programmes I could get into.",
    name: "Yaw M.",
    details: "BSc Nursing, UCC",
  },
];

export default function HomePage() {
  const { isAuthenticated } = useAuth();
  const ctaLink = isAuthenticated ? "/dashboard" : "/login";

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <PublicHeader />

      <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-[1.3fr_0.9fr] lg:items-start">
          <div className="space-y-10">
            <PageHero
              badge="Trusted by 10,000+ students"
              title="Ghana's #1 University Admission Checker"
              description="The fastest way to check your university admission chances in Ghana. Enter your WASSCE or NOVDEC grades and instantly see which universities and programmes you qualify for."
              ctaText="Check My Admission Chances"
              ctaLink={ctaLink}
            >
              <div className="mt-8 grid gap-4 sm:grid-cols-3">
                <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-primary">
                    <FiClock className="h-5 w-5" />
                  </div>
                  <p className="mt-4 font-semibold text-slate-900">Instant eligibility results</p>
                </div>
                <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-primary">
                    <FiCompass className="h-5 w-5" />
                  </div>
                  <p className="mt-4 font-semibold text-slate-900">20+ universities covered</p>
                </div>
                <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-primary">
                    <FiCheckCircle className="h-5 w-5" />
                  </div>
                  <p className="mt-4 font-semibold text-slate-900">Affordable & easy to use</p>
                </div>
              </div>
            </PageHero>

            <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
              <h2 className="text-2xl font-semibold text-foreground">Universities We Cover</h2>
              <p className="mt-3 max-w-2xl text-sm text-muted-foreground">
                We help you compare admission chances across major public and private universities in Ghana.
              </p>
              <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {COVERED_UNIVERSITIES.map((university) => (
                  <div key={university} className="rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm font-semibold text-slate-900">
                    {university}
                  </div>
                ))}
              </div>
            </section>

            <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-primary">Why Ghana Uni Checker</p>
                  <h2 className="mt-3 text-2xl font-semibold text-foreground">The admission tool built for Ghanaian students</h2>
                </div>
                <div className="rounded-3xl bg-primary/5 px-4 py-3 text-sm text-primary">
                  <FiShield className="inline-block h-5 w-5 align-middle" />
                  <span className="ml-2">Reliable guidance for programme selection and cut-off checks.</span>
                </div>
              </div>

              <div className="mt-8 grid gap-4 md:grid-cols-3">
                {WHY_CARDS.map((card) => (
                  <div key={card.title} className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
                    <h3 className="font-semibold text-foreground">{card.title}</h3>
                    <p className="mt-3 text-sm text-muted-foreground">{card.description}</p>
                  </div>
                ))}
              </div>
            </section>
          </div>

          <aside className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
            <div className="flex items-center gap-4 rounded-3xl bg-slate-50 p-5">
              <div className="flex h-14 w-14 items-center justify-center rounded-3xl bg-primary/10 text-primary">
                <FiSearch className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-foreground">Start Your Check</h2>
                <p className="mt-2 text-sm text-muted-foreground">Find out which universities and programmes fit your grades.</p>
              </div>
            </div>

            <div className="space-y-4 rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">Desired university</p>
                <button className="mt-3 flex w-full items-center justify-between rounded-2xl bg-white px-4 py-4 text-left text-sm text-slate-700 shadow-sm transition hover:border-slate-300">
                  <span>Choose a university...</span>
                  <FiChevronDown className="h-5 w-5 text-slate-500" />
                </button>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">Level of study</p>
                <button className="mt-3 flex w-full items-center justify-between rounded-2xl bg-white px-4 py-4 text-left text-sm text-slate-700 shadow-sm transition hover:border-slate-300">
                  <span>Choose level...</span>
                  <FiChevronDown className="h-5 w-5 text-slate-500" />
                </button>
              </div>
            </div>

            <Link
              to={ctaLink}
              className="inline-flex w-full items-center justify-center rounded-3xl bg-primary px-5 py-4 text-sm font-semibold text-white transition hover:bg-primary/90"
            >
              Check My Admission Chances
            </Link>
            <p className="text-center text-sm text-slate-500">No sign-up required · Results in seconds</p>
          </aside>
        </div>

        <section className="mt-16 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
          <div className="text-center">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-primary">Student Testimonials</p>
            <h2 className="mt-3 text-3xl font-semibold text-foreground">Trusted by thousands of students</h2>
            <p className="mx-auto mt-4 max-w-2xl text-sm text-muted-foreground">
              See how Ghana Uni Checker helped students confirm their admission chances and apply with confidence.
            </p>
          </div>

          <div className="mt-10 grid gap-6 lg:grid-cols-3">
            {TESTIMONIALS.map((testimonial) => (
              <div key={testimonial.name} className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
                <p className="text-sm leading-7 text-slate-700">“{testimonial.quote}”</p>
                <div className="mt-6 text-sm">
                  <p className="font-semibold text-foreground">{testimonial.name}</p>
                  <p className="text-muted-foreground">{testimonial.details}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-16 rounded-[2rem] border border-slate-200 bg-primary/5 p-8 text-center shadow-sm">
          <h2 className="text-3xl font-semibold text-foreground">Check Your University Admission Chances in Ghana</h2>
          <p className="mx-auto mt-4 max-w-2xl text-sm text-muted-foreground">
            Join thousands of Ghanaian students who used the admission checker to find the programmes they qualify for.
          </p>
          <Link
            to={ctaLink}
            className="mt-8 inline-flex rounded-full bg-primary px-8 py-4 text-sm font-semibold text-white transition hover:bg-primary/90"
          >
            Check My Chances Now
          </Link>
        </section>
      </main>
    </div>
  );
}
