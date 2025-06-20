// src/components/AIChatPanel.jsx
import React, { useEffect, useRef, useState } from "react";
import { useAppContext } from "../context/useAppContext";
import "../styles/AIChatPanel.css";
import ReactMarkdown from "react-markdown";

function AIChatPanel() {
  const { chatHistory } = useAppContext();
  const bottomRef = useRef(null);
  const [showTyping, setShowTyping] = useState(false);
  const [displayedMessages, setDisplayedMessages] = useState([]);

  useEffect(() => {
    setDisplayedMessages(chatHistory);
    console.log("🧠 Updated chat messages:", chatHistory);

    const lastMsg = chatHistory[chatHistory.length - 1];
    if (lastMsg?.role === "user") {
      setShowTyping(true);
      const timeout = setTimeout(() => setShowTyping(false), 1000);
      return () => clearTimeout(timeout);
    } else {
      setShowTyping(false);
    }
  }, [chatHistory]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [displayedMessages, showTyping]);

  return (
    <div className="chat-panel">
      <div className="chat-scroll-area">
        {displayedMessages.length === 0 ? (
          <p className="placeholder-text">
            Start a conversation with the AI assistant.
          </p>
        ) : (
          <>
            {displayedMessages.map((msg, idx) => (
              <div
                key={idx}
                className={`chat-bubble ${
                  msg.role === "user" ? "user" : "ai"
                } fade-in`}
              >
                {msg.role === "ai" ? (
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                ) : (
                  msg.content
                )}
              </div>
            ))}

            {showTyping && (
              <div className="chat-bubble ai typing-bubble fade-in">
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
              </div>
            )}

            <div ref={bottomRef} />
          </>
        )}
      </div>
    </div>
  );
}

export default AIChatPanel;
