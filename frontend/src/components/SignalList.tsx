import { useTranslations } from "next-intl";
import type { Signal } from "@/lib/api";

export function SignalList({ signals }: { signals: Signal[] }) {
  const t = useTranslations("home");
  const tCategories = useTranslations("home.categories");
  const tCatalog = useTranslations("home.signalCatalog");

  if (signals.length === 0) {
    return (
      <p className="rounded-lg border border-border bg-good-bg px-4 py-3 text-sm text-good">
        {t("noSignals")}
      </p>
    );
  }

  return (
    <ul className="flex flex-col gap-3">
      {signals.map((signal) => (
        <li
          key={signal.id}
          className="rounded-lg border border-border bg-surface p-4 shadow-sm"
        >
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <span className="rounded-full bg-accent-soft px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide text-accent-strong">
                {tCategories(signal.category as "sophisme" | "lexique")}
              </span>
              <span className="font-medium text-heading">
                {tCatalog(`${signal.id}.label`)}
              </span>
            </div>
            <span className="text-xs text-muted">
              {t("occurrences", { count: signal.occurrences })} ·{" "}
              {t("weightLabel")} {signal.weight.toFixed(1)}
            </span>
          </div>
          <p className="mt-2 text-sm text-muted">
            {tCatalog(`${signal.id}.explanation`)}
          </p>
          <p className="mt-2 rounded-md bg-surface-alt px-3 py-2 font-mono text-xs text-foreground">
            &ldquo;{signal.excerpt}&rdquo;
          </p>
        </li>
      ))}
    </ul>
  );
}
