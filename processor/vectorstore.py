import chromadb

class VectorStore:
    def __init__(self, persist_directory="./chroma_store"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="hr_docs")

    def store(self, chunks, embeddings, source):
        metadatas = [{"source": source, "chunk_id": i} for i in range(len(chunks))]
        ids = [f"{source}_{i}" for i in range(len(chunks))]  # Unique ID for each chunk

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def show_stored_chunks(self, limit=5):
        data = self.collection.get(include=['documents', 'metadatas'])  # ✅ Fixed
        print(f"🧠 Total chunks stored: {len(data['documents'])}")
        for i in range(min(limit, len(data['documents']))):
            print(f"\nChunk ID: {data['ids'][i]}")
            print(f"Source: {data['metadatas'][i]['source']}")
            print(f"Text: {data['documents'][i][:300]}...")  # Preview 300 characters
