import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { FiMenu, FiX } from "react-icons/fi";

const NAV_LINKS = [
  { to: "/", label: "Home" },
  { to: "/best-universities", label: "Universities" },
  { to: "/cut-off-points", label: "Cut-Off Points" },
  { to: "/admission-requirements", label: "Requirements" },
];

export default function PublicHeader() {
  const { isAuthenticated } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const ctaLink = isAuthenticated ? "/dashboard" : "/register";
  const ctaLabel = isAuthenticated ? "Dashboard" : "Register";

  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-3 text-lg font-semibold tracking-tight text-slate-900">
          <span className="rounded-full bg-primary/10 px-3 py-1 text-sm font-semibold text-primary">Ghana</span>
          <span>Uni Checker</span>
        </Link>

        <button
          type="button"
          onClick={() => setMenuOpen((current) => !current)}
          className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-700 md:hidden"
          aria-label="Toggle navigation menu"
        >
          {menuOpen ? <FiX className="h-5 w-5" /> : <FiMenu className="h-5 w-5" />}
        </button>

        <nav className={`flex-1 basis-full md:basis-auto md:block ${menuOpen ? "block" : "hidden"}`}>
          <div className="mt-4 grid gap-3 rounded-3xl border border-slate-200 bg-slate-50 p-4 md:mt-0 md:grid-flow-col md:border-0 md:bg-transparent md:p-0 md:items-center md:justify-center md:gap-8">
            {NAV_LINKS.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </nav>

        <div className="hidden items-center gap-3 md:flex">
          <Link to="/login" className="text-sm font-medium text-slate-600 hover:text-slate-900">
            Login
          </Link>
          <Link
            to={ctaLink}
            className="rounded-full bg-primary px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-primary/90"
          >
            {ctaLabel}
          </Link>
        </div>

        {menuOpen && (
          <div className="w-full md:hidden">
            <div className="mt-4 flex flex-col gap-3 px-4 pb-4">
              <Link to="/login" className="rounded-2xl bg-slate-100 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-200" onClick={() => setMenuOpen(false)}>
                Login
              </Link>
              <Link
                to={ctaLink}
                className="rounded-2xl bg-primary px-4 py-3 text-sm font-semibold text-white transition hover:bg-primary/90"
                onClick={() => setMenuOpen(false)}
              >
                {ctaLabel}
              </Link>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
