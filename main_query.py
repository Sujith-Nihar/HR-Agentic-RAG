from processor.vectorstore import VectorStore
from processor.query_engine import QueryEngine

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

if __name__ == "__main__":
    vectorstore = VectorStore()
    engine = QueryEngine(vectorstore)

    while True:
        user_question = input("\nAsk a question (or type 'exit'): ")
        if user_question.lower() in ['exit', 'quit']:
            break

        result = engine.answer_question(user_question)
        print(f"\n🔍 Answer:\n{result['answer']}")
        print("\n📚 Sources:")
        for src in result['sources']:
            print(f"• {src['source']} (chunk {src['chunk_id']})")
