from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

try:
    from . import analyze, upload
except ImportError:
    import analyze  # type: ignore
    import upload  # type: ignore

app = FastAPI(title="Legal AI System")

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:4000,http://localhost:8000",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload")
app.include_router(analyze.router, prefix="/analyze")

@app.get("/")
def root():
    return {"status": "Legal AI Backend Running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4000)
