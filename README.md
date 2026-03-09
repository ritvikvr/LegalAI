# LegalAI - Intelligent Legal Document Analysis System

A comprehensive AI-powered platform for analyzing, extracting, and understanding legal documents. LegalAI leverages advanced natural language processing and machine learning to identify critical clauses, assess legal risks, detect compliance issues, and extract key entities from legal contracts and agreements.

## 🚀 Features

### Document Processing
- **OCR Support**: Extract text from scanned PDF documents and images using Tesseract OCR
- **Text Extraction**: Automatic text extraction and preprocessing for various document formats
- **Chunking**: Intelligent document chunking for optimized analysis of large documents

### Legal Analysis
- **Clause Classification**: Automatically classify and identify different types of legal clauses
- **Risk Scoring**: AI-powered risk assessment for clauses with severity scoring
- **Compliance Checking**: Verify documents against compliance standards and regulations
- **Entity Extraction**: Extract key entities such as parties, dates, amounts, and obligations
- **Missing Clause Detection**: Identify missing clauses that should be present in specific document types

### Technology Stack
- **Backend**: FastAPI with Python for high-performance REST APIs
- **Frontend**: Next.js with React and TypeScript for modern UI
- **AI/ML**: 
  - LangChain for LLM orchestration
  - Sentence Transformers for semantic embeddings
  - Spacy for advanced NLP tasks
  - Transformers library for state-of-the-art NLP models
- **Vector Database**: FAISS for efficient semantic search and similarity matching
- **PDF Processing**: pdfplumber and python-docx for document parsing
- **OCR**: Pytesseract for optical character recognition

## 📋 Project Structure

```
LegalAI/
├── Frontend (Next.js/React)
│   ├── AnalyzeBox.tsx          # Document analysis UI component
│   ├── UploadBox.tsx           # File upload component
│   ├── page.tsx                # Main page component
│   ├── layout.tsx              # Application layout
│   └── api.ts                  # Frontend API client
│
├── Backend (FastAPI/Python)
│   ├── main.py                 # FastAPI application entry point
│   ├── analyze.py              # Document analysis router and endpoints
│   ├── upload.py               # Document upload and management
│   │
│   ├── Core Analysis Modules
│   ├── clause_classifier.py    # Classify legal clauses
│   ├── clause_risk_scorer.py   # Risk assessment for clauses
│   ├── compliance_checker.py   # Compliance validation
│   ├── entity_extraction.py    # Extract key information
│   ├── missing_clause_detector.py # Detect missing clauses
│   │
│   ├── Infrastructure
│   ├── chunker.py              # Document chunking logic
│   ├── embedding_service.py    # Embedding generation
│   ├── vector_store.py         # Vector database management
│   ├── ocr_services.py         # OCR processing
│   └── api.ts                  # API route definitions
│
├── Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── package.json            # Node.js dependencies
│   ├── tsconfig.json           # TypeScript configuration
│   └── .env                    # Environment variables
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- pip and npm
- Tesseract OCR (for OCR support)

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/ritvikvr/LegalAI.git
cd LegalAI
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

## 🚀 Running the Application

### Start the Backend Server
```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 4000 --reload
```

The backend API will be available at `http://localhost:4000`

### Start the Frontend Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📚 Dependencies

### Python Dependencies
- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **langchain**: Framework for LLM application development
- **langchain-openai**: OpenAI integration for LangChain
- **sentence-transformers**: For semantic embeddings
- **spacy**: Advanced NLP library
- **spacy-transformers**: Transformers integration for Spacy
- **faiss-cpu**: Vector database for similarity search
- **pdfplumber**: PDF text extraction
- **python-docx**: DOCX file processing
- **pytesseract**: OCR support
- **pillow**: Image processing
- **python-multipart**: File upload handling
- **torch**: PyTorch for deep learning models
- **transformers**: Hugging Face transformers library
- **numpy**: Numerical computing

### Frontend Dependencies
- **next**: React framework
- **react**: UI library
- **react-dom**: React DOM rendering
- **axios**: HTTP client
- **typescript**: Type safety

## 🔌 API Endpoints

### Document Upload
- `POST /upload/document` - Upload a legal document for analysis

### Analysis
- `POST /analyze/clauses` - Classify and analyze clauses
- `POST /analyze/risks` - Assess legal risks
- `POST /analyze/compliance` - Check compliance issues
- `POST /analyze/entities` - Extract entities
- `POST /analyze/missing-clauses` - Detect missing clauses
- `GET /` - Health check endpoint

## 💡 Usage Examples

### Upload and Analyze a Document
```bash
curl -X POST http://localhost:4000/upload/document \
  -F "file=@contract.pdf"
```

### Analyze Clauses
```bash
curl -X POST http://localhost:4000/analyze/clauses \
  -H "Content-Type: application/json" \
  -d '{"document_id": "doc-123", "text": "Termination clause..."}'
```

## 🎯 Key Features Explained

### Clause Classification
Automatically identifies different types of clauses (e.g., payment terms, confidentiality, liability, termination) using transformer-based models trained on legal documents.

### Risk Scoring
Assigns risk scores to clauses based on patterns that indicate unfavorable terms or potential legal exposure. Higher scores indicate riskier provisions.

### Compliance Checking
Verifies that documents comply with regulatory requirements and industry standards, flagging potential compliance violations.

### Entity Extraction
Extracts critical information such as:
- Party names and details
- Contract dates and renewal periods
- Financial amounts and payment terms
- Obligations and conditions
- Liability limitations

### Missing Clause Detection
Identifies clauses that should be present based on document type (e.g., Non-Disclosure Agreements should include confidentiality period clauses).

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4000,http://localhost:8000
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-3.5-turbo
```

## 🔍 Advanced Features

### Vector Database Integration
LegalAI uses FAISS for semantic similarity search, enabling:
- Finding similar clauses across documents
- Identifying common contract patterns
- Quick retrieval of relevant precedents

### Document Chunking
Intelligent chunking strategies for optimal processing:
- Sentence-level chunking
- Clause-level chunking
- Context-aware overlapping windows

## 📊 Model Information

The system uses multiple AI models:
- **Semantic Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **NLP Processing**: spacy-transformers with BERT
- **LLM Integration**: OpenAI GPT models via LangChain
- **Classification**: Fine-tuned transformer models for legal domains

## 🚦 Error Handling

The system includes comprehensive error handling for:
- Invalid file formats
- Corrupted PDFs
- OCR failures
- API timeouts
- Model inference errors

## 🔒 Security Considerations

- Document data should be encrypted in transit (HTTPS)
- Implement proper authentication for API endpoints
- Store sensitive documents securely
- Consider data retention policies for legal compliance

## 📝 License

This project is open source. Please refer to the LICENSE file for more information.

## 👤 Author

**Ritvik R** - Creator and maintainer of LegalAI

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request with improvements, bug fixes, or new features.

## 📞 Support

For issues, questions, or feature requests, please open an issue on GitHub.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Hugging Face for transformers
- LangChain for LLM orchestration framework
- The open-source community for all the amazing libraries

---

**Last Updated**: March 2026
