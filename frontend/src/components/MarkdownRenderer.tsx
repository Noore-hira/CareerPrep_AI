import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Components } from "react-markdown";

interface MarkdownRendererProps {
  content: string;
  searchTerm?: string;
}

function highlight(text: string, term: string): React.ReactNode {
  if (!term) return text;

  const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  return text.split(new RegExp(`(${escaped})`, "gi")).map((part, i) =>
    part.toLowerCase() === term.toLowerCase() ? (
      <mark
        key={i}
        className="bg-yellow-400/30 text-yellow-200 rounded px-1"
      >
        {part}
      </mark>
    ) : (
      part
    )
  );
}

function slugify(text: string) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .trim()
    .replace(/\s+/g, "-");
}

function buildComponents(searchTerm?: string): Components {
  const renderHeading = (children: React.ReactNode) => {
    const text = String(children ?? "");
    return {
      text,
      highlighted: searchTerm ? highlight(text, searchTerm) : text,
    };
  };

  return {
    h1({ children }) {
      const { text, highlighted } = renderHeading(children);

      return (
        <h1
          id={slugify(text)}
          className="text-4xl font-bold text-white mt-10 mb-5 border-b border-white/10 pb-3 scroll-mt-24"
        >
          {highlighted}
        </h1>
      );
    },

    h2({ children }) {
      const { text, highlighted } = renderHeading(children);

      return (
        <h2
          id={slugify(text)}
          className="text-2xl font-semibold text-white mt-8 mb-3 scroll-mt-24"
        >
          {highlighted}
        </h2>
      );
    },

    h3({ children }) {
      const { text, highlighted } = renderHeading(children);

      return (
        <h3
          id={slugify(text)}
          className="text-xl font-semibold text-slate-200 mt-6 mb-2 scroll-mt-24"
        >
          {highlighted}
        </h3>
      );
    },

    p({ children }) {
      return (
        <p className="leading-8 text-slate-300 mb-5">
          {children}
        </p>
      );
    },

    ul({ children }) {
      return (
        <ul className="list-disc pl-6 space-y-2 mb-5 text-slate-300">
          {children}
        </ul>
      );
    },

    ol({ children }) {
      return (
        <ol className="list-decimal pl-6 space-y-2 mb-5 text-slate-300">
          {children}
        </ol>
      );
    },

    li({ children }) {
      return <li>{children}</li>;
    },

    strong({ children }) {
      return <strong className="text-white font-semibold">{children}</strong>;
    },

    em({ children }) {
      return <em className="italic text-slate-200">{children}</em>;
    },

    blockquote({ children }) {
      return (
        <blockquote className="border-l-4 border-violet-500 pl-4 italic text-slate-400 my-5">
          {children}
        </blockquote>
      );
    },

    hr() {
      return <hr className="my-8 border-white/10" />;
    },

    pre({ children }) {
      return (
        <pre className="bg-[#0d1117] border border-white/10 rounded-xl p-4 overflow-x-auto my-5">
          {children}
        </pre>
      );
    },

    code({ className, children }) {
      const isBlock = className?.startsWith("language-");

      if (!isBlock) {
        return (
          <code className="px-1.5 py-0.5 rounded bg-white/10 text-violet-300">
            {children}
          </code>
        );
      }

      return (
        <code className={className}>
          {children}
        </code>
      );
    },

    table({ children }) {
      return (
        <div className="overflow-x-auto my-5">
          <table className="w-full border-collapse">
            {children}
          </table>
        </div>
      );
    },

    thead({ children }) {
      return <thead className="bg-white/5">{children}</thead>;
    },

    tr({ children }) {
      return (
        <tr className="border-b border-white/10">
          {children}
        </tr>
      );
    },

    th({ children }) {
      return (
        <th className="text-left p-3 font-semibold border border-white/10">
          {children}
        </th>
      );
    },

    td({ children }) {
      return (
        <td className="p-3 border border-white/10 text-slate-300">
          {children}
        </td>
      );
    },

    a({ href, children }) {
      return (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-violet-400 hover:text-violet-300 underline"
        >
          {children}
        </a>
      );
    },
  };
}

export function MarkdownRenderer({
  content,
  searchTerm,
}: MarkdownRendererProps) {
  return (
    <article className="prose prose-invert max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={buildComponents(searchTerm)}
      >
        {content}
      </ReactMarkdown>
    </article>
  );
}