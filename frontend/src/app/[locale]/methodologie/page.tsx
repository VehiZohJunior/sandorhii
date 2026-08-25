import { getTranslations, setRequestLocale } from "next-intl/server";

const SIGNAL_GROUPS: { category: "sophisme" | "lexique" | "attribution"; ids: string[] }[] = [
  {
    category: "sophisme",
    ids: [
      "faux_dilemme",
      "pente_glissante",
      "generalisation_abusive",
      "ad_hominem",
      "autorite_vague",
      "complot",
      "detournement_whataboutism",
      "homme_de_paille",
    ],
  },
  {
    category: "lexique",
    ids: [
      "urgence_partage",
      "urgence_lexicale",
      "superlatifs",
      "mots_choc",
      "appel_emotion_peur",
      "metaphore_guerriere",
      "majuscules_excessives",
      "ponctuation_excessive",
      "repetition_suspecte",
    ],
  },
  {
    category: "attribution",
    ids: ["attribution_non_identifiee"],
  },
];

export default async function MethodologyPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("methodology");
  const tCategories = await getTranslations("home.categories");
  const tCatalog = await getTranslations("home.signalCatalog");

  const steps = [
    { title: t("step1Title"), text: t("step1Text") },
    { title: t("step2Title"), text: t("step2Text") },
    { title: t("step3Title"), text: t("step3Text") },
    { title: t("step4Title"), text: t("step4Text") },
  ];

  return (
    <div className="mx-auto max-w-4xl px-5 py-12">
      <div className="flex flex-col gap-10">
        <div>
          <h1 className="text-3xl font-extrabold text-heading text-balance">
            {t("title")}
          </h1>
          <p className="mt-3 max-w-2xl text-[.95rem] leading-relaxed text-muted">
            {t("intro")}
          </p>
        </div>

        <section className="flex flex-col gap-4">
          <h2 className="text-lg font-bold text-heading">{t("stepsTitle")}</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {steps.map((step) => (
              <div
                key={step.title}
                className="rounded-[14px] border border-border bg-surface p-5"
              >
                <h3 className="text-sm font-bold text-accent-strong">
                  {step.title}
                </h3>
                <p className="mt-1.5 text-sm leading-relaxed text-muted">
                  {step.text}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="flex flex-col gap-4">
          <div>
            <h2 className="text-lg font-bold text-heading">
              {t("pillarTitle")}
            </h2>
            <p className="mt-1.5 max-w-2xl text-sm leading-relaxed text-muted">
              {t("pillarIntro")}
            </p>
          </div>

          <div className="flex flex-col gap-6">
            {SIGNAL_GROUPS.map((group) => (
              <div key={group.category}>
                <span className="inline-block rounded-full bg-accent-soft px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-accent-strong">
                  {tCategories(group.category)}
                </span>
                <ul className="mt-3 grid gap-3 sm:grid-cols-2">
                  {group.ids.map((id) => (
                    <li
                      key={id}
                      className="rounded-[12px] border border-border bg-surface p-4"
                    >
                      <p className="text-sm font-semibold text-heading">
                        {tCatalog(`${id}.label`)}
                      </p>
                      <p className="mt-1 text-[.85rem] leading-relaxed text-muted">
                        {tCatalog(`${id}.explanation`)}
                      </p>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-[14px] border border-warn/30 bg-warn-bg p-6">
          <h2 className="text-base font-bold text-heading">
            {t("limitsTitle")}
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted">
            {t("limitsText")}
          </p>
        </section>
      </div>
    </div>
  );
}
