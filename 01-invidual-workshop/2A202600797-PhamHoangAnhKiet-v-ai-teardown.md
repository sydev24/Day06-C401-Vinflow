# Workshop — Mổ App AI Thật
**Sinh viên:** Phạm Hoàng Anh Kiệt  
**MSSV:** 2A202600797  
**Sản phẩm phân tích:** V-App — V-AI (Vinhomes AI Assistant)  
**Ngày thực hiện:** 2026-06-03

---

## 1. Sản phẩm được chọn: V-App — V-AI

| Mục | Nội dung |
|---|---|
| Sản phẩm | V-App — V-AI |
| AI feature | Trợ lý voice/text, gợi ý theo ngữ cảnh |
| Cách truy cập | App V-App (Android) |
| Prompt thử nghiệm | `"Tra cứu bất cứ điều gì"` — gửi lặp lại 13 lần |
| Thời gian quan sát | 11:36 – 11:49 cùng ngày |
| Phương thức | Mỗi lần gửi prompt trong cùng hội thoại hoặc hội thoại mới |

---

## 2. Promise vs Reality

### Product hứa gì?
V-AI được quảng bá là **trợ lý theo ngữ cảnh** — gợi ý thông minh dựa trên hành vi người dùng trong app. Tên gọi "V-AI" ngụ ý khả năng xử lý intent đa dạng và cá nhân hoá phản hồi.

### User nào được hứa sẽ được giúp?
Cư dân hoặc khách hàng tiềm năng của Vinhomes — muốn tra cứu thông tin **bất kỳ** trong hệ sinh thái V-App: tiện ích, sức khoẻ, giáo dục, giải trí, bất động sản, v.v.

### Kỳ vọng thực tế khi dùng:
Prompt `"Tra cứu bất cứ điều gì"` là một **open-domain query** — user không chỉ định chủ đề → AI nên hỏi lại, gợi ý domain, hoặc ít nhất trả về câu trả lời tổng quát.

### Điểm gãy quan sát được:

| Lần gửi | Thời gian | Title AI trả về |
|---|---|---|
| 1 | 11:36 | Tra cứu thông tin bất động sản và **phong thủy** |
| 2 | 11:40 | Tra cứu thông tin **nhà đất** và pháp lý |
| 3 | 11:41 | Tra cứu thông tin bất động sản và **pháp lý** |
| 4 | 11:42 | Tra cứu thông tin bất động sản và **định danh điện tử** |
| 5 | 11:43 | Tra cứu thông tin bất động sản và **pháp lý** |
| 6–13 | (similar) | Tất cả đều xoay quanh: BĐS / Pháp lý / Phong thủy / Định danh |

**Pattern phát hiện:**
- Title thay đổi ngẫu nhiên → tạo *illusion of variety* giả tạo
- Nội dung thực tế (body) gần như giống nhau ở mọi lần
- 4 nguồn dữ liệu hardcoded: `market.vinhomes.vn · 24h.com.vn · tuoitre.vn` (không thay đổi)
- `market.vinhomes.vn` luôn chiếm vị trí **#1 VÀ #3** → Business bias rõ ràng

**Evidence (screenshots quan sát):**
- 11:43 → source list: #1 market.vinhomes.vn, #2 24h.com.vn, #3 market.vinhomes.vn, #4 tuoitre.vn
- 11:42 → "Định danh điện tử" nhưng vẫn dùng nguồn BĐS
- 11:40 → "Đã xem xét 4 nguồn" luôn giữ nguyên 4 nguồn đó
- 11:36 → Nội dung về phong thủy nhưng source vẫn là market.vinhomes.vn

**Evidence bổ sung — Home Screen V-App (11:48):**

App home screen đã hiển thị context data phong phú của chính user này:

| Vị trí trên home | Dữ liệu hiển thị |
|---|---|
| "Sử dụng gần đây" | VinUni, VinBus |
| "Gợi ý sử dụng" | VinUni (Cá nhân hóa trải nghiệm Sinh viên), Green SM Food |
| "Yêu thích" | VPoint · Thanh toán điện · Gọi Green Car · Tìm trạm sạc · Xem tin cho thuê · Đặt khách sạn |
| "Top tiện ích yêu thích" | Pin & Sạc · Đặt xe Green SM · Đặt đồ ăn Green SM · Ưu đãi · VPoint |

→ **App đã có đủ data** để biết user này đang quan tâm đến VinUni, VinBus, sức khoẻ, di chuyển.  
→ **V-AI hoàn toàn bỏ qua toàn bộ data đó** và vẫn trả về BĐS/Pháp lý.  
→ Đây là gap lớn nhất: **data tồn tại ngay trong app, không cần collect thêm, nhưng không được truyền vào AI.**

---

## 3. Bốn Paths

### Path 1 — Happy Path
**Câu hỏi:** Khi AI đúng và tự tin, user thấy gì?

```
User hỏi cụ thể: "Thủ tục sang tên sổ hồng"
→ AI trả về đúng quy trình pháp lý từ 24h.com.vn
→ User đọc và thực hiện được
→ Không cần làm gì thêm
```
**Tình trạng:** Happy path tồn tại nhưng **chỉ với domain BĐS/Pháp lý**. Với bất kỳ domain nào khác, AI vẫn kéo về BĐS.

---

### Path 2 — Low-confidence Path
**Câu hỏi:** Khi AI không chắc, hệ thống có hỏi lại, show options hoặc chuyển người không?

```
User: "Tra cứu bất cứ điều gì"
→ AI KHÔNG hỏi lại: "Bạn muốn tra cứu về chủ đề gì?"
→ AI KHÔNG đưa ra domain options để chọn
→ AI KHÔNG chuyển sang human agent
→ AI tự quyết định domain = BĐS và trả lời luôn
```
**Tình trạng:** ❌ **Low-confidence path KHÔNG TỒN TẠI** trong sản phẩm hiện tại. Hệ thống không có cơ chế nhận biết độ không chắc chắn về intent của user.

---

### Path 3 — Failure Path
**Câu hỏi:** Khi AI sai, user biết bằng cách nào và sửa thế nào?

```
User: "Tra cứu bất cứ điều gì"  (intent thực: tìm thông tin Vinmec/VinUni)
→ AI trả về: BĐS + Pháp lý
→ User đọc xong nhận ra không đúng nhu cầu
→ User CÓ THỂ reply tiếp trong cùng hội thoại (không cần bắt đầu lại)
→ Nhưng: KHÔNG có nút "Wrong topic", KHÔNG có domain switcher trong chat
→ Không có signal nào từ hệ thống thông báo "Tôi không chắc chủ đề của bạn"
```
**Tình trạng:** ⚠️ **Failure path có thể tiếp tục conversation, nhưng thiếu recovery signal**.  
User phải tự nhận ra AI sai — hệ thống không có cơ chế phát hiện hoặc thông báo mismatch.  
Việc "reply tiếp" vẫn tạo ra response BĐS vì AI không tích luỹ context từ conversation history.

---

### Path 4 — Correction Path
**Câu hỏi:** Khi user sửa, correction có được lưu/log/học lại không hay biến mất?

```
User reply tiếp trong cùng hội thoại: "Tôi muốn tìm thông tin VinUni"
→ AI có thể trả lời đúng VinUni lần này (do prompt đủ cụ thể)
→ Nhưng: không có "Đổi chủ đề" action cho phép redirect nhanh
→ Không có feedback button (👍👎) để log correction
→ Nếu user mở hội thoại mới và gửi lại prompt mở → AI quay về BĐS
→ Correction chỉ tồn tại trong session, không được persist/học lại
```
**Tình trạng:** ⚠️ **Correction path hoạt động một phần trong cùng session**.  
User CÓ THỂ sửa bằng cách clarify prompt trong cùng hội thoại.  
Tuy nhiên: correction không được log, không được học lại, và không persist sang session tiếp theo.  
App context (recent activity, favorites) cũng không được đọc để tự động pre-correct.

---

## 4. Finding → Product Decision

### Finding 1 (chính)

```
Khi user gửi một open-domain prompt như "Tra cứu bất cứ điều gì",
AI mặc định chọn domain BĐS/Pháp lý mà không đọc app context,
hậu quả là user nào dùng V-AI cho mục đích khác (y tế, giáo dục, 
giải trí) sẽ liên tục nhận phản hồi sai topic và không biết cách sửa.

Lỗi thuộc layer: Promise + Intent + UX Recovery.
Nên sửa bằng: inject "recent activity context" vào API call trước 
khi model xử lý prompt — không cần retrain model, không cần redesign UI.
```

### Finding 2 (business bias)

```
Khi bất kỳ user nào hỏi bất kỳ điều gì,
AI luôn ưu tiên market.vinhomes.vn ở vị trí #1 VÀ #3 trong 4 nguồn,
hậu quả là user mất tin tưởng vào tính trung lập của AI 
và nhận thức AI là kênh quảng cáo nội bộ.

Lỗi thuộc layer: Data-tool (source selection policy).
Nên sửa bằng: dynamic source routing — nguồn được chọn dựa trên 
domain đã xác định, không hardcode vị trí cho bất kỳ domain nào.
```

### Finding 3 (illusion of variety)

```
Khi AI trả lời lặp lại 13 lần với cùng 1 prompt,
title thay đổi ngẫu nhiên ("phong thủy", "định danh", "pháp lý")
nhưng body content và source list giữ nguyên,
hậu quả là user cảm thấy AI "đa dạng" nhưng thực chất không có 
giá trị thêm — đây là Illusion of Variety, không phải personalization.

Lỗi thuộc layer: Promise (AI "thông minh") vs Reality (template cố định).
Nên sửa bằng: content cần thay đổi thực sự dựa trên context, 
không chỉ randomize title.
```

### Finding 4 — Context gap (quan trọng nhất, phát hiện bổ sung)

```
Khi user mở V-AI và gửi prompt bất kỳ,
app home screen (11:48) đã hiển thị "Sử dụng gần đây: VinUni, VinBus"
và "Yêu thích: VPoint, Thanh toán điện, Gọi Green Car" — 
tức là data đã có sẵn, đã được render trên UI, 
nhưng V-AI hoàn toàn bỏ qua và vẫn trả về domain BĐS,
hậu quả là app đang có "personalization data" nhưng AI không được
kết nối với nó — tạo ra trải nghiệm tách rời (disconnected experience)
giữa home screen và V-AI.

Lỗi thuộc layer: Architecture (AI không được cấp quyền đọc app state).
Nên sửa bằng: truyền recent_activity + favorites vào system prompt
dưới dạng structured metadata — data đã có, không cần collect thêm.
```

---

## 5. Sketch As-is / To-be

### As-is Flow (hiện tại — điểm gãy đánh dấu bằng ✗)

```
[App Home Screen]
  recent activity: VinUni, VinBus  ─────────┐
  favorites: VPoint, Green Car...  ─────────│── ✗ V-AI KHÔNG đọc
  gợi ý: VinUni, Green SM Food    ─────────┘    data này

    │
    ▼
User mở V-AI → nhập prompt (bất kỳ)
    │
    ▼
AI xử lý ────────────────────────────────────────────────────
    │ ✗ KHÔNG đọc app context (recent activity, favorites)
    │ ✗ KHÔNG nhận biết open-domain / low-confidence intent
    ▼
AI chọn domain = BĐS  ✗ (hardcoded default, bất kể user là ai)
    │
    ▼
Lấy source từ 4 nguồn cố định  ✗ (market.vinhomes.vn #1 và #3)
    │
    ▼
Trả về response với title ngẫu nhiên  ✗ (illusion of variety)
    │
    ▼
User đọc kết quả
    │
    ├── [Đúng nhu cầu] → Happy path ✓ (chỉ với BĐS user)
    │
    └── [Sai nhu cầu]
            │
            ▼
        User CÓ THỂ reply tiếp trong cùng hội thoại ✓
        (không cần bắt đầu lại)
            │
            ├── [Clarify cụ thể: "Tôi muốn tìm VinUni"]
            │       → AI có thể trả lời đúng
            │       → Nhưng: correction không được log/persist ✗
            │
            └── [Gửi lại prompt mở tương tự]
                    → AI vẫn trả về BĐS ✗
                    → Không có "Đổi chủ đề" nhanh ✗
                    → Không có feedback button ✗
```

---

### To-be Flow (đề xuất — path đã sửa đánh dấu bằng ✓)

```
User mở V-AI
    │
    ▼
User nhập prompt (bất kỳ)
    │
    ▼
Pre-processing layer ──────────────────────────────────────────
    │                                                          
    │ ✓ Đọc "recent activity" từ app context metadata         
    │   (e.g., user vừa xem trang Vinmec → inject health context)
    │                                                         
    ▼                                                          
Intent classification ─────────────────────────────────────────
    │
    ├── [High confidence → domain rõ] → Trả lời thẳng
    │
    └── [Low confidence → open-domain] ✓ Show domain options
                │
                ▼
            "Bạn muốn tra cứu về chủ đề nào?"
            [🏠 Nhà đất] [🏥 Sức khoẻ] [📚 Giáo dục] [💡 Tiện ích]
                │
                ▼
            User chọn domain
                │
                ▼
            ✓ Dynamic source routing theo domain được chọn
            (Vinmec → vinmec.com; VinUni → vinuni.edu.vn; v.v.)
                │
                ▼
            Trả về response đúng domain
                │
                ▼
            ✓ Feedback bar: [👍 Đúng rồi] [🔄 Đổi chủ đề] [✏️ Sửa]
                │
                ├── [👍] → Log positive signal
                │
                └── [🔄 Đổi chủ đề] → Quay lại domain options
                        │
                        ▼
                    ✓ Correction path: session context giữ nguyên,
                      chỉ đổi domain → không mất lịch sử hội thoại
```

---

## 6. Tự kiểm trước khi nộp

- [x] Có ít nhất 1 screenshot hoặc observation cụ thể.  
  → 5 screenshots chat (11:36–11:43) + 7 screenshots home screen (11:48–11:49) + bảng 13 lần thử nghiệm

- [x] Có đủ 4 paths hoặc nói rõ path nào chưa có trong product.  
  → Happy ✓ (chỉ với BĐS domain) / Low-confidence ❌ / Failure ⚠️ (partial) / Correction ⚠️ (trong session, không persist)

- [x] Finding được viết thành product decision, không chỉ là nhận xét.  
  → 4 findings với format: trigger → failure → impact → layer → fix

- [x] Sketch có as-is và to-be.  
  → ASCII flow diagram cho cả 2 states, gồm cả context gap từ home screen; điểm gãy/sửa được đánh dấu rõ

- [x] Có một câu nói rõ finding này sẽ đổi gì trong SPEC.  
  → **"V-AI bắt buộc phải đọc `recent_activity` và `favorites` từ app state trước mỗi API call — data đã có sẵn trên home screen, không cần collect thêm, không cần retrain model, không cần redesign UI. Đây là thay đổi ở tầng pre-processing (inject vào system prompt), không phải thay đổi model."**

---

*File này là output của workshop cá nhân theo yêu cầu `app-teardown.md`.*
