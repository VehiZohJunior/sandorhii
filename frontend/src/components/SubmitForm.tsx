"use client";

import { useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { api, ApiError, type Submission } from "@/lib/api";
import { ScoreGauge } from "@/components/ScoreGauge";
import { SignalList } from "@/components/SignalList";
import { PulseDots } from "@/components/PulseDots";

export function SubmitForm() {
  const t = useTranslations("home");
  const tBrand = useTranslations("brand");
  const locale = useLocale();
  const [texte, setTexte] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Submission | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (texte.trim().length < 20) {
      setError(t("minLength"));
      return;
    }
    setLoading(true);
    try {
      const submission = await api.submitText(texte, locale);
      setResult(submission);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("error"));
    } finally {
      setLoading(false);
    }
  }

  const analysis = result?.linguistic_analysis;

  return (
    <>
      <div className="relative mx-auto -mt-20 max-w-[480px] rounded-[28px] border border-white/10 bg-surface px-[7vw] py-10 text-center shadow-[0_30px_70px_rgba(6,17,33,.35)]">
        <div className="mx-auto mb-5 h-[168px] w-[168px] overflow-hidden rounded-full shadow-[0_4px_14px_rgba(15,42,77,.18)]">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/avatar-inspecteur.png"
            alt={tBrand("name")}
            className="h-full w-full scale-[1.06] object-cover"
          />
        </div>
        <h1 className="text-2xl font-extrabold text-[#4F46E5] text-balance">
          {t("title")}
        </h1>
        <p className="mx-auto mt-2 max-w-sm text-xl font-extrabold text-heading text-balance">
          {t("subtitle")}
        </p>

        <form onSubmit={handleSubmit} className="mt-7 flex flex-col gap-1 text-left">
          <textarea
            value={texte}
            onChange={(e) => setTexte(e.target.value)}
            placeholder={t("placeholder")}
            rows={6}
            className="w-full resize-none rounded-[14px] border-2 border-accent/40 p-[18px] text-[1rem] text-foreground outline-none transition-shadow placeholder:text-muted-2 focus:border-accent focus:shadow-[0_0_0_4px_rgba(46,109,164,.1)]"
          />
          <div
            className={`text-right text-[.78rem] ${texte.length >= 3000 ? "text-accent" : "text-muted-2"}`}
          >
            {texte.length} / 3000
          </div>
          {error && <p className="mb-2 text-sm text-bad">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="mt-1 flex w-full items-center justify-center gap-2 rounded-[14px] bg-[#4F46E5] px-[30px] py-4 text-[1.05rem] font-bold tracking-[.4px] text-white transition-all hover:not-disabled:-translate-y-px hover:not-disabled:bg-[#4338CA] hover:not-disabled:shadow-[0_8px_20px_rgba(79,70,229,.32)] disabled:cursor-not-allowed disabled:bg-[#4F46E5]/50"
          >
            {loading && <PulseDots />}
            🚀 {loading ? t("submitting") : t("submit")}
          </button>

          <div className="mt-6 border-t border-border pt-4 text-center text-[.8rem] text-muted-2">
            {t("footerTag")}
          </div>
          <div className="mt-3 rounded-xl bg-surface-alt px-4 py-3 text-left text-[.74rem] text-muted">
            {t("disclaimer")}
          </div>
        </form>
      </div>

      {analysis && (
        <div className="mx-auto max-w-[880px] px-5 pt-12">
          <section className="flex flex-col gap-5 rounded-[18px] border border-border bg-surface p-7">
            <h2 className="text-xl font-bold text-heading">
              {t("resultTitle")}
            </h2>
            <p className="rounded-lg bg-accent-soft px-4 py-3 text-sm text-accent-strong">
              {t("resultNote")}
            </p>
            {!analysis.language_supported && (
              <p className="rounded-lg bg-warn-bg px-4 py-3 text-sm text-warn">
                {t("langUnsupported")}
              </p>
            )}
            <ScoreGauge
              score={analysis.score}
              title={t("scoreLabel")}
              label={t(`levels.${analysis.suggested_level}`)}
            />
            <div>
              <h3 className="mb-3 text-[.78rem] font-bold tracking-wide text-muted-2 uppercase">
                {t("signalsTitle")}
              </h3>
              <SignalList signals={analysis.signals} />
            </div>
          </section>
        </div>
      )}
    </>
  );
}
