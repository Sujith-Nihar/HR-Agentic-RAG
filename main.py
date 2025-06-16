import os
from processor.loader import FileLoader
from processor.chunker import TextChunker
from processor.embedder import Embedder
from processor.vectorstore import VectorStore

class HRDocProcessor:
    def __init__(self):
        self.loader = FileLoader()
        self.chunker = TextChunker()
        self.embedder = Embedder()
        self.vectorstore = VectorStore()

    def process_file(self, file_path):
        print(f"Processing: {file_path}")
        text = self.loader.load(file_path)
        chunks = self.chunker.chunk(text)
        embeddings = self.embedder.embed(chunks)
        self.vectorstore.store(chunks, embeddings, source=os.path.basename(file_path))
        print(f"✅ Completed: {file_path}")

# Example usage
if __name__ == "__main__":
    processor = HRDocProcessor()
    processor.process_file("uploads/Benefits_Guide.txt")
    processor.vectorstore.show_stored_chunks()
