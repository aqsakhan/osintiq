// src/components/ModeToggle.jsx
import React from "react";
import { useAppContext } from "../context/useAppContext";
import "../styles/ModeToggle.css";

function ModeToggle() {
  const { mode, setMode } = useAppContext();

  return (
    <div className="mode-toggle">
      <button
        className={mode === "analysis" ? "active" : ""}
        onClick={() => setMode("analysis")}
      >
        Analysis View
      </button>
      <button
        className={mode === "chat" ? "active" : ""}
        onClick={() => setMode("chat")}
      >
        AI Chat Mode
      </button>
    </div>
  );
}

export default ModeToggle;
