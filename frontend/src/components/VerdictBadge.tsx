import { useTranslations } from "next-intl";
import type { Verdict } from "@/lib/api";

const STYLES: Record<Verdict, string> = {
  vrai: "bg-good-bg text-good",
  faux: "bg-bad-bg text-bad",
  trompeur: "bg-bad-bg text-bad",
  partiellement_vrai: "bg-warn-bg text-warn",
  non_verifiable: "bg-surface-alt text-muted",
};

export function VerdictBadge({ verdict }: { verdict: Verdict }) {
  const t = useTranslations("verdicts");
  return (
    <span
      className={`inline-flex items-center rounded-full px-4 py-1.5 text-[.78rem] font-bold uppercase tracking-wide ${STYLES[verdict]}`}
    >
      {t(verdict)}
    </span>
  );
}
