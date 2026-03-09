"use client";
import UploadBox from "@/components/UploadBox";
import AnalyzeBox from "@/components/AnalyzeBox";

export default function Home() {
    return (
        <main className="container">
            <header>
                <h1>Legal AI</h1>
                <div className="subtitle">Advanced Contract Analysis & Risk Assessment</div>
            </header>

            <div className="grid">
                <UploadBox />
                <AnalyzeBox />
            </div>
        </main>
    );
}
