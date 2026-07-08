import { useState } from "react";
import { AnimatePresence } from "framer-motion";

import { HomePage } from "@/pages/HomePage";
import { ResultPage } from "@/pages/ResultPage";
import { GeneratedGuide } from "@/types";

import SettingsSidebar from "@/components/SettingsSidebar";

function App() {
  const [guide, setGuide] = useState<GeneratedGuide | null>(null);

  // Sidebar state
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <>
      <SettingsSidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <AnimatePresence mode="wait">
        {guide ? (
          <ResultPage
            key="result"
            guide={guide}
            onReset={() => setGuide(null)}
          />
        ) : (
          <HomePage
            key="home"
            onGuideReady={(g) => setGuide(g)}

            // We'll use this in HomePage
            onOpenSidebar={() => setSidebarOpen(true)}
          />
        )}
      </AnimatePresence>
    </>
  );
}

export default App;
