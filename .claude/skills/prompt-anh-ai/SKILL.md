---
name: prompt-anh-ai
description: Viết prompt tạo/chỉnh ảnh bằng AI (Gemini / Nano Banana, ChatGPT Image, Google AI Studio) cho ảnh quảng cáo sản phẩm, poster/banner, người mẫu mặc đồ, nhân vật 3D, ảnh người que minh họa, thumbnail, infographic. Dùng khi người dùng muốn "AI vẽ", "tạo ảnh quảng cáo", "ảnh người mẫu ảo", "prompt ảnh", hoặc cần hình mà không có ảnh thật.
---

# Prompt ảnh AI

Workspace **không tự gọi dịch vụ AI tạo ảnh** (tránh phí và rò rỉ dữ liệu). Bạn viết prompt hoàn chỉnh để người dùng **dán vào Gemini (gemini.google.com) hoặc ChatGPT**, rồi họ tải ảnh về `01-DAU-VAO` để bạn hậu kỳ tiếp (đổi cỡ, chèn logo, làm video). Nếu `05-CONG-CU-THEM/DANH-SACH.md` có công cụ tạo ảnh chạy trên máy → ưu tiên dùng công cụ đó.

**Thư viện mẫu chi tiết: `04-THU-VIEN-PROMPT/anh-ai.md`** — đọc phần liên quan trước khi viết.

## Quy trình
1. Hỏi tối đa 2 câu nếu thiếu: (a) ảnh dùng để làm gì / đăng ở đâu → quyết định **tỉ lệ**; (b) có ảnh sản phẩm/ảnh mẫu thật để đính kèm không.
2. Đọc `03-THUONG-HIEU/thuong-hieu.md` (tên, slogan, màu, phong cách).
3. Viết prompt theo công thức **5 phần** (dựa trên R-C-T-O + "code + giữ nguyên + ràng buộc"):
   1. **VAI & MỤC TIÊU** — "Bạn là nhiếp ảnh gia quảng cáo..." / "Tạo ảnh quảng cáo studio..."
   2. **GIỮ NGUYÊN** — nếu có ảnh đính kèm: "Giữ nguyên 100% hình dáng, màu sắc, logo, nhãn mác, tỉ lệ sản phẩm trong ảnh đính kèm".
   3. **MÔ TẢ CỤ THỂ** — chủ thể, bối cảnh, đạo cụ, ánh sáng (hướng, ấm/lạnh, mềm/cứng), góc máy, chất liệu, cảm xúc. Cụ thể thay vì mơ hồ.
   4. **CHỮ TRÊN ẢNH** — ghi chính xác trong ngoặc đơn: `dòng chữ 'SALE 50%'`, kèm "đúng chính tả tiếng Việt, không méo chữ, font hiện đại". Ít chữ thì ảnh đẹp hơn; chữ dài → để trống, bạn chèn sau bằng `studio chu-anh`.
   5. **ĐẦU RA** — tỉ lệ (1:1, 4:5, 9:16, 16:9), độ nét (2K/4K), phong cách tổng thể, điều cần tránh.
4. Trả cho người dùng:
   - Prompt trong **khung code** (để họ bấm copy), tiếng Việt; thêm bản tiếng Anh nếu dùng cho Midjourney/công cụ nước ngoài.
   - 3 bước ngắn: mở Gemini → đính kèm ảnh (nếu có) → dán prompt. Mẹo: chữ tiếng Việt dễ lỗi → dùng chế độ "Tư duy/Thinking" hoặc Google AI Studio (chọn mô hình Nano Banana, chọn 2K/4K).
   - 2 biến thể (vd: nền khác, góc khác) để họ chọn.
5. Khi họ có ảnh về: đề nghị hậu kỳ (đổi cỡ theo kênh, chèn logo, ghép thành video).

## Lưu ý đạo đức & bản quyền
- Không tạo ảnh giả mạo người thật (người nổi tiếng, khách hàng) hay logo thương hiệu khác.
- Lấy cảm hứng từ banner trên Pinterest được — nhưng chỉ học **phong cách/bố cục**, nội dung phải của người dùng.
- Ảnh người mẫu AI dùng bán hàng: khuyên ghi chú "ảnh minh họa" nếu sàn yêu cầu.
