import { useTranslations } from "next-intl";
import type { Verdict } from "@/lib/api";

const GRADIENTS: Record<Verdict, string> = {
  vrai: "linear-gradient(135deg, #1b5e20, #2e7d32)",
  faux: "linear-gradient(135deg, #7f0000, #c62828)",
  trompeur: "linear-gradient(135deg, #7f0000, #c62828)",
  partiellement_vrai: "linear-gradient(135deg, #8d5300, #e6a700)",
  non_verifiable: "linear-gradient(135deg, #37474f, #607d8b)",
};

const ICONS: Record<Verdict, string> = {
  vrai: "✅",
  faux: "❌",
  trompeur: "🚫",
  partiellement_vrai: "⚠️",
  non_verifiable: "❓",
};

export function VerdictCard({
  verdict,
  children,
}: {
  verdict: Verdict;
  children?: React.ReactNode;
}) {
  const t = useTranslations("verdicts");
  return (
    <div
      className="rounded-[18px] p-9 text-center text-white"
      style={{ background: GRADIENTS[verdict] }}
    >
      <div className="mb-3 text-[1.9rem] font-extrabold tracking-[1.5px]">
        {ICONS[verdict]} {t(verdict).toUpperCase()}
      </div>
      {children}
    </div>
  );
}
