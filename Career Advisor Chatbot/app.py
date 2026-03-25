import streamlit as st
from core.mistral_client import MistralClient
from core.prompt_manager import PromptManager
from core.memory_manager import ConversationMemory
from utils.logger import get_logger

from assets.ui_styles import CUSTOM_CSS

logger = get_logger()

# --- Page Configuration ---
st.set_page_config(
    page_title="Career Advisor AI (Mistral)",
    page_icon="🎓",
    layout="wide"
)

# --- App Styling ---
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.info("Powered by Mistral AI Experimental API")
    
    st.subheader("👤 Your Profile")
    custom_instructions = st.text_area(
        "Custom Instructions",
        placeholder="e.g., I am a final-year CS student looking for remote DevOps roles. I have experience with Docker but need to learn Kubernetes.",
        help="Provide context about your background, goals, or constraints to get tailored advice.",
        height=150
    )
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.memory.clear()
        st.rerun()
    
    st.divider()
    st.caption("AI Career Strategy System")
    st.caption("Built with Python & Streamlit")

# --- App Header ---
st.title("🎓 Career Advisor Chatbot")
st.markdown("---")

# --- Initialize Session State ---
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Mistral Client ---
try:
    mistral_client = MistralClient()
except Exception:
    st.error("❌ Mistral API Key not found. Please configure Streamlit Secrets (MISTRAL_API_KEY).")
    st.stop()

prompt_manager = PromptManager()

# --- Callback for Feedback ---
def handle_feedback(idx):
    feedback = st.session_state[f"fb_{idx}"]
    st.session_state.messages[idx]["feedback"] = feedback
    st.toast("Thank you for your feedback!")

# --- Chat History Display ---
if not st.session_state.messages:
    st.info("👋 **Welcome to Career Advisor AI!** I'm your elite career strategist. To get started, you can:")
    cols = st.columns(2)
    with cols[0]:
        if st.button("🚀 Roadmap for AI Engineer", use_container_width=True):
            st.session_state.suggested_input = "What is the detailed roadmap to become an AI Engineer in 2026?"
            st.rerun()
    with cols[1]:
        if st.button("💼 Transition to Tech", use_container_width=True):
            st.session_state.suggested_input = "I'm in a non-tech role. How can I transition to software development?"
            st.rerun()
else:
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            # Feedback for assistant messages
            if msg["role"] == "assistant":
                fb_key = f"fb_{i}"
                st.feedback(
                    "thumbs",
                    key=fb_key,
                    on_change=handle_feedback,
                    args=[i],
                    disabled=msg.get("feedback") is not None
                )

# --- User Input Logic ---
# Handle suggested queries
if "suggested_input" in st.session_state:
    user_input = st.session_state.pop("suggested_input")
else:
    user_input = st.chat_input("Ask about careers, skills, roadmaps...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Response
    with st.chat_message("assistant"):
        # 1. Build messages with context
        messages = prompt_manager.build_messages(
            user_input, 
            st.session_state.memory.get_messages(),
            custom_instructions=custom_instructions
        )
        
        # 2. Stream response
        full_response = ""
        try:
            full_response = st.write_stream(
                mistral_client.generate_response_stream(messages)
            )
        except Exception as e:
            logger.error(f"Streaming Error: {str(e)}")
            st.error("⚠️ An error occurred during response generation.")
            full_response = "I'm sorry, I couldn't process that request."

        # 3. Update state and memory
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.memory.update("user", user_input)
        st.session_state.memory.update("assistant", full_response)
        
        # Rerun to show feedback widget for the new message
        st.rerun()
