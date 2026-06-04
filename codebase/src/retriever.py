"""
Course retriever module for searching the knowledge base.

Usage:
    retriever = CourseRetriever()
    results = retriever.search("Day 5 cần nộp gì?", top_k=4)
"""

import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class CourseRetriever:
    """
    Retriever for searching course content in ChromaDB.
    
    Provides semantic search over course chunks with metadata.
    """
    
    def __init__(
        self,
        persist_dir: str = "data/vectorstore/chroma",
        collection_name: str = "ai_thuc_chien_docs",
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ):
        """
        Initialize the retriever.
        
        Args:
            persist_dir: Path to ChromaDB persistence directory
            collection_name: Name of the ChromaDB collection
            model_name: Sentence-transformers model for embeddings
        """
        import chromadb
        from sentence_transformers import SentenceTransformer
        
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        
        # Load embedding model
        self.model = SentenceTransformer(model_name)
        
        # Connect to ChromaDB
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Get collection
        try:
            self.collection = self.client.get_collection(collection_name)
        except Exception:
            raise ValueError(
                f"Collection '{collection_name}' not found in {persist_dir}.\n"
                f"Please run 'python -m src.dataset.build_index' first."
            )
    
    def search(
        self,
        query: str,
        top_k: int = 4,
        filter_day: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            filter_day: Optional filter by day (e.g., "day5")
            
        Returns:
            List of result dicts with keys:
                - content: Chunk text content
                - source_file: Original filename
                - day: Day identifier
                - section: Section heading
                - score: Relevance score (0-1, higher is better)
        """
        # Generate query embedding
        query_embedding = self.model.encode([query]).tolist()
        
        # Build filter
        where_filter = None
        if filter_day:
            where_filter = {"day": filter_day}
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        
        if results and results["documents"] and results["documents"][0]:
            documents = results["documents"][0]
            metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(documents)
            distances = results["distances"][0] if results["distances"] else [0.0] * len(documents)
            
            for doc, meta, dist in zip(documents, metadatas, distances):
                # Convert distance to similarity score (cosine distance -> similarity)
                # ChromaDB returns cosine distance = 1 - cosine_similarity
                score = max(0.0, 1.0 - dist)
                
                formatted_results.append({
                    "content": doc,
                    "source_file": meta.get("source_file", "unknown"),
                    "day": meta.get("day", "unknown"),
                    "section": meta.get("section", "unknown"),
                    "score": round(score, 4)
                })
        
        return formatted_results
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        return {
            "name": self.collection_name,
            "count": self.collection.count(),
            "persist_dir": self.persist_dir
        }


# Convenience function for quick searches
def search_course(query: str, top_k: int = 4) -> List[Dict[str, Any]]:
    """
    Quick search function.
    
    Args:
        query: Search query
        top_k: Number of results
        
    Returns:
        List of result dicts
    """
    retriever = CourseRetriever()
    return retriever.search(query, top_k=top_k)
