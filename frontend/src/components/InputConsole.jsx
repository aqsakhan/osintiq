import React, { useState } from "react";
import axios from "axios";
import { useAppContext } from "../context/useAppContext";

function InputConsole() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const {
    mode,
    setLastInsight,
    addChatMessage,
    lastInsight,
    setLoadingInsight,
    stopTyping,
    setStopTyping,
    loadingInsight,
    isRenderingInsight,
  } = useAppContext();

  const handleSubmit = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setStopTyping(false); // Reset stop on new submission

    try {
      if (mode === "analysis") {
        setLoadingInsight(true);

        const response = await axios.post(
          "http://localhost:5000/generate-insight",
          {
            input_text: input,
          }
        );

        setLastInsight(response.data.insight);
        setLoadingInsight(false);
      } else if (mode === "chat") {
        addChatMessage("user", input);

        const response = await axios.post("http://localhost:5000/ask-ai", {
          question: input,
          previous_context: lastInsight || "No context available",
        });

        addChatMessage("ai", response.data.insight);
      }
    } catch (error) {
      console.error("Error:", error);
      addChatMessage("ai", "⚠️ Something went wrong.");
    } finally {
      setInput("");
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleButtonClick();
    }
  };

  const handleButtonClick = () => {
    if (mode === "analysis") {
      if (isRenderingInsight && !stopTyping) {
        setStopTyping(true);
        return;
      }

      if (!loading && !loadingInsight) {
        handleSubmit();
      }
    } else if (mode === "chat") {
      if (!loading) {
        handleSubmit();
      }
    } else {
      console.error(`❌ Unrecognized mode: "${mode}" in InputConsole`);
    }
  };

  const getButtonLabel = () => {
    if (mode === "analysis") {
      if (isRenderingInsight && !stopTyping) return "⏹ Stop";
      if (isRenderingInsight && stopTyping) return "Stopping...";
      if (loadingInsight) return "Analyzing...";
      return "Go";
    } else if (mode === "chat") {
      return loading ? "Thinking..." : "Go";
    } else {
      return "Go";
    }
  };

  return (
    <div className="console-box">
      <input
        className="console-input"
        placeholder={
          mode === "analysis"
            ? "> Analyze IOC, CVE, Threat Actor..."
            : "> Ask a question..."
        }
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
      />
      <button
        className="analyze-button"
        onClick={handleButtonClick}
        disabled={mode === "chat" && loading}
      >
        {getButtonLabel()}
      </button>
    </div>
  );
}

export default InputConsole;
