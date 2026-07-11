import { useState } from "react";
import { AnimatePresence } from "framer-motion";

import { HomePage } from "@/pages/HomePage";
import { ResultPage } from "@/pages/ResultPage";
import { GeneratedGuide } from "@/types";

import SettingsSidebar from "@/components/SettingsSidebar";


function App() {

  const [guide, setGuide] =
    useState<GeneratedGuide | null>(null);


  const [sidebarOpen, setSidebarOpen] =
    useState(false);



  return (

    <>

      <SettingsSidebar

        open={sidebarOpen}

        onClose={() =>
          setSidebarOpen(false)
        }

      />



      <AnimatePresence mode="wait">


        {
          guide ? (


            <ResultPage

              key="result"

              guide={guide}

              onReset={() =>
                setGuide(null)
              }

            />


          ) : (


            <HomePage

              key="home"

              onGuideReady={(g)=>
                setGuide(g)
              }


              onOpenSidebar={()=>
                setSidebarOpen(true)
              }


            />


          )

        }


      </AnimatePresence>


    </>

  );

}


export default App;