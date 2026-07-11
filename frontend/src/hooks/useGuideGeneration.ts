import { useState, useCallback } from "react";
import { generateGuide } from "@/services/api";
import { GeneratedGuide, BACKEND_URL } from "@/types";


type Status =
  | "idle"
  | "loading"
  | "success"
  | "error";


interface UseGuideGenerationResult {

  status: Status;

  guide: GeneratedGuide | null;

  errorMessage: string | null;


  generate: (
    prompt: string,
    provider?: string,
    model?: string,
    apiKey?: string
  ) => Promise<void>;


  reset: () => void;

}



export function useGuideGeneration(): UseGuideGenerationResult {


  const [status, setStatus] =
    useState<Status>("idle");


  const [guide, setGuide] =
    useState<GeneratedGuide | null>(null);


  const [errorMessage, setErrorMessage] =
    useState<string | null>(null);



  const generate = useCallback(

    async (

      prompt: string,

      provider: string = "groq",

      model: string =
        "llama-3.3-70b-versatile",

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



        if (result.status === "success") {



          const pdfUrl = result.pdf_path

            ? `${BACKEND_URL}/guide/download/${result.pdf_path}`

            : "";



          setGuide({

            role:
              result.role ||
              "AI Engineer",


            content:
              result.response,


            pdfUrl,

          });



          setStatus("success");



        } else {


          setErrorMessage(
            result.message ||
            "Failed to generate guide."
          );


          setStatus("error");

        }



      } catch (err: unknown) {


        if (err instanceof Error) {


          if (
            err.message
              .toLowerCase()
              .includes("timeout")
          ) {


            setErrorMessage(
              "Request timed out. The AI is taking too long — please try again."
            );


          } else if (

            err.message.includes(
              "Network Error"
            )

            ||

            err.message.includes(
              "ERR_NETWORK"
            )

          ) {


            setErrorMessage(
              "Cannot connect to backend. Check API URL."
            );


          } else {


            setErrorMessage(
              err.message
            );

          }



        } else {


          setErrorMessage(
            "An unexpected error occurred."
          );


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