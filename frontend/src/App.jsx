import React from "react";
import "./styles/App.css";
import { AppProvider } from "./context/AppProvider";
import { useAppContext } from "./context/useAppContext";
import Sidebar from "./components/Sidebar";
import ModeToggle from "./components/ModeToggle";
import InsightPanel from "./components/InsightPanel";
import AIChatPanel from "./components/AIChatPanel";
import InputConsole from "./components/InputConsole";

function OSINTIQMain() {
  const { mode } = useAppContext();

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-panel">
        <div className="header-section">
          <div className="title-wrapper">
            <h1 className="app-title">
              OSINTIQ: AI-Powered SOC Intelligence Hub
            </h1>
            <p className="app-subtitle">
              Open-source threat intelligence enriched by AI, built for SOC
              analysts.
            </p>
          </div>
          <div className="toggle-wrapper">
            <ModeToggle />
          </div>
        </div>

        <div className="content-panel">
          <div
            className="mode-panel"
            style={{ display: mode === "analysis" ? "flex" : "none" }}
          >
            <InsightPanel />
          </div>
          <div
            className="mode-panel"
            style={{ display: mode === "chat" ? "flex" : "none" }}
          >
            <AIChatPanel />
          </div>
        </div>

        <InputConsole />
      </div>
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <OSINTIQMain />
    </AppProvider>
  );
}

export default App;
