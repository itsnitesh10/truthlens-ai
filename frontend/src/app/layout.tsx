import type { Metadata } from "next";
import { Toaster } from "react-hot-toast";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "TruthLens AI — Misinformation Forensics",
  description: "Multi-modal AI forensics platform for detecting fake news, deepfakes, and manipulated media",
  keywords: ["fake news detection", "deepfake", "misinformation", "AI forensics", "fact check"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "#16161f",
              color: "#f1f1f5",
              border: "1px solid rgba(255,255,255,0.08)",
            },
          }}
        />
        {children}
      </body>
    </html>
  );
}
