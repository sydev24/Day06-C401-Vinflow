# AI IN ACTION Copilot

> Track A · Learning OS (Vin AI Thực Chiến) · Batch 02 · Nhóm C401-Vinflow

## Thành viên

| Tên | MSSV | Vai trò |
|-----|------|---------|
| Vũ Quốc Bảo | 2A202600541 | Data owner — chuẩn bị data text, chunking, embedding, vector DB |
| Vũ Văn Huy | 2A202600750 | Backend RAG + API — RAG chain, prompt rule, MIMO API |
| Nguyễn Trung Kiên | 2A202600969 | Prototype owner — Streamlit UI, chat box, hiển thị output |
| Lê Đình Sỹ | 2A202600770 | QA/Test — test 4 paths: happy, low-confidence, failure, correction |
| Phạm Hoàng Anh Kiệt | 2A202600797 | Demo script / Repo owner — README, demo script, product decision |

## Sản phẩm: AI IN ACTION Copilot

RAG chatbot tra lời câu hỏi về nội dung khoá học AI Thực Chiến (6 ngày đầu).
Trả về **Answer + Source + Next Action**. Có fallback khi hỏi ngoài phạm vi tài liệu.

```
Question → RAG Search (ChromaDB) → LLM (MIMO API) → Answer + Source + Next Action
```

## Cấu trúc repo

```
Day06-C401-Vinflow/
├── README.md                  ← Bạn đang đọc file này
├── spec/
│   └── spec.md                ← Thin SPEC cuối Day 05
├── docs/
│   ├── demo_script.md         ← Kịch bản thuyết trình 3–5 phút
│   ├── product_decision.md    ← Các quyết định sản phẩm chính
│   ├── test_cases.md          ← Test cases 4 paths (TV4)
│   └── demo_questions.md      ← Câu hỏi demo + expected output (TV4)
├── 02-group-spec/
│   ├── evidence-pack-template.md
│   └── evidence_screenshot/   ← Screenshot bằng chứng self-use
└── codebase/
    ├── README.md              ← Hướng dẫn chạy chi tiết
    ├── app.py                 ← Streamlit UI
    ├── src/
    │   ├── retriever.py       ← ChromaDB retriever
    │   ├── rag_chain.py       ← RAG logic + prompt rule
    │   └── prompt.py          ← Prompt template
    └── data/
        ├── raw_text/          ← Text từ slide 6 ngày đầu
        ├── processed/
        │   ├── chunks.jsonl
        │   └── manifest.json
        └── vectorstore/chroma/
```

## Chạy nhanh

```bash
cd codebase
pip install -r requirements.txt
cp .env.example .env      # điền MIMO API key vào .env
python -m src.dataset.build_index --rebuild
streamlit run app.py
```

Mở trình duyệt tại `http://localhost:8501`

## Câu hỏi demo (Happy path)

| # | Câu hỏi | Expected output |
|---|---------|-----------------|
| 1 | "Day 5 cần nộp gì?" | Checklist Evidence Pack + Thin SPEC, nguồn slide Day 5 |
| 2 | "Evidence Pack gồm những phần nào?" | 6 phần, nguồn template Day 5 |
| 3 | "Thin SPEC Draft là gì?" | Định nghĩa + cấu trúc, nguồn Day 5 slide 40 |
| 4 | "Prototype Level 3 yêu cầu gì?" | Yêu cầu cụ thể, nguồn Day 5 |

## Câu hỏi demo (Failure path)

| Câu hỏi | Expected output |
|---------|-----------------|
| "Tôi nên mua laptop gaming nào?" | "Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu. Bạn có thể hỏi về slide, lab, assignment hoặc framework của chương trình AI Thực Chiến." |

## Tài liệu Day 05

| Folder/File | Nội dung |
|-------------|----------|
| `spec/spec.md` | Thin SPEC — cam kết build slice, 4 paths, owner plan |
| `02-group-spec/evidence-pack-template.md` | Evidence Pack với self-use, user, competitor evidence |
| `02-group-spec/evidence_screenshot/` | 7 screenshot bằng chứng từ slide Day 3/4/5 |
| `docs/demo_script.md` | Kịch bản demo 3–5 phút |
| `docs/product_decision.md` | Lý do chọn RAG, Augmentation, ChromaDB, fallback |
