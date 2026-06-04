# Product Decision — AI IN ACTION Copilot

Tài liệu này ghi lại các quyết định sản phẩm chính và lý do chọn, để giám khảo và thành viên mới hiểu tại sao nhóm build theo cách này.

---

## Quyết định 1: RAG thay vì chatbot chung

**Chọn:** RAG (Retrieval-Augmented Generation) trên data text slide 5 ngày đầu.

**Không chọn:** Chatbot AI chung không có context khoá học.

**Lý do:**

Evidence cho thấy pain cụ thể là "không biết tìm ở slide nào khi đang làm lab" — không phải "không có AI để hỏi". Học viên đã có ChatGPT/Gemini; vấn đề là chúng không biết nội dung giáo trình AI Thực Chiến và không có nguồn để verify.

RAG giải quyết đúng pain: câu trả lời grounded trên đúng slide, có source cụ thể. Chatbot generic không làm được điều này.

**Trade-off chấp nhận:** RAG phức tạp hơn, cần build index trước. Nhưng scope chỉ là 6 ngày đầu, đủ nhỏ để build trong 1 ngày.

---

## Quyết định 2: Augmentation thay vì Automation

**Chọn:** Augmentation — AI gợi ý answer + source, user tự verify và quyết định dùng thông tin nào.

**Không chọn:** Automation — AI tự submit bài, tự điền form, tự quyết định.

**Lý do:**

Sản phẩm hỗ trợ học tập. Nếu AI tự quyết và sai, học viên nộp bài sai. Human role phải là Reviewer/Decider.

**Human role cụ thể:**
- **Reviewer:** kiểm tra lại source Copilot đưa ra
- **Decider:** chọn thông tin nào dùng cho bài nộp
- **Rescuer:** nếu AI sai, hỏi lại cụ thể hơn hoặc hỏi mentor

---

## Quyết định 3: Xử lý 4 paths bằng similarity threshold

**Chọn:** Dùng similarity score của ChromaDB để phân loại path tự động.

| Path | Similarity score | Hành động |
|---|---|---|
| Happy | ≥ 0.75 | Generate answer + source + next action |
| Low-confidence | 0.40 – 0.74 | Hiển thị 2–3 chunk liên quan nhất kèm tên section để user tự chọn; hoặc hỏi lại "Bạn đang làm lab Day mấy?" |
| Failure | < 0.40 | Fallback cố định, không generate |
| Correction | User gõ lại / sửa câu hỏi | Search lại với context mới, không dùng cache câu cũ |

**Lý do:**

Threshold rõ ràng giúp prototype hành xử nhất quán và test được. Không dùng threshold → AI tự generate kể cả khi chunk không liên quan → hallucinate.

---

## Quyết định 4: Fallback rõ ràng thay vì hallucinate

**Chọn:** Khi similarity < 0.40, trả về fallback cố định:

> "Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu. Bạn có thể hỏi về slide, lab, assignment hoặc framework của chương trình AI Thực Chiến."

**Không chọn:** Để model tự trả lời bằng kiến thức chung.

**Lý do:**

Failure mode nguy hiểm nhất của sản phẩm học tập: AI trả lời tự tin nhưng sai context → học viên hiểu sai yêu cầu assignment, làm sai form, nộp thiếu artifact.

Prompt rule: "Chỉ trả lời dựa trên CONTEXT được cung cấp. Nếu không tìm thấy thông tin liên quan, dùng fallback." Kết hợp với RAG grounding và show source.

---

## Quyết định 5: ChromaDB thay vì vector DB khác

**Chọn:** ChromaDB (local, in-process).

**Không chọn:** Pinecone, Weaviate, pgvector.

**Lý do:**

- Scope là 5 ngày × ~50 slide — không cần cloud vector DB
- ChromaDB chạy local, không cần API key riêng, không có latency mạng
- Setup đơn giản: `pip install chromadb`, không cần infrastructure
- Phù hợp với constraint "build trong 1 ngày"

**Trade-off chấp nhận:** Không scale lên production lớn. Nhưng scope cam kết trong spec chỉ là 5 ngày đầu.

---

## Quyết định 6: Output bắt buộc có Answer + Source + Next Action

**Chọn:** Mọi happy-path response đều có đủ 3 phần.

**Lý do từ evidence:**

- Học viên không chỉ cần định nghĩa — cần biết làm gì tiếp (next action)
- Thiếu source → không verify được → mất độ tin cậy
- Pattern học từ GitHub Copilot Chat (answer + source)

Prompt template enforce 3 phần này ở mọi happy-path response.

---

## Scope cam kết (không thay đổi)

**Trong scope:**
- Chat box nhập câu hỏi tự nhiên
- RAG trên data text slide Day 1–5
- Output: Answer + Source + Next Action
- Xử lý đủ 4 paths với similarity threshold
- 4 câu hỏi demo + 1 failure path

**Ngoài scope (không build trong Day 06):**
- Login/register, dashboard học viên
- Upload tài liệu động từ UI
- Fine-tune model, chấm điểm tự động
- Tích hợp Discord thật
- Nội dung ngoài 5 ngày đầu
