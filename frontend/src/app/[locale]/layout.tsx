import type { Metadata } from "next";
import { NextIntlClientProvider, hasLocale } from "next-intl";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { notFound } from "next/navigation";
import { routing } from "@/i18n/routing";
import { Link } from "@/i18n/navigation";
import { LocaleSwitcher } from "@/components/LocaleSwitcher";
import { MobileNav } from "@/components/MobileNav";
import { ThemeToggle } from "@/components/ThemeToggle";
import "../globals.css";

// Applique le theme sauvegarde avant le premier rendu pour eviter un
// flash de la mauvaise palette (FOUC) au chargement.
const THEME_INIT_SCRIPT = `
try {
  var t = localStorage.getItem('sandorhii_theme');
  if (t === 'light' || t === 'dark') {
    document.documentElement.setAttribute('data-theme', t);
  }
} catch (e) {}
`;

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export async function generateMetadata(): Promise<Metadata> {
  const t = await getTranslations("brand");
  return {
    title: `${t("name")} — ${t("tagline")}`,
    description: t("metaDescription"),
  };
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!hasLocale(routing.locales, locale)) {
    notFound();
  }
  setRequestLocale(locale);
  const t = await getTranslations();

  return (
    <html lang={locale} suppressHydrationWarning className="h-full antialiased">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&display=swap"
        />
        <script dangerouslySetInnerHTML={{ __html: THEME_INIT_SCRIPT }} />
      </head>
      <body className="flex min-h-full flex-col font-body">
        <NextIntlClientProvider>
          <header className="relative bg-ink">
            <div className="mx-auto flex max-w-4xl items-center justify-between gap-4 px-6 py-4">
              <Link
                href="/"
                aria-label={t("brand.name")}
                className="flex items-center gap-3"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src="/logo-sandorhii.jpg"
                  alt={t("brand.name")}
                  className="h-11 w-auto rounded-md bg-white p-0.5"
                />
                <span className="font-display text-lg font-bold tracking-tight text-white sm:text-xl">
                  San<span className="text-accent-light">Dor</span>Hii
                </span>
              </Link>
              <nav className="hidden items-center gap-5 text-sm sm:flex">
                <Link
                  href="/"
                  className="text-[#ccc] transition-colors hover:text-white"
                >
                  {t("nav.home")}
                </Link>
                <Link
                  href="/fil"
                  className="text-[#ccc] transition-colors hover:text-white"
                >
                  {t("nav.feed")}
                </Link>
                <Link
                  href="/methodologie"
                  className="text-[#ccc] transition-colors hover:text-white"
                >
                  {t("methodology.navLabel")}
                </Link>
                <Link
                  href="/admin"
                  className="text-[#ccc] transition-colors hover:text-white"
                >
                  {t("nav.admin")}
                </Link>
                <LocaleSwitcher />
                <ThemeToggle />
              </nav>
              <MobileNav />
            </div>
          </header>
          <main className="flex-1">{children}</main>
          <footer className="flex flex-col items-center gap-2 px-5 py-7 text-center text-[13px] text-muted-2">
            <span>
              🔍 {t("brand.name")} — {t("brand.tagline")}
            </span>
            <Link
              href="/confidentialite"
              className="underline decoration-dotted underline-offset-2 hover:text-muted"
            >
              {t("legal.navLabel")}
            </Link>
          </footer>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
