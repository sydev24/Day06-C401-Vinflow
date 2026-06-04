# Codebase - AI IN ACTION Copilot

## Huong dan chay

### 1. Cai dat dependencies

pip install -r requirements.txt

### 2. Cau hinh API key

Copy .env.example thanh .env va dien API key.

### 3. Build knowledge base

python -m src.dataset.build_index --rebuild

### 4. Chay UI

streamlit run app.py

### 5. Test nhanh tu terminal

python run_test_copilot.py

## Cong nghe su dung

| Layer | Technology |
|-------|-----------|
| Embedding | paraphrase-multilingual-MiniLM-L12-v2 |
| Vector DB | ChromaDB (cosine, local SQLite) |
| LLM | MIMO API (OpenAI-compatible) |
| UI | Streamlit |
| Language | Python 3.10+ |
