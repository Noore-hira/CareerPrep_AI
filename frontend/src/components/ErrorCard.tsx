import { motion } from "framer-motion";
import { RiErrorWarningLine, RiRefreshLine } from "react-icons/ri";

interface ErrorCardProps {
  message: string;
  onRetry?: () => void;
}

export function ErrorCard({ message, onRetry }: ErrorCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      className="rounded-2xl border border-red-500/20 bg-red-500/8 p-6 flex flex-col items-center gap-4 text-center max-w-md mx-auto"
    >
      <div className="w-12 h-12 rounded-full bg-red-500/15 flex items-center justify-center">
        <RiErrorWarningLine className="text-red-400 text-2xl" />
      </div>
      <div>
        <p className="font-semibold text-white mb-1">Something went wrong</p>
        <p className="text-sm text-slate-400">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-slate-300 hover:text-white transition-all duration-200"
        >
          <RiRefreshLine />
          Try again
        </button>
      )}
    </motion.div>
  );
}
