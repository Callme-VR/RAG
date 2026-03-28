from typing import List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
from src.data_loader import Load_all_documents


class EmbeddingGenerator:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, model_name: str = "all-MiniLM-L6-v2"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = SentenceTransformer(model_name)
        print(f"Loaded model: {model_name}")
        
    def chunk_documents(self, documents: List[Any]) -> List[Any]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = splitter.split_documents(documents)
        return chunks
   
    def embed_chunks(self, chunks: List[Any]) -> np.ndarray:
        texts = [chunk.page_content for chunk in chunks]
        print(f"Embedding {len(texts)} chunks...")
        
        if not texts:
            print("[WARNING] No chunks to embed")
            return np.array([])
        
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Generated {len(embeddings)} embeddings {embeddings.shape}")
        return embeddings


# example usage
if __name__ == "__main__":
    docs = Load_all_documents("data")
    
    emb_pipelines = EmbeddingGenerator()
    chunks = emb_pipelines.chunk_documents(docs)
    embeddings = emb_pipelines.embed_chunks(chunks)
    
    print(
        f"Generated {len(embeddings)} embeddings",
        embeddings[0] if len(embeddings) > 0 else "No embeddings generated"
    )