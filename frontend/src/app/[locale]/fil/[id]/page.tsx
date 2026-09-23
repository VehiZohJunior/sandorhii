import { getTranslations, setRequestLocale } from "next-intl/server";
import { notFound } from "next/navigation";
import { Link } from "@/i18n/navigation";
import { api, ApiError } from "@/lib/api";
import { VerdictCard } from "@/components/VerdictCard";
import { ScoreGauge } from "@/components/ScoreGauge";
import { SignalList } from "@/components/SignalList";

export default async function FeedItemPage({
  params,
}: {
  params: Promise<{ locale: string; id: string }>;
}) {
  const { locale, id } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("feed");
  const tHome = await getTranslations("home");

  const submission = await api.getFeedItem(id).catch((err) => {
    if (err instanceof ApiError && err.status === 404) return null;
    throw err;
  });

  if (!submission || !submission.fact_check) {
    notFound();
  }

  const { fact_check: factCheck, linguistic_analysis: analysis } = submission;

  return (
    <div className="mx-auto max-w-[880px] px-5 py-12">
      <div className="flex flex-col gap-8">
        <Link href="/fil" className="text-sm font-medium text-accent hover:text-accent-strong">
          {t("back")}
        </Link>

        <VerdictCard verdict={factCheck.verdict}>
          {factCheck.published_at && (
            <span className="mb-3 inline-block rounded-full bg-white/20 px-4 py-1 text-[.82rem] font-bold">
              {t("publishedOn", {
                date: new Date(factCheck.published_at).toLocaleDateString(
                  locale
                ),
              })}
            </span>
          )}
        </VerdictCard>

        <div className="rounded-[18px] border border-border bg-surface p-7">
          <p className="whitespace-pre-wrap font-mono text-sm text-muted">
            &ldquo;{submission.raw_content}&rdquo;
          </p>
          <div className="mt-5 border-t border-border pt-5">
            <h2 className="mb-2 text-[.78rem] font-bold tracking-wide text-muted-2 uppercase">
              {t("resume")}
            </h2>
            <p className="text-foreground">{factCheck.resume}</p>
            <p className="mt-2 text-xs text-muted-2">— {factCheck.auteur}</p>
          </div>
        </div>

        {analysis && (
          <section className="flex flex-col gap-5 rounded-[18px] border border-border bg-surface p-7">
            <h2 className="font-display text-xl font-bold text-heading">
              {t("fullAnalysis")}
            </h2>
            <ScoreGauge
              score={analysis.score}
              title={tHome("scoreLabel")}
              label={tHome(`levels.${analysis.suggested_level}`)}
            />
            <div>
              <h3 className="mb-3 text-[.78rem] font-bold tracking-wide text-muted-2 uppercase">
                {tHome("signalsTitle")}
              </h3>
              <SignalList signals={analysis.signals} />
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
