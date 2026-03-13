# Career Advisor Chatbot (GenAI)

### Live App: https://career-advisor-chatbot.streamlit.app

A production-style AI career guidance chatbot built using **Python**, **Streamlit**, and **Google Gemini GenAI API**.
This application provides **structured career advice**, **skill recommendations**, and **learning roadmaps** based on user queries.

The project demonstrates how to build a **modular, production-ready GenAI system** with proper architecture, prompt engineering, memory management, and API integration.

## Project Overview

The **Career Advisor Chatbot** is an AI-powered assistant designed to help users explore career paths, identify required skills, and understand realistic learning roadmaps.

Unlike simple chatbots, this system follows a **production-ready architecture** with clear separation between:
- UI layer
- API layer
- Prompt engineering
- Conversation memory
- Response processing
- Logging and error handling

The chatbot leverages the **Google Gemini GenAI API** to generate intelligent responses and provides **structured career guidance** to users.

The project was designed to simulate a **real-world GenAI system implementation** rather than a simple prototype.

The application includes:
- Domain-specific prompt engineering
- Multi-turn conversation memory
- Modular backend design
- Secure API key management
- Streamlit-based chat interface
- Cloud deployment via Streamlit Community Cloud

The chatbot focuses on providing **actionable, realistic career advice** instead of generic responses.

## Features

### AI-Powered Career Guidance

Users can ask questions about:
- Career paths
- Required skills
- Learning roadmaps
- Career transitions
- Industry demand

The AI generates structured responses using the Gemini GenAI model.

### Structured Career Advice Format

Responses are designed using prompt engineering to always include:

1. Career Insight
2. Recommended Skills
3. Learning Path
4. Potential Risks
5. Next Actions

This ensures **consistent** and **practical advice**.

### Multi-Turn Conversation Memory

The chatbot maintains conversation context to support follow-up questions.

Conversation memory stores recent interactions and passes them to the model as context.

This enables the chatbot to understand:
- previous questions
- previous advice
- evolving career discussions

### Prompt Engineering Layer

A dedicated **Prompt Manager** constructs structured prompts that guide the AI to generate domain-specific responses.

The prompt enforces rules such as:
- Avoid vague advice
- Ask clarifying questions when needed
- Provide actionable steps
- Avoid unrealistic guarantees

### Modular Backend Architecture

The project separates responsibilities into different modules:
- Gemini API integration
- Prompt engineering
- Conversation memory
- Response processing
- Logging
- Exception handling

This design improves **maintainability** and **scalability**.

### Secure API Key Handling

The Gemini API key is securely stored using **Streamlit Secrets** instead of hardcoding credentials.

### Error Handling and Logging

The system includes:
- centralized logging
- API error handling
- graceful failure responses

Logging is implemented using Python's logging module.

### Interactive Chat UI

The chatbot interface is built with **Streamlit’s chat components** for a modern conversational experience.

The interface supports:
- chat-style messaging
- conversation history
- loading indicators
- real-time responses

## Tech Stack

- Language: Python
- Framework: Streamlit
- AI Model: Google Gemini GenAI API
- Libraries: streamlit, google-genai

## System Architecture

The application follows a layered architecture similar to production AI systems.
```
 User
   ↓
Streamlit UI
   ↓
Backend Controller (app.py)
   ↓
Prompt Manager
   ↓
Conversation Memory
   ↓
Gemini API Client
   ↓
Response Handler
   ↓
UI Rendering
```

### Component Responsibilities
- **UI Layer:** Handles user input and displays responses.
- **Prompt Engineering Layer:** Constructs structured prompts to guide the AI model.
- **Memory Layer:** Maintains conversation history for contextual responses.
- **API Layer:** Handles communication with the Gemini API.
- **Response Layer:** Processes and formats the final output.

## Project Structure:

```

Career_Advisor_Chatbot_GenAI/
│
├── app.py
│
├── requirements.txt
│
├── config/
│   └── settings.py
│
├── core/
│   ├── gemini_client.py
│   ├── prompt_manager.py
│   ├── memory_manager.py
│   └── response_handler.py
│
├── utils/
│   ├── logger.py
│   └── exceptions.py
│
└── assets/
    └── ui_styles.py

```

### app.py
Main Streamlit application entry point. Responsibilities include:
- UI rendering
- Handling chat input
- Managing session state
- Calling backend modules
- Displaying responses

The application initializes conversation memory and processes user queries through the backend pipeline.

### core/
Contains the **core backend logic** of the chatbot.

#### gemini_client.py
Handles communication with the **Google Gemini API**. Responsibilities include:
- API client initialization
- Model selection
- Response generation
- Error handling

The model used is **gemini-2.5-flash-lite** for fast responses.

#### prompt_manager.py
Responsible for **prompt engineering**. Creates structured prompts that guide the AI to generate high-quality responses. The prompt includes:
- role definition
- response rules
- structured output format

#### memory_manager.py
Manages **conversation history**. Stores recent chat interactions and passes them as context to the model. Memory size is configurable and limited to recent turns to avoid token overflow.

#### response_handler.py
Processes model responses before displaying them. Responsibilities include:
- cleaning responses
- handling empty outputs
- formatting final responses

### utils/
Utility modules used across the project.

#### logger.py
Provides centralized logging functionality for the application. Used for debugging and monitoring API behavior.

#### exceptions.py

Defines custom exceptions used in the application. Example: `GeminiAPIException`

### config/

Contains configuration settings for the application. Example settings include:
- application name
- conversation memory limits

### assets/

Contains UI styling resources. Custom CSS is used to slightly enhance chat message formatting.

## Running the Project Locally
**1.** Clone the repository.
```
git clone https://github.com/Avik-Das-567/Career_Advisor_Chatbot_GenAI.git
cd Career_Advisor_Chatbot_GenAI
```
**2.** Create a Virtual Environment.
```
python -m venv venv
```
Activate it: 
```
venv\Scripts\activate
```
**3.** Install dependencies.
```
pip install -r requirements.txt
```
**4.** Configure Gemini API Key.

Create a **Streamlit secrets file:**
```
.streamlit/secrets.toml
```
Add your API key:
```
GEMINI_API_KEY = "your_api_key_here"
```
**5.** Run the Streamlit application.
```
streamlit run app.py
```
**6.** Open in browser.

Streamlit will automatically launch the app at:
```
http://localhost:8501
```

## Deployment

This project is deployed using **Streamlit Community Cloud**.

The live app is available at: https://career-advisor-chatbot.streamlit.app

## Example Queries

Users can interact with the chatbot by asking questions like:

- _What skills do I need to become a data scientist?_
- _How can I transition from mechanical engineering to software development?_
- _Is cybersecurity a good career path in 2026?_
- _What roadmap should I follow to become a machine learning engineer?_
- _What are the risks of switching careers into AI?_

The chatbot will generate **structured, actionable career advice.**

---
