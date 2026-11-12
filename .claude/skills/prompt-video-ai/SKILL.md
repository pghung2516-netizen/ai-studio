---
name: prompt-video-ai
description: Viết prompt tạo video bằng AI (Google Veo, Sora, Kling, Runway, Higgsfield...) - cảnh quay điện ảnh, quảng cáo sản phẩm 8 giây, video người mẫu xoay đồ, chuyển động theo video mẫu, giữ nhân vật đồng nhất qua nhiều cảnh, góc máy và ánh sáng. Dùng khi người dùng muốn "AI tạo video", "prompt Veo", "video quảng cáo AI", "video từ ảnh".
---

# Prompt video AI

Workspace không tự gọi dịch vụ tạo video AI (tốn phí). Bạn viết prompt để người dùng dán vào **Veo (Gemini / Google Flow), Sora, Kling, Runway...**, họ tải clip về `01-DAU-VAO`, rồi bạn ghép/chèn chữ/phụ đề/nhạc bằng `studio`. Nếu `05-CONG-CU-THEM/DANH-SACH.md` có công cụ tạo video → ưu tiên dùng.

**Thư viện chi tiết: `04-THU-VIEN-PROMPT/video-ai.md`** — đọc phần liên quan trước khi viết.

## 4 nguyên tắc vàng (bắt buộc)
1. **Cụ thể tuyệt đối** — "người đàn ông gầy cuối 50 tuổi, mắt sâu mệt mỏi, gục trên ghế bành da cũ trong phòng làm việc bụi bặm thiếu sáng" thay vì "người đàn ông buồn".
2. **Đa giác quan** — luôn có hình ảnh + chuyển động + tâm trạng + **âm thanh** (Veo tạo cả tiếng).
3. **Chỉ mô tả những gì có trong khung hình** — cận cảnh bàn tay thì đừng tả đôi giày.
4. **Một prompt = một cảnh quay** (5–8 giây). Video dài = nhiều prompt nối nhau, giữ nhân vật đồng nhất.

## Cấu trúc 1 prompt
`[Loại cảnh + góc máy + chuyển động máy] + [chủ thể chi tiết] + [hành động trong X giây] + [bối cảnh] + [ánh sáng & màu] + [âm thanh: tiếng môi trường, nhạc, lời thoại trong ngoặc kép] + [phong cách / chất lượng] + [thời lượng, tỉ lệ]`

## Quy trình
1. Hỏi tối đa 2 câu: mục đích (quảng cáo/kể chuyện/giới thiệu) & nền tảng (TikTok 9:16 / YouTube 16:9); có ảnh làm khung đầu không (image-to-video giữ sản phẩm chính xác hơn).
2. Nếu video nhiều cảnh: viết **bảng phân cảnh** trước (cảnh – thời lượng – mục đích – lời thoại/chữ), người dùng duyệt rồi mới viết prompt từng cảnh.
3. Viết prompt **tiếng Anh** (các mô hình video hiểu tốt nhất) + 1 dòng dịch nghĩa tiếng Việt bên dưới để người dùng hiểu. Lời thoại tiếng Việt thì giữ nguyên tiếng Việt trong ngoặc kép và ghi rõ "spoken in Vietnamese".
4. Kèm **"Khóa nhân vật"** (character sheet) — cùng một đoạn mô tả nhân vật dán nguyên văn vào mọi cảnh.
5. Hướng dẫn 3 bước dán prompt + nhắc: clip tạo xong lưu vào `01-DAU-VAO/<tên-dự-án>/` đặt tên `01.mp4, 02.mp4...` để mình ghép.
6. Khi có clip: `studio ghep <thư-mục> --ti-le 9:16` → `phu-de` / `chu` / `nhac` / `logo`.

## Lưu ý
- Không tạo video giả mạo người thật, người nổi tiếng, tin tức giả; không dùng gương mặt người khác khi chưa được đồng ý.
- Veo Fast rẻ hơn, phù hợp thử nghiệm; bản chất lượng cao dùng cho bản cuối.
