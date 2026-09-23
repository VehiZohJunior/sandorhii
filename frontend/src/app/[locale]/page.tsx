import { getTranslations, setRequestLocale } from "next-intl/server";
import { SubmitForm } from "@/components/SubmitForm";
import { PillarsBand } from "@/components/PillarsBand";

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("home");

  const stats = [t("heroStat1"), t("heroStat2"), t("heroStat3")];

  return (
    <div>
      <section className="relative overflow-hidden bg-ink px-[6vw] pt-16 pb-28 text-center">
        <div className="hero-grid pointer-events-none absolute inset-0" />
        <div
          className="hero-glow pointer-events-none absolute left-1/2 top-[-10%] h-[420px] w-[420px] -translate-x-1/2 rounded-full bg-accent-light/25 blur-[90px]"
          aria-hidden="true"
        />

        <div className="relative flex flex-col items-center">
          <span className="rounded-full border border-white/15 bg-white/5 px-4 py-1.5 text-[.72rem] font-semibold uppercase tracking-[1.5px] text-accent-light">
            {t("heroEyebrow")}
          </span>

          <h1 className="mt-5 font-display text-[2.6rem] leading-[1.05] font-extrabold tracking-tight text-white text-balance sm:text-[3.6rem]">
            San<span className="text-accent-light">Dor</span>Hii
          </h1>

          <p className="mt-3 max-w-lg font-display text-lg font-medium text-[#cdd8e6] text-balance sm:text-xl">
            {t("heroTagline")}
          </p>

          <p className="mt-5 max-w-xl text-[.95rem] leading-relaxed text-[#a9b8ca] text-balance">
            {t.rich("heroMission", {
              accent: (chunks) => (
                <span className="font-bold text-accent-light">{chunks}</span>
              ),
            })}
          </p>

          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            {stats.map((stat) => (
              <span
                key={stat}
                className="rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-[.8rem] font-semibold text-white"
              >
                {stat}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="px-[6vw] pt-0 pb-10">
        <SubmitForm />
      </section>

      <div className="mx-auto max-w-4xl px-5 pt-4 pb-10">
        <PillarsBand />
      </div>
    </div>
  );
}
