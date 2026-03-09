"use client";

import { useState } from "react";

import { api } from "@/lib/api";

type AnalyzeResponse = {
  entities: string[];
  clause_type: string;
  risk: "Low" | "Medium" | "High" | string;
  risk_score: number;
  risk_reason: string;
  compliance: boolean;
  compliance_issues: string[];
  recommendations: string[];
};

export default function AnalyzeBox() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const analyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await api.post<AnalyzeResponse>("/analyze/", { text });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Analyze Clause</h2>
      <div className="form-group">
        <label htmlFor="clause-text">Paste Clause Text</label>
        <textarea
          id="clause-text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste legal text here..."
        />
      </div>
      <button onClick={analyze} disabled={loading || !text.trim()}>
        {loading ? "Analyzing..." : "Analyze Text"}
      </button>

      {result && (
        <div className="result-section">
          <div className="result-item">
            <div className="result-label">Clause Type</div>
            <div className="result-value">{result.clause_type}</div>
          </div>

          <div className="result-item">
            <div className="result-label">Risk Level</div>
            <div className="result-value">
              <span className={`badge badge-risk-${result.risk.toLowerCase()}`}>
                {result.risk} ({result.risk_score}/100)
              </span>
            </div>
            <div style={{ fontSize: "0.9rem", color: "#94a3b8", marginTop: "0.35rem" }}>
              {result.risk_reason}
            </div>
          </div>

          <div className="result-item">
            <div className="result-label">Entities</div>
            <div className="result-value" style={{ fontSize: "0.9rem" }}>
              {result.entities.length > 0 ? result.entities.join(", ") : "None detected"}
            </div>
          </div>

          <div className="result-item">
            <div className="result-label">Compliance</div>
            <div
              className="result-value"
              style={{
                color: result.compliance ? "var(--success)" : "var(--danger)",
              }}
            >
              {result.compliance ? "Compliant" : "Non-Compliant"}
            </div>
            {!result.compliance && result.compliance_issues.length > 0 && (
              <div style={{ marginTop: "0.5rem", fontSize: "0.9rem" }}>
                {result.compliance_issues.join("; ")}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
