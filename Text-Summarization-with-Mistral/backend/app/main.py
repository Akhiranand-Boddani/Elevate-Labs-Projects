from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
from mistralai.client.sdk import Mistral
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import re
import io
from pypdf import PdfReader
from docx import Document

# Load environment variables
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI App
app = FastAPI(
    title="Mistral Text Summarizer API",
    description="API for summarizing text using Mistral AI",
    version="1.0.0"
)

# Add state to app for limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
origins = [
    "http://localhost:5173", # Vite default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Model for Input Validation
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=30000, description="The text to be summarized.")

def sanitize_input(text: str) -> str:
    # Basic sanitization to strip potential HTML/JS tags
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text.strip()

@app.post("/api/summarize")
@limiter.limit("5/minute")
async def summarize_text(request: Request, payload: SummarizeRequest):
    if not MISTRAL_API_KEY:
        raise HTTPException(status_code=500, detail="Mistral API key is not configured on the server.")
    
    sanitized_text = sanitize_input(payload.text)
    
    if len(sanitized_text) < 20:
        raise HTTPException(status_code=400, detail="Text is too short after sanitization.")

    # Initialize Mistral client
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    try:
        # Prompt for summarization
        messages = [
            {
                "role": "system",
                "content": "You are a professional text summarizer. Provide a concise, clear, and accurate summary of the following text using markdown formatting. Use bullet points if helpful."
            },
            {
                "role": "user",
                "content": sanitized_text
            }
        ]
        
        response = await client.chat.complete_async(
            model="mistral-small-latest",
            messages=messages,
            temperature=0.3,
            max_tokens=800
        )
        
        summary = response.choices[0].message.content
        return {"summary": summary}
        
    except Exception as e:
        print(f"Mistral API Error: {str(e)}")
        raise HTTPException(status_code=502, detail=f"Failed to communicate with Mistral API: {str(e)}")

@app.post("/api/extract-text")
@limiter.limit("10/minute")
async def extract_text(request: Request, file: UploadFile = File(...)):
    print(f"Extracting text from file: {file.filename}")
    extension = file.filename.split('.')[-1].lower()
    content = await file.read()
    
    # Check file size (5MB limit)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")

    extracted_text = ""
    
    try:
        if extension == 'pdf':
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                extracted_text += page.extract_text() + "\n"
        
        elif extension == 'docx':
            docx_file = io.BytesIO(content)
            doc = Document(docx_file)
            for para in doc.paragraphs:
                extracted_text += para.text + "\n"
        
        elif extension == 'txt':
            extracted_text = content.decode('utf-8', errors='ignore')
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOCX, or TXT.")

        clean_text = extracted_text.strip()
        if not clean_text:
            raise HTTPException(status_code=400, detail="Could not extract any readable text from the file.")
            
        return {"text": clean_text, "filename": file.filename}

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Extraction Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
