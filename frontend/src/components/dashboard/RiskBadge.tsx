"use client";

interface Props {
  label: string;
  level: string;
}

const LEVEL_CONFIG: Record<string, { color: string; bg: string }> = {
  LOW:      { color: "text-emerald-400", bg: "bg-emerald-500/10" },
  MEDIUM:   { color: "text-yellow-400",  bg: "bg-yellow-500/10" },
  HIGH:     { color: "text-orange-400",  bg: "bg-orange-500/10" },
  CRITICAL: { color: "text-red-400",     bg: "bg-red-500/10" },
};

export function RiskBadge({ label, level }: Props) {
  const config = LEVEL_CONFIG[level] || LEVEL_CONFIG.MEDIUM;
  return (
    <div className={`${config.bg} rounded-lg px-2.5 py-1.5 text-center`}>
      <div className="text-xs text-gray-500 mb-0.5 truncate">{label}</div>
      <div className={`text-xs font-bold ${config.color}`}>{level}</div>
    </div>
  );
}
