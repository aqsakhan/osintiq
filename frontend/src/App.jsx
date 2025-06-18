import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./styles.css";

function App() {
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState(null);
  const [displayedText, setDisplayedText] = useState("");
  const [loading, setLoading] = useState(false);
  const resultRef = useRef(null);

  const analyzeTopic = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setResult(null);
    setDisplayedText("");
    try {
      const response = await axios.post(
        "http://localhost:5000/generate-insight",
        {
          input_text: topic,
        }
      );
      setResult(response.data.insight || response.data);
    } catch (error) {
      console.error(error);
      setResult("❌ Error connecting to backend.");
    }
    setLoading(false);
  };

  useEffect(() => {
    if (typeof result === "string" && result.length > 0) {
      let index = 0;
      setDisplayedText("");
      const interval = setInterval(() => {
        setDisplayedText((prev) => {
          const next = prev + result.charAt(index);
          if (resultRef.current) {
            resultRef.current.scrollTop = resultRef.current.scrollHeight;
          }
          return next;
        });
        index++;
        if (index >= result.length) clearInterval(interval);
      }, 10);
      return () => clearInterval(interval);
    }
  }, [result]);

  // Parser (only for non-typewriter mode, fallback)
  const formatMarkdownToElements = (text) => {
    if (!text || typeof text !== "string") return null;
    const lines = text.split("\n");

    return lines.map((line, idx) => {
      if (/^\*\*(.*?)\*\*$/.test(line)) {
        return (
          <h3 key={idx} className="insight-heading">
            {line.replace(/\*\*/g, "")}
          </h3>
        );
      }
      if (/^### (.*)/.test(line)) {
        return (
          <h4 key={idx} className="insight-subheading">
            {line.replace(/^### /, "")}
          </h4>
        );
      }
      if (/^[-*] (.*)/.test(line)) {
        return (
          <li key={idx} className="insight-bullet">
            {line.replace(/^[-*] /, "")}
          </li>
        );
      }
      return (
        <p key={idx} className="insight-text">
          {line}
        </p>
      );
    });
  };

  return (
    <div className="app-container">
      <div className="title-wrapper">
        <h1 className="app-title">OSINTIQ: AI-Powered SOC Intelligence Hub</h1>
        <p className="app-subtitle">
          Open-source threat intelligence enriched by AI, built for SOC
          analysts.
        </p>
      </div>

      <div className="console-box">
        <input
          className="console-input"
          placeholder="> Analyze IOC, CVE, Threat Actor..."
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && analyzeTopic()}
        />
        <button
          className="analyze-button"
          onClick={analyzeTopic}
          disabled={loading || !topic.trim()}
        >
          {loading ? "Analyzing..." : "Run Analysis"}
        </button>
      </div>

      <div className="result-box" ref={resultRef}>
        {!result && !loading ? (
          <div className="insight-default-message">
            🛰️ Awaiting intelligence query... <br />
            <span className="insight-subtle">Feed me threat data!</span>
          </div>
        ) : loading ? (
          <div className="loading-lines">
            <div className="shimmer-line" />
            <div className="shimmer-line short" />
            <div className="shimmer-line" />
          </div>
        ) : (
          <div className="insight-output">
            {/* Show parsed elements only if typewriter isn't running */}
            {displayedText ? formatMarkdownToElements(displayedText) : null}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
