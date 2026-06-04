# QA / Evaluation Report - AI IN ACTION Copilot

**Người phụ trách:** Lê Sỹ - Người 4    QA / Evaluation / Demo Test  
**Ngày chạy test:** 2026-06-04  
**File log:** `C:\Users\Asus\AI_Labs\Day06-C401-Vinflow\codebase\data\logs\test_results_20260604_112552.csv`  
**Bộ test:** `data/test_cases.csv`

## 1. Mục tiêu và Phương pháp test

**Mục tiêu:**
Kiểm tra đánh giá toàn diện hệ thống AI Copilot trên bộ câu hỏi `test_cases.csv` nhằm đảm bảo hệ thống đáp ứng đủ các tiêu chí kỹ thuật và trải nghiệm người dùng trước khi tiến hành demo. Các khía cạnh được đánh giá bao gồm:

- **Độ chính xác (Accuracy):** Khả năng truy xuất và trả lời đúng các câu hỏi fact-based (dựa trên sự thật) từ tài liệu khóa học Day 1 đến Day 5.
- **Khả năng suy luận (Reasoning):** Đánh giá việc AI kết hợp nhiều luồng thông tin để so sánh và giải thích các khái niệm phức tạp (ví dụ: Agent vs Chatbot, Automation vs Augmentation).
- **Khả năng xử lý ngoại lệ (Fallback Handling):** Đánh giá hành vi của AI khi đối mặt với các câu hỏi nằm ngoài phạm vi khóa học, câu hỏi thiếu dữ kiện hoặc mơ hồ. AI phải biết từ chối khéo léo thay vì bịa đặt (hallucination).
- **Trải nghiệm UX:** Chatbot có trả lời kèm nguồn (source) minh bạch và đề xuất bước đi tiếp theo (next action) hợp lý hay không.
- **Hiệu năng (Performance):** Đo lường độ trễ (latency) của từng câu trả lời trong điều kiện chạy thực tế.

**Phương pháp:**
Sử dụng script chạy tự động `run_test_copilot.py` để gửi lần lượt 20 câu hỏi vào hệ thống RAG và ghi nhận phản hồi. Sau đó, kết quả được đối chiếu thủ công (human review) với `Ground Truth` đã chuẩn bị sẵn để chấm điểm PASS/FAIL.

## 2. Kết quả tổng quan

Hệ thống được chạy trên tập 20 test cases. Dưới đây là bảng tổng hợp kết quả chi tiết:

| Chỉ số | Kết quả |
|---|---:|
| Tổng số test cases hợp lệ | 20 |
| Số câu trả lời đạt (PASS) | 18 |
| Số câu trả lời sai/lỗi (FAIL) | 2 |
| Tỉ lệ chính xác (Accuracy) | 90% |
| Độ trễ trung bình (Latency) | ~21s |
| Độ trễ cao nhất | Test #3 - ~133s |

**Nhận định nhanh:** 
Hệ thống thể hiện sự ổn định cao và hoàn toàn đủ tiêu chuẩn để tham gia demo prototype. Đa số các câu hỏi fact-based và reasoning đều được AI trả lời đúng trọng tâm, văn phong tự nhiên và luôn trích dẫn nguồn rõ ràng. Các lỗi còn tồn đọng rất ít, chủ yếu xoay quanh việc tìm kiếm tài liệu (retriever) bị sót ở một số câu đặc thù và xử lý chưa thực sự tinh tế đối với các câu hỏi quá mơ hồ.

## 3. Phân tích chi tiết các case FAIL

Hệ thống hiện ghi nhận 2 case FAIL. Việc phân tích các case này giúp nhóm nhận diện rõ điểm yếu của RAG chain để khắc phục trong phiên bản tới.

### Test #4 - Lỗi truy xuất dữ liệu (Retrieval miss)

**Loại câu hỏi:** Fact-based (Day 2)  
**Câu hỏi:** Ba mức giải pháp hệ thống AI được đề cập trong Day 2 là gì?  
**Ground truth mong đợi:** Rule / Script, LLM Feature, và Agent.  
**Kết quả thực tế:** AI phản hồi rằng trong context không có thông tin này, sau đó lấy nhầm sang các đoạn tài liệu nói về `Model + Context + Planning + Tools` và các lý do doanh nghiệp đầu tư vào AI.

**Đánh giá:** 
Đây là một lỗi `retrieval miss` điển hình. Mặc dù câu hỏi rất rõ ràng và thông tin thực sự tồn tại trong slide Day 2 (trang 28), nhưng module Retriever (ChromaDB) đã không chấm điểm cao cho đoạn chunk chứa đáp án, dẫn đến việc không đưa đúng tài liệu vào context cho LLM.

**Hướng xử lý đề xuất:**
- **Kiểm tra dữ liệu gốc:** Xác minh lại xem chunk tương ứng với slide 28 của Day 2 đã được nhúng (embed) thành công vào `chunks.jsonl` hay chưa.
- **Tối ưu Retrieval:** Tăng tham số `top_k` khi gọi hàm `ask_copilot` (hiện tại đang thiết lập `top_k=3`, có thể tăng lên 5 để mở rộng phạm vi tìm kiếm).
- **Metadata Filtering:** Nếu người dùng nhắc rõ "Day 2" trong câu hỏi, hệ thống nên có cơ chế pre-filtering để chỉ tìm kiếm trong không gian tài liệu của Day 2.

### Test #17 - Lỗi xử lý sự mơ hồ (Ambiguity handling)

**Loại câu hỏi:** Edge Case (Mơ hồ)  
**Câu hỏi:** Ngày mai phải nộp bài tập thực hành như thế nào?  
**Ground truth mong đợi:** AI nên nhận diện sự thiếu hụt ngữ cảnh (không rõ người dùng đang ở ngày học thứ mấy) và hỏi ngược lại để làm rõ.  
**Kết quả thực tế:** AI báo rằng context không có format nộp bài cụ thể, nhưng ngay sau đó lại tự động suy luận sang bài tập của Day 6 và trả lời một tràng dài dựa trên dữ liệu của Day 5.

**Đánh giá:** 
Hệ thống có biểu hiện fallback một phần (nhận ra không có format), nhưng bộ Prompt Rule chưa đủ chặt chẽ khiến AI vẫn cố gắng "đoán mò" (hallucinate) ý định của người dùng thay vì dừng lại và đặt câu hỏi làm rõ.

**Hướng xử lý đề xuất:**
- Cập nhật **System Prompt**: Thêm quy tắc xử lý nghiêm ngặt đối với các câu hỏi sử dụng trạng từ chỉ thời gian tương đối (ví dụ: "hôm nay", "ngày mai", "bài này"). Nếu không có ID bài học cụ thể, AI bắt buộc phải phản hồi: *"Bạn vui lòng làm rõ bạn đang hỏi về bài tập của Day mấy?"*.

## 4. Đánh giá hiệu năng (Latency)

Độ trễ là một yếu tố quan trọng ảnh hưởng đến trải nghiệm người dùng (UX). Dưới đây là top các câu hỏi có thời gian phản hồi lâu nhất:

| Test Case | Phân loại | Thời gian phản hồi (Latency) |
|---:|---|---:|
| #3 | Fact-based (Day 2) | ~133s |
| #11 | Reasoning | ~75s |
| #1 | Fact-based (Day 1) | ~34s |
| #10 | Fact-based (Day 5) | ~25s |
| #13 | Reasoning | ~21s |

**Nhận xét:** 
Độ trễ trung bình bị kéo lên khá cao bởi một vài trường hợp cá biệt (đặc biệt là Test #3 mất hơn 2 phút). Nguyên nhân chính có thể do:
1. Lần khởi chạy đầu tiên (Cold start): Việc load vectorstore và khởi tạo LLM API mất nhiều thời gian.
2. Context đưa vào quá dài khiến LLM mất nhiều thời gian để sinh token phản hồi.
3. Độ ổn định của mạng lưới hoặc MIMO API tại thời điểm test.

**Hướng xử lý cho buổi Demo:**
- Khởi động hệ thống (Warm-up) bằng việc gửi thử 1-2 câu hỏi đơn giản trước khi bắt đầu phần trình bày chính thức.
- Ghi chú rõ trong kịch bản demo (`demo_script.md`) rằng đây là phiên bản Prototype chạy Local/API miễn phí, do đó độ trễ đôi khi sẽ bị ảnh hưởng bởi server.

## 5. Đề xuất các Case chuẩn dùng cho Demo

Để buổi demo diễn ra trơn tru và thuyết phục nhất, nhóm nên chọn 3 case đại diện cho 3 năng lực cốt lõi của sản phẩm:

1. **Năng lực truy xuất (Fact-based PASS):** Chọn một câu hỏi hỏi về định nghĩa trong Day 1, Day 3 hoặc Day 5 (ví dụ: "3 nguyên tắc của Vibe Coding là gì?"). Cần show rõ AI trả lời đúng và có kèm `Source`.
2. **Năng lực suy luận (Reasoning PASS):** Chọn một câu hỏi yêu cầu so sánh hoặc vận dụng (ví dụ: hỏi về Agent loop, hay phân biệt Automation và Augmentation).
3. **Năng lực phòng thủ (Fallback / Edge Case):** Đặt một câu hỏi hoàn toàn ngoài phạm vi khóa học (ví dụ: "Nên mua laptop nào?") để chứng minh cơ chế an toàn của bot, không bịa đặt thông tin sai lệch.

*(Lưu ý: Tuyệt đối không dùng Test #4 và #17 trong buổi demo chính thức cho đến khi các lỗi liên quan được khắc phục triệt để).*

## 6. Kế hoạch hành động tiếp theo (Next Steps)

Dựa trên báo cáo QA này, nhóm ưu tiên thực hiện các tác vụ sau theo thứ tự:

1. **Cải thiện Retriever cho Test #4:** Đây là lỗi nghiêm trọng nhất ảnh hưởng trực tiếp đến nhóm câu hỏi fact-based. (Người 1 & 2 phụ trách).
2. **Siết chặt Rule Fallback:** Bổ sung rule vào prompt để AI ngừng đoán mò khi gặp câu hỏi mơ hồ về thời gian (Test #17). (Người 2 phụ trách).
3. **Chạy hồi quy (Regression Test):** Sau khi Người 2 cập nhật code, Người 4 sẽ chạy lại tự động toàn bộ 20 test cases để đảm bảo việc sửa lỗi không làm hỏng các câu hỏi đang PASS.
4. **Cập nhật hình ảnh Evidence:** Chụp lại các ảnh screenshot tương ứng với 3 case đề xuất ở mục 5 để chèn vào `Evidence Pack`. (Người 4 & 5 phụ trách).

## 7. Kết luận QA

Với tỉ lệ **18/20 câu trả lời đúng (Accuracy 90%)**, hệ thống RAG Chatbot của nhóm C401-Vinflow đã đạt độ trưởng thành cần thiết cho mức độ Prototype Level 3. Sản phẩm có khả năng trả lời chính xác, trích dẫn nguồn rõ ràng và sở hữu cơ chế bảo vệ cơ bản trước các câu hỏi nằm ngoài phạm vi tài liệu. Một số lỗi nhỏ về truy xuất và độ trễ hoàn toàn có thể khắc phục nhanh hoặc giải thích hợp lý trong buổi thuyết trình.

**Trạng thái đề xuất cuối cùng:** 🟢 **DEMO-READY** (Sau khi chuẩn bị kỹ kịch bản an toàn và thực hiện warm-up hệ thống).
