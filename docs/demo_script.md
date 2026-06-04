# Demo Script — AI IN ACTION Copilot

---

## Mở đầu

> "Nhóm mình là C401-Vinflow, làm Track A — Learning OS.
>
> Pain nhóm tự dùng thật: khi làm hackathon Day 5, cần tra lại Thin SPEC gồm những phần nào?' — phải mở PDF 53 trang của Day 5, cuộn tìm thủ công mất 3-5 phút. Không có semantic search, nhấn Ctrl+F không được. [Day 5 slide 40 — Thin SPEC]
>
> Sản phẩm là **AI IN ACTION Copilot** — RAG chatbot tra cứu nội dung giáo trình 6 ngày đầu, trả về Answer + Source + Next Action."

---

## Demo 1 — Happy path

**Câu hỏi nhập vào:**

```
Day 5 cần nộp gì?
```

**Chỉ vào output:**
- **Answer:** checklist cụ thể — Evidence Pack và Thin SPEC Draft
- **Source:** "Day 5 · Mini-hackathon instruction" — user tự verify được
- **Next Action:** viết Evidence Pack, viết Thin SPEC, chuẩn bị repo demo

> "Output không chỉ là câu trả lời — còn có nguồn để kiểm tra và next action để biết làm gì tiếp."

**Câu hỏi thứ 2:**

```
Evidence Pack gồm những phần nào?
```

Chỉ vào source trỏ đúng tài liệu Day 5 và next action gợi ý học viên điền vào template.

---

## Demo 2 — Low-confidence path

**Câu hỏi nhập vào (mơ hồ):**

```
Tôi cần làm gì cho project?
```

**Chỉ vào output:**
- Copilot **không tự generate** câu trả lời chung chung
- Hiển thị 2–3 chunk liên quan nhất kèm tên section để user tự chọn
- Hoặc hỏi lại: "Bạn đang làm lab Day mấy?" để thu hẹp scope

> "Câu mơ hồ có thể khớp với nhiều Day khác nhau — thay vì đoán sai, Copilot để user chọn đúng context."

---

## Demo 3 — Failure path

**Câu hỏi nhập vào (ngoài phạm vi):**

```
Tôi nên mua laptop gaming nào?
```

**Chỉ vào output — fallback:**

```
Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu.
Bạn có thể hỏi về slide, lab, assignment hoặc framework của chương trình AI Thực Chiến.
```

> "Đây là điểm quan trọng nhất: AI học tập mà hallucinate sẽ khiến học viên làm sai assignment. Copilot không generate khi similarity score < 0.40 — chọn fallback thay vì bịa."

---

## Demo 4 — Correction path

**Kịch bản:** user thấy answer chưa đúng và sửa lại câu hỏi.

```
Không phải, tôi hỏi về Thin SPEC Draft chứ không phải Evidence Pack.
```

**Chỉ vào output:**
- Copilot search lại theo context mới
- Trả lời đúng về Thin SPEC Draft với source và next action phù hợp

> "Copilot không bị stuck với câu hỏi cũ — nhận correction và search lại ngay."

---

## Kết luận

> "Toàn bộ flow: **Question → RAG Search (ChromaDB) → MIMO API → Answer + Source + Next Action**
>
> Build slice cam kết trong Thin SPEC đã chạy end-to-end với đủ 4 paths.
>
> Sản phẩm dùng **Augmentation** — AI gợi ý, học viên tự verify và quyết định.
>
> Cảm ơn."

---

## Câu hỏi thường gặp từ giám khảo

| Câu hỏi | Trả lời |
|---|---|
| "Tại sao dùng RAG mà không fine-tune?" | RAG nhanh hơn, không cần GPU, data cập nhật được mà không train lại |
| "ChromaDB có scale được không?" | Đủ cho 6 ngày × ~50 slide — đúng scope cam kết trong spec |
| "Tại sao chọn MIMO API?" | API được khoá học hướng dẫn; có thể swap bằng cách đổi 1 file config |
| "User verify source bằng cách nào?" | Source hiển thị tên file + Day — user mở slide gốc kiểm tra |
| "Low-confidence xử lý thế nào?" | Similarity 0.40–0.74: hiển thị 2–3 chunk kèm section để user tự chọn, không tự generate |
