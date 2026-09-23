import { getTranslations, setRequestLocale } from "next-intl/server";
import { AdminPanel } from "@/components/AdminPanel";

export default async function AdminPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("admin");

  return (
    <div className="mx-auto max-w-4xl px-5 py-12">
      <div className="flex flex-col gap-8">
        <h1 className="font-display text-3xl font-extrabold text-heading">{t("title")}</h1>
        <AdminPanel />
      </div>
    </div>
  );
}
