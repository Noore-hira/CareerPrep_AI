import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { RiCheckLine } from "react-icons/ri";
import { LOADING_STEPS } from "@/types";

export function LoadingSteps() {
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);

  useEffect(() => {
    const totalSteps = LOADING_STEPS.length;
    let step = 0;

    const advance = () => {
      if (step >= totalSteps) return;
      
      setCompletedSteps((prev) => {
        const next = [...prev, step];
        
        // ---> FIX: When Step 0 completes, instantly tick Step 1 ("Identifying Role") as well!
        if (step === 0 && !next.includes(1)) {
          next.push(1);
        }
        return next;
      });

      // Let the steps count naturally: 0, then 1, then 2, etc.
      step++;
      setCurrentStep(step);

      if (step < totalSteps) {
        // Dynamic reading delay: makes it feel like an actual AI thinking engine processing sections
        const delay = 1000 + Math.random() * 800;
        setTimeout(advance, delay);
      }
    };

    const initial = setTimeout(advance, 600);
    return () => clearTimeout(initial);
  }, []);

  return (
    <div className="flex flex-col gap-3 w-full max-w-sm">
      {LOADING_STEPS.map((step, i) => {
        const isDone = completedSteps.includes(i);
        
        // Active indicator states: 
        // If step is 1, it's sharing step 0's loader. Otherwise, match the current sequential step index counter.
        const isActive = currentStep === i || (i === 1 && currentStep === 0);

        return (
          <motion.div
            key={step}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: i <= currentStep || (i === 1 && currentStep >= 0) ? 1 : 0.25, x: 0 }}
            transition={{ delay: i * 0.08, duration: 0.3 }}
            className="flex items-center gap-3"
          >
            <div className="w-6 h-6 flex-shrink-0 flex items-center justify-center">
              {isDone ? (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 400, damping: 20 }}
                  className="w-5 h-5 rounded-full bg-violet-500 flex items-center justify-center"
                >
                  <RiCheckLine className="text-white text-xs" />
                </motion.div>
              ) : isActive ? (
                <div className="w-5 h-5 rounded-full border-2 border-violet-400 border-t-transparent animate-spin" />
              ) : (
                <div className="w-5 h-5 rounded-full border border-white/15" />
              )}
            </div>
            <AnimatePresence mode="wait">
              <span
                className={`text-sm transition-colors duration-300 ${
                  isDone
                    ? "text-violet-300"
                    : isActive
                    ? "text-white"
                    : "text-slate-600"
                }`}
              >
                {isDone ? "✔ " : ""}{step}
              </span>
            </AnimatePresence>
          </motion.div>
        );
      })}
    </div>
  );
}