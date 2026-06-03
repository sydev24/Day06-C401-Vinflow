# Synthesis & Decision — AI IN ACTION Copilot

## 1. Gom evidence thành cụm

Gom theo **workflow/pain**, không gom theo tên feature:

- **"Không nhớ slide nào"** — học viên biết khái niệm tồn tại nhưng không định vị được trong 300+ trang slide
- **"Hỏi lặp lại trong Discord"** — cùng câu hỏi xuất hiện ≥3 lần/buổi; TA phải trả lời thủ công
- **"Câu trả lời không có nguồn"** — khi hỏi bạn bè hoặc Google, không chắc đáp án đúng với context khoá học này
- **"Mất tập trung khi đang code"** — phải rời IDE để mở PDF, tìm kiếm, rồi quay lại → mất flow

## 2. Insight

```text
Học viên AI Thực Chiến không chỉ cần một chatbot.
Họ thật ra cần tra cứu đúng context khoá học, đúng lúc (trong 40 phút lab),
vì slide nhiều và không có semantic search — tra thủ công vừa chậm vừa dễ tìm sai nguồn.
```

## 3. Opportunity

```text
Cơ hội là dùng RAG để augment quá trình học/làm lab:
nhận câu hỏi tự nhiên → tìm đoạn liên quan nhất trong ChromaDB → trả answer + source (Day X, section Y) + next action,
trong khi vẫn kiểm soát failure bằng fallback rõ khi câu hỏi ngoài scope khoá học.
```

## 4. Kiểm tra build slice

| Câu hỏi | Kết quả |
|---|---|
| User cụ thể chưa? | **Đạt** — học viên Batch 02 đang làm lab/hackathon, cần tra nhanh nội dung slide |
| Task đủ hẹp chưa? | **Đạt** — một câu hỏi → RAG → answer + source, demo trong < 2 phút |
| AI decision rõ chưa? | **Đạt** — AI chọn chunk liên quan nhất, generate answer, gắn source |
| Failure path rõ chưa? | **Đạt** — câu hỏi ngoài scope (hỏi về tin tức, code ngoài khoá) → fallback thay vì hallucinate |
| Có evidence không? | **Đạt** — Discord observation, self-use timing, slide volume count |

## 5. Quyết định: giữ, giảm scope, hay đổi hướng?

| Tình huống | Quyết định |
|---|---|
| Build full chatbot đa chức năng | Không — cắt xuống một flow: hỏi → RAG → answer + source + next action |
| Thêm quiz generator | Vào backlog — không build Day 06 |
| Thêm voice input | Vào backlog |
| RAG trên tài liệu ngoài khoá học | Không — scope cố định là 6 ngày slide; ngoài đó fallback |

## 6. Câu chốt

```text
Dựa trên evidence (Discord observation: câu hỏi lặp ≥3 lần/buổi; self-use: tra slide mất 3–5 phút),
nhóm sẽ build RAG chatbot trả lời câu hỏi về nội dung 6 ngày khoá học AI Thực Chiến,
cho học viên Batch 02 đang làm lab hoặc hackathon,
để giải quyết pain "không tra được theo ngữ nghĩa dưới áp lực thời gian",
bằng cách AI augment bằng RAG → answer + source (Day X, section Y) + next action gợi ý,
và sẽ test failure path: câu hỏi ngoài scope → fallback rõ, không hallucinate.
```

## 7. 4 Paths — RAG Copilot

### Path 1 · Happy

```text
Nếu user hỏi câu trong scope khoá học ("tool_choice là gì?", "4 paths gồm những gì?"),
AI retrieve được chunk có similarity cao (≥0.75) và generate answer tự tin,
hậu quả nếu sai là user tin vào answer sai và áp dụng nhầm trong lab.

Prototype sẽ xử lý bằng: hiển thị answer + source rõ (Day X · section Y) + 1 gợi ý next action,
user thấy nguồn và có thể tự verify slide gốc.
Owner kiểm thử path này là Lê Đình Sỹ.
```

### Path 2 · Low-confidence

```text
Nếu user hỏi câu mơ hồ ("AI tools có mấy loại?") hoặc similarity score thấp (0.40–0.74)
vì nhiều chunk cùng liên quan từ nhiều Day khác nhau,
AI có thể chọn nhầm chunk và trả lời không đúng context ngày/section user đang làm,
hậu quả là user bị dẫn sang nội dung sai buổi.

Prototype sẽ xử lý bằng: hỏi lại "Bạn đang làm lab Day mấy?" hoặc hiển thị
2–3 chunk liên quan nhất kèm tên section để user tự chọn, không tự generate.
Owner kiểm thử path này là Vũ Văn Huy.
```

### Path 3 · Failure

```text
Nếu user hỏi ngoài scope khoá học ("ChatGPT 5 ra mắt khi nào?", "viết code Python cho tôi"),
AI có thể hallucinate câu trả lời hoặc trả lời generic không liên quan đến khoá,
hậu quả là user mất niềm tin vào toàn bộ app sau khi phát hiện câu trả lời bịa.

Prototype sẽ xử lý bằng: fallback rõ ràng —
"Câu này ngoài nội dung 6 ngày AI Thực Chiến. Hãy hỏi TA hoặc tìm tài liệu ngoài khoá."
Không generate answer khi không có chunk đủ similarity (<0.40).
Owner kiểm thử path này là Lê Đình Sỹ.
```

### Path 4 · Correction

```text
Nếu user thấy answer sai hoặc source không đúng và bấm "Báo sai" hoặc gõ lại câu hỏi,
AI không tự biết mình sai và sẽ lặp lại lỗi tương tự với user khác,
hậu quả là lỗi hệ thống không cải thiện được và mất signal học.

Prototype sẽ xử lý bằng: ghi lại (câu hỏi + answer + chunk được chọn + feedback)
vào correction log; hiển thị "Cảm ơn — đã ghi lại để cải thiện."
Owner kiểm thử path này là Vũ Văn Huy + Lê Đình Sỹ.
```

## 8. Backlog (không build trong Day 06)

- Quiz generator từ nội dung slide
- Voice input / speech-to-text
- Lịch sử chat / session memory
- RAG trên tài liệu ngoài khoá (Stack Overflow, docs thư viện)
- Cá nhân hoá theo tiến độ học từng học viên
