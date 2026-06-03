# Evidence Pack — AI IN ACTION Copilot

## 1. Nhóm và track

**Tên nhóm:** AI IN ACTION Copilot Team  
**Track:** A · Learning OS (Vin AI Thực Chiến)  
**Product/app đã chọn:** App RAG chatbot standalone — tra cứu nội dung khoá học AI Thực Chiến  
**Build slice đang nghĩ:** RAG chatbot tra cứu nội dung slide khoá học, trả về answer + source + next action

## 2. Self-use evidence

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| Khi làm lab Day 3, cần nhớ lại cách dùng `tool_choice` trong Claude API — phải mở slide tìm thủ công mất 3–5 phút | — | Failure: tìm không ra, bỏ qua | Học viên không nhớ slide nào chứa thông tin cụ thể; search Discord cũng không ra vì câu hỏi dùng từ khác |
| Câu hỏi "prompt caching hoạt động thế nào?" được hỏi lại ít nhất 3 lần trong Discord lớp trong cùng một buổi | Discord #general-batch02 | Failure: không có công cụ tra cứu nhanh, phải chờ TA hoặc cuộn slide | Cùng một câu hỏi lặp lại → không ai có nơi tra nhanh mà không làm phiền TA |
| Slide Day 5 có 53 trang, không có mục lục/search — khi cần tìm "4 paths" phải cuộn thủ công | — | Low-confidence: không chắc tìm đúng slide | Lượng nội dung lớn, không có cơ chế tra cứu theo ngữ nghĩa |

## 3. User / review / social evidence

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Hỏi TA xong quên mất rồi, không biết tìm lại ở đâu" | Quan sát trực tiếp trong lớp Day 4 | Học viên batch 02 | Không có nơi tra lại câu trả lời đã được giải thích |
| "Slide nhiều quá, em không nhớ Day mấy nói về augmentation vs automation" | Discord #questions-batch02 | Học viên batch 02 | Nội dung phân tán trên 6 ngày, không tra được theo khái niệm |
| Trong 30 phút hackathon, có ≥5 câu hỏi trùng nhau về "build slice là gì" được hỏi trong Discord | Discord #day05-batch02 | Học viên đang làm lab | Câu trả lời có trong slide nhưng học viên không tìm ra nhanh dưới áp lực thời gian |

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| GitHub Copilot Chat (trong IDE) | Trả lời câu hỏi về codebase theo ngữ cảnh, kèm source file + line number | Answer + source là baseline tối thiểu; không có source = không tin được | Có — đây chính là RAG pattern cơ bản |
| Khan Academy Khanmigo | Không cho đáp án thẳng; gợi ý next step để học viên tự suy | Augmentation tốt hơn automation trong học tập: AI gợi ý, người quyết | Có — thêm next action vào response |
| Notion AI (Q&A trên workspace) | Tìm kiếm semantic trong workspace, trả lời kèm link nguồn | Confidence display + source link giúp user tự verify | Có — hiển thị section nguồn thay vì chỉ page |

## 5. Evidence → Insight

```text
Evidence nổi bật nhất:
- Học viên hỏi lặp lại cùng câu hỏi ≥3 lần trong một buổi (Discord observation)
- Tra slide thủ công mất 3–5 phút, dùng keyword sai thì không ra (self-use)
- 53 trang slide/ngày × 6 ngày = ~300 trang không có semantic search

Insight:
Học viên AI Thực Chiến không chỉ thiếu thông tin.
Thật ra họ cần tra cứu theo ngữ nghĩa đúng lúc — trong 40 phút làm lab hoặc hackathon
khi không có thời gian cuộn slide hay chờ TA.

Opportunity:
AI có thể augment bằng cách nhận câu hỏi tự nhiên, tìm đoạn slide liên quan nhất qua RAG,
trả về answer + nguồn cụ thể (Day X, section Y) + gợi ý next step,
trong khi fallback rõ ràng khi câu hỏi ngoài scope thay vì hallucinate.
```

## 6. Evidence đổi SPEC như thế nào?

- [x] Đổi user chính: ban đầu nghĩ "mọi người dùng LMS" → thu hẹp thành "học viên đang làm lab/hackathon dưới áp lực thời gian"
- [x] Đổi pain statement: ban đầu "khó tìm slide" → thực ra "không tra được theo ngữ nghĩa khi đang code"
- [x] Đổi build slice: bỏ ý định build full chatbot → chỉ build một flow: hỏi → RAG → answer + source + next action
- [x] Đổi Auto/Aug decision: chọn augmentation (AI gợi ý, user verify source) thay vì automation
- [x] Đổi 4 paths → xem `synthesis-decide-toolkit.md` Section 7: Happy / Low-confidence / Failure / Correction
- [x] Đổi failure mode → Failure path: câu ngoài scope → fallback rõ, không hallucinate (owner: Lê Đình Sỹ)
- [x] Đổi owner/test plan → Vũ Văn Huy: backend + low-confidence/correction; Lê Đình Sỹ: QA happy/failure path

```text
Trước evidence, nhóm định build chatbot trả lời câu hỏi chung về AI.
Sau evidence, nhóm đổi thành RAG trên đúng nội dung 6 ngày khoá học, kèm source.
Lý do: evidence cho thấy pain cụ thể là "không biết tìm ở slide nào" — không phải "không có AI".
Chatbot generic không giải quyết pain này; RAG với source mới giải quyết được.
```
