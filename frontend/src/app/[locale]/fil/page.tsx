import { getTranslations, setRequestLocale } from "next-intl/server";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { VerdictBadge } from "@/components/VerdictBadge";

export default async function FeedPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("feed");
  const items = await api.getFeed().catch(() => []);

  return (
    <div className="mx-auto max-w-4xl px-5 py-12">
      <div className="flex flex-col gap-8">
        <div>
          <h1 className="text-3xl font-extrabold text-heading text-balance">
            {t("title")}
          </h1>
          <p className="mt-3 max-w-2xl text-muted">{t("subtitle")}</p>
        </div>

        {items.length === 0 ? (
          <p className="rounded-[16px] border border-border bg-surface p-6 text-sm text-muted">
            {t("empty")}
          </p>
        ) : (
          <ul className="flex flex-col gap-4">
            {items.map((item) => (
              <li
                key={item.submission_id}
                className="rounded-[16px] border border-border bg-surface p-5 shadow-[0_2px_10px_rgba(0,0,0,.04)]"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <VerdictBadge verdict={item.verdict} />
                  {item.published_at && (
                    <span className="text-xs text-muted-2">
                      {t("publishedOn", {
                        date: new Date(item.published_at).toLocaleDateString(
                          locale
                        ),
                      })}
                    </span>
                  )}
                </div>
                <p className="mt-3 font-mono text-sm text-muted">
                  &ldquo;{item.extrait}&rdquo;
                </p>
                <p className="mt-3 text-sm text-foreground">{item.resume}</p>
                <Link
                  href={`/fil/${item.submission_id}`}
                  className="mt-3 inline-block text-sm font-bold text-accent hover:text-accent-strong"
                >
                  {t("readMore")} →
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
