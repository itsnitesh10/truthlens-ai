"use client";

interface Props {
  score: number;
}

export function CredibilityMeter({ score }: Props) {
  const color =
    score >= 70 ? "#10b981" :
    score >= 45 ? "#f59e0b" :
    score >= 25 ? "#f97316" :
    "#ef4444";

  const label =
    score >= 70 ? "Credible" :
    score >= 45 ? "Uncertain" :
    score >= 25 ? "Suspicious" :
    "Not Credible";

  return (
    <div>
      <div className="flex justify-between items-center mb-1.5">
        <span className="text-xs text-gray-500">Credibility Score</span>
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium" style={{ color }}>{label}</span>
          <span className="text-sm font-bold text-white">{score}<span className="text-gray-600">/100</span></span>
        </div>
      </div>
      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${score}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}
