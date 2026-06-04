"""
Build index module for creating the vector database from text files.

Pipeline: Text → Clean → Chunk → Embedding → ChromaDB

Usage:
    python -m src.dataset.build_index
    python -m src.dataset.build_index --raw-dir data/raw_text --rebuild
"""

import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.dataset.text_loader import load_text_files
from src.dataset.text_cleaner import clean_documents
from src.dataset.chunker import chunk_text


def ensure_directories():
    """Ensure all required directories exist."""
    dirs = [
        "data/raw_text",
        "data/processed",
        "data/vectorstore/chroma"
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def save_chunks_jsonl(chunks: List[Dict[str, Any]], output_path: str = "data/processed/chunks.jsonl"):
    """Save chunks to JSONL file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    print(f"Saved {len(chunks)} chunks to {output_path}")


def save_manifest(
    total_files: int,
    total_chunks: int,
    embedding_model: str,
    vector_db: str,
    collection_name: str,
    output_path: str = "data/processed/manifest.json"
):
    """Save manifest metadata."""
    manifest = {
        "total_files": total_files,
        "total_chunks": total_chunks,
        "embedding_model": embedding_model,
        "vector_db": vector_db,
        "collection_name": collection_name
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Saved manifest to {output_path}")


def build_chroma_index(
    chunks: List[Dict[str, Any]],
    collection_name: str = "ai_thuc_chien_docs",
    persist_dir: str = "data/vectorstore/chroma",
    rebuild: bool = False
):
    """
    Build ChromaDB vector store from chunks.
    
    Args:
        chunks: List of chunk dicts
        collection_name: Name for the ChromaDB collection
        persist_dir: Directory to persist ChromaDB
        rebuild: If True, delete existing collection before building
    """
    import chromadb
    from sentence_transformers import SentenceTransformer
    
    # Load embedding model
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    
    # Initialize ChromaDB
    print(f"Initializing ChromaDB at {persist_dir}")
    client = chromadb.PersistentClient(path=persist_dir)
    
    # Delete existing collection if rebuild is requested
    if rebuild:
        try:
            client.delete_collection(collection_name)
            print(f"Deleted existing collection: {collection_name}")
        except Exception:
            pass
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    # Check if collection already has data
    existing_count = collection.count()
    if existing_count > 0 and not rebuild:
        print(f"Collection '{collection_name}' already has {existing_count} items. Use --rebuild to recreate.")
        return
    
    # Prepare data for ChromaDB
    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["content"] for chunk in chunks]
    metadatas = [
        {
            "day": chunk["day"],
            "source_file": chunk["source_file"],
            "section": chunk["section"],
            "chunk_index": chunk["chunk_index"],
            "char_count": chunk["char_count"]
        }
        for chunk in chunks
    ]
    
    # Generate embeddings in batches
    batch_size = 100
    print(f"Generating embeddings for {len(chunks)} chunks...")
    
    for i in range(0, len(chunks), batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_embeddings = model.encode(batch_docs, show_progress_bar=False).tolist()
        
        collection.add(
            ids=ids[i:i + batch_size],
            documents=batch_docs,
            embeddings=batch_embeddings,
            metadatas=metadatas[i:i + batch_size]
        )
        
        print(f"  Indexed {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")
    
    print(f"ChromaDB index built successfully with {collection.count()} items")


def build_index(
    raw_dir: str = "data/raw_text",
    rebuild: bool = False
):
    """
    Main function to build the complete index.
    
    Pipeline: Text → Clean → Chunk → Embedding → ChromaDB
    """
    print("=" * 60)
    print("Building Knowledge Base Index")
    print("=" * 60)
    
    # Step 1: Ensure directories exist
    ensure_directories()
    
    # Step 2: Load text files
    print("\n[1/4] Loading text files...")
    try:
        documents = load_text_files(raw_dir)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return
    
    print(f"Loaded {len(documents)} files")
    for doc in documents:
        print(f"  - {doc['source_file']} ({doc['day']})")
    
    # Step 3: Clean text
    print("\n[2/4] Cleaning text...")
    cleaned_docs = clean_documents(documents)
    print(f"Cleaned {len(cleaned_docs)} documents")
    
    # Step 4: Chunk text
    print("\n[3/4] Chunking text...")
    all_chunks = []
    for doc in cleaned_docs:
        chunks = chunk_text(
            text=doc["cleaned_text"],
            source_file=doc["source_file"],
            day=doc["day"]
        )
        all_chunks.extend(chunks)
        print(f"  {doc['source_file']}: {len(chunks)} chunks")
    
    print(f"Total chunks: {len(all_chunks)}")
    
    # Step 5: Save chunks and manifest
    print("\n[4/4] Saving chunks and building vector index...")
    save_chunks_jsonl(all_chunks)
    
    save_manifest(
        total_files=len(documents),
        total_chunks=len(all_chunks),
        embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        vector_db="chroma",
        collection_name="ai_thuc_chien_docs"
    )
    
    # Step 6: Build ChromaDB index
    build_chroma_index(
        chunks=all_chunks,
        collection_name="ai_thuc_chien_docs",
        persist_dir="data/vectorstore/chroma",
        rebuild=rebuild
    )
    
    print("\n" + "=" * 60)
    print("Index build complete!")
    print("=" * 60)
    print(f"\nOutputs:")
    print(f"  - Chunks: data/processed/chunks.jsonl")
    print(f"  - Manifest: data/processed/manifest.json")
    print(f"  - Vector DB: data/vectorstore/chroma/")


def main():
    parser = argparse.ArgumentParser(
        description="Build knowledge base index from text files"
    )
    parser.add_argument(
        "--raw-dir",
        default="data/raw_text",
        help="Directory containing raw .txt files (default: data/raw_text)"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild vector index from scratch"
    )
    
    args = parser.parse_args()
    build_index(raw_dir=args.raw_dir, rebuild=args.rebuild)


if __name__ == "__main__":
    main()
