import { getTranslations } from "next-intl/server";

const LINGUISTIC_ICON = (
  <svg viewBox="0 0 32 32" fill="none" className="h-7 w-7">
    <path
      d="M6 8h20M6 14h20M6 20h13"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
    />
    <path
      d="M23 24l2.5 3L29 21"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const MEDIA_ICON = (
  <svg viewBox="0 0 32 32" fill="none" className="h-7 w-7">
    <rect x="5" y="7" width="22" height="18" rx="2" stroke="currentColor" strokeWidth="2" />
    <circle cx="12" cy="14" r="2.4" stroke="currentColor" strokeWidth="2" />
    <path
      d="M6 22l6.5-6.5a2 2 0 0 1 2.8 0L21 21l1.8-1.8a2 2 0 0 1 2.8 0L27 21"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const TECH_ICON = (
  <svg viewBox="0 0 32 32" fill="none" className="h-7 w-7">
    <rect x="11" y="11" width="10" height="10" rx="1.5" stroke="currentColor" strokeWidth="2" />
    <path
      d="M16 5v4M16 23v4M5 16h4M23 16h4M8 8l2.5 2.5M23.5 23.5 21 21M8 24l2.5-2.5M23.5 8.5 21 11"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
);

export async function PillarsBand() {
  const t = await getTranslations("home.pillars");

  const pillars = [
    {
      key: "linguistic",
      icon: LINGUISTIC_ICON,
      label: t("linguistic.label"),
      description: t("linguistic.description"),
      status: t("statusActive"),
      active: true,
    },
    {
      key: "media",
      icon: MEDIA_ICON,
      label: t("media.label"),
      description: t("media.description"),
      status: t("statusSoon"),
      active: false,
    },
    {
      key: "tech",
      icon: TECH_ICON,
      label: t("tech.label"),
      description: t("tech.description"),
      status: t("statusSoon"),
      active: false,
    },
  ];

  return (
    <section className="flex flex-col gap-5 rounded-2xl border border-border bg-surface-alt/60 p-6">
      <div>
        <h2 className="font-display text-xl font-bold text-heading text-balance">
          {t("title")}
        </h2>
        <p className="mt-1.5 max-w-2xl text-sm text-muted">{t("subtitle")}</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        {pillars.map((pillar) => (
          <div
            key={pillar.key}
            className={`flex flex-col gap-3 rounded-xl border p-4 ${
              pillar.active
                ? "border-accent bg-accent-soft"
                : "border-border bg-surface"
            }`}
          >
            <div className="flex items-center justify-between gap-2">
              <span
                className={pillar.active ? "text-accent-strong" : "text-muted"}
              >
                {pillar.icon}
              </span>
              <span
                className={`rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${
                  pillar.active
                    ? "bg-good-bg text-good"
                    : "bg-surface-alt text-muted"
                }`}
              >
                {pillar.status}
              </span>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-heading">
                {pillar.label}
              </h3>
              <p className="mt-1 text-xs leading-relaxed text-muted">
                {pillar.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
