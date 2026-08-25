import { setRequestLocale } from "next-intl/server";
import { SubmitForm } from "@/components/SubmitForm";
import { PillarsBand } from "@/components/PillarsBand";

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);

  return (
    <div>
      <section className="px-[6vw] pt-14 pb-10">
        <SubmitForm />
      </section>

      <div className="mx-auto max-w-4xl px-5 pt-4 pb-10">
        <PillarsBand />
      </div>
    </div>
  );
}
