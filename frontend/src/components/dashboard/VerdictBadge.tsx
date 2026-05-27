"use client";

interface Props {
  verdict: string;
  large?: boolean;
}

const VERDICT_CONFIG: Record<string, { label: string; className: string }> = {
  VERIFIED:          { label: "✓ Verified",           className: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
  LIKELY_TRUE:       { label: "✓ Likely True",         className: "bg-green-500/20 text-green-400 border-green-500/30" },
  UNCERTAIN:         { label: "? Uncertain",            className: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30" },
  MISLEADING:        { label: "⚠ Misleading",           className: "bg-orange-500/20 text-orange-400 border-orange-500/30" },
  HIGHLY_MISLEADING: { label: "✗ Highly Misleading",   className: "bg-red-500/20 text-red-400 border-red-500/30" },
  FABRICATED:        { label: "✗ Fabricated",           className: "bg-red-900/40 text-red-300 border-red-600/40" },
};

export function VerdictBadge({ verdict, large }: Props) {
  const config = VERDICT_CONFIG[verdict] || {
    label: verdict,
    className: "bg-gray-500/20 text-gray-400 border-gray-500/30",
  };

  return (
    <span
      className={`border rounded-full font-semibold ${large ? "px-4 py-1.5 text-sm" : "px-2.5 py-0.5 text-xs"} ${config.className}`}
    >
      {config.label}
    </span>
  );
}
