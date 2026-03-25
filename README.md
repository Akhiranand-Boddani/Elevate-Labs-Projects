# Career Advisor AI (Mistral Edition) 🎓

### Professional GenAI Career Guidance System

A high-performance, production-ready AI career guidance chatbot built using **Python**, **Streamlit**, and the **Mistral AI SDK**. This system leverages the latest advancements in GenAI to provide structured, evidence-based career strategy, including real-time streaming responses and contextual memory.

## 🚀 Key Features

### 1. Mistral AI Integration
- **Engine:** Powered by **Mistral AI** (`open-mistral-nemo`) for advanced reasoning and industry-standard performance.
- **Client:** Implements the latest `mistralai` v2.x SDK with synchronous streaming support.
- **Custom Logic:** Uses a specialized DECODE / AUDIT / REFINE protocol to identify core career hurdles and provide "brutally honest" feedback.

### 2. Modern UI/UX
- **Streaming Responses:** Advice is delivered token-by-token for a responsive, "live" assistant feel.
- **Integrated Feedback:** Built-in sentiment collection widgets under every response for continuous improvement.
- **Contextual Awareness:** Users can provide custom profile instructions (background, goals, constraints) to get hyper-personalized advice.
- **Interactive Start:** Quick-start suggested queries to guide users toward high-impact career roadmaps.

### 3. Professional Architecture
- **Modular Design:** Strict separation of concerns between UI, API Client, Prompt Engineering, and Memory Management.
- **Sliding Window Memory:** Maintains conversation coherence through a configurable history buffer.
- **Structured Outputs:** Enforces a consistent 5-point strategic layout (Executive Summary, Strategic Analysis, Roadmap, Project Artifacts, and Risks).

## 📁 Project Structure
```text
Career_Advisor_Chatbot_GenAI/
├── app.py                # Main Application Entry Point
├── requirements.txt      # Project Dependencies
├── ARCHITECTURE.md       # Technical Design Documentation
├── GEMINI.md             # Development & Agent Guidelines
├── config/
│   └── settings.py       # System Configuration & Model Constants
├── core/
│   ├── mistral_client.py # Mistral API Integration Layer
│   ├── prompt_manager.py # Advanced Prompt Engineering Logic
│   └── memory_manager.py # Conversation History Management
├── utils/
│   └── logger.py         # Centralized System Logging
└── assets/
    └── ui_styles.py      # Custom CSS & Theme Definitions
```

## ⚙️ Setup & Installation

**1. Clone the repository**
```bash
git clone <your-repository-url>
cd Career_Advisor_Chatbot_GenAI
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure API Keys**
Create a `.streamlit/secrets.toml` file in the project root:
```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
```

**4. Run the application**
```bash
streamlit run app.py
```

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Frontend:** Streamlit
- **AI Core:** Mistral AI API
- **Tooling:** `mistralai` SDK, `logging`
