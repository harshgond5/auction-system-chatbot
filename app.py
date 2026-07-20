import streamlit as st
from openai import OpenAI
import json
import numpy as np
from PIL import Image
from data import PLATFORM_DB, BUYER_DB, SELLER_DB

TF_AVAILABLE = False
try:
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    TF_AVAILABLE = True
except ImportError:
    pass

# ==========================================
# 1. UI Configuration
# ==========================================
st.set_page_config(page_title="Smart Auction AI", page_icon="🔨", layout="centered")

# ==========================================
# 2. Cached Deep Learning Models
# ==========================================
@st.cache_resource
def load_vision_model():
    # Load MobileNetV2 - Fast and efficient for web apps
    return tf.keras.applications.MobileNetV2(weights='imagenet')

# ==========================================
# 3. Sidebar: Tools & Image Processor
# ==========================================
with st.sidebar:
    st.title("⚙️ Auction Tools")
    active_role = st.selectbox("Switch Profile:", ["Buyer", "Seller"])
    st.divider()
    
    st.markdown("### 🖼️ Image Recognition")
    uploaded_file = st.file_uploader("Upload an item photo...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).resize((224, 224))
        st.image(image, use_column_width=True)
        
        # --- SAFE VISION LOGIC ---
        if TF_AVAILABLE:
            if st.button("Identify Object"):
                with st.spinner("Analyzing image..."):
                    model = load_vision_model()
                    # Prepare image for the model
                    img_array = tf.keras.preprocessing.image.img_to_array(image)
                    img_array = np.expand_dims(img_array, axis=0)
                    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
                    
                    # Predict
                    preds = model.predict(img_array)
                    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0]
                    label = decoded[0][1].replace('_', ' ').title()
                    confidence = decoded[0][2] * 100
                    
                    st.success(f"Detected: **{label}** ({confidence:.1f}%)")
        else:
            st.warning("⚠️ Vision Engine: Not available in Cloud Mode. Please view local demo for full functionality.")
# ==========================================
# 4. Main Chat Logic
# ==========================================
# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Welcome to Smart Auction AI! How can I help you today?"}]

st.title("🔨 Smart Auction AI")

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if user_query := st.chat_input("Message the AI Concierge..."):
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # API Logic
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        
        sys_inst = f"""You are an expert auction assistant. Platform Data: {json.dumps(PLATFORM_DB)}. 
        User: {json.dumps(BUYER_DB if active_role == 'Buyer' else SELLER_DB)}"""
        
        api_messages = [{"role": "system", "content": sys_inst}] + st.session_state.messages
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=api_messages
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"API/System Error: {e}")