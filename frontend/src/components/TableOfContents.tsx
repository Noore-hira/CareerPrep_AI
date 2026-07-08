import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { TocHeading } from "@/types";

interface TableOfContentsProps {
  content: string;
}

export function TableOfContents({ content }: TableOfContentsProps) {
  const [headings, setHeadings] = useState<TocHeading[]>([]);
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    const lines = content.split("\n");
    const found: TocHeading[] = [];

    for (const line of lines) {
      const match = line.match(/^(#{1,3})\s+(.+)/);
      if (match) {
        const level = match[1].length;
        const text = match[2].replace(/[*_`]/g, "").trim();
        const id = text
          .toLowerCase()
          .replace(/[^\w\s-]/g, "")
          .replace(/\s+/g, "-");
        found.push({ id, text, level });
      }
    }

    setHeadings(found);
  }, [content]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        }
      },
      { rootMargin: "-80px 0px -60% 0px" }
    );

    const elements = document.querySelectorAll("h1, h2, h3");
    elements.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, [headings]);

  const scrollToHeading = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      const offset = 100;
      const top = el.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: "smooth" });
    }
  };

  if (headings.length === 0) return null;

  return (
    <motion.aside
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.3, duration: 0.4 }}
      className="sticky top-24 hidden xl:block w-56 flex-shrink-0"
    >
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-3">
        On this page
      </p>
      <nav className="flex flex-col gap-0.5 max-h-[calc(100vh-160px)] overflow-y-auto pr-1">
        {headings.map((h) => (
          <button
            key={`${h.id}-${h.level}`}
            onClick={() => scrollToHeading(h.id)}
            className={`text-left text-sm py-1 px-2 rounded transition-all duration-150 cursor-pointer leading-snug ${
              h.level === 1 ? "pl-2" : h.level === 2 ? "pl-4" : "pl-6"
            } ${
              activeId === h.id
                ? "text-violet-400 bg-violet-500/10"
                : "text-slate-500 hover:text-slate-300 hover:bg-white/5"
            }`}
          >
            {h.text}
          </button>
        ))}
      </nav>
    </motion.aside>
  );
}
