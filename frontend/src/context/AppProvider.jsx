import React, { useState } from "react";
import { AppContext } from "./AppContext";

export function AppProvider({ children }) {
  const [mode, setMode] = useState("analysis");
  const [lastInsight, setLastInsight] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [loadingInsight, setLoadingInsight] = useState(false);
  const [stopTyping, setStopTyping] = useState(false);
  const [isRenderingInsight, setIsRenderingInsight] = useState(false);

  const addChatMessage = (role, content) => {
    setChatHistory((prev) => [...prev, { role, content }]);
  };

  return (
    <AppContext.Provider
      value={{
        mode,
        setMode,
        lastInsight,
        setLastInsight,
        chatHistory,
        setChatHistory,
        addChatMessage,
        loadingInsight,
        setLoadingInsight,
        stopTyping,
        setStopTyping,
        isRenderingInsight,
        setIsRenderingInsight,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}
