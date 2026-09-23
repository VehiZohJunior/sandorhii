"use client";

import { useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { api, ApiError, type Submission, type Verdict } from "@/lib/api";
import { ScoreGauge } from "@/components/ScoreGauge";
import { SignalList } from "@/components/SignalList";

const VERDICTS: Verdict[] = [
  "vrai",
  "faux",
  "partiellement_vrai",
  "non_verifiable",
  "trompeur",
];

export function AdminPanel() {
  const t = useTranslations("admin");
  const [password, setPassword] = useState<string | null>(null);
  const [passwordInput, setPasswordInput] = useState("");
  const [loginError, setLoginError] = useState<string | null>(null);
  const [queue, setQueue] = useState<Submission[]>([]);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("sandorhii_admin_password");
    // eslint-disable-next-line react-hooks/set-state-in-effect -- lecture unique de
    // sessionStorage au montage : impossible cote serveur, donc pas de valeur initiale
    // fiable sans risquer un decalage d'hydratation.
    if (stored) setPassword(stored);
  }, []);

  async function loadQueue(pwd: string) {
    try {
      const items = await api.getQueue(pwd);
      setQueue(items);
      setLoginError(null);
      setLoadError(null);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        setLoginError(t("wrongPassword"));
        setPassword(null);
        sessionStorage.removeItem("sandorhii_admin_password");
      } else {
        setLoadError(t("loadError"));
      }
    }
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- rechargement de la
    // file d'attente quand le mot de passe change (connexion) : cas normal de
    // synchronisation avec le backend, pas un anti-pattern.
    if (password) loadQueue(password);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [password]);

  function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    sessionStorage.setItem("sandorhii_admin_password", passwordInput);
    setPassword(passwordInput);
  }

  if (!password) {
    return (
      <form
        onSubmit={handleLogin}
        className="mx-auto flex w-full max-w-[360px] flex-col gap-3.5 rounded-2xl bg-ink p-10 text-center shadow-[0_10px_40px_rgba(0,0,0,.5)]"
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src="/logo-sandorhii.jpg"
          alt="SandorHii"
          className="mx-auto mb-1 w-[70px] rounded-md bg-white p-1"
        />
        <label className="text-[.8rem] text-[#999]">{t("passwordLabel")}</label>
        <input
          type="password"
          value={passwordInput}
          onChange={(e) => setPasswordInput(e.target.value)}
          placeholder={t("passwordPlaceholder")}
          className="rounded-lg border border-[#333] bg-[#222] px-3 py-3 text-center text-sm text-white tracking-wide outline-none focus:border-accent"
        />
        {loginError && <p className="text-[.85rem] text-[#ff6b6b]">{loginError}</p>}
        <button
          type="submit"
          className="rounded-lg bg-accent px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-accent-strong"
        >
          {t("login")}
        </button>
      </form>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <h2 className="font-display text-lg font-bold text-heading">
        {t("queueTitle", { count: queue.length })}
      </h2>
      {feedback && (
        <p className="rounded-lg bg-good-bg px-4 py-3 text-sm text-good">
          {feedback}
        </p>
      )}
      {loadError && (
        <p className="rounded-lg bg-warn-bg px-4 py-3 text-sm text-warn">
          {loadError}
        </p>
      )}
      {queue.length === 0 && !loadError ? (
        <p className="rounded-[14px] border border-border bg-surface p-6 text-sm text-muted">
          {t("queueEmpty")}
        </p>
      ) : (
        <ul className="flex flex-col gap-[18px]">
          {queue.map((submission) => (
            <QueueItem
              key={submission.id}
              submission={submission}
              password={password}
              onDone={(msg) => {
                setFeedback(msg);
                loadQueue(password);
              }}
            />
          ))}
        </ul>
      )}
    </div>
  );
}

function QueueItem({
  submission,
  password,
  onDone,
}: {
  submission: Submission;
  password: string;
  onDone: (message: string) => void;
}) {
  const t = useTranslations("admin");
  const tVerdicts = useTranslations("verdicts");
  const tLevels = useTranslations("home.levels");
  const [verdict, setVerdict] = useState<Verdict>("non_verifiable");
  const [resume, setResume] = useState("");
  const [auteur, setAuteur] = useState("");
  const [busy, setBusy] = useState(false);
  const analysis = submission.linguistic_analysis;

  async function handlePublish(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      await api.publish(submission.id, { verdict, resume, auteur }, password);
      onDone(t("publishSuccess"));
    } finally {
      setBusy(false);
    }
  }

  async function handleReject() {
    setBusy(true);
    try {
      await api.reject(submission.id, password);
      onDone(t("rejectSuccess"));
    } finally {
      setBusy(false);
    }
  }

  return (
    <li className="rounded-[14px] bg-surface p-[22px] shadow-[0_2px_10px_rgba(0,0,0,.06)]">
      <p className="whitespace-pre-wrap font-mono text-sm text-muted">
        &ldquo;{submission.raw_content}&rdquo;
      </p>

      {analysis && (
        <div className="mt-4 rounded-[10px] bg-surface-alt p-4">
          <p className="mb-3 text-sm font-medium text-heading">
            {t("linguisticScore", {
              score: analysis.score.toFixed(0),
              label: tLevels(analysis.suggested_level),
            })}
          </p>
          <ScoreGauge score={analysis.score} title="" label="" />
          <div className="mt-4">
            <SignalList signals={analysis.signals} />
          </div>
        </div>
      )}

      <form
        onSubmit={handlePublish}
        className="mt-[14px] flex flex-col gap-2.5 border-t border-border pt-[14px]"
      >
        <select
          value={verdict}
          onChange={(e) => setVerdict(e.target.value as Verdict)}
          className="rounded-lg border border-border bg-surface px-3 py-2 text-sm"
        >
          {VERDICTS.map((v) => (
            <option key={v} value={v}>
              {tVerdicts(v)}
            </option>
          ))}
        </select>

        <textarea
          value={resume}
          onChange={(e) => setResume(e.target.value)}
          placeholder={t("resumePlaceholder")}
          rows={3}
          required
          minLength={10}
          className="min-h-[60px] rounded-lg border border-border bg-surface px-3 py-2 text-sm outline-none focus:border-accent"
        />

        <input
          value={auteur}
          onChange={(e) => setAuteur(e.target.value)}
          placeholder={t("authorPlaceholder")}
          required
          minLength={2}
          className="rounded-lg border border-border bg-surface px-3 py-2 text-sm outline-none focus:border-accent"
        />

        <div className="flex gap-2.5">
          <button
            type="submit"
            disabled={busy}
            className="flex-1 rounded-lg bg-good px-4 py-2.5 text-sm font-bold text-white disabled:opacity-60"
          >
            {t("publish")}
          </button>
          <button
            type="button"
            onClick={handleReject}
            disabled={busy}
            className="flex-1 rounded-lg bg-accent px-4 py-2.5 text-sm font-bold text-white disabled:opacity-60"
          >
            {t("reject")}
          </button>
        </div>
      </form>
    </li>
  );
}
