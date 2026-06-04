# Thin SPEC Cuối Day 05

## Project: AI IN ACTION Copilot

Thin SPEC không phải PRD đầy đủ. Đây là bản cam kết đủ rõ để sáng Day 06 nhóm build ngay.

---

## 1. Track, product/app và user

**Track:** Learning OS

**Product/app thật:** AI IN ACTION Copilot

**User cụ thể:**
Học viên chương trình AI Thực Chiến, đặc biệt là học viên đang làm assignment, mini-hackathon hoặc cần tra cứu lại nội dung trong slide 6 ngày đầu.

**Nhóm có phải user thật không? Nếu không, khác ở đâu?**
Có. Nhóm Vinflow cũng là học viên đang học chương trình AI Thực Chiến, đang phải đọc slide, hiểu assignment, viết Evidence Pack, Thin SPEC và chuẩn bị demo Day 06.

Điểm khác là nhóm đang trực tiếp build sản phẩm nên hiểu kỹ hơn về workflow kỹ thuật. User thật ngoài nhóm có thể ít hiểu RAG/API hơn, nên output của Copilot phải ngắn, rõ, có nguồn và có next action.

---

## 2. Evidence summary

| Evidence                                                                                                                                               | Nguồn                                                        | User/pain nói lên điều gì?                                                                   | SPEC phải đổi gì?                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Khi muốn biết “Day 5 cần nộp gì?”, học viên phải tự mở slide hoặc tài liệu, tìm đúng phần Evidence Pack và Thin SPEC.                                  | Self-use: nhóm tự dùng slide/folder tài liệu của 6 ngày đầu. | Học viên có tài liệu nhưng tìm lại thông tin mất thời gian và dễ bỏ sót.                     | Build slice phải tập trung vào hỏi đáp trên giáo trình, không làm LMS rộng.                 |
| Khi đọc phần Evidence Pack / Thin SPEC, học viên vẫn phải tự tổng hợp thành checklist cần làm.                                                         | Self-use khi nhóm làm Day 05.                                | User không chỉ cần định nghĩa, mà cần output dạng checklist/action.                          | Output bắt buộc có Answer / Source / Next Action.                                           |
| Khi hỏi chatbot AI chung như ChatGPT/MiMo nếu không đưa context, AI có thể trả lời theo kiến thức chung, không chắc đúng với giáo trình AI Thực Chiến. | Competitor/analog test với chatbot AI chung.                 | AI trả lời nhanh nhưng thiếu grounding và thiếu nguồn kiểm chứng.                            | Phải dùng RAG trên data text giáo trình và luôn hiển thị nguồn.                             |
| Nhiều câu hỏi có thể bị lặp lại như “Evidence Pack gồm gì?”, “Thin SPEC là gì?”, “Prototype Level 3 yêu cầu gì?”                                       | Quan sát trong quá trình học và làm assignment nhóm.         | Mentor/TA có thể mất thời gian trả lời lặp lại các câu có trong giáo trình.                  | Copilot cần ưu tiên các câu hỏi lặp về assignment, framework, prototype và yêu cầu nộp bài. |
| Nếu hỏi ngoài phạm vi như “Tôi nên mua laptop gaming nào?”, chatbot chung vẫn có thể trả lời.                                                          | Failure path test.                                           | Với sản phẩm học tập dựa trên giáo trình, trả lời ngoài tài liệu có thể làm giảm độ tin cậy. | Cần fallback: “Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu.”                 |

---

## 3. Pain statement

```text
User học viên AI Thực Chiến đang gặp khó ở bước tìm lại, hiểu và áp dụng nội dung trong giáo trình 6 ngày đầu,
vì tài liệu nằm trong nhiều slide/file khác nhau và học viên phải tự đọc, tự tìm, tự tổng hợp thành checklist/action,
dẫn tới mất thời gian, dễ bỏ sót yêu cầu nộp bài và phải hỏi lại mentor/TA hoặc nhóm học.
Bằng chứng chính là self-use observation khi nhóm phải tìm lại yêu cầu Day 5, Evidence Pack, Thin SPEC và build slice trong slide/tài liệu.
```

---

## 4. Build slice

```text
Cho học viên AI Thực Chiến đang làm assignment hoặc mini-hackathon,
prototype sẽ dùng AI để augment hành động tra cứu và tổng hợp giáo trình 6 ngày đầu,
tạo ra câu trả lời ngắn gọn kèm nguồn và next action,
và xử lý failure mode AI trả lời ngoài phạm vi bằng fallback: “Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu.”
```

Build slice cuối cùng:

```text
Question → RAG Search → API Model Answer → Source Citation → Next Action
```

Ví dụ:

```text
User hỏi:
“Day 5 cần nộp gì?”

Copilot trả lời:
- Day 5 cần nộp Evidence Pack và Thin SPEC Draft.
- Nguồn: Day 5 / Mini-hackathon instruction.
- Next action: viết Evidence Pack, Thin SPEC và chuẩn bị repo demo.
```

---

## 5. Auto/Aug decision

Chọn một:

* [x] **Augmentation:** AI gợi ý/draft/phân loại, user quyết cuối.
* [ ] **Conditional automation:** AI tự làm trong case hẹp; case mơ hồ/rủi ro chuyển người.
* [ ] **Automation:** AI tự quyết và tự hành động.

**Lý do chọn:**
AI IN ACTION Copilot không thay thế mentor, TA hoặc LMS. Sản phẩm chỉ hỗ trợ học viên tra cứu nhanh giáo trình, tóm tắt nội dung, tạo checklist và gợi ý bước tiếp theo. Học viên vẫn phải kiểm tra nguồn và tự quyết định cách dùng câu trả lời cho bài nộp.

**Human role:**
Reviewer / Decider / Rescuer

Cụ thể:

* **Reviewer:** học viên kiểm tra lại nguồn được Copilot đưa ra.
* **Decider:** học viên quyết định dùng thông tin nào cho bài nộp.
* **Rescuer:** nếu AI không tìm thấy hoặc trả lời chưa đúng, học viên hỏi lại cụ thể hơn hoặc hỏi mentor/TA.

---

## 6. Four paths

| Path           | Prototype phải thể hiện gì?                                                                                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Happy          | User hỏi câu có trong giáo trình, ví dụ “Day 5 cần nộp gì?”. Prototype phải trả lời đúng, có checklist, có nguồn và next action.                                                      |
| Low-confidence | User hỏi câu mơ hồ, ví dụ “Tôi cần làm gì cho project?”. Prototype phải trả lời phần liên quan trong tài liệu, đồng thời gợi ý user hỏi cụ thể hơn theo Day, artifact hoặc framework. |
| Failure        | User hỏi ngoài phạm vi giáo trình, ví dụ “Tôi nên mua laptop gaming nào?”. Prototype không được bịa, phải fallback: “Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu.”     |
| Correction     | User sửa lại câu hỏi, ví dụ “Không phải, tôi hỏi về Thin SPEC Draft”. Prototype phải search lại theo context mới và trả lời theo tài liệu liên quan đến Thin SPEC.                    |

---

## 7. Failure mode nguy hiểm nhất

```text
Nếu user hỏi một câu ngoài phạm vi giáo trình hoặc câu hỏi có rủi ro sai context,
AI có thể trả lời tự tin bằng kiến thức chung thay vì dựa trên tài liệu AI Thực Chiến,
hậu quả là học viên có thể hiểu sai yêu cầu assignment, làm sai form hoặc nộp thiếu artifact.
Prototype sẽ xử lý bằng RAG grounding, show source, prompt rule “chỉ trả lời dựa trên CONTEXT” và fallback khi không tìm thấy thông tin.
Owner kiểm thử path này là Thành viên 4 – QA/Test.
```

Failure test bắt buộc:

```text
Question:
Tôi nên mua laptop gaming nào?

Expected:
Mình chưa tìm thấy thông tin này trong tài liệu 6 ngày đầu. Bạn có thể hỏi về slide, lab, assignment hoặc framework của chương trình AI Thực Chiến.
```

---

## 8. Owner plan cho sáng Day 06

| Thành viên                                           | Việc phụ trách                                                                                           | Bằng chứng cần có trong repo                                                                                                                               |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vũ Quốc Bảo (2A202600541) – Data owner              | Research / evidence + chuẩn bị data text từ slide 6 ngày đầu, chunking, embedding, vector DB, retriever. | `data/raw_text/`, `data/processed/chunks.jsonl`, `data/processed/manifest.json`, `data/vectorstore/chroma/`, `src/retriever.py`, screenshot inspect index. |
| Vũ Văn Huy (2A202600750) – Backend RAG + API        | RAG logic + prompt rule + hàm `ask_copilot(question)`, đảm bảo output đúng Answer / Source / Next Action. | `src/prompt.py`, `src/rag_chain.py`, `src/ask_copilot.py`, `.env.example`.                                                                                 |
| Nguyễn Trung Kiên (2A202600969) – Frontend owner    | Prototype UI Streamlit, chat box, loading, hiển thị answer/source/next action, sidebar câu hỏi demo.     | `app.py`, screenshot UI, demo chạy được bằng `streamlit run app.py`.                                                                                       |
| Lê Đình Sỹ (2A202600770) – QA / Test owner          | Test happy path, low-confidence path, failure path, correction path.                                     | `docs/test_cases.md`, `docs/demo_questions.md`, screenshot kết quả test, bảng pass/fail.                                                                   |
| Phạm Hoàng Anh Kiệt (2A202600797) – Repo / SPEC owner | README, evidence pack, thin spec, demo script, chuẩn bị repo để nộp và thuyết trình 3–5 phút.          | `README.md`, `docs/demo_script.md`, `02-group-spec/evidence-pack-template.md`, `02-group-spec/thin-spec-template.md`, video/screenshot backup nếu demo lỗi. |

---

## 9. Scope cam kết cho Day 06

### Build trong Day 06

1. Chat box nhập câu hỏi.
2. RAG search trên data text slide 6 ngày đầu.
3. API model trả lời dựa trên context.
4. Output có Answer / Source / Next Action.
5. Có fallback khi không tìm thấy thông tin.
6. Có ít nhất 4 câu hỏi demo:

   * “Day 5 cần nộp gì?”
   * “Evidence Pack gồm những phần nào?”
   * “Thin SPEC Draft là gì?”
   * “Prototype Level 3 yêu cầu gì?”
7. Có 1 câu hỏi failure:

   * “Tôi nên mua laptop gaming nào?”

### Không build trong Day 06

1. Login/register.
2. Dashboard học viên.
3. LMS hoàn chỉnh.
4. Tích hợp Discord thật.
5. Upload tài liệu động từ UI.
6. Fine-tune model.
7. Chấm điểm assignment tự động.
8. Tracking tiến độ học tập.
9. Xử lý toàn bộ chương trình ngoài 6 ngày đầu.

---

## 10. Success criteria

MVP được xem là đạt nếu:

1. User nhập được câu hỏi.
2. Hệ thống tìm được chunk liên quan trong data text.
3. API model trả lời dựa trên context.
4. Có phần Answer rõ ràng.
5. Có phần Source để user kiểm tra.
6. Có phần Next Action để user biết bước tiếp theo.
7. Có fallback khi hỏi ngoài phạm vi.
8. Demo end-to-end chạy được trong 3–5 phút.
9. Repo có README hướng dẫn chạy.
10. Evidence Pack và Thin SPEC khớp với prototype thực tế.
