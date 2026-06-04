# Demo Script — AI IN ACTION Copilot

**Thời gian:** 3–5 phút  
**Người thuyết trình:** Phạm Hoàng Anh Kiệt (Thành viên 5)  
**Backup:** Screenshot từ `evidence_screenshot/` nếu demo lỗi

---

## Mở đầu (30 giây)

> "Nhóm mình là C401-Vinflow, làm Track A — Learning OS.
>
> Pain mình tự dùng thật: khi làm hackathon Day 5, mình cần tra lại 'Evidence Pack gồm những phần nào?' — phải mở file PDF 74 trang của Day 4, cuộn tìm thủ công mất 3–5 phút.
>
> Sản phẩm là **AI IN ACTION Copilot** — RAG chatbot tra cứu nội dung giáo trình 6 ngày đầu, trả về Answer + Source + Next Action."

---

## Demo 1 — Happy path (1 phút)

**Nhập câu hỏi vào chat box:**

```
Day 5 cần nộp gì?
```

**Chỉ vào output và giải thích:**
- **Answer:** checklist cụ thể — Evidence Pack và Thin SPEC Draft
- **Source:** "Day 5 · Mini-hackathon instruction" — user có thể tự verify
- **Next Action:** bước tiếp theo — viết Evidence Pack, viết Thin SPEC, chuẩn bị repo

> "Output không chỉ là câu trả lời — còn có nguồn để kiểm tra và next action để biết làm gì tiếp."

---

## Demo 2 — Happy path thứ 2 (45 giây)

**Nhập câu hỏi:**

```
Evidence Pack gồm những phần nào?
```

**Chỉ vào:**
- Answer có đủ 6 phần của Evidence Pack
- Source trỏ đúng tài liệu Day 5
- Next Action gợi ý học viên điền vào template

---

## Demo 3 — Failure path (45 giây)

**Nhập câu hỏi:**

```
Tôi nên mua laptop gaming nào?
```

**Chỉ vào:**
- Copilot **không bịa** — không hallucinate
- Fallback rõ ràng: "Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu."
- Gợi ý user hỏi lại đúng phạm vi

> "Đây là điểm quan trọng nhất: AI học tập mà hallucinate sẽ khiến học viên làm sai assignment. Copilot chọn fallback thay vì trả lời bừa."

---

## Kết luận (30 giây)

> "Toàn bộ flow: **Question → RAG Search → MIMO API → Answer + Source + Next Action**
>
> Build slice cam kết trong Thin SPEC đã chạy được end-to-end.
>
> Sản phẩm dùng **Augmentation**, không phải Automation — AI gợi ý, học viên tự verify và quyết định dùng thông tin nào.
>
> Cảm ơn."

---

## Backup nếu demo lỗi

Nếu app không chạy được, dùng screenshot trong `02-group-spec/evidence_screenshot/` để minh hoạ pain, rồi walk through code trong `codebase/src/rag_chain.py` và `codebase/app.py`.

| Slide backup | Nội dung |
|---|---|
| `day5_slide29_4paths.png` | 4 paths — happy/low-confidence/failure/correction |
| `day4_slide14_RTCF.png` | RTCF framework — ví dụ pain self-use |
| `day5_slide40_thin_spec.png` | Thin SPEC — bằng chứng output khớp spec |

---

## Câu hỏi thường gặp từ giám khảo

| Câu hỏi | Trả lời |
|---|---|
| "Tại sao dùng RAG mà không fine-tune?" | RAG nhanh hơn, không cần GPU, data có thể cập nhật mà không train lại |
| "ChromaDB có scale được không?" | Đủ cho 6 ngày × ~50 slide — scope cam kết trong spec |
| "Tại sao chọn MIMO API?" | Đây là API được khoá học hướng dẫn; có thể swap sang Claude/OpenAI bằng cách đổi 1 file config |
| "User verify source bằng cách nào?" | Source hiển thị tên file + Day — user mở slide gốc kiểm tra |
