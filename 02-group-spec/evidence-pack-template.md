# Evidence Pack — AI IN ACTION Copilot

## 1. Nhóm và track

**Tên nhóm:** AI IN ACTION Copilot Team  
**Track:** A · Learning OS (Vin AI Thực Chiến)  
**Product/app đã chọn:** App RAG chatbot standalone — tra cứu nội dung khoá học AI Thực Chiến  
**Build slice đang nghĩ:** RAG chatbot tra cứu nội dung slide khoá học, trả về answer + nguồn (Day X, slide Y) + next action

## 2. Self-use evidence

| Observation | Screenshot/link | Path liên quan | Điều học được |
|---|---|---|---|
| Khi làm lab Day 3, cần nhớ lại cách dùng `tool_choice` trong Claude API — phải mở PDF Day 4 (74 trang), cuộn tìm phần Tool declaration thủ công mất 3–5 phút | [Day 4 agenda 74 trang](evidence_screenshot/day4_agenda_74trang.png) | Failure: tìm không ra, bỏ qua bước đó | Cùng một khái niệm (`tool_choice`) dùng keyword khác nhau ở các slide khác nhau — Ctrl+F không đủ |
| Day 5 slide 29/53 giải thích "4 paths" (happy/low-confidence/failure/correction) — khi làm hackathon cần tra lại path nào là gì, nhưng không nhớ đây là slide Day 5 block 3 hay block 4 | [Day 5 slide 29 — 4 paths](evidence_screenshot/day5_slide29_4paths.png) | Low-confidence: phải mở lại toàn bộ Day 5 slide, cuộn từng trang để tìm | Day 4 có 74 trang, Day 5 có 53 trang — không có semantic search, Ctrl+F chỉ tìm được chính xác từ khoá |
| Day 4 slide 14/74 dạy framework "Role · Task · Context · Format" — đến buổi hackathon Day 5 cần nhớ lại scaffold này để viết prompt, nhưng không nhớ nó ở Day mấy | [Day 4 slide 14 — RTCF framework](evidence_screenshot/day4_slide14_RTCF.png) | Failure: không nhớ Day 4 slide 14, phải đoán và tìm lại từ đầu | Kiến thức trải đều trên nhiều ngày, không có cơ chế tra theo khái niệm |

## 3. User / review / social evidence

| Quote / review / observation | Nguồn | User là ai? | Pain/failure mode |
|---|---|---|---|
| "Thầy giải thích xong rồi, nhưng về lab em không còn nhớ slide đó ở đâu nữa" | [Day 4 agenda — 74 trang 5 section](evidence_screenshot/day4_agenda_74trang.png) | Học viên khóa 2 | Day 4 có 74 slide chia 5 section — giảng viên giảng liên tục, học viên không ghi kịp reference |
| "Slide nhiều quá, em không nhớ Day mấy nói về augmentation vs automation" | [Day 5 — Augmentation vs Automation](evidence_screenshot/day5_augmentation_vs_automation.png) | Học viên khóa 2 | Nội dung này ở Day 5 Block 2 slide 14/53 — nhưng không tra được nếu không nhớ keyword chính xác |
| Trong 30 phút hackathon Day 5, nhiều học viên dừng code để mở PDF tìm lại định nghĩa "build slice" và "thin SPEC" | [Day 5 slide 40 — Thin SPEC](evidence_screenshot/day5_slide40_thin_spec.png) | Học viên khóa 2 đang làm hackathon | Day 5 slide 40/53 có bảng thin SPEC đầy đủ, nhưng dưới áp lực thời gian không ai biết chính xác slide mấy |
| TA phải giải thích lại cùng khái niệm (automation ladder, 4 paths, context packet) cho nhiều nhóm khác nhau trong cùng một buổi lab | [Day 5 agenda — 53 trang](evidence_screenshot/day5_agenda_53trang.png) · [Day 3 mục lục](evidence_screenshot/day3_muc_luc.png) | TA khoá học | Câu trả lời đã có trong slide nhưng học viên không tìm nhanh được → TA tốn thời gian lặp lại |

## 4. Competitor / analog evidence

| App / mô hình tham khảo | Họ xử lý task này thế nào? | Pattern học được | Có áp dụng trong 1 ngày không? |
|---|---|---|---|
| GitHub Copilot Chat (trong IDE) | Trả lời câu hỏi về codebase theo ngữ cảnh, kèm source file + line number | Answer + source là baseline tối thiểu; không có source = không tin được | Có — đây chính là RAG pattern cơ bản |
| Khan Academy Khanmigo | Không cho đáp án thẳng; gợi ý next step để học viên tự suy | Augmentation tốt hơn automation trong học tập: AI gợi ý, người quyết | Có — thêm next action vào response |
| Notion AI (Q&A trên workspace) | Tìm kiếm semantic trong workspace, trả lời kèm link nguồn | Confidence display + source link giúp user tự verify | Có — hiển thị "Day X · slide Y/Z" thay vì chỉ trả lời chung |

## 5. Evidence → Insight

```text
Evidence nổi bật nhất:
- Day 3: ~34 trang · Day 4: 74 trang · Day 5: 53 trang = ~160+ trang PDF chỉ 3 ngày
  (chưa tính Day 1, 2) — không có semantic search, chỉ có Ctrl+F
- Học viên dừng hackathon để mở PDF tìm lại "build slice", "4 paths",
  "automation ladder" — mất 3–5 phút mỗi lần (self-use observation)
- TA lặp lại cùng câu giải thích nhiều lần trong một buổi lab vì không
  có công cụ tra nhanh

Insight:
Học viên khóa 2 không thiếu nội dung — nội dung đã được trình bày đầy đủ
trong slideshow từng ngày.
Vấn đề là họ cần tra cứu theo ngữ nghĩa đúng lúc: trong 30–40 phút làm lab
hoặc hackathon khi không có thời gian cuộn 74 trang PDF hay chờ TA giải thích lại.

Opportunity:
RAG trên toàn bộ slide khoá học: nhận câu hỏi tự nhiên ("4 paths là gì?",
"thin SPEC gồm những gì?"), tìm đoạn slide liên quan nhất, trả về
answer + nguồn cụ thể (Day X · slide Y/Z · section name) + gợi ý next step.
Fallback rõ ràng khi câu hỏi ngoài scope slide — không hallucinate.
```

## 6. Evidence đổi SPEC như thế nào?

- [x] Đổi user chính: ban đầu nghĩ "mọi người cần học AI" → thu hẹp thành "học viên khóa 2 đang làm lab/hackathon dưới áp lực thời gian"
- [x] Đổi pain statement: ban đầu "slide nhiều" → thực ra "không tra được theo ngữ nghĩa khi đang code, Ctrl+F không đủ vì không nhớ keyword chính xác"
- [x] Đổi build slice: bỏ ý định build full chatbot → chỉ build một flow: hỏi → RAG trên slide → answer + nguồn (Day X, slide Y) + next action
- [x] Đổi Auto/Aug decision: chọn augmentation (AI gợi ý answer + source, user verify) thay vì automation
- [x] Đổi 4 paths → xem `synthesis-decide-toolkit.md` Section 7: Happy / Low-confidence / Failure / Correction
- [x] Đổi failure mode → Failure path: câu ngoài scope slide → fallback rõ, không hallucinate (owner: Lê Đình Sỹ)
- [x] Đổi owner/test plan → Vũ Văn Huy: backend RAG + low-confidence/correction; Lê Đình Sỹ: QA happy/failure path

```text
Trước evidence, nhóm định build chatbot trả lời câu hỏi chung về AI.
Sau evidence, nhóm đổi thành RAG trên đúng nội dung khoá học
(Day 3 ~34 trang + Day 4 74 trang + Day 5 53 trang + ...), kèm source slide cụ thể.
Lý do: evidence cho thấy pain cụ thể là "không biết tìm ở slide nào khi đang làm lab"
— không phải "không có AI để hỏi".
Chatbot generic không giải quyết pain này; RAG với source "Day 4 · slide 14/74" mới giải quyết được.
```
