import { useState, useCallback } from "react";
import { generateGuide } from "@/services/api";
import { GeneratedGuide } from "@/types";

type Status = "idle" | "loading" | "success" | "error";

interface UseGuideGenerationResult {
  status: Status;
  guide: GeneratedGuide | null;
  errorMessage: string | null;
  generate: (
    prompt: string,
    provider?: string, // Made optional with default tracking fallback
    model?: string,    // Made optional
    apiKey?: string    // Made optional
  ) => Promise<void>;
  reset: () => void;
}

export function useGuideGeneration(): UseGuideGenerationResult {
  const [status, setStatus] = useState<Status>("idle");
  const [guide, setGuide] = useState<GeneratedGuide | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const generate = useCallback(
    async (
      prompt: string,
      provider: string = "groq",
      model: string = "llama-3.3-70b-versatile", // Safe default option matching your backend logs
      apiKey: string = "" 
    ) => {
      setStatus("loading");
      setErrorMessage(null);
      setGuide(null);

      try {
        const result = await generateGuide({
          question: prompt,
          model: model,
          api_key: apiKey,
        });

        // Match your custom FastAPI response scheme mapping keys directly
        if (result.status === "success") {
          setGuide({
            role: result.role || "AI Engineer",
            content: result.response, // Binds backend string variable securely
            pdfUrl: result.pdf_path || "", 
          });

          setStatus("success");
        } else {
          setErrorMessage(result.message || "Failed to parse guide details.");
          setStatus("error");
        }
      } catch (err: unknown) {
        if (err instanceof Error) {
          if (err.message.toLowerCase().includes("timeout")) {
            setErrorMessage(
              "Request timed out. The AI is taking too long — please try again."
            );
          } else if (
            err.message.includes("Network Error") ||
            err.message.includes("ERR_NETWORK")
          ) {
            setErrorMessage(
              "Cannot connect to the backend. Make sure it's running at localhost:8000."
            );
          } else {
            setErrorMessage(err.message);
          }
        } else {
          setErrorMessage("An unexpected error occurred.");
        }

        setStatus("error");
      }
    },
    []
  );

  const reset = useCallback(() => {
    setStatus("idle");
    setGuide(null);
    setErrorMessage(null);
  }, []);

  return {
    status,
    guide,
    errorMessage,
    generate,
    reset,
  };
}