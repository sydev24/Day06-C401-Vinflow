# Day06-C401-NhomXX

> Track A - Learning OS (Vin AI Thuc Chien) - Batch 02

## Thanh vien

| Ten | MSSV | Vai tro |
|-----|------|---------|
| Vu Quoc Bao | 2A202600541 | Data / Knowledge Base |
| Vu Van Huy | 2A202600750 | Backend RAG + API |
| Nguyen Trung Kien | 2A202600969 | Frontend Streamlit UI |
| Le Dinh Sy | 2A202600770 | QA / Evaluation / Demo Test |
| Pham Hoang Anh Kiet | 2A202600797 | README / Evidence / SPEC / Presentation |

## San pham: AI IN ACTION Copilot

RAG chatbot tra loi cau hoi noi dung khoa hoc AI Thuc Chien, tra ve answer + source + next action.

```
Question -> RAG Search (ChromaDB) -> LLM (MIMO API) -> Answer + Source + Next Action
```

## Cau truc repo

```
Day06-C401-NhomXX/
├── README.md        <- Ban dang doc file nay
├── spec/            <- SPEC san pham (spec.md)
│   ├── README.md
│   └── spec.md
└── codebase/        <- Toan bo code prototype
    ├── README.md    <- Huong dan chay
    ├── app.py       <- Streamlit UI
    ├── src/         <- RAG backend
    └── data/        <- Knowledge base
```

## Chay nhanh

```bash
cd codebase
pip install -r requirements.txt
cp .env.example .env        # dien API key
python -m src.dataset.build_index --rebuild
streamlit run app.py
```

## Cau hoi demo

- "Day 5 can nop gi?"
- "Evidence Pack gom nhung phan nao?"
- "Prototype Level 3 yeu cau gi?"
- "Toi nen mua laptop gaming nao?" (failure path)

## Tai lieu Day 05

| Folder | Noi dung |
|--------|----------|
| `01-invidual-workshop/` | Mo app AI that: ve flow, tim path yeu, viet finding |
| `02-group-spec/` | Evidence pack, synthesis toolkit, thin SPEC template |
