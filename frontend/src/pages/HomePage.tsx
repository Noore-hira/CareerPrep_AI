import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  RiSendPlaneLine,
  RiBrainLine,
  RiRocketLine,
  RiShieldLine,
  RiFileTextLine,
  RiMenuLine,
} from "react-icons/ri";
import { Navbar } from "@/components/Navbar";
import { PromptChips } from "@/components/PromptChips";
import { LoadingSteps } from "@/components/LoadingSteps";
import { ErrorCard } from "@/components/ErrorCard";
import { useGuideGeneration } from "@/hooks/useGuideGeneration";
import { GeneratedGuide } from "@/types";
import api from "@/lib/api"; // Added Axios backend routing engine

interface HomePageProps {
  onGuideReady: (guide: GeneratedGuide) => void;
  onOpenSidebar: () => void;
}

export function HomePage({
  onGuideReady,
  onOpenSidebar,
}: HomePageProps) {
    useEffect(() => {

    // Remove old keys saved by previous localStorage version
    localStorage.removeItem("groq_api_key");
    localStorage.removeItem("groq_model");

  }, []);
  const [prompt, setPrompt] = useState("");
  const [localLoading, setLocalLoading] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const [conversationalReply, setConversationalReply] = useState<string | null>(null);
  
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  // Combine internal hook loading state with local request state
  const isLoading = localLoading;

  const handleGenerate = async () => {

    if (!prompt.trim() || isLoading) return;


    setLocalLoading(true);
    setLocalError(null);
    setConversationalReply(null);



    try {

      const apiKey =
        sessionStorage.getItem("groq_api_key") || "";


      const model =
        sessionStorage.getItem("groq_model") ||
        "llama-3.3-70b-versatile";



      console.log(
        "Groq API Key:",
        apiKey
          ? apiKey.substring(0, 10) + "..."
          : "EMPTY"
      );


      if (!apiKey) {

        setLocalError(
          "Please add your Groq API Key from the sidebar before generating a guide."
        );

        return;

      }



      const response = await api.post(
        "/guide/generate",
        {

          question: prompt.trim(),

          api_key: apiKey,

          model: model,

        }
      );



      if (response.data?.status === "stopped") {


        setConversationalReply(
          response.data.response
        );


      } 


      else if (response.data?.status === "success") {



        const pdfUrl =
          response.data.pdf_path

          ? `${import.meta.env.VITE_API_URL}/guide/download/${response.data.pdf_path}`

          : "";



        onGuideReady({

          role:
            response.data.role ||
            "AI Engineer",


          content:
            response.data.response,


          pdfUrl,

        });



      } 


      else {


        setLocalError(
          response.data?.message ||
          "Guide generation failed."
        );


      }



    } 


    catch (err: any) {


      console.error(err);



      if (err.response) {


        const message =
          err.response.data?.detail ||
          err.response.data?.message ||
          err.response.data?.error ||
          "";



        if (
          message
            .toLowerCase()
            .includes("api key")
        ) {


          setLocalError(
            "⚠️ Invalid Groq API key."
          );


        } 

        else {


          setLocalError(
            message ||
            "An unexpected error occurred."
          );


        }


      } 


      else {


        setLocalError(
          "🚫 Cannot connect to backend."
        );


      }


    } 


    finally {


      setLocalLoading(false);


    }

  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      handleGenerate();
    }
  };

  const handleResetAll = () => {
    setConversationalReply(null);
    setLocalError(null);
    setPrompt("");
  };

  return (
    <div className="min-h-screen bg-[#080b14] text-white">
      <Navbar onOpenSidebar={onOpenSidebar} />
      <AnimatePresence mode="wait">
        {isLoading ? (
          <LoadingPage key="loading" />
        ) : (
          <motion.main
            key="home"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex flex-col items-center justify-center min-h-screen px-4 pt-20 pb-16"
          >
            {/* Gradient orbs */}
            <div className="fixed inset-0 pointer-events-none overflow-hidden">
              <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-violet-600/10 blur-[120px]" />
              <div className="absolute top-1/3 left-1/4 w-[400px] h-[400px] rounded-full bg-indigo-600/8 blur-[100px]" />
              <div className="absolute bottom-1/4 right-1/4 w-[300px] h-[300px] rounded-full bg-purple-600/8 blur-[80px]" />
            </div>

            <div className="relative z-10 flex flex-col items-center gap-8 w-full max-w-2xl">
              {/* Badge */}
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="flex items-center gap-2 px-4 py-1.5 rounded-full border border-violet-500/30 bg-violet-500/10 text-violet-300 text-sm"
              >
                <RiBrainLine />
                <span>AI-Powered Career Guidance</span>
              </motion.div>

              {/* Heading */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="text-center"
              >
                <h1 className="text-5xl md:text-6xl font-bold leading-tight tracking-tight">
                  Build Your{" "}
                  <span className="bg-gradient-to-r from-violet-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent">
                    Dream Career
                  </span>{" "}
                  with AI
                </h1>
                <p className="mt-4 text-lg text-slate-400 max-w-lg mx-auto leading-relaxed">
                  Generate complete career preparation guides using AI.{" "}
                  <span className="text-slate-500">Your AI Career Mentor.</span>
                </p>
              </motion.div>

              {/* Conversational Responses Block ("hello", jokes, etc.) */}
              {conversationalReply && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="w-full p-5 rounded-2xl border border-violet-500/20 bg-violet-950/20 backdrop-blur-md"
                >
                  <div className="flex items-start gap-3">
                    <RiBrainLine className="text-xl text-violet-400 mt-1 shrink-0" />
                    <div className="flex-1">
                      <h3 className="text-sm font-semibold text-violet-300 mb-2">Mentor Response</h3>
                      <p className="text-sm text-slate-300 whitespace-pre-line leading-relaxed">
                        {conversationalReply}
                      </p>
                      <button
                        onClick={handleResetAll}
                        className="mt-4 text-xs font-medium text-violet-400 hover:text-violet-300 transition-colors"
                      >
                        Clear message & ask another question
                      </button>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Error state */}
              {localError && (
                <motion.div
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="w-full"
                >
                  <ErrorCard
                    message={localError}
                    onRetry={handleResetAll}
                  />
                </motion.div>
              )}
              {/* Prompt input */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.35 }}
                className="w-full"
              >
                <div className="relative rounded-2xl border border-white/10 bg-white/4 backdrop-blur-sm focus-within:border-violet-500/50 focus-within:bg-white/6 transition-all duration-300 shadow-2xl shadow-black/40">
                  <textarea
                    ref={textareaRef}
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Generate a complete AI Engineer career guide..."
                    rows={4}
                    aria-label="Career guide prompt"
                    className="w-full bg-transparent text-white placeholder-slate-500 px-5 pt-4 pb-14 resize-none outline-none text-base leading-relaxed"
                  />
                  <div className="absolute bottom-3 right-3 flex items-center gap-2">
                    <span className="text-xs text-slate-600">⌘ + Enter</span>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleGenerate}
                      disabled={!prompt.trim() || isLoading}
                      aria-label="Generate guide"
                      className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white text-sm font-medium disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-200 shadow-lg shadow-violet-500/25"
                    >
                      <RiSendPlaneLine />
                      Generate
                    </motion.button>
                  </div>
                </div>
              </motion.div>

              {/* Prompt chips */}
              <PromptChips onSelect={setPrompt} />

              {/* Features */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
                className="flex flex-wrap justify-center gap-6 mt-4"
              >
                {[
                  { icon: RiRocketLine, label: "Roadmaps" },
                  { icon: RiShieldLine, label: "Interview Prep" },
                  { icon: RiFileTextLine, label: "Resume Tips" },
                ].map(({ icon: Icon, label }) => (
                  <div key={label} className="flex items-center gap-2 text-sm text-slate-500">
                    <Icon className="text-violet-500" />
                    {label}
                  </div>
                ))}
              </motion.div>
            </div>
          </motion.main>
        )}
      </AnimatePresence>
    </div>
  );
}

function LoadingPage() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-[#080b14] flex flex-col items-center justify-center gap-10 px-4"
    >
      {/* Animated gradient orb */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full bg-violet-600/15 blur-[100px] animate-pulse" />
      </div>

      {/* ---> FIXED: Added pt-24 here to push elements out from underneath the sticky navbar <--- */}
      <div className="relative z-10 flex flex-col items-center gap-8 pt-24">
        {/* Spinner logo */}
        <div className="relative">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center shadow-2xl shadow-violet-500/40">
            <RiBrainLine className="text-white text-3xl" />
          </div>
          <div className="absolute -inset-1.5 rounded-2xl border-2 border-violet-400/30 animate-ping" />
        </div>

        <div className="text-center">
          <h2 className="text-2xl font-semibold text-white mb-1">Generating your guide</h2>
          <p className="text-slate-500 text-sm">This usually takes 20–40 seconds</p>
        </div>

        <LoadingSteps />
      </div>
    </motion.div>
  );
}