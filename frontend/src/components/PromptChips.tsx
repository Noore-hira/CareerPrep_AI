import { motion } from "framer-motion";
import { PROMPT_CHIPS } from "@/types";

interface PromptChipsProps {
  onSelect: (chip: string) => void;
}

export function PromptChips({ onSelect }: PromptChipsProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5, duration: 0.4 }}
      className="flex flex-wrap gap-2 justify-center"
    >
      {PROMPT_CHIPS.map((chip, i) => (
        <motion.button
          key={chip}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6 + i * 0.06 }}
          whileHover={{ scale: 1.04, y: -1 }}
          whileTap={{ scale: 0.97 }}
          onClick={() => onSelect(chip)}
          className="px-3.5 py-1.5 text-sm rounded-full border border-white/10 bg-white/5 text-slate-300 hover:border-violet-400/50 hover:bg-violet-500/10 hover:text-violet-300 transition-all duration-200 cursor-pointer"
        >
          {chip}
        </motion.button>
      ))}
    </motion.div>
  );
}
