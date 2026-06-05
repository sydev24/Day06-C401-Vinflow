# UX Workshop – Moni (MoMo)

## App được chọn

**Moni – Trợ lý AI của MoMo**

---

# 1. Flow As-Is

## Scenario

Người dùng muốn kiếm nhiều tiền hơn và hỏi:

> "Tôi muốn kiếm nhiều tiền như Elon Musk"

### Flow hiện tại

```text
User hỏi về Elon Musk
↓
Moni trả lời như chatbot tổng quát
↓
User hỏi Elon Musk học lập trình từ nhỏ không
↓
Moni trả lời
↓
User yêu cầu roadmap học lập trình
↓
Moni tạo roadmap
↓
User yêu cầu ví dụ code Python
↓
Moni sinh code Python
↓
Cuộc hội thoại tiếp tục như ChatGPT
```

---

# 2. Path yếu nhất

## Failure Path

```text
User hỏi ngoài phạm vi MoMo
↓
Moni vẫn trả lời như chatbot đa năng
↓
User tiếp tục hỏi ngoài domain
↓
Moni tiếp tục hỗ trợ
↓
Người dùng không còn thấy giá trị riêng của Moni
```

### Vấn đề

Moni giới thiệu rằng:

> "Chỉ hỗ trợ trong phạm vi sản phẩm MoMo"

Nhưng thực tế lại:

* Tư vấn nghề nghiệp
* Tạo roadmap học tập
* Viết code Python

Điều này tạo ra sự không nhất quán giữa:

**Promise của sản phẩm**
↓
và
↓
**Hành vi thực tế của AI**

Người dùng không hiểu đâu là giới hạn của hệ thống.

---

# 3. To-Be Flow

## Mục tiêu

Khi gặp câu hỏi ngoài domain, Moni nên đưa cuộc trò chuyện quay lại giá trị cốt lõi của MoMo.

### Flow đề xuất

```text
User: Tôi muốn kiếm nhiều tiền như Elon Musk
↓
Moni nhận diện đây là câu hỏi ngoài phạm vi tài chính cá nhân trên MoMo
↓
Moni trả lời ngắn gọn
↓
Moni chuyển hướng:

"Tôi không thể tư vấn nghề nghiệp chuyên sâu như một chatbot tổng quát.

Tuy nhiên tôi có thể giúp bạn:
- Phân tích chi tiêu
- Lập kế hoạch tiết kiệm
- Theo dõi mục tiêu tài chính
- Quản lý ngân sách"

↓
User chọn một nhu cầu tài chính
↓
Moni sử dụng dữ liệu MoMo để hỗ trợ
```

---

# 4. Product Decision

**Khi người dùng đặt câu hỏi ngoài phạm vi quản lý tài chính, Moni sẽ không cố gắng trở thành chatbot đa năng mà chủ động chuyển hướng cuộc trò chuyện về các tác vụ tài chính có thể tận dụng dữ liệu và lợi thế riêng của hệ sinh thái MoMo.**
