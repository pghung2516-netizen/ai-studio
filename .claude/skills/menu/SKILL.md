---
name: menu
description: Chào người dùng và giới thiệu những việc workspace làm được. Dùng khi người dùng chào hỏi, mở workspace lần đầu, gõ "menu", "bắt đầu", "giúp", "làm được gì", "hướng dẫn", hoặc có vẻ chưa biết bắt đầu từ đâu.
---

# Menu chào mừng

1. Kiểm tra nhanh (không nói ra chi tiết kỹ thuật):
   - Nếu chưa có thư mục `.venv` → nói "Mình cần chuẩn bị máy một chút (chỉ lần đầu, khoảng 5–10 phút)" rồi làm theo skill `cai-dat`, xong mới quay lại menu.
   - Đọc `03-THUONG-HIEU/thuong-hieu.md`: nếu còn các ô `[...]` trống → ghi nhớ để gợi ý ở cuối.
   - Chạy `uv run python -m studio danh-sach` để biết trong `01-DAU-VAO` đang có file gì.

2. Chào ngắn gọn và đưa menu đúng dạng sau (giữ emoji, không thêm thuật ngữ):

```
Chào bạn 👋 Mình là trợ lý sáng tạo. Bạn chỉ cần nói việc muốn làm, ví dụ:

🎬 SỬA VIDEO
  • "Cắt lấy đoạn từ giây 10 đến 40"      • "Ghép 3 video này lại"
  • "Đổi sang video dọc cho TikTok"        • "Thêm nhạc nền / logo / chữ"
  • "Nén nhẹ để gửi Zalo"                  • "Làm GIF từ đoạn này"
💬 PHỤ ĐỀ
  • "Làm phụ đề tiếng Việt cho video"      • "Chép lời video thành văn bản"
🖼️ ẢNH
  • "Xóa nền ảnh sản phẩm"                 • "Đổi cỡ ảnh cho Shopee / Facebook / YouTube"
  • "Chèn chữ khuyến mãi lên ảnh"          • "Ghép ảnh trước – sau"
✨ ẢNH & VIDEO TỪ ẢNH
  • "Làm video TikTok từ 5 tấm ảnh này"    • "Thiết kế poster / ảnh bìa"
🎞️ VIDEO KHÔNG CẦN QUAY
  • "Làm video chữ chạy khuyến mãi 10 giây" • "Làm intro logo"
  • "20 sản phẩm làm 20 video từ bảng giá"  • "Video hoạt hình giải thích 3 bước đặt hàng"
  • "Biểu đồ doanh thu chạy số"             • "Dựng ảnh 3D hộp sản phẩm / xoay 360°"
🤖 AI TẠO ẢNH / VIDEO
  • "Viết prompt để Gemini/ChatGPT tạo ảnh quảng cáo"
  • "Viết prompt Veo tạo video người mẫu mặc áo"
✍️ CONTENT
  • "Viết caption bán hàng"  • "Kịch bản video 30 giây"  • "Lịch đăng bài 1 tuần"
🔎 NHẬN XÉT
  • "Xem video này có gì cần sửa không"
✂️ CAPCUT
  • "Cắt khoảng lặng trong dự án CapCut"

📁 Cách đưa file: bỏ vào thư mục 01-DAU-VAO (hoặc kéo thả vào khung chat).
📦 Kết quả: luôn nằm trong thư mục 02-THANH-PHAM, chia theo ngày.
```

3. Nếu `01-DAU-VAO` đã có file → thêm 1 dòng: "Mình thấy bạn có sẵn [số] video/ảnh, ví dụ `tên-file`. Bạn muốn làm gì với chúng?"
4. Nếu bộ thương hiệu còn trống → thêm 1 dòng: "💡 Mẹo: dành 5 phút cho mình biết về shop/thương hiệu của bạn, content và thiết kế sẽ đúng 'chất' hơn. Gõ: **thiết lập thương hiệu**."
5. Nếu `05-CONG-CU-THEM/DANH-SACH.md` có công cụ đã đăng ký **ngoài** 4 công cụ đã nằm trong mục 🎞️ (HyperFrames, Remotion, Manim, Blender) → liệt kê thêm mục "🧩 CÔNG CỤ THÊM" với tên + 1 câu mô tả mỗi công cụ.
