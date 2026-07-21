import streamlit as st
from openai import OpenAI
import json
import numpy as np
from PIL import Image
from data import PLATFORM_DB, DEFAULT_USER, featuredAuctions, fraudAnalysis

TF_AVAILABLE = False
try:
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    TF_AVAILABLE = True
except ImportError:
    pass


st.set_page_config(page_title="AuctioHub", page_icon="🔨", layout="centered")

 
@st.cache_resource
def load_vision_model():
    return tf.keras.applications.MobileNetV2(weights='imagenet')

 
with st.sidebar:
    st.title("⚙️ AuctioHub Tools")
    st.caption("Logged in as: **Active User**")
    st.divider()
    
    st.markdown("### 🖼️ Image Recognition")
    uploaded_file = st.file_uploader("Upload an item photo...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).resize((224, 224))
        st.image(image, use_column_width=True)
        
        if TF_AVAILABLE:
            if st.button("Identify Object"):
                with st.spinner("Analyzing image..."):
                    model = load_vision_model()
                    img_array = tf.keras.preprocessing.image.img_to_array(image)
                    img_array = np.expand_dims(img_array, axis=0)
                    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)    
                    preds = model.predict(img_array)
                    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0]
                    label = decoded[0][1].replace('_', ' ').title()
                    confidence = decoded[0][2] * 100
                    
                    st.success(f"Detected: **{label}** ({confidence:.1f}%)")
        else:
            st.info("💡 **Vision Engine:** Running in Cloud Mode.")

 
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Welcome to AuctioHub! Are you looking to place a bid on an item or list something new to sell today?"}]

st.title("🔨 AuctioHub")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input & Dynamic Intent Processing
if user_query := st.chat_input("Ask about bidding, selling, or platform items..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        api_key = st.secrets["GROQ_API_KEY"]
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        
        # System instructions allowing the AI to interpret buyer or seller intent dynamically
        sys_inst = f"""You are an expert AI concierge and assistant for 'AuctioHub'. 
        
        PLATFORM METRICS:
        {json.dumps(PLATFORM_DB, indent=2)}
        
        AVAILABLE AUCTIONS CATALOG:
        {json.dumps(featuredAuctions, indent=2)}
        
        USER PROFILE:
        {json.dumps(DEFAULT_USER, indent=2)}
        
        Instructions:
        - Analyze the user's query to automatically determine their intent (whether they want to **BUY** an item, **SELL/list** an item, check their wallet balance, or review active bids/listings).
        - NEVER use a personal name. 
        - Address the user strictly as **"Bidder"** if their intent involves buying, browsing, or checking their wallet balance.
        - Address the user strictly as **"Auctioneer"** if their intent involves selling, listing items, or checking their payout balance.
        """
        
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