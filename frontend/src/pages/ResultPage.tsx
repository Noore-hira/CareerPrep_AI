import { useState, useRef } from "react";
import { motion } from "framer-motion";
import {
  RiDownloadLine,
  RiFileCopyLine,
  RiRefreshLine,
  RiSearchLine,
  RiCloseLine,
  RiCheckLine,
  RiBrainLine,
} from "react-icons/ri";
import { MarkdownRenderer } from "@/components/MarkdownRenderer";
import { TableOfContents } from "@/components/TableOfContents";
import { GeneratedGuide } from "@/types";
import { getPdfDownloadUrl } from "@/services/api";

interface ResultPageProps {
  guide: GeneratedGuide & {
    intro_response?: string;
    rcs_response?: string;
    rm_response?: string;
    iv_response?: string;
    pj_response?: string;
    response?: string;
    pdf_path?: string;
  };
  onReset: () => void;
}

export function ResultPage({ guide, onReset }: ResultPageProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const searchRef = useRef<HTMLInputElement>(null);

  // ---> FIX IS HERE: Join all separate parallel LangGraph nodes into one clean markdown text stream <---
  const displayContent = (() => {
    if (guide.content) return guide.content;
    if (guide.response && !guide.intro_response) return guide.response;

    // Collate the multi-node outputs into structural order
    const sections = [
      guide.intro_response,
      guide.rm_response,
      guide.rcs_response,
      guide.pj_response,
      guide.iv_response
    ].filter(Boolean); // Drop missing sections

    return sections.join("\n\n---\n\n");
  })();

  const targetPdfUrl = guide.pdfUrl || guide.pdf_path || "";

  const handleDownloadPdf = () => {
    if (!targetPdfUrl) return;
    const filename = targetPdfUrl.split("/").pop() ?? targetPdfUrl;
    const url = getPdfDownloadUrl(filename);
    window.open(url, "_blank");
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(displayContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const toggleSearch = () => {
    setSearchOpen((prev) => !prev);
    if (!searchOpen) {
      setTimeout(() => searchRef.current?.focus(), 100);
    } else {
      setSearchTerm("");
    }
  };

  return (
    <div className="min-h-screen bg-[#080b14] text-white">
      {/* Header */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="sticky top-0 z-50 flex items-center justify-between px-6 py-3 border-b border-white/8 backdrop-blur-xl bg-[#080b14]/90"
      >
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center flex-shrink-0">
            <RiBrainLine className="text-white text-sm" />
          </div>
          <div className="min-w-0">
            <p className="text-xs text-slate-500 leading-none mb-0.5">Career Guide</p>
            <h1 className="text-sm font-semibold text-white truncate">{guide.role || "AI Engineer"}</h1>
          </div>
        </div>

        <div className="flex items-center gap-2 flex-shrink-0">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleSearch}
            className={`p-2 rounded-lg border transition-all duration-200 ${
              searchOpen
                ? "border-violet-500/50 bg-violet-500/10 text-violet-400"
                : "border-white/10 bg-white/4 text-slate-400 hover:text-white hover:bg-white/8"
            }`}
          >
            <RiSearchLine className="text-sm" />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/10 bg-white/4 text-slate-400 hover:text-white hover:bg-white/8 transition-all duration-200 text-sm"
          >
            {copied ? <RiCheckLine className="text-green-400" /> : <RiFileCopyLine />}
            <span className="hidden sm:inline">{copied ? "Copied" : "Copy"}</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleDownloadPdf}
            disabled={!targetPdfUrl}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-violet-500/40 bg-violet-500/10 text-violet-300 hover:bg-violet-500/20 hover:text-violet-200 transition-all duration-200 text-sm disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <RiDownloadLine />
            <span className="hidden sm:inline">PDF</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onReset}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/10 bg-white/4 text-slate-400 hover:text-white hover:bg-white/8 transition-all duration-200 text-sm"
          >
            <RiRefreshLine />
            <span className="hidden sm:inline">New Guide</span>
          </motion.button>
        </div>
      </motion.header>

      {/* Search bar */}
      {searchOpen && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: "auto", opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          className="sticky top-[57px] z-40 px-6 py-2.5 bg-[#0d1117] border-b border-white/8 flex items-center gap-3"
        >
          <RiSearchLine className="text-slate-500 flex-shrink-0" />
          <input
            ref={searchRef}
            type="search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search in guide..."
            className="flex-1 bg-transparent text-white placeholder-slate-500 outline-none text-sm"
          />
          {searchTerm && (
            <button onClick={() => setSearchTerm("")} className="text-slate-500 hover:text-white transition-colors">
              <RiCloseLine />
            </button>
          )}
        </motion.div>
      )}

      {/* Main layout */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10 flex gap-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex-1 min-w-0"
        >
          {/* MarkdownRenderer will now cleanly interpret headings and content lists! */}
          <MarkdownRenderer content={displayContent} searchTerm={searchTerm || undefined} />
        </motion.div>

        <TableOfContents content={displayContent} />
      </div>
    </div>
  );
}