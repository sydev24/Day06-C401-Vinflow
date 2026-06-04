"""
Text cleaner module for normalizing and cleaning raw text content.

Handles:
- Removing excessive whitespace
- Collapsing multiple blank lines
- Preserving headings, bullets, and numbered lists
- Maintaining Vietnamese text integrity
"""

import re


def _split_slide_lines(text: str) -> str:
    """Insert newlines before SLIDE markers that are glued to content."""
    text = re.sub(r'(?<!\n)(SLIDE\s+\d+)', r'\n\1', text)
    text = re.sub(r'(?<!\n)(DAY\s+\d+\s*[·•])', r'\n\1', text)
    text = re.sub(r'(?<!\n)(BLOCK\s+\d+\s*[·•])', r'\n\1', text)
    return text


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.

    Operations:
    1. Normalize line endings (CRLF -> LF)
    2. Insert newlines before SLIDE/DAY/BLOCK markers
    3. Strip trailing whitespace from each line
    4. Collapse multiple blank lines to max 2
    5. Remove leading/trailing whitespace from document

    Args:
        text: Raw text content

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Split glued slide markers onto separate lines
    text = _split_slide_lines(text)

    # Strip trailing whitespace from each line (preserve leading for indentation)
    lines = [line.rstrip() for line in text.split("\n")]

    # Collapse multiple blank lines (more than 2 consecutive -> 2)
    cleaned_lines = []
    blank_count = 0

    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                cleaned_lines.append(line)
        else:
            blank_count = 0
            cleaned_lines.append(line)

    # Join and strip document-level whitespace
    result = "\n".join(cleaned_lines).strip()

    return result


def clean_documents(documents: list) -> list:
    """
    Clean text content for a list of document dicts.
    
    Args:
        documents: List of dicts with 'raw_text' key
        
    Returns:
        List of dicts with 'cleaned_text' key added
    """
    cleaned = []
    for doc in documents:
        cleaned_doc = doc.copy()
        cleaned_doc["cleaned_text"] = clean_text(doc["raw_text"])
        cleaned.append(cleaned_doc)
    return cleaned
