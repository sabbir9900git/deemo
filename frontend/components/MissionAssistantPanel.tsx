"use client";
import React, { useState } from "react";
import { askMissionAssistant } from "../services/api";

export default function MissionAssistantPanel() {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<Array<{ role: string; text: string }>>([
    {
      role: "assistant",
      text: "Welcome to the Grounded Mars Explorer Mission Assistant. Ask me about USGS Martian locations, MOLA terrain slopes, Odyssey GRS/SHARAD water-ice evidence, MSL RAD radiation doses, or Marswalk route planning.",
    },
  ]);

  const handleSend = async () => {
    if (!question.trim()) return;
    const q = question;
    setQuestion("");
    setHistory((prev) => [...prev, { role: "user", text: q }]);
    try {
      const res = await askMissionAssistant({ question: q });
      setHistory((prev) => [...prev, { role: "assistant", text: res.answer }]);
    } catch {
      setHistory((prev) => [
        ...prev,
        { role: "assistant", text: "Unable to reach backend assistant service." },
      ]);
    }
  };

  return (
    <div className="glass-panel rounded-xl p-5 space-y-4">
      <h3 className="text-lg font-bold text-white">Grounded AI Mission Assistant</h3>
      <div className="space-y-3 max-h-[380px] overflow-y-auto p-3 bg-slate-950/70 rounded-lg border border-slate-800 text-xs">
        {history.map((m, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg whitespace-pre-wrap ${
              m.role === "user"
                ? "bg-mars-600/30 border border-mars-500/40 text-white ml-8"
                : "bg-slate-900 border border-slate-800 text-slate-200 mr-8"
            }`}
          >
            {m.text}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about Olympus Mons, Jezero Crater, water-ice evidence, or radiation..."
          className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white"
        />
        <button
          onClick={handleSend}
          className="bg-mars-500 hover:bg-mars-600 text-white font-semibold px-4 py-2 rounded-lg text-xs"
        >
          Transmit Query
        </button>
      </div>
    </div>
  );
}
