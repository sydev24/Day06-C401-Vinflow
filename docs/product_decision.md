# Product Decision — AI IN ACTION Copilot

Tài liệu này ghi lại các quyết định sản phẩm chính và lý do chọn, để giám khảo và thành viên mới hiểu tại sao nhóm build theo cách này.

---

## Quyết định 1: RAG thay vì chatbot chung

**Chọn:** RAG (Retrieval-Augmented Generation) trên data text slide 6 ngày đầu.

**Không chọn:** Chatbot AI chung như ChatGPT/MiMo không có context.

**Lý do:**

Evidence cho thấy pain cụ thể là "không biết tìm ở slide nào khi đang làm lab" — không phải "không có AI để hỏi". Học viên đã có ChatGPT; vấn đề là ChatGPT không biết nội dung giáo trình AI Thực Chiến.

RAG giải quyết đúng pain này: câu trả lời được grounded trên đúng slide, có source để verify. Chatbot generic không giải quyết được.

**Trade-off chấp nhận:** RAG phức tạp hơn, cần build index trước. Nhưng scope chỉ là 6 ngày đầu (~160 trang slide) — đủ nhỏ để build trong 1 ngày.

---

## Quyết định 2: Augmentation thay vì Automation

**Chọn:** Augmentation — AI gợi ý answer + source, user tự verify và quyết định dùng thông tin nào.

**Không chọn:** Automation — AI tự submit bài, tự điền form, tự quyết định.

**Lý do:**

Sản phẩm hỗ trợ học tập. Nếu AI tự quyết và sai, học viên nộp bài sai. Human role phải là Reviewer/Decider.

Augmentation cũng phù hợp với nguyên tắc của khoá học: "AI gợi ý, người quyết."

**Human role cụ thể:**
- **Reviewer:** kiểm tra lại source Copilot đưa ra
- **Decider:** chọn thông tin nào dùng cho bài nộp
- **Rescuer:** nếu AI sai, hỏi lại cụ thể hơn hoặc hỏi mentor

---

## Quyết định 3: Fallback rõ ràng thay vì hallucinate

**Chọn:** Khi câu hỏi ngoài phạm vi tài liệu 6 ngày đầu, trả về fallback cố định:
> "Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu. Bạn có thể hỏi về slide, lab, assignment hoặc framework của chương trình AI Thực Chiến."

**Không chọn:** Để model tự trả lời bằng kiến thức chung.

**Lý do:**

Failure mode nguy hiểm nhất của sản phẩm học tập: AI trả lời tự tin nhưng sai context → học viên hiểu sai yêu cầu assignment, làm sai form, nộp thiếu artifact.

Prompt rule: "Chỉ trả lời dựa trên CONTEXT được cung cấp. Nếu không tìm thấy thông tin liên quan, dùng fallback." Kết hợp với RAG grounding và show source, độ tin cậy cao hơn chatbot chung.

---

## Quyết định 4: ChromaDB thay vì vector DB khác

**Chọn:** ChromaDB (local, in-process).

**Không chọn:** Pinecone, Weaviate, pgvector.

**Lý do:**

- Scope là 6 ngày × ~50 slide — không cần cloud vector DB
- ChromaDB chạy local, không cần API key riêng, không có latency mạng
- Setup đơn giản: `pip install chromadb`, không cần infrastructure
- Phù hợp với constraint "build trong 1 ngày"

**Trade-off chấp nhận:** Không scale lên production lớn. Nhưng scope cam kết trong spec chỉ là 6 ngày đầu — không cần scale.

---

## Quyết định 5: Output bắt buộc có Answer + Source + Next Action

**Chọn:** Mọi response đều có 3 phần: Answer, Source, Next Action.

**Không chọn:** Chỉ trả về answer như chatbot thông thường.

**Lý do từ evidence:**

- Học viên không chỉ cần định nghĩa — cần biết làm gì tiếp (next action)
- Thiếu source → không tin được, không verify được → giảm độ tin cậy
- Pattern này học từ GitHub Copilot Chat (answer + source file) và Notion AI (source link)

Prompt template enforce 3 phần này ở mọi response.

---

## Scope cam kết (không thay đổi)

**Trong scope:**
- Chat box nhập câu hỏi tự nhiên
- RAG trên data text slide Day 1–6
- Output: Answer + Source + Next Action
- Fallback cho câu hỏi ngoài phạm vi
- 4 câu hỏi demo + 1 failure path

**Ngoài scope (không build trong Day 06):**
- Login/register, dashboard học viên
- Upload tài liệu động từ UI
- Fine-tune model, chấm điểm tự động
- Tích hợp Discord thật
- Nội dung ngoài 6 ngày đầu
