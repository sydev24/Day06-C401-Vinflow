"""
RAG Copilot module.

Usage:
    from src.copilot import ask_copilot
    result = ask_copilot("Day 5 cần nộp gì?")
"""

import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

log_dir = project_root / "data" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("copilot")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(log_dir / "copilot.log", encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("%(message)s"))

if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(ch)

from src.retriever import CourseRetriever
from src.llm.client import get_llm_client

_retriever_instance: Optional[CourseRetriever] = None
_cache: Dict[str, Dict[str, Any]] = {}


def _get_retriever() -> CourseRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = CourseRetriever()
    return _retriever_instance


def _build_prompt(question: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("source_file", "unknown")
        day = chunk.get("day", "unknown")
        section = chunk.get("section", "unknown")
        content = chunk.get("content", "")
        context_parts.append(
            f"[Nguồn {i}] ({source} | {day} | {section})\n{content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    system_prompt = (
        "Bạn là AI Copilot hỗ trợ chương trình 'AI Thực Chiến' (Batch 02, VinUniversity).\n"
        "Nhiệm vụ: trả lời câu hỏi dựa trên nội dung được cung cấp bên dưới.\n\n"
        "QUY TẮC:\n"
        "- Chỉ trả lời dựa trên context được cung cấp. Không bịa thông tin.\n"
        "- Trả lời bằng tiếng Việt, rõ ràng, ngắn gọn.\n"
        "- Nếu context không đủ để trả lời, nói rõ rằng thông tin chưa có trong knowledge base.\n\n"
        "OUTPUT FORMAT (JSON):\n"
        '{{\n'
        '  "answer": "Câu trả lời chi tiết bằng tiếng Việt",\n'
        '  "sources": ["Nguồn 1: mô tả ngắn", "Nguồn 2: mô tả ngắn"],\n'
        '  "next_action": "Gợi ý hành động tiếp theo cho người hỏi"\n'
        '}}\n\n'
        "Chỉ trả về JSON, không thêm markdown hay text khác."
    )

    user_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {question}"

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _call_mimo(prompt_messages: List[Dict[str, str]], timeout: int = 60) -> str:
    client = get_llm_client()
    return client.chat(
        messages=prompt_messages,
        temperature=0.3,
        max_tokens=1024,
    )


def _parse_json(text: str) -> Dict[str, Any]:
    text = text.strip()

    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]

    return json.loads(text)


def _format_source(chunk: Dict[str, Any]) -> str:
    source = chunk.get("source_file", "unknown")
    day = chunk.get("day", "unknown")
    section = chunk.get("section", "unknown")
    return f"{source} | {day} | {section}"


def _detect_day_filter(question: str) -> Optional[str]:
    """Extract day filter from question if user asks about a specific day."""
    import re
    match = re.search(r'(?:day|ngày)\s*(\d)', question, re.IGNORECASE)
    if match:
        return f"day{match.group(1)}"
    return None


def ask_copilot(
    question: str,
    top_k: int = 4,
    retriever: Optional[CourseRetriever] = None,
) -> Dict[str, Any]:
    """
    Ask the RAG backend and return answer + sources + next action.

    Args:
        question: User question string
        top_k: Number of chunks to retrieve
        retriever: Optional CourseRetriever instance (created if not provided)

    Returns:
        Dict with keys:
            - question: Original question
            - answer: LLM-generated answer
            - sources: List of source descriptions
            - next_action: Suggested next step
            - retrieved_chunks: Raw chunks from retriever (for debug/frontend)
    """
    if not question or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    logger.info("=" * 50)
    logger.info(f"[INPUT] {question}")

    cache_key = question.strip().lower()
    if cache_key in _cache:
        logger.info("[CACHE] Hit - tra loi tu cache")
        return _cache[cache_key]

    if retriever is None:
        retriever = _get_retriever()

    t0 = time.time()
    filter_day = _detect_day_filter(question)
    if filter_day:
        logger.info(f"[FILTER] Detect day filter: {filter_day}")
    retrieved_chunks = retriever.search(question, top_k=top_k, filter_day=filter_day)
    t1 = time.time()
    logger.info(f"[RETRIEVER] Tim thay {len(retrieved_chunks)} chunks ({round(t1-t0, 2)}s)")
    for i, c in enumerate(retrieved_chunks, 1):
        logger.debug(f"  chunk {i}: {c['source_file']} | {c['day']} | {c['section'][:50]} | score={round(c['score'],4)}")

    if not retrieved_chunks:
        logger.warning("[RETRIEVER] Khong tim thay chunks phu hop")
        result = {
            "question": question,
            "answer": "Không tìm thấy thông tin phù hợp trong knowledge base.",
            "sources": [],
            "next_action": "Kiểm tra lại câu hỏi hoặc cập nhật thêm nội dung vào knowledge base.",
            "retrieved_chunks": [],
        }
        _cache[cache_key] = result
        return result

    prompt = _build_prompt(question, retrieved_chunks)
    logger.info(f"[PROMPT] Xay dung prompt ({len(prompt[0]['content']) + len(prompt[1]['content'])} chars)")

    try:
        t2 = time.time()
        model_output = _call_mimo(prompt)
        t3 = time.time()
        logger.info(f"[LLM] Nhan response tu MIMO ({round(t3-t2, 2)}s)")
        logger.debug(f"[LLM] Raw output: {model_output[:200]}")
    except Exception as e:
        logger.error(f"[LLM] Loi: {e}")
        return {
            "question": question,
            "answer": f"Lỗi khi gọi LLM: {e}",
            "sources": [_format_source(c) for c in retrieved_chunks],
            "next_action": "Thử lại sau hoặc kiểm tra API key trong .env.",
            "retrieved_chunks": retrieved_chunks,
        }

    try:
        parsed = _parse_json(model_output)
        logger.info("[PARSE] Parse JSON thanh cong")
    except (ValueError, json.JSONDecodeError):
        logger.warning("[PARSE] JSON khong hop le, dung raw output")
        parsed = {
            "answer": model_output,
            "sources": [_format_source(c) for c in retrieved_chunks],
            "next_action": "Xem lại các nguồn tham chiếu hoặc hỏi lại cụ thể hơn.",
        }

    sources = parsed.get("sources")
    if isinstance(sources, str):
        sources = [sources]
    if not sources:
        sources = [_format_source(c) for c in retrieved_chunks]

    result = {
        "question": question,
        "answer": parsed.get("answer", ""),
        "sources": sources,
        "next_action": parsed.get("next_action", "Thử đặt câu hỏi tiếp theo."),
        "retrieved_chunks": retrieved_chunks,
    }
    _cache[cache_key] = result
    logger.info(f"[DONE] Tra loi xong. Answer: {result['answer'][:80]}...")
    logger.info("=" * 50)
    return result
