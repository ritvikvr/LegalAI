"use client";

import { api } from "@/lib/api";
import type { AxiosError } from "axios";
import { useState, type ChangeEvent } from "react";

type UploadResponse = {
  status: string;
  chunks: number;
  filename: string;
};

type AnalyzeResponse = {
  filename?: string;
  entities: string[];
  clause_type: string;
  risk: "Low" | "Medium" | "High" | string;
  risk_score: number;
  risk_reason: string;
  compliance: boolean;
  compliance_issues: string[];
  recommendations: string[];
  analyzed_chars?: number;
  total_chars?: number;
};

export default function UploadBox() {
  const [status, setStatus] = useState<string>("");
  const [uploadedFilename, setUploadedFilename] = useState<string>("");
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalyzeResponse | null>(null);

  const upload = async (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];
    if (!file) return;

    setStatus("Uploading...");
    setAnalysisResult(null);

    const form = new FormData();
    form.append("file", file);

    try {
      const response = await api.post<UploadResponse>("/upload/", form);
      setUploadedFilename(response.data.filename);
      setStatus(`Upload Successful: ${response.data.filename}`);
    } catch (err) {
      console.error(err);
      const axiosError = err as AxiosError<{ detail?: string }>;
      const detail = axiosError.response?.data?.detail;
      setStatus(detail ? `Upload Failed: ${detail}` : "Upload Failed");
    }
  };

  const analyzeUploadedFile = async () => {
    if (!uploadedFilename) return;
    setAnalyzing(true);
    try {
      const response = await api.post<AnalyzeResponse>("/analyze/file/", {
        filename: uploadedFilename,
      });
      setAnalysisResult(response.data);
      setStatus(`Analysis complete for ${uploadedFilename}`);
    } catch (err) {
      console.error(err);
      const axiosError = err as AxiosError<{ detail?: string }>;
      const detail = axiosError.response?.data?.detail;
      setStatus(detail ? `Analyze Failed: ${detail}` : "Analyze Failed");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload Contract</h2>
      <div className="form-group">
        <label htmlFor="file-upload">Select Document</label>
        <input
          id="file-upload"
          type="file"
          onChange={upload}
          accept=".pdf,.txt,.docx"
        />
      </div>

      {uploadedFilename && (
        <button onClick={analyzeUploadedFile} disabled={analyzing}>
          {analyzing ? "Analyzing file..." : "Analyze Uploaded File"}
        </button>
      )}

      {status && (
        <div
          style={{
            marginTop: "1rem",
            color: status.includes("Failed") ? "var(--danger)" : "var(--success)",
            fontWeight: 500,
            fontSize: "0.9rem",
          }}
        >
          {status}
        </div>
      )}

      {analysisResult && (
        <div className="result-section">
          <div className="result-item">
            <div className="result-label">Clause Type</div>
            <div className="result-value">{analysisResult.clause_type}</div>
          </div>

          <div className="result-item">
            <div className="result-label">Risk Level</div>
            <div className="result-value">
              <span className={`badge badge-risk-${analysisResult.risk.toLowerCase()}`}>
                {analysisResult.risk} ({analysisResult.risk_score}/100)
              </span>
            </div>
          </div>

          <div className="result-item">
            <div className="result-label">Entities</div>
            <div className="result-value" style={{ fontSize: "0.9rem" }}>
              {analysisResult.entities.length > 0
                ? analysisResult.entities.join(", ")
                : "None detected"}
            </div>
          </div>

          <div className="result-item">
            <div className="result-label">Compliance</div>
            <div
              className="result-value"
              style={{ color: analysisResult.compliance ? "var(--success)" : "var(--danger)" }}
            >
              {analysisResult.compliance ? "Compliant" : "Non-Compliant"}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
