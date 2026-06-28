import { Link } from "react-router-dom";

export default function PageHero({ badge, title, description, ctaText, ctaLink, children }) {
  return (
    <section className="rounded-[2rem] border border-border bg-white p-8 shadow-sm">
      <div className="space-y-4">
        {badge && (
          <p className="inline-flex rounded-full bg-primary/10 px-4 py-1 text-sm font-semibold text-primary">
            {badge}
          </p>
        )}
        <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl">{title}</h1>
        <p className="max-w-3xl text-base text-muted-foreground sm:text-lg">{description}</p>
        {ctaText && ctaLink && (
          <Link
            to={ctaLink}
            className="inline-flex rounded-full bg-primary px-5 py-3 text-sm font-semibold text-white transition hover:bg-primary/90"
          >
            {ctaText}
          </Link>
        )}
        {children}
      </div>
    </section>
  );
}
