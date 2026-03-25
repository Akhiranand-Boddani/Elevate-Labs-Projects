# Mental Health Chatbot using Hugging Face and Mistral API

---

### Project Overview
This repository contains the implementation of a lightweight, modern mental health chatbot designed to classify user emotions and provide empathetic, solution-oriented responses. The application has been refactored from a local PyTorch-heavy application to a **fully cloud-native, API-driven architecture** using free-tier services.

#### Key Features:
- **Zero Local Footprint**: No need to download heavy PyTorch models or weights. The application is highly lightweight and deploys instantly.
- **Emotion Detection (Hugging Face Hub)**: Identifies 28 distinct emotions using the `joeddav/distilbert-base-uncased-go-emotions-student` model via the official `InferenceClient`.
- **Solution-Oriented Responses (Mistral AI)**: Generates actionable mental health responses using the Mistral LLM API (`mistral-small-latest`).
- **Interactive UI**: A user-friendly chatbot interface built using Streamlit.
- **Visualization**: Bar charts showcasing real-time emotion probabilities.

---

### Architecture

The application relies on two primary external APIs:

1. **Hugging Face Serverless Inference API**: 
   When a user submits text, it is sent to the Hugging Face API where a RoBERTa model (fine-tuned on the GoEmotions dataset) calculates the probabilities of 28 different emotions. These are mapped to Ekman’s six basic emotions (anger, disgust, fear, joy, sadness, surprise) for easier interpretation.

2. **Mistral API**:
   The top 3 emotions detected by the Hugging Face API are extracted and prepended to the user's message as hidden context. This enriched prompt is sent to the Mistral API, instructing it to act as an empathetic mental health expert and formulate an actionable response.

#### Repository Structure
```
Mental-Health-Chatbot/
├── app.py                  # Main application script (Streamlit)
├── README.md               # Project documentation
├── ARCHITECTURE.md         # Detailed architectural blueprint
├── GEMINI.md               # Code conventions and guidelines
├── requirements.txt        # Python dependencies
└── .env.example            # Example environment variables file
```

---

### Dataset & Emotion Mapping
The underlying model used by the Hugging Face API was trained on the **GoEmotions** dataset by Google, which contains 58k Reddit comments labeled with 28 fine-grained emotion categories.

The application dynamically maps these 28 emotions to **Ekman's 6 Basic Emotions**:
- **Anger**: anger, annoyance, disapproval
- **Disgust**: disgust
- **Fear**: fear, nervousness
- **Joy**: joy, amusement, approval, gratitude, love, optimism, relief, pride
- **Sadness**: sadness, disappointment, grief
- **Surprise**: surprise, realization, confusion, curiosity
- **Neutral**: neutral

---

### Usage & Installation

#### 1. Clone the repository:
```bash
git clone https://github.com/username/project-repo.git
cd project-repo
```

#### 2. Install the dependencies:
Because we offload inference to the cloud, the requirements are incredibly lightweight.
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment Variables:
Create a `.env` file in the root directory and add your free API keys:
```env
HUGGINGFACE_API_KEY=hf_your_huggingface_token
MISTRAL_API_KEY=your_mistral_api_key
```

#### 4. Start the Streamlit app:
```bash
streamlit run app.py
```

---

### Detailed Workflow

1. **Input Handling**: The user enters a message in the Streamlit chatbot interface.
2. **Emotion Classification**:
   - The app sends an HTTP POST request to the Hugging Face API.
   - The API returns probabilities for each of the 28 emotion classes.
   - These probabilities are mapped to Ekman’s six basic emotions.
3. **Response Generation**:
   - The top-3 emotions are identified.
   - These emotions are sent alongside the user prompt to the Mistral API.
   - Mistral generates an empathetic and actionable response tailored to the user’s emotional state.
4. **Visualization**:
   - Streamlit renders dynamic bar charts displaying the probabilities for both GoEmotions and Ekman mappings.

---

### References
1. GoEmotions Dataset by Google
2. Hugging Face Serverless Inference API
3. Mistral AI Platform
4. Streamlit Documentation
