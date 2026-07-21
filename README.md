# 🔨 Smart AuctionHub

**An Intelligent, GenAI-Powered Auction Management System**

AuctionHub is a next-generation marketplace platform that leverages **Generative AI** for conversational management and **Deep Learning** for automated product valuation. Built for efficiency, the system allows users to switch seamlessly between Buyer and Seller roles while utilizing a modular data-agnostic pipeline.

---

## 🚀 Key Features

* **Intelligent Agent Interface:** A conversational UI powered by Llama-3.1-8b-instant, providing real-time assistance based on current user context (Buyer vs. Seller).
* **Computer Vision Pipeline:** Utilizes **MobileNetV2** (Transfer Learning) to automatically identify and categorize item images uploaded by sellers.
* **Predictive Valuation:** Features a custom-trained **Keras Sequential Neural Network** to forecast auction closing prices based on categorical data.
* **Modular Architecture:** Designed with "Separation of Concerns" where the data layer (`data.py`) is isolated from the UI, ensuring scalability for future SQL/NoSQL migrations.
* **Dynamic Contextual Awareness:** The system manages state and dynamically injects platform/user data into the LLM system prompt for accurate, context-aware responses.

---

## 🛠️ Tech Stack

* **Frontend & UI:** Streamlit
* **AI/LLM:** Llama-3.1-8b-instant via Groq Cloud API
* **Deep Learning:** TensorFlow & Keras
* **Vision Model:** MobileNetV2 (Pre-trained on ImageNet)
* **Language:** Python 3.10+

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
```bash
git clone <your-repo-url>
cd auction-system

```


2. **Create Virtual Environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

```


3. **Install Dependencies:**
```bash
pip install streamlit openai tensorflow numpy pillow

```


4. **Configure API Keys:**
Create a folder named `.streamlit` and a file inside it named `secrets.toml`:
```toml
GROQ_API_KEY = "your_actual_api_key_here"

```


5. **Run the Application:**
```bash
streamlit run app.py

```



---

## 🏗️ Project Architecture

This project utilizes a multi-modal pipeline to handle disparate AI tasks efficiently:

* **The Ingestion Layer:** Streamlit handles user input and state management, providing a "ChatGPT-like" conversational experience.
* **The Intelligence Layer (LLM):** The Groq API processes user queries, using a system-prompt injection technique to provide answers scoped specifically to the current platform database.
* **The Valuation Layer (Deep Learning):**
* **Vision:** Employs Transfer Learning with MobileNetV2 for low-latency image classification.
* **Regression:** A custom Keras sequential model trained on synthetic historical velocity data to predict auction outcomes.



---

## 🎓 Why this Project?

This project demonstrates a transition from basic chatbot wrappers to **Integrated AI Agents**. By combining Cloud-based LLMs with local Deep Learning microservices, the system proves the feasibility of running robust AI tools in a lightweight web environment.

---

**Developed for:** [Your Institution/Course Name]

**Status:** MVP (Minimum Viable Product)

**License:** MIT