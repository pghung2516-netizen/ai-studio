---
name: viet-content
description: Viết content mạng xã hội tiếng Việt - caption bán hàng Facebook/TikTok/Instagram/Zalo, hashtag, tiêu đề viral, kịch bản video ngắn theo phân cảnh, lời đọc (voiceover), bài đăng dài, mô tả sản phẩm Shopee, lịch đăng bài, trả lời bình luận. Dùng khi người dùng nhờ "viết", "caption", "kịch bản", "ý tưởng content", "tiêu đề", "hashtag".
---

# Viết content

**Mẫu & công thức chi tiết: `04-THU-VIEN-PROMPT/content.md`.**

## Quy trình
1. **Dự án**:
   - Nếu đang làm việc trong một dự án (hoặc viết bài cho video/ảnh của dự án đó): dùng tên dự án hiện tại.
   - Nếu là việc viết bài độc lập mới: `uv run python -m studio du-an moi "Bài viết <chủ đề>"` hoặc mở dự án cũ qua `du-an ds`.
2. **Trước khi viết & Hỏi ý tưởng**:
   - Đọc `03-THUONG-HIEU/thuong-hieu.md` → tên shop, sản phẩm, khách hàng, giọng văn, từ cấm, CTA, hashtag riêng.
   - Nếu viết cho 1 video cụ thể trong dự án: lấy nội dung thật qua `studio phu-de <video> --du-an "<dự án>"` (đọc .txt) và `studio khung-hinh` để caption **khớp chuẩn nội dung video**.
   - Chạy skill `hoi-y-tuong` (hỏi nhanh bằng các lựa chọn bấm được: góc tiếp cận, kênh đăng Facebook/TikTok/Shopee, thông tin ưu đãi/giá). Người dùng có thể chọn hoặc nói "bạn quyết giúp mình".
   - Lưu tóm tắt brief: `uv run python -m studio du-an ghi "<dự án>" "<bản yêu cầu bài viết>"`.
3. **Nguyên tắc viết**:
   - Câu đầu tiên là **hook** (người ta chỉ đọc 1–2 dòng trước chữ "Xem thêm").
   - Viết như người thật nói chuyện, đúng giọng thương hiệu; câu ngắn; xuống dòng nhiều; emoji vừa phải.
   - **Không bịa** công dụng, số liệu, cam kết, giá, chương trình khuyến mãi. Thiếu thông tin → để `[điền giá]`.
   - Sản phẩm sức khỏe/làm đẹp/thực phẩm chức năng: tránh từ "chữa khỏi", "điều trị", "cam kết 100%", "tốt nhất" (dễ bị khóa bài, vi phạm quảng cáo).
   - Luôn có **CTA** rõ (inbox, bấm link, comment "SIZE"...).
   - Đưa **2–3 phiên bản** khác góc tiếp cận để người dùng chọn, trừ khi họ chỉ cần 1.
4. **Đầu ra & Lưu thành phẩm**:
   - Trình bày gọn trong khung chat để người dùng copy nhanh.
   - Khi làm việc trong dự án, lưu nội dung hoàn thiện vào file tạm trong `.cache/nhap/<dự án>/content.md` (hoặc `.txt`), rồi chốt vào `Thành phẩm/`:
     `uv run python -m studio du-an chot "<dự án>" ".cache/nhap/<dự án>/content.md" --ten "Bài viết <kênh/chủ đề>"`
   - Ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "Đã chốt nội dung bài viết vào Thành phẩm."`.
   - Mở thư mục `Thành phẩm` cho người dùng: PowerShell `Invoke-Item "02-DU-AN\<dự án>\Thành phẩm"` (Mac: `open`).
5. **Gợi ý bước tiếp / tùy chỉnh**:
   - Gợi ý lựa chọn bấm được: đổi giọng văn, rút ngắn cho TikTok, thiết kế ảnh minh họa (`sua-anh`), hoặc lên kịch bản video ngắn (bảng phân cảnh: cảnh – thời lượng – hình – chữ trên màn hình – lời đọc) rồi gợi ý: quay thật → `sua-video`; tạo ảnh/video AI → `prompt-anh-ai` / `prompt-video-ai` → `video-tu-anh`.
