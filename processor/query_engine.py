from sentence_transformers import SentenceTransformer
import subprocess

class QueryEngine:
    def __init__(self, vectorstore, model_name="all-MiniLM-L6-v2", top_k=3, llm="mistral"):
        self.vectorstore = vectorstore  # an instance of VectorStore
        self.embedder = SentenceTransformer(model_name)
        self.top_k = top_k
        self.llm_model = llm

    def retrieve_relevant_chunks(self, user_question):
        query_embedding = self.embedder.encode(user_question).tolist()

        results = self.vectorstore.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
            include=['documents', 'metadatas']
        )

        chunks = results['documents'][0]
        metadatas = results['metadatas'][0]
        return chunks, metadatas

    def generate_answer_with_ollama(self, context, question):
        prompt = f"""
        You are a helpful and knowledgeable HR assistant.

        The user may greet you, ask a general question, or ask something related to HR policies.

        If it is a greeting (e.g., "hi", "hello", "good morning"), just respond politely and don't mention any documents or any information.

        If it's a real question about HR topics like benefits, leave, remote work, sick days, etc., then answer clearly using the information below. Don't say "According to the document" or "based on context" — just answer confidently.

        HR Knowledge Base:
        {context}

        User: {question}

        Answer:
        """.strip()

        result = subprocess.run(
            ["ollama", "run", self.llm_model],
            input=prompt,
            text=True,
            capture_output=True
        )

        return result.stdout.strip()

    def answer_question(self, user_question):
        chunks, metadatas = self.retrieve_relevant_chunks(user_question)
        context = "\n\n".join(chunks)
        answer = self.generate_answer_with_ollama(context, user_question)

        return {
            "answer": answer,
            "sources": metadatas
        }
