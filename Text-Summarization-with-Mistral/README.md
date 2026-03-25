# NotebookAI - Mistral Text Summarizer

A professional, NotebookLM-inspired application that allows users to manage multiple text sources and generate concise, high-quality summaries using **Mistral AI**.

---

## 🚀 Key Features
- **NotebookLM-Style Interface**: Manage multiple documents in a single session with a sleek, multi-pane dashboard.
- **Document Upload Support**: Seamlessly extract text from **PDF**, **DOCX**, and **TXT** files for immediate summarization.
- **API-Driven Summarization**: Leverages Mistral's latest large language models for superior summary quality.
- **Markdown Rendering**: AI-generated summaries are beautifully formatted with headers, bold text, and bullet points.
- **Enterprise-Grade Security**: Includes rate limiting, input sanitization, and Pydantic validation.
- **Real-time Analytics**: Live character and word count tracking for all text sources.

---

## 🏗️ Architecture & Security
For a deep dive into the system design, file extraction logic, and security protocols, please refer to:
👉 **[ARCHITECTURE.md](./ARCHITECTURE.md)**

---

## 🛠️ Setup Instructions

### Prerequisites
- [Conda](https://docs.conda.io/en/latest/) installed on your system.
- [Node.js](https://nodejs.org/) (v18+) for the frontend.
- A valid **Mistral AI API Key**.

### 1. Backend Setup (FastAPI)
1. Navigate to the backend folder:
   ```powershell
   cd backend
   ```
2. Create and activate the Conda environment:
   ```powershell
   conda create -n mistral-summarizer python=3.10 -y
   conda activate mistral-summarizer
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Configure your environment:
   - Create a `.env` file based on `.env.example`.
   - Add your `MISTRAL_API_KEY` to the `.env` file.
5. Start the server:
   ```powershell
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

### 2. Frontend Setup (React)
1. In a new terminal, navigate to the frontend folder:
   ```powershell
   cd frontend
   ```
2. Install Node packages:
   ```powershell
   npm install
   ```
3. Launch the development server:
   ```powershell
   npm run dev
   ```

---

## 🧪 Testing & Verification
You can verify the backend functionality using the included test scripts (requires backend to be running):
- **API Health**: `python backend/test_api.py`
- **File Extraction**: `python backend/test_extraction.py`

---

## 📜 License
See [Mistral AI's Terms of Use](https://mistral.ai/) for model usage policies.
