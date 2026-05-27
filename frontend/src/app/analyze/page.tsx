"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useDropzone } from "react-dropzone";
import toast from "react-hot-toast";
import Link from "next/link";
import {
  FileText, Image, Video, Upload, X, Loader2,
  Eye, AlertTriangle, ChevronRight, Zap
} from "lucide-react";
import {
  analyzeText, analyzeImage, analyzeVideo, synthesizeReport,
  TextAnalysisResult, ImageAnalysisResult, VideoAnalysisResult, ForensicReport
} from "../../lib/api";
import { CredibilityMeter } from "../../components/dashboard/CredibilityMeter";
import { VerdictBadge } from "../../components/dashboard/VerdictBadge";
import { EvidenceChain } from "../../components/dashboard/EvidenceChain";
import { RiskBadge } from "../../components/dashboard/RiskBadge";

type Tab = "text" | "image" | "video";

export default function AnalyzePage() {
  const [activeTab, setActiveTab] = useState<Tab>("text");
  const [textInput, setTextInput] = useState("");
  const [urlInput, setUrlInput] = useState("");
  const [titleInput, setTitleInput] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  const [synthesizing, setSynthesizing] = useState(false);

  const [textResult, setTextResult] = useState<TextAnalysisResult | null>(null);
  const [imageResult, setImageResult] = useState<ImageAnalysisResult | null>(null);
  const [videoResult, setVideoResult] = useState<VideoAnalysisResult | null>(null);
  const [report, setReport] = useState<ForensicReport | null>(null);

  // ── Image dropzone ───────────────────────────────────────────────
  const onImageDrop = useCallback((files: File[]) => {
    if (files[0]) {
      setImageFile(files[0]);
      setImagePreview(URL.createObjectURL(files[0]));
    }
  }, []);

  const { getRootProps: getImageRootProps, getInputProps: getImageInputProps, isDragActive: isImageDragActive } =
    useDropzone({ onDrop: onImageDrop, accept: { "image/*": [] }, maxFiles: 1 });

  const { getRootProps: getVideoRootProps, getInputProps: getVideoInputProps, isDragActive: isVideoDragActive } =
    useDropzone({
      onDrop: (files: File[]) => files[0] && setVideoFile(files[0]),
      accept: { "video/*": [] },
      maxFiles: 1,
    });

  // ── Run analysis ─────────────────────────────────────────────────
  const handleAnalyze = async () => {
    setLoading(true);
    setReport(null);
    try {
      if (activeTab === "text") {
        if (!textInput.trim() || textInput.trim().length < 10) {
          toast.error("Please enter at least 10 characters of text");
          return;
        }
        const result = await analyzeText(textInput, urlInput || undefined, titleInput || undefined);
        setTextResult(result);
        toast.success("Text analysis complete");
      } else if (activeTab === "image") {
        if (!imageFile) { toast.error("Please upload an image"); return; }
        const result = await analyzeImage(imageFile);
        setImageResult(result);
        toast.success("Image analysis complete");
      } else if (activeTab === "video") {
        if (!videoFile) { toast.error("Please upload a video"); return; }
        toast.loading("Analyzing video frames...", { id: "video" });
        const result = await analyzeVideo(videoFile);
        setVideoResult(result);
        toast.dismiss("video");
        toast.success("Video analysis complete");
      }
    } catch (err: any) {
      toast.error(err.message || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  // ── Synthesize full report ────────────────────────────────────────
  const handleSynthesize = async () => {
    setSynthesizing(true);
    try {
      const r = await synthesizeReport({
        text_result: textResult,
        image_result: imageResult,
        video_result: videoResult,
        original_claim: textInput || undefined,
      });
      setReport(r);
      toast.success("Forensic report generated");
    } catch (err: any) {
      toast.error(err.message || "Report generation failed");
    } finally {
      setSynthesizing(false);
    }
  };

  const hasAnyResult = textResult || imageResult || videoResult;

  return (
    <div className="min-h-screen" style={{ background: "var(--bg-primary)" }}>
      {/* Nav */}
      <nav className="border-b border-white/5 sticky top-0 z-50 backdrop-blur-md bg-black/30">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
              <Eye className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-white">TruthLens <span className="text-indigo-400">AI</span></span>
          </Link>
          <span className="text-sm text-gray-500">Forensic Investigation Platform</span>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-10">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Forensic Analysis</h1>
          <p className="text-gray-500">Upload or paste content to begin multi-modal investigation</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* ── Left: Input Panel ────────────────────────────────── */}
          <div>
            {/* Tabs */}
            <div className="flex gap-2 mb-6">
              {([
                { id: "text", label: "Text", icon: FileText },
                { id: "image", label: "Image", icon: Image },
                { id: "video", label: "Video", icon: Video },
              ] as const).map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    activeTab === tab.id
                      ? "bg-indigo-600 text-white"
                      : "bg-white/5 text-gray-400 hover:text-white hover:bg-white/10"
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </div>

            <AnimatePresence mode="wait">
              {/* Text input */}
              {activeTab === "text" && (
                <motion.div
                  key="text"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 10 }}
                  className="space-y-4"
                >
                  <input
                    value={titleInput}
                    onChange={(e) => setTitleInput(e.target.value)}
                    placeholder="Article title (optional)"
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500 text-sm"
                  />
                  <input
                    value={urlInput}
                    onChange={(e) => setUrlInput(e.target.value)}
                    placeholder="Source URL (optional)"
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500 text-sm"
                  />
                  <textarea
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    placeholder="Paste article text, social post, or claim here..."
                    rows={10}
                    className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500 text-sm resize-none"
                  />
                  <div className="text-xs text-gray-600">{textInput.length} characters</div>
                </motion.div>
              )}

              {/* Image input */}
              {activeTab === "image" && (
                <motion.div
                  key="image"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 10 }}
                >
                  {!imageFile ? (
                    <div
                      {...getImageRootProps()}
                      className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
                        isImageDragActive
                          ? "border-indigo-500 bg-indigo-500/10"
                          : "border-white/10 hover:border-white/20 hover:bg-white/5"
                      }`}
                    >
                      <input {...getImageInputProps()} />
                      <Upload className="w-8 h-8 text-gray-600 mx-auto mb-3" />
                      <p className="text-gray-400 font-medium">Drop image here or click to browse</p>
                      <p className="text-gray-600 text-sm mt-1">JPG, PNG, WebP — max 20MB</p>
                    </div>
                  ) : (
                    <div className="relative">
                      <img src={imagePreview!} alt="Preview" className="w-full rounded-xl object-cover max-h-72" />
                      <button
                        onClick={() => { setImageFile(null); setImagePreview(null); }}
                        className="absolute top-2 right-2 bg-black/60 rounded-full p-1 hover:bg-red-600 transition-colors"
                      >
                        <X className="w-4 h-4 text-white" />
                      </button>
                      <div className="mt-2 text-xs text-gray-500">{imageFile.name} ({(imageFile.size / 1024 / 1024).toFixed(2)} MB)</div>
                    </div>
                  )}
                </motion.div>
              )}

              {/* Video input */}
              {activeTab === "video" && (
                <motion.div
                  key="video"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 10 }}
                >
                  {!videoFile ? (
                    <div
                      {...getVideoRootProps()}
                      className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
                        isVideoDragActive
                          ? "border-indigo-500 bg-indigo-500/10"
                          : "border-white/10 hover:border-white/20 hover:bg-white/5"
                      }`}
                    >
                      <input {...getVideoInputProps()} />
                      <Video className="w-8 h-8 text-gray-600 mx-auto mb-3" />
                      <p className="text-gray-400 font-medium">Drop video here or click to browse</p>
                      <p className="text-gray-600 text-sm mt-1">MP4, WebM, AVI — max 100MB</p>
                    </div>
                  ) : (
                    <div className="glass-card p-4 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-pink-500/20 rounded-lg flex items-center justify-center">
                          <Video className="w-5 h-5 text-pink-400" />
                        </div>
                        <div>
                          <p className="text-white text-sm font-medium">{videoFile.name}</p>
                          <p className="text-gray-500 text-xs">{(videoFile.size / 1024 / 1024).toFixed(2)} MB</p>
                        </div>
                      </div>
                      <button onClick={() => setVideoFile(null)} className="text-gray-500 hover:text-red-400 transition-colors">
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Analyze button */}
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full mt-5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white py-3.5 rounded-xl font-semibold transition-all flex items-center justify-center gap-2"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing...</>
              ) : (
                <><Zap className="w-4 h-4" /> Run Analysis</>
              )}
            </button>

            {/* Synthesize button */}
            {hasAnyResult && (
              <motion.button
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={handleSynthesize}
                disabled={synthesizing}
                className="w-full mt-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 disabled:opacity-50 text-white py-3.5 rounded-xl font-semibold transition-all flex items-center justify-center gap-2"
              >
                {synthesizing ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Generating Report...</>
                ) : (
                  <><AlertTriangle className="w-4 h-4" /> Generate Forensic Report</>
                )}
              </motion.button>
            )}
          </div>

          {/* ── Right: Results Panel ─────────────────────────────── */}
          <div className="space-y-4">
            <AnimatePresence>
              {/* Text result */}
              {textResult && (
                <motion.div
                  key="text-result"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="glass-card p-5 space-y-4"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-blue-400 text-sm font-medium">
                      <FileText className="w-4 h-4" />
                      Text Forensics
                    </div>
                    <VerdictBadge verdict={textResult.verdict} />
                  </div>
                  <CredibilityMeter score={textResult.credibility_score} />
                  <div className="grid grid-cols-3 gap-2">
                    <RiskBadge label="AI Generated" level={textResult.ai_generated_risk} />
                    <RiskBadge label="Propaganda" level={textResult.propaganda_risk} />
                    <RiskBadge label="Emotional Manip." level={textResult.emotional_manipulation ? "HIGH" : "LOW"} />
                  </div>
                  {textResult.manipulation_patterns.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-500 mb-2">Manipulation Patterns</p>
                      <div className="space-y-1">
                        {textResult.manipulation_patterns.map((p, i) => (
                          <div key={i} className="text-xs text-orange-400 bg-orange-500/10 rounded px-2 py-1">{p}</div>
                        ))}
                      </div>
                    </div>
                  )}
                  <p className="text-xs text-gray-400 italic leading-relaxed">{textResult.reasoning}</p>
                  <p className="text-xs text-gray-600">{textResult.processing_time_ms}ms</p>
                </motion.div>
              )}

              {/* Image result */}
              {imageResult && (
                <motion.div
                  key="image-result"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="glass-card p-5 space-y-4"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-purple-400 text-sm font-medium">
                      <Image className="w-4 h-4" />
                      Image Forensics
                    </div>
                    <VerdictBadge verdict={imageResult.verdict} />
                  </div>
                  <CredibilityMeter score={imageResult.credibility_score} />
                  <div className="grid grid-cols-2 gap-2">
                    <RiskBadge label="AI Generated" level={imageResult.ai_generated_risk} />
                    <RiskBadge label="Manipulation" level={imageResult.manipulation_detected ? "HIGH" : "LOW"} />
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500">ELA Score:</span>
                    <span className={`text-xs font-mono font-bold ${imageResult.ela_anomaly_score > 0.5 ? "text-red-400" : imageResult.ela_anomaly_score > 0.25 ? "text-yellow-400" : "text-green-400"}`}>
                      {imageResult.ela_anomaly_score.toFixed(3)}
                    </span>
                  </div>
                  {imageResult.metadata_issues.length > 0 && (
                    <div className="space-y-1">
                      {imageResult.metadata_issues.map((issue, i) => (
                        <div key={i} className="text-xs text-yellow-400 bg-yellow-500/10 rounded px-2 py-1">{issue}</div>
                      ))}
                    </div>
                  )}
                  <p className="text-xs text-gray-400 italic">{imageResult.reasoning}</p>
                </motion.div>
              )}

              {/* Video result */}
              {videoResult && (
                <motion.div
                  key="video-result"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="glass-card p-5 space-y-4"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-pink-400 text-sm font-medium">
                      <Video className="w-4 h-4" />
                      Video Forensics
                    </div>
                    <VerdictBadge verdict={videoResult.verdict} />
                  </div>
                  <CredibilityMeter score={videoResult.credibility_score} />
                  <RiskBadge label="Deepfake Risk" level={videoResult.deepfake_risk} />
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className={`rounded px-2 py-1.5 ${videoResult.blink_anomaly ? "bg-red-500/10 text-red-400" : "bg-green-500/10 text-green-400"}`}>
                      Blink: {videoResult.blink_anomaly ? "⚠ Abnormal" : "✓ Normal"}
                    </div>
                    <div className="bg-white/5 text-gray-400 rounded px-2 py-1.5">
                      Frames: {videoResult.frames_analyzed || "?"}
                    </div>
                  </div>
                  {videoResult.frame_artifacts.length > 0 && (
                    <div className="space-y-1">
                      {videoResult.frame_artifacts.map((a, i) => (
                        <div key={i} className="text-xs text-red-400 bg-red-500/10 rounded px-2 py-1">{a}</div>
                      ))}
                    </div>
                  )}
                  <p className="text-xs text-gray-400 italic">{videoResult.reasoning}</p>
                </motion.div>
              )}

              {/* Forensic report */}
              {report && (
                <motion.div
                  key="report"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="glass-card p-5 space-y-5 border border-indigo-500/30 glow-purple"
                >
                  <div className="flex items-center gap-2 text-indigo-400 font-semibold">
                    <AlertTriangle className="w-4 h-4" />
                    Forensic Report
                  </div>

                  <div className="flex items-center justify-between">
                    <VerdictBadge verdict={report.final_verdict} large />
                    <div className="text-right">
                      <div className="text-2xl font-bold text-white">{report.overall_credibility_score}<span className="text-gray-500 text-sm">/100</span></div>
                      <div className="text-xs text-gray-500">Overall Credibility</div>
                    </div>
                  </div>

                  <p className="text-sm text-gray-300 leading-relaxed italic bg-white/3 rounded-lg p-3">
                    {report.reasoning_narrative}
                  </p>

                  {report.key_findings.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-500 mb-2 uppercase tracking-wide">Key Findings</p>
                      <div className="space-y-1.5">
                        {report.key_findings.map((f, i) => (
                          <div key={i} className="flex items-start gap-2 text-xs text-gray-300">
                            <ChevronRight className="w-3 h-3 text-indigo-400 mt-0.5 shrink-0" />
                            {f}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {report.contradictions.length > 0 && (
                    <div>
                      <p className="text-xs text-red-400 mb-2 uppercase tracking-wide">Contradictions</p>
                      {report.contradictions.map((c, i) => (
                        <div key={i} className="text-xs text-red-300 bg-red-500/10 rounded px-2 py-1.5 mb-1">{c}</div>
                      ))}
                    </div>
                  )}

                  <EvidenceChain items={report.evidence_chain} />

                  {report.recommendations.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-500 mb-2 uppercase tracking-wide">Recommendations</p>
                      {report.recommendations.map((r, i) => (
                        <div key={i} className="text-xs text-emerald-400 bg-emerald-500/10 rounded px-2 py-1.5 mb-1">{r}</div>
                      ))}
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {!hasAnyResult && (
              <div className="glass-card p-10 text-center text-gray-600">
                <Eye className="w-10 h-10 mx-auto mb-3 opacity-30" />
                <p className="text-sm">Analysis results will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
