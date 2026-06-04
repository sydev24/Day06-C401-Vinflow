"""
Text chunker module for splitting cleaned text into manageable chunks.

Handles:
- Splitting by headings when available
- Falling back to character-based splitting
- Configurable chunk size and overlap
- Generating chunk metadata (id, day, source_file, section, chunk_index)
"""

import re
from typing import List, Dict, Any


def detect_headings(text: str) -> List[Dict[str, Any]]:
    """
    Detect headings in text using common patterns.
    
    Heading patterns:
    - Markdown headings: # Heading, ## Heading
    - Numbered sections: 1. Section, 1.1 Subsection
    - Slide markers: Slide X:
    - Chapter markers: Chương X:
    - Bold headings: **Heading**
    
    Args:
        text: Cleaned text content
        
    Returns:
        List of dicts with 'position' and 'heading' keys
    """
    headings = []
    
    patterns = [
        r'^(#{1,6})\s+(.+)$',           # Markdown: # Heading
        r'^(?:Chương|Chapter)\s+\d+',    # Chapter markers
        r'(?i)^SLIDE\s+\d+',             # Slide markers (case-insensitive)
        r'^\*\*(.+?)\*\*',               # Bold headings
        r'^(?:\d+\.)\s+[A-Z]',           # Numbered sections starting with caps
        r'(?i)^BLOCK\s+\d+',             # Block markers
    ]
    
    for i, line in enumerate(text.split('\n')):
        stripped = line.strip()
        if not stripped:
            continue
            
        for pattern in patterns:
            if re.match(pattern, stripped, re.MULTILINE):
                # Clean the heading text
                heading_text = re.sub(r'^#+\s*', '', stripped)
                heading_text = re.sub(r'\*\*', '', heading_text)
                heading_text = re.sub(r'(?i)^SLIDE\s+\d+\s*', '', heading_text)
                heading_text = re.sub(r'(?i)^BLOCK\s+\d+\s*[·•]?\s*', '', heading_text)
                
                if len(heading_text) > 3:  # Skip very short matches
                    headings.append({
                        "position": i,
                        "heading": heading_text[:100]  # Cap length
                    })
                break
    
    return headings


def chunk_by_headings(text: str, chunk_size: int = 1200) -> List[Dict[str, Any]]:
    """
    Split text into chunks based on detected headings.
    
    Args:
        text: Cleaned text content
        chunk_size: Target chunk size in characters
        
    Returns:
        List of dicts with 'content' and 'section' keys
    """
    headings = detect_headings(text)
    lines = text.split('\n')
    
    if not headings:
        return []
    
    chunks = []
    
    for i, heading_info in enumerate(headings):
        start_line = heading_info["position"]
        end_line = headings[i + 1]["position"] if i + 1 < len(headings) else len(lines)
        
        section_text = '\n'.join(lines[start_line:end_line]).strip()
        
        if len(section_text) <= chunk_size:
            chunks.append({
                "content": section_text,
                "section": heading_info["heading"]
            })
        else:
            # Try splitting by paragraphs first
            paragraphs = [p for p in section_text.split('\n\n') if p.strip()]
            
            # If only 1 paragraph (no \n\n breaks), split by single newlines
            if len(paragraphs) <= 1:
                paragraphs = [p for p in section_text.split('\n') if p.strip()]
            
            # If still only 1 block, force character-based split
            if len(paragraphs) <= 1 and len(section_text) > chunk_size:
                sub_chunks = chunk_by_characters(section_text, chunk_size, overlap=200)
                for j, sub in enumerate(sub_chunks):
                    chunks.append({
                        "content": sub["content"],
                        "section": heading_info["heading"] + (" (continued)" if j > 0 else "")
                    })
                continue
            
            current_chunk = ""
            current_section = heading_info["heading"]
            
            for para in paragraphs:
                if len(current_chunk) + len(para) + 2 <= chunk_size:
                    current_chunk += ("\n\n" if current_chunk else "") + para
                else:
                    if current_chunk:
                        chunks.append({
                            "content": current_chunk,
                            "section": current_section
                        })
                    current_chunk = para
                    current_section = heading_info["heading"] + " (continued)"
            
            if current_chunk:
                chunks.append({
                    "content": current_chunk,
                    "section": current_section
                })
    
    return chunks


def chunk_by_characters(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Split text into chunks by character count with overlap.
    
    Args:
        text: Cleaned text content
        chunk_size: Maximum chunk size in characters
        overlap: Overlap between consecutive chunks
        
    Returns:
        List of dicts with 'content' and 'section' keys
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        if end < len(text):
            # Try to break at a natural boundary (paragraph, sentence)
            break_points = ['\n\n', '\n', '. ', '。', '！', '？', '! ', '? ']
            best_break = end
            
            for bp in break_points:
                pos = text.rfind(bp, start + chunk_size // 2, end)
                if pos > start:
                    best_break = pos + len(bp)
                    break
            
            end = best_break
        
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({
                "content": chunk_text,
                "section": "unknown"
            })
        
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks


def chunk_text(
    text: str,
    source_file: str,
    day: str,
    chunk_size: int = 1200,
    overlap: int = 200
) -> List[Dict[str, Any]]:
    """
    Split text into chunks with metadata.
    
    Strategy:
    1. Try to chunk by headings first
    2. Fall back to character-based chunking if no headings found
    
    Args:
        text: Cleaned text content
        source_file: Original filename
        day: Day identifier (e.g., "day1")
        chunk_size: Target chunk size in characters
        overlap: Overlap for character-based chunking
        
    Returns:
        List of chunk dicts with full metadata
    """
    # Try heading-based chunking first
    heading_chunks = chunk_by_headings(text, chunk_size)
    
    if heading_chunks and len(heading_chunks) > 1:
        chunks = heading_chunks
    else:
        # Fall back to character-based chunking
        chunks = chunk_by_characters(text, chunk_size, overlap)
    
    MIN_CHUNK_SIZE = 100

    # Merge tiny chunks with the next one
    merged = []
    carry = ""
    carry_section = ""
    for chunk in chunks:
        content = chunk["content"]
        section = chunk.get("section", "unknown")
        if len(content) < MIN_CHUNK_SIZE:
            carry += ("\n" if carry else "") + content
            carry_section = carry_section or section
        else:
            if carry:
                content = carry + "\n" + content
                section = carry_section or section
                carry = ""
                carry_section = ""
            merged.append({"content": content, "section": section})
    if carry and merged:
        merged[-1]["content"] += "\n" + carry

    # Generate final chunk objects with metadata
    result = []
    for i, chunk in enumerate(merged):
        chunk_id = f"{day}_chunk_{i+1:04d}"
        content = chunk["content"]

        result.append({
            "id": chunk_id,
            "day": day,
            "source_file": source_file,
            "section": chunk.get("section", "unknown"),
            "chunk_index": i + 1,
            "content": content,
            "char_count": len(content)
        })

    return result
