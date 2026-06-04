"""
Text loader module for reading raw .txt files from the data directory.

Handles:
- Reading .txt files from a configurable directory
- Extracting metadata (source_file, day) from filename
- Preserving Vietnamese text content
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any


def extract_day_from_filename(filename: str) -> str:
    """
    Extract day identifier from filename.
    
    Examples:
        day1.txt -> day1
        day_1.txt -> day1
        Day1.txt -> day1
    """
    stem = Path(filename).stem
    match = re.search(r'day[_\-]?(\d+)', stem, re.IGNORECASE)
    if match:
        return f"day{match.group(1)}"
    return stem.lower()


def load_text_files(raw_dir: str = "data/raw_text") -> List[Dict[str, Any]]:
    """
    Load all .txt files from the specified directory.
    
    Args:
        raw_dir: Path to directory containing .txt files
        
    Returns:
        List of dicts with keys: source_file, day, raw_text
        
    Raises:
        FileNotFoundError: If directory doesn't exist
        ValueError: If no .txt files found
    """
    raw_path = Path(raw_dir)
    
    if not raw_path.exists():
        raise FileNotFoundError(
            f"Directory not found: {raw_dir}\n"
            f"Please create the directory and add .txt files.\n"
            f"Expected structure:\n"
            f"  {raw_dir}/\n"
            f"    day1.txt\n"
            f"    day2.txt\n"
            f"    ..."
        )
    
    txt_files = sorted(raw_path.glob("*.txt"))
    
    if not txt_files:
        raise ValueError(
            f"No .txt files found in {raw_dir}\n"
            f"Please add .txt files to this directory."
        )
    
    documents = []
    for txt_file in txt_files:
        try:
            content = txt_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = txt_file.read_text(encoding="latin-1")
        
        documents.append({
            "source_file": txt_file.name,
            "day": extract_day_from_filename(txt_file.name),
            "raw_text": content,
        })
    
    return documents
