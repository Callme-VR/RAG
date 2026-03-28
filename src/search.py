import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.vector_store import FaissVectorStore

load_dotenv()


class SearchRag:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "llama-3.1-8b-instant"):
        self.vector_store = FaissVectorStore(persist_dir, embedding_model)
        
        # load and build the VectorStore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "faiss_metadata.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from src.data_loader import Load_all_documents
            docs = Load_all_documents("data")
            self.vector_store.build_from_documents(docs)
        else:
            self.vector_store.load()

        # initialize LLM
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.llm = ChatGroq(
            model=llm_model,
            api_key=api_key
        )
        
    def search_summarize(self, query: str, top_k: int = 3) -> str:
        results = self.vector_store.query(query, top_k)
        
        # safer extraction
        texts = [
            r.get("metadata", {}).get("text", "")
            for r in results
            if r.get("metadata")
        ]
        
        if not texts:
            return "No relevant information found."
        
        context = "\n\n".join(texts)

        prompt = f"""Based on the following context, answer the question concisely and accurately:

Context:
{context}

Question: {query}

Answer:"""

        response = self.llm.invoke(prompt)
        return response.content


# example usage
if __name__ == "__main__":
    search_rag = SearchRag()
    result = search_rag.search_summarize("What is context engineering?")
    print(result)