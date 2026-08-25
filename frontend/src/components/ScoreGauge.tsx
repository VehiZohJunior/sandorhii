function scoreColor(score: number) {
  if (score > 70) return "#c62828";
  if (score > 50) return "#e65100";
  if (score > 30) return "#e6a700";
  return "#2e7d32";
}

export function ScoreGauge({
  score,
  title,
  label,
}: {
  score: number;
  title: string;
  label: string;
}) {
  const color = scoreColor(score);
  return (
    <div className="flex flex-wrap items-center gap-[22px]">
      <div
        className="flex h-[76px] w-[76px] flex-none items-center justify-center rounded-full border-[3px] text-[1.5rem] font-extrabold"
        style={{ borderColor: color, color }}
      >
        {score.toFixed(0)}%
      </div>
      <div>
        <strong className="text-heading">{title}</strong>
        <br />
        <small className="text-muted">{label}</small>
      </div>
    </div>
  );
}
