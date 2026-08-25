import { getTranslations, setRequestLocale } from "next-intl/server";

const CONTACT_EMAIL = "zohjunior@gmail.com";

export default async function LegalPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("legal");

  const sections = [
    { title: t("whoTitle"), text: t("whoText", { email: CONTACT_EMAIL }) },
    { title: t("dataTitle"), text: t("dataText") },
    { title: t("useTitle"), text: t("useText") },
    { title: t("retentionTitle"), text: t("retentionText") },
    { title: t("neverTitle"), text: t("neverText") },
    { title: t("securityTitle"), text: t("securityText") },
    { title: t("dontSubmitTitle"), text: t("dontSubmitText") },
    { title: t("resultsTitle"), text: t("resultsText") },
    { title: t("changesTitle"), text: t("changesText") },
  ];

  return (
    <div className="mx-auto max-w-4xl px-5 py-12">
      <div className="flex flex-col gap-8">
        <div>
          <h1 className="text-3xl font-extrabold text-heading text-balance">
            {t("title")}
          </h1>
          <p className="mt-2 text-sm text-muted-2">{t("updated")}</p>
        </div>

        <div className="flex flex-col gap-6">
          {sections.map((section) => (
            <section
              key={section.title}
              className="rounded-[14px] border border-border bg-surface p-6"
            >
              <h2 className="text-base font-bold text-heading">
                {section.title}
              </h2>
              <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted">
                {section.text}
              </p>
            </section>
          ))}
        </div>
      </div>
    </div>
  );
}
