"""
Inspect index module for verifying the built knowledge base.

Usage:
    python -m src.dataset.inspect_index
"""

import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.retriever import CourseRetriever


def inspect_index():
    """Inspect the built index and test search functionality."""
    print("=" * 60)
    print("Knowledge Base Inspection")
    print("=" * 60)
    
    # Load manifest
    manifest_path = Path("data/processed/manifest.json")
    if not manifest_path.exists():
        print(f"\nError: Manifest not found at {manifest_path}")
        print("Please run 'python -m src.dataset.build_index' first.")
        return
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    print(f"\n[INDEX STATISTICS]")
    print(f"  - Total files: {manifest['total_files']}")
    print(f"  - Total chunks: {manifest['total_chunks']}")
    print(f"  - Embedding model: {manifest['embedding_model']}")
    print(f"  - Vector DB: {manifest['vector_db']}")
    print(f"  - Collection name: {manifest['collection_name']}")
    
    # Load and display sample chunks
    chunks_path = Path("data/processed/chunks.jsonl")
    if chunks_path.exists():
        print(f"\n[SAMPLE CHUNKS] (first 3):")
        print("-" * 60)
        
        with open(chunks_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= 3:
                    break
                chunk = json.loads(line)
                print(f"\n[Chunk {i+1}]")
                print(f"  ID: {chunk['id']}")
                print(f"  Day: {chunk['day']}")
                print(f"  Source: {chunk['source_file']}")
                print(f"  Section: {chunk['section']}")
                print(f"  Char count: {chunk['char_count']}")
                print(f"  Content preview: {chunk['content'][:200]}...")
    
    # Test search
    print(f"\n\n[SEARCH TESTS]")
    print("=" * 60)
    
    test_queries = [
        "Day 5 cần nộp gì?",
        "Evidence Pack gồm những phần nào?",
        "Prototype Level 3 là gì?",
        "Find Decide Prep nghĩa là gì?",
    ]
    
    try:
        retriever = CourseRetriever()
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            print("-" * 60)
            
            results = retriever.search(query, top_k=3)
            
            if results:
                for j, result in enumerate(results):
                    print(f"\n  Result {j+1}:")
                    print(f"    Source: {result['source_file']}")
                    print(f"    Day: {result['day']}")
                    print(f"    Section: {result['section']}")
                    print(f"    Score: {result['score']:.4f}")
                    print(f"    Content: {result['content'][:150]}...")
            else:
                print("  No results found.")
    
    except Exception as e:
        print(f"\nError during search test: {e}")
        print("Make sure ChromaDB index is built.")
    
    print("\n" + "=" * 60)
    print("Inspection complete!")


def main():
    inspect_index()


if __name__ == "__main__":
    main()
