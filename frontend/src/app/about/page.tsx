"use client";

import Link from "next/link";
import { Eye, ArrowLeft } from "lucide-react";

const phases = [
  { num: 1, title: "Text Forensics + Dashboard", desc: "Fake news detection, AI text detection, propaganda analysis, credibility scoring", status: "ready" },
  { num: 2, title: "Image Manipulation Detection", desc: "ELA analysis, metadata forensics, GAN artifact detection, face inconsistency", status: "ready" },
  { num: 3, title: "Video Deepfake Detection", desc: "Frame analysis, blink patterns, face consistency, frame-level GAN artifacts", status: "ready" },
  { num: 4, title: "Forensic Reasoning Engine", desc: "Claude AI synthesizes all signals into explainable verdict with evidence chain", status: "ready" },
  { num: 5, title: "Social Tracking + Extension", desc: "Media evolution tracking, browser extension, real-time monitoring", status: "planned" },
];

export default function AboutPage() {
  return (
    <div className="min-h-screen" style={{ background: "var(--bg-primary)" }}>
      <nav className="border-b border-white/5 sticky top-0 z-50 backdrop-blur-md bg-black/30">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
              <Eye className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-white">TruthLens <span className="text-indigo-400">AI</span></span>
          </Link>
          <Link href="/" className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back
          </Link>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-16">
        <h1 className="text-4xl font-bold text-white mb-4">How TruthLens AI Works</h1>
        <p className="text-gray-400 text-lg mb-12">
          A multi-modal forensic platform that combines NLP, computer vision, deepfake detection, and Claude AI reasoning.
        </p>

        <h2 className="text-xl font-semibold text-white mb-6">Development Phases</h2>
        <div className="space-y-4 mb-16">
          {phases.map((p) => (
            <div key={p.num} className="glass-card p-5 flex items-start gap-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shrink-0 ${p.status === "ready" ? "bg-indigo-600 text-white" : "bg-white/5 text-gray-500"}`}>
                {p.num}
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold text-white">{p.title}</h3>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${p.status === "ready" ? "bg-emerald-500/20 text-emerald-400" : "bg-gray-500/20 text-gray-500"}`}>
                    {p.status === "ready" ? "✓ Implemented" : "Planned"}
                  </span>
                </div>
                <p className="text-sm text-gray-500">{p.desc}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="glass-card p-6 border border-indigo-500/20">
          <h2 className="font-semibold text-white mb-3">Tech Stack</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm text-gray-400">
            {["Next.js 14", "FastAPI", "Claude API", "RoBERTa", "OpenCV", "DeepFace", "Framer Motion", "Tailwind CSS"].map(t => (
              <div key={t} className="bg-white/5 rounded px-3 py-2 text-center">{t}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
