---
name: nhan-xet-video
description: Xem và nhận xét video như một biên tập viên mạng xã hội - đánh giá 3 giây đầu (hook), nhịp, chữ, âm thanh, khung hình, lời thoại; chỉ ra đoạn thừa và đề xuất sửa cụ thể, rồi làm luôn nếu người dùng đồng ý. Dùng khi người dùng hỏi "video này ổn chưa", "góp ý giúp", "sao video ít view", "nên cắt đoạn nào".
---

# Nhận xét video

## Cách "xem" video
1. `uv run python -m studio thong-tin <video>` — độ dài, khung, có tiếng không, dung lượng.
2. `studio khung-hinh <video> --so 16 --kiem-tra` (video > 1 phút: `--so 24`) → **mở và xem kỹ `_TONG-HOP.jpg`**; xem thêm từng khung trong thư mục nếu cần chi tiết.
3. Nếu có tiếng nói: `studio phu-de <video>` → đọc file `.txt` (lời thoại) và `.srt` (biết câu nào ở giây nào).

## Chấm theo 7 tiêu chí (mỗi tiêu chí: ✅ tốt / ⚠️ nên sửa + lý do ngắn)
1. **Hook 3 giây đầu**: có câu hỏi/vấn đề/hình ảnh gây tò mò không? Có mở bằng màn hình đen, chào hỏi dài dòng không?
2. **Khung hình đúng kênh**: TikTok/Reels/Shorts cần 9:16; YouTube 16:9; Facebook feed 4:5 hoặc 1:1.
3. **Nhịp**: đoạn nào đứng hình/lặng > 2 giây, nói lặp, vấp? (dựa vào khoảng trống trong .srt)
4. **Chữ & phụ đề**: có phụ đề không (80% người xem tắt tiếng)? Chữ có bị che bởi giao diện TikTok (mép dưới ~20% và mép phải)?
5. **Âm thanh**: có tiếng không, nhạc át giọng không, âm lượng đều không.
6. **Thông điệp & kêu gọi hành động**: cuối video có bảo người xem làm gì (mua, inbox, follow) không?
7. **Độ dài**: video ngắn bán hàng nên 15–45 giây; dài hơn cần lý do.

## Trả lời người dùng
- Mở đầu 1 câu tổng quan (điểm mạnh nhất).
- Liệt kê tối đa **3 việc nên sửa quan trọng nhất**, mỗi việc kèm mốc thời gian và cách sửa cụ thể.
- Kết thúc: "Bạn muốn mình sửa luôn mấy chỗ này không?" → nếu đồng ý, dùng skill `sua-video` / `phu-de` để làm, rồi so sánh bản trước/sau.
- Gợi ý thêm 2–3 caption/tiêu đề phù hợp nội dung (skill `viet-content`).
