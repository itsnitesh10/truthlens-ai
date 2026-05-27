"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import {
  Search, Shield, Eye, Zap, FileText, Image, Video,
  ChevronRight, Activity, Brain
} from "lucide-react";

const features = [
  {
    icon: FileText,
    title: "Text Forensics",
    description: "Detect fake news, AI-generated content, propaganda patterns, and emotional manipulation in articles.",
    color: "text-blue-400",
    bg: "bg-blue-500/10",
    border: "border-blue-500/20",
  },
  {
    icon: Image,
    title: "Image Forensics",
    description: "ELA analysis, metadata inspection, GAN artifact detection, and face inconsistency detection.",
    color: "text-purple-400",
    bg: "bg-purple-500/10",
    border: "border-purple-500/20",
  },
  {
    icon: Video,
    title: "Video Deepfake Detection",
    description: "Blink pattern analysis, frame artifact detection, lip-sync mismatch, and face consistency.",
    color: "text-pink-400",
    bg: "bg-pink-500/10",
    border: "border-pink-500/20",
  },
  {
    icon: Brain,
    title: "Forensic Reasoning Engine",
    description: "Claude AI synthesizes all signals into an explainable verdict with evidence chain.",
    color: "text-indigo-400",
    bg: "bg-indigo-500/10",
    border: "border-indigo-500/20",
  },
  {
    icon: Activity,
    title: "Evidence Chain",
    description: "Track media evolution — from original upload to viral mutation across platforms.",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
    border: "border-emerald-500/20",
  },
  {
    icon: Shield,
    title: "Credibility Scoring",
    description: "Multi-dimensional 0-100 credibility score with risk levels and confidence metrics.",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
    border: "border-amber-500/20",
  },
];

const stats = [
  { label: "Analysis Modules", value: "5" },
  { label: "AI Models", value: "8+" },
  { label: "Detection Types", value: "15+" },
  { label: "Formats Supported", value: "Text / Image / Video" },
];

export default function HomePage() {
  return (
    <main className="min-h-screen" style={{ background: "var(--bg-primary)" }}>
      {/* Nav */}
      <nav className="border-b border-white/5 sticky top-0 z-50 backdrop-blur-md bg-black/30">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
              <Eye className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-lg text-white">TruthLens <span className="text-indigo-400">AI</span></span>
          </div>
          <div className="flex items-center gap-6">
            <Link href="/analyze" className="text-sm text-gray-400 hover:text-white transition-colors">
              Analyze
            </Link>
            <Link href="/about" className="text-sm text-gray-400 hover:text-white transition-colors">
              About
            </Link>
            <Link
              href="/analyze"
              className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm px-4 py-2 rounded-lg transition-colors font-medium"
            >
              Start Analysis
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-6 pt-24 pb-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 rounded-full px-4 py-1.5 text-indigo-400 text-sm mb-6">
            <Zap className="w-3.5 h-3.5" />
            Multi-Modal Misinformation Forensics
          </div>

          <h1 className="text-5xl md:text-7xl font-black text-white mb-6 leading-tight">
            Expose the Truth
            <br />
            <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              Behind Every Claim
            </span>
          </h1>

          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            AI-powered forensic investigation platform that analyzes text, images, and videos
            to detect misinformation, deepfakes, and manipulation — with full explainable reasoning.
          </p>

          <div className="flex items-center justify-center gap-4">
            <Link
              href="/analyze"
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all hover:scale-105 flex items-center gap-2"
            >
              <Search className="w-5 h-5" />
              Start Investigation
              <ChevronRight className="w-4 h-4" />
            </Link>
            <Link
              href="/about"
              className="border border-white/10 hover:border-white/20 text-gray-300 px-8 py-4 rounded-xl font-semibold text-lg transition-all"
            >
              How It Works
            </Link>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20"
        >
          {stats.map((stat) => (
            <div key={stat.label} className="glass-card p-5">
              <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
              <div className="text-sm text-gray-500">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-6 pb-24">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-white mb-3">Full Forensic Arsenal</h2>
          <p className="text-gray-500">Every module works together for a complete picture</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              className={`glass-card p-6 border ${feature.border} hover:scale-[1.02] transition-transform`}
            >
              <div className={`w-10 h-10 rounded-lg ${feature.bg} flex items-center justify-center mb-4`}>
                <feature.icon className={`w-5 h-5 ${feature.color}`} />
              </div>
              <h3 className="font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8 text-center text-gray-600 text-sm">
        TruthLens AI — Built for truth, powered by multi-modal forensics
      </footer>
    </main>
  );
}
