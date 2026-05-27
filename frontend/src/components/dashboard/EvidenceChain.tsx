"use client";

interface EvidenceItem {
  type: string;
  description: string;
  confidence: number;
  source: string;
}

interface Props {
  items: EvidenceItem[];
}

const TYPE_COLORS: Record<string, string> = {
  text_analysis:     "bg-blue-500",
  text_manipulation: "bg-orange-500",
  image_analysis:    "bg-purple-500",
  image_metadata:    "bg-yellow-500",
  video_analysis:    "bg-pink-500",
  deepfake_indicator: "bg-red-500",
};

export function EvidenceChain({ items }: Props) {
  if (!items || items.length === 0) return null;

  return (
    <div>
      <p className="text-xs text-gray-500 mb-3 uppercase tracking-wide">Evidence Chain</p>
      <div className="relative">
        {/* Vertical line */}
        <div className="absolute left-2 top-0 bottom-0 w-px bg-white/5" />

        <div className="space-y-3">
          {items.map((item, i) => (
            <div key={i} className="flex gap-3 pl-6 relative">
              {/* Dot */}
              <div
                className={`absolute left-0 top-1.5 w-4 h-4 rounded-full ${TYPE_COLORS[item.type] || "bg-indigo-500"} flex items-center justify-center`}
              >
                <div className="w-1.5 h-1.5 rounded-full bg-white" />
              </div>

              <div className="flex-1 bg-white/3 rounded-lg p-2.5">
                <p className="text-xs text-gray-300">{item.description}</p>
                <div className="flex items-center gap-3 mt-1.5">
                  <span className="text-xs text-gray-600">{item.source}</span>
                  <div className="flex items-center gap-1">
                    <div className="h-1 w-12 bg-white/5 rounded-full">
                      <div
                        className="h-full bg-indigo-500 rounded-full"
                        style={{ width: `${Math.round(item.confidence * 100)}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-600">{Math.round(item.confidence * 100)}%</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
