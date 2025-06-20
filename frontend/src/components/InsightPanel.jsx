// src/components/InsightPanel.jsx
import React, { useEffect, useState, useRef } from "react";
import { useAppContext } from "../context/useAppContext";
import "../styles/InsightPanel.css";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function InsightPanel() {
  const { lastInsight, stopTyping, setStopTyping } = useAppContext();
  const scrollRef = useRef(null);

  return (
    <div className="insight-panel">
      {!lastInsight ? (
        <p className="placeholder-text">
          Run an OSINT analysis to view insights here.
        </p>
      ) : (
        <TypewriterMarkdown
          text={lastInsight}
          scrollRef={scrollRef}
          stopTyping={stopTyping}
          setStopTyping={setStopTyping}
        />
      )}
      <div ref={scrollRef} />
    </div>
  );
}

function TypewriterMarkdown({ text, scrollRef, stopTyping, setStopTyping }) {
  const [displayedText, setDisplayedText] = useState("");
  const [index, setIndex] = useState(0);
  const { setIsRenderingInsight } = useAppContext();
  const lastTypedRef = useRef("");

  useEffect(() => {
    if (text && text !== lastTypedRef.current) {
      lastTypedRef.current = text;
      setDisplayedText("");
      setIndex(0);
      setStopTyping(false);
      setIsRenderingInsight(true);
    }
  }, [text, setStopTyping, setIsRenderingInsight]);

  useEffect(() => {
    let timeoutId;

    if (stopTyping) {
      setIsRenderingInsight(false);
      return;
    }

    if (text && index < text.length) {
      timeoutId = setTimeout(() => {
        setDisplayedText((prev) => prev + text.charAt(index));
        setIndex((prev) => prev + 1);
        scrollRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 12);
    } else if (index >= text.length) {
      setIsRenderingInsight(false);
    }

    return () => clearTimeout(timeoutId);
  }, [index, text, stopTyping, scrollRef, setIsRenderingInsight]);

  return (
    <div className="typewriter-markdown">
      <ReactMarkdown
        children={displayedText}
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          code({ inline, className, children, ...props }) {
            return !inline ? (
              <SyntaxHighlighter
                style={oneDark}
                language={className?.replace("language-", "") || "json"}
                PreTag="div"
                {...props}
              >
                {String(children).replace(/\n$/, "")}
              </SyntaxHighlighter>
            ) : (
              <code className={className} {...props}>
                {children}
              </code>
            );
          },
        }}
      />
    </div>
  );
}

export default InsightPanel;
