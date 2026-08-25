"use client";

import { useEffect, useState } from "react";
import { useTranslations } from "next-intl";

type Theme = "system" | "light" | "dark";

const ICONS: Record<Theme, React.ReactNode> = {
  system: (
    <svg viewBox="0 0 20 20" fill="none" className="h-4 w-4">
      <rect x="3" y="4" width="14" height="9" rx="1.5" stroke="currentColor" strokeWidth="1.4" />
      <path d="M7 16.5h6" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
    </svg>
  ),
  light: (
    <svg viewBox="0 0 20 20" fill="none" className="h-4 w-4">
      <circle cx="10" cy="10" r="3.5" stroke="currentColor" strokeWidth="1.4" />
      <path
        d="M10 2v2M10 16v2M18 10h-2M4 10H2M15.5 4.5l-1.4 1.4M5.9 14.1l-1.4 1.4M15.5 15.5l-1.4-1.4M5.9 5.9 4.5 4.5"
        stroke="currentColor"
        strokeWidth="1.4"
        strokeLinecap="round"
      />
    </svg>
  ),
  dark: (
    <svg viewBox="0 0 20 20" fill="none" className="h-4 w-4">
      <path
        d="M17 11.5A7 7 0 0 1 8.5 3a7 7 0 1 0 8.5 8.5Z"
        stroke="currentColor"
        strokeWidth="1.4"
        strokeLinejoin="round"
      />
    </svg>
  ),
};

function applyTheme(theme: Theme) {
  const root = document.documentElement;
  if (theme === "system") {
    root.removeAttribute("data-theme");
  } else {
    root.setAttribute("data-theme", theme);
  }
}

export function ThemeToggle() {
  const t = useTranslations("theme");
  const [theme, setTheme] = useState<Theme>("system");

  useEffect(() => {
    const stored = localStorage.getItem("sandorhii_theme") as Theme | null;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- lecture unique de
    // localStorage au montage : impossible cote serveur, donc pas de valeur initiale
    // fiable sans risquer un decalage d'hydratation.
    if (stored) setTheme(stored);
  }, []);

  function cycle() {
    const order: Theme[] = ["system", "light", "dark"];
    const next = order[(order.indexOf(theme) + 1) % order.length];
    setTheme(next);
    localStorage.setItem("sandorhii_theme", next);
    applyTheme(next);
  }

  const label = t("label", { theme: t(theme) });

  return (
    <button
      onClick={cycle}
      aria-label={label}
      title={label}
      className="flex h-8 w-8 items-center justify-center rounded-full border border-white/20 text-[#ccc] transition-colors hover:text-white"
    >
      {ICONS[theme]}
    </button>
  );
}
