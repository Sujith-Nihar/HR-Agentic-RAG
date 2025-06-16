import os
import streamlit as st
from processor.loader import FileLoader
from processor.chunker import TextChunker
from processor.embedder import Embedder
from processor.vectorstore import VectorStore
from processor.query_engine import QueryEngine

st.set_page_config(page_title="HR Assistant", layout="wide")
st.markdown("<h1 style='text-align: center;'>💼 HR Assistant Chatbot</h1>", unsafe_allow_html=True)

st.markdown("""
    <style>
        .user-msg {
            background-color: #D1FFD6;
            padding: 10px 15px;
            border-radius: 12px;
            margin: 10px 0;
            width: fit-content;
            max-width: 80%;
            align-self: flex-end;
            color: #000;
            font-size: 16px;
        }
        .bot-msg {
            background-color: #EAEAEA;
            padding: 10px 15px;
            border-radius: 12px;
            margin: 10px 0;
            width: fit-content;
            max-width: 80%;
            align-self: flex-start;
            color: #222;  /* ✅ darker text for bot */
            font-size: 16px;
        }
        .msg-container {
            display: flex;
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tabs
tab1, tab2 = st.tabs(["📤 Upload Documents", "💬 Chatbot"])

# Upload tab
with tab1:
    st.subheader("Upload HR Policy Files")
    uploaded_file = st.file_uploader("Upload .txt, .pdf, or .docx", type=["txt", "pdf", "docx"])
    if uploaded_file:
        filepath = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Uploaded: {uploaded_file.name}")

        try:
            loader = FileLoader()
            text = loader.load(filepath)

            chunker = TextChunker(chunk_size=300, overlap=50)
            chunks = chunker.chunk(text)

            embedder = Embedder()
            embeddings = embedder.embed(chunks)

            store = VectorStore()
            store.store(chunks, embeddings, uploaded_file.name)

            st.success("✅ File processed and added to knowledge base.")
        except Exception as e:
            st.error(f"Error: {e}")

# Chatbot tab
with tab2:
    st.subheader("Chat with your HR Assistant")

    # Display chat messages
    st.markdown("<div class='msg-container'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>🤖 {msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    prompt = st.chat_input("Ask something about HR policies...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        greetings = {"hi", "hello", "hey", "good morning", "hey", "good evening"}
        if prompt.lower().strip() in greetings:
            bot_response = "👋 Hello! I'm your HR assistant. Ask me about leave, benefits, or remote work policies!"
        else:
            try:
                vectorstore = VectorStore()
                engine = QueryEngine(vectorstore)
                result = engine.answer_question(prompt)
                answer = result["answer"]
                sources = result["sources"]
                source_info = "<br>".join([f"• <i>{s['source']}</i> (chunk {s['chunk_id']})" for s in sources])
                bot_response = f"{answer}<br><br><small><b>Sources:</b><br>{source_info}</small>"
            except Exception as e:
                bot_response = f"❌ Error: {e}"

        st.session_state.messages.append({"role": "bot", "content": bot_response})
        st.rerun()
