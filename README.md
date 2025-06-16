# 🤖 HR-RAG: Generative AI-Powered HR Assistant

**HR-RAG** is a Generative AI chatbot system designed to answer employee HR-related queries using an intelligent combination of **Retrieval-Augmented Generation (RAG)** and **Large Language Models (LLMs)**. This system enables employees to get immediate answers from internal documents like HR manuals, policies, and benefit guides—without waiting on human intervention.

---

## 🧠 Concept

At its core, the HR Assistant leverages the **RAG paradigm**:

- **Retrieval**: Finds relevant content from uploaded HR documents.
- **Augmentation**: Passes retrieved content into a language model.
- **Generation**: Produces a fluent, accurate response grounded in the retrieved text.

This ensures that all answers are both contextually rich and based on actual company policies, avoiding hallucinations or vague generalizations.

---

## 🧱 Architecture Overview

The system is modular and includes the following stages:

1. **Document Ingestion**  
   Documents like PDFs, DOCX, or text files are uploaded. These files are loaded, cleaned, and prepared for processing.

2. **Text Chunking**  
   Long documents are split into smaller overlapping chunks using a custom `TextChunker` to ensure semantic integrity across sections.

3. **Embedding**  
   Each chunk is converted into a high-dimensional vector representation using a sentence transformer model. These embeddings capture the semantic meaning of each chunk.

4. **Vector Storage (ChromaDB)**  
   The embeddings are stored in a local vector database (Chroma), allowing for fast similarity-based retrieval later.

5. **Querying (RAG Pipeline)**  
   - When a user asks a question, it is also embedded.
   - The most relevant document chunks are retrieved based on vector similarity.
   - These chunks, along with the user’s question, are fed into an LLM (via Ollama).
   - The LLM generates a natural language answer grounded in the retrieved content.

6. **Response Generation**  
   The model provides a final answer, along with references or citations to the source document chunks used for generation—ensuring traceability and reliability.

---

## 📁 Project Modules

- `streamlit_app.py`: User interface for uploading documents and chatting
- `main.py`: Backend script for ingestion (optional)
- `main_query.py`: Terminal-based query testing (optional)
- `processor/loader.py`: Loads and parses documents
- `processor/chunker.py`: Splits text into manageable units
- `processor/embedder.py`: Generates vector embeddings
- `processor/vectorstore.py`: Manages the ChromaDB storage
- `processor/query_engine.py`: Orchestrates retrieval + LLM response

---

## 💼 Real-World Relevance

This project aligns with modern enterprise goals:
- **Efficiency**: Automates responses to frequent HR queries
- **Cost Savings**: Reduces repetitive workload from HR teams
- **Improved Experience**: Employees get instant, accurate answers
- **Auditability**: Answers cite the actual source documents


---

## 🛠️ Future Extensions

- Slack or MS Teams integration
- Personalized responses using employee context
- Multi-turn conversation memory
- Admin dashboard for analytics
- Document access controls based on roles

---

## 📄 License

MIT – Free for use and modification.

---
