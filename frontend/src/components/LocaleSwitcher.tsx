"use client";

import { useLocale } from "next-intl";
import { routing } from "@/i18n/routing";
import { usePathname, useRouter } from "@/i18n/navigation";

const LABELS: Record<string, string> = { fr: "FR", en: "EN" };

export function LocaleSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  return (
    <div className="flex items-center gap-1 rounded-full border border-white/20 bg-white/10 p-1">
      {routing.locales.map((loc) => (
        <button
          key={loc}
          onClick={() => router.replace(pathname, { locale: loc })}
          className={`rounded-full px-2.5 py-1 text-xs font-medium transition-colors ${
            loc === locale
              ? "bg-accent text-white"
              : "text-[#ccc] hover:text-white"
          }`}
          aria-current={loc === locale}
        >
          {LABELS[loc]}
        </button>
      ))}
    </div>
  );
}
