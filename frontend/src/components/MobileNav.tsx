"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { LocaleSwitcher } from "@/components/LocaleSwitcher";
import { ThemeToggle } from "@/components/ThemeToggle";

export function MobileNav() {
  const t = useTranslations("nav");
  const [open, setOpen] = useState(false);

  return (
    <div className="sm:hidden">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-label="Menu"
        className="flex h-9 w-9 flex-col items-center justify-center gap-1.5 rounded-full border border-white/20"
      >
        <span
          className={`h-0.5 w-4 bg-white transition-transform ${open ? "translate-y-2 rotate-45" : ""}`}
        />
        <span
          className={`h-0.5 w-4 bg-white transition-opacity ${open ? "opacity-0" : ""}`}
        />
        <span
          className={`h-0.5 w-4 bg-white transition-transform ${open ? "-translate-y-2 -rotate-45" : ""}`}
        />
      </button>

      {open && (
        <div className="absolute inset-x-0 top-full bg-ink px-5 py-4 shadow-md">
          <nav className="flex flex-col gap-3 text-sm">
            <Link
              href="/"
              onClick={() => setOpen(false)}
              className="text-[#ccc] hover:text-white"
            >
              {t("home")}
            </Link>
            <Link
              href="/fil"
              onClick={() => setOpen(false)}
              className="text-[#ccc] hover:text-white"
            >
              {t("feed")}
            </Link>
            <Link
              href="/admin"
              onClick={() => setOpen(false)}
              className="text-[#ccc] hover:text-white"
            >
              {t("admin")}
            </Link>
            <div className="flex items-center gap-2">
              <LocaleSwitcher />
              <ThemeToggle />
            </div>
          </nav>
        </div>
      )}
    </div>
  );
}
