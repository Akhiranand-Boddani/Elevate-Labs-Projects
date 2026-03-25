import os
import streamlit as st
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from mistralai.client import Mistral
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Check if keys are present
if not HUGGINGFACE_API_KEY or not MISTRAL_API_KEY:
    st.error("Missing API keys. Please ensure HUGGINGFACE_API_KEY and MISTRAL_API_KEY are set in your .env file.")
    st.stop()

# Configure Clients
mistral_client = Mistral(api_key=MISTRAL_API_KEY)
hf_client = InferenceClient(token=HUGGINGFACE_API_KEY)

# Models
MISTRAL_MODEL = "mistral-small-latest" 
HF_MODEL_ID = "joeddav/distilbert-base-uncased-go-emotions-student"

# Define Ekman Mapping
ekman_mapping = {
    "anger": ["anger", "annoyance", "disapproval"],
    "disgust": ["disgust"],
    "fear": ["fear", "nervousness"],
    "joy": ["joy", "amusement", "approval", "gratitude", "love", "optimism", "relief", "pride"],
    "sadness": ["sadness", "disappointment", "grief"],
    "surprise": ["surprise", "realization", "confusion", "curiosity"],
    "neutral": ["neutral"]
}

# Function to map GoEmotions to Ekman emotions
def map_to_ekman(goemotions_probs):
    ekman_probs = {emotion: 0.0 for emotion in ekman_mapping.keys()}
    for ekman_emotion, goemotions_list in ekman_mapping.items():
        ekman_probs[ekman_emotion] = sum(
            [goemotions_probs.get(label, 0.0) for label in goemotions_list]
        )
    return ekman_probs

# Function to classify emotion using Hugging Face InferenceClient
def classify_emotion(text):
    try:
        results = hf_client.text_classification(text, model=HF_MODEL_ID)
        
        # Convert list of dicts/namedtuples to a dictionary
        goemotions_probs = {item['label'] if isinstance(item, dict) else item.label: 
                            item['score'] if isinstance(item, dict) else item.score 
                            for item in results}
        
        # Sort to find the top 3
        top_3_emotions = sorted(goemotions_probs.items(), key=lambda x: x[1], reverse=True)[:3]
        ekman_probs = map_to_ekman(goemotions_probs)
        
        return goemotions_probs, ekman_probs, top_3_emotions

    except Exception as e:
        st.error(f"An error occurred during emotion classification: {e}")
        return {}, {}, []

# Function to generate responses using Mistral API with solutions
def get_mistral_response_with_solutions(prompt, emotions):
    emotions_text = ", ".join([f"{emotion} ({round(prob * 100, 2)}%)" for emotion, prob in emotions])
    
    system_prompt = (
        "You are an empathetic, professional mental health chatbot expert. "
        "The user's input was analyzed and the following underlying emotions were detected: "
        f"{emotions_text}.\n\n"
        "Please provide a highly supportive, concise, and actionable response. "
        "Include possible coping mechanisms or solutions to help the user based on these emotions. "
        "Keep the solutions strictly to the point, and feel free to gently ask a follow-up question to keep the conversation engaging."
    )
    
    try:
        chat_response = mistral_client.chat.complete(
            model=MISTRAL_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred while generating the response: {e}")
        return "I'm sorry, but I am having trouble connecting to my brain right now. Please try again later."

# Chat history management
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Streamlit App
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠", layout="centered")
st.title("🧑‍⚕️ Mental Health Chatbot 🧠 ")
st.markdown("Powered by **Hugging Face** (Emotion Detection) and **Mistral AI** (Response Generation).")

# Display chat history
st.subheader("Chat History")
if not st.session_state["chat_history"]:
    st.info("Your conversation history will appear here. Try typing a message below!")

for idx, entry in enumerate(st.session_state["chat_history"]):
    with st.chat_message("user"):
        st.write(entry['user_input'])
    
    with st.chat_message("assistant"):
        st.write(entry['response'])
        
        with st.expander("📊 View Emotion Analysis Details"):
            st.write("**Top 3 Emotions Detected:**")
            for emotion, prob in entry["top_3_emotions"]:
                st.write(f"- **{emotion.capitalize()}**: {round(prob * 100, 2)}%")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**GoEmotions Probabilities:**")
                st.bar_chart(entry["goemotions_probs_df"])
            with col2:
                st.write("**Ekman Emotion Probabilities:**")
                st.bar_chart(entry["ekman_probs_df"])

# Persistent prompt bar at the bottom
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
st.markdown("---")

with st.container():
    with st.form("user_input_form", clear_on_submit=True):
        user_input = st.text_area("How are you feeling today?", placeholder="Type your message here...", key="user_input", height=100)
        submit_button = st.form_submit_button("Submit", use_container_width=True)

if submit_button and user_input:
    with st.spinner("Analyzing your emotions..."):
        # Classify emotion
        goemotions_probs, ekman_probs, top_3_emotions = classify_emotion(user_input)

    if top_3_emotions:
        with st.spinner("Formulating an empathetic response..."):
            # Prepare dataframes for visualization
            goemotions_probs_df = pd.DataFrame.from_dict(
                goemotions_probs, orient="index", columns=["Probability"]
            ).sort_values(by="Probability", ascending=False).head(10) # Only show top 10 to avoid clutter
            
            ekman_probs_df = pd.DataFrame.from_dict(
                ekman_probs, orient="index", columns=["Probability"]
            ).sort_values(by="Probability", ascending=False)

            # Generate response with solutions
            mistral_response = get_mistral_response_with_solutions(user_input, top_3_emotions)

        # Append to chat history
        st.session_state["chat_history"].append(
            {
                "user_input": user_input,
                "response": mistral_response,
                "top_3_emotions": top_3_emotions,
                "goemotions_probs_df": goemotions_probs_df,
                "ekman_probs_df": ekman_probs_df,
            }
        )
        
        st.rerun()
