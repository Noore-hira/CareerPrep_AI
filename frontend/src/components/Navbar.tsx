import { motion } from "framer-motion";
import { RiBrainLine, RiMenuLine } from "react-icons/ri";

interface NavbarProps {
  onLogoClick?: () => void;
  onOpenSidebar?: () => void;
}

export function Navbar({
  onLogoClick,
  onOpenSidebar,
}: NavbarProps) {
  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 border-b border-white/8 backdrop-blur-xl bg-[#080b14]/80"
    >
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenSidebar}
          className="p-2.5 rounded-xl hover:bg-white/10 transition-all duration-200"
          aria-label="Open Settings"
        >
          <RiMenuLine className="text-2xl text-white" />
        </button>

        <button
          onClick={onLogoClick}
          className="flex items-center gap-2.5 group cursor-pointer"
          aria-label="CareerPrep AI home"
        >
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-violet-500/30 group-hover:shadow-violet-500/50 transition-all duration-300">
            <RiBrainLine className="text-white text-lg" />
          </div>

          <span className="text-white font-semibold text-lg tracking-tight">
            CareerPrep <span className="text-violet-400">AI</span>
          </span>
        </button>
      </div>

      <div className="flex items-center gap-1">
        <a
          href="https://github.com/Noore-hira/CareerPrep_AI"
          target="_blank"
          rel="noopener noreferrer"
          className="px-3 py-1.5 text-sm text-slate-400 hover:text-white transition-colors duration-200 rounded-md hover:bg-white/5"
        >
          GitHub
        </a>
      </div>
    </motion.nav>
  );
}