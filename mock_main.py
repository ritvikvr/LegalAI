from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Legal AI System (Lite Mode)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Legal AI Backend Running (Lite Mode)"}

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    # Simulate processing
    return {"status": "Indexed", "chunks": random.randint(5, 20)}

@app.post("/analyze/")
def analyze(text: str = ""):
    # Simulate analysis
    risks = ["Low", "Medium", "High"]
    compliance = [True, False]
    
    return {
        "entities": ["Company A", "Supplier B", "$50,000", "Termination Clause"],
        "clause_type": "Termination",
        "risk": random.choice(risks),
        "compliance": random.choice(compliance)
    }
