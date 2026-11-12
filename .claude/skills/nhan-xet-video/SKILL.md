---
name: nhan-xet-video
description: Xem và nhận xét video như một biên tập viên mạng xã hội - đánh giá 3 giây đầu (hook), nhịp, chữ, âm thanh, khung hình, lời thoại; chỉ ra đoạn thừa và đề xuất sửa cụ thể, rồi làm luôn nếu người dùng đồng ý. Dùng khi người dùng hỏi "video này ổn chưa", "góp ý giúp", "sao video ít view", "nên cắt đoạn nào".
---

# Nhận xét video

## Cách "xem" video
1. **Mở hoặc tạo dự án**:
   - Nếu video đã thuộc một dự án: dùng dự án đó (`du-an xem "<dự án>"`).
   - Nếu là video mới: `uv run python -m studio du-an moi "Đánh giá video" <video> [--lay-hop-thu]` (hoặc lấy tên theo video) để lưu file vào `Gốc/`.
   - Nếu người dùng nói "lấy video vừa tải về": `tim-file-moi --loai video`.
2. **Kiểm tra thông số**: `uv run python -m studio thong-tin <video> --du-an "<dự án>"` — độ dài, khung, có tiếng không, dung lượng.
3. **Xem hình ảnh**: `studio khung-hinh <video> --du-an "<dự án>" --so 16 --kiem-tra` (video > 1 phút: `--so 24`) → **mở và xem kỹ `_TONG-HOP.jpg`**; xem thêm từng khung trong thư mục nháp nếu cần chi tiết.
4. **Xem lời thoại** (nếu có tiếng nói): `studio phu-de <video> --du-an "<dự án>"` → đọc file `.txt` (lời thoại) và `.srt` (biết câu nào ở giây nào) trong `.cache/nhap/<dự án>/`.

## Chấm theo 7 tiêu chí (mỗi tiêu chí: ✅ tốt / ⚠️ nên sửa + lý do ngắn)
1. **Hook 3 giây đầu**: có câu hỏi/vấn đề/hình ảnh gây tò mò không? Có mở bằng màn hình đen, chào hỏi dài dòng không?
2. **Khung hình đúng kênh**: TikTok/Reels/Shorts cần 9:16; YouTube 16:9; Facebook feed 4:5 hoặc 1:1.
3. **Nhịp**: đoạn nào đứng hình/lặng > 2 giây, nói lặp, vấp? (dựa vào khoảng trống trong .srt)
4. **Chữ & phụ đề**: có phụ đề không (80% người xem tắt tiếng)? Chữ có bị che bởi giao diện TikTok (mép dưới ~20% và mép phải)?
5. **Âm thanh**: có tiếng không, nhạc át giọng không, âm lượng đều không.
6. **Thông điệp & kêu gọi hành động**: cuối video có bảo người xem làm gì (mua, inbox, follow) không?
7. **Độ dài**: video ngắn bán hàng nên 15–45 giây; dài hơn cần lý do.

## Trả lời người dùng & Thực hiện sửa
- Mở đầu 1 câu tổng quan (điểm mạnh nhất).
- Liệt kê tối đa **3 việc nên sửa quan trọng nhất**, mỗi việc kèm mốc thời gian và cách sửa cụ thể.
- Ghi tóm tắt nhận xét vào nhật ký dự án: `uv run python -m studio du-an ghi "<dự án>" "<tóm tắt nhận xét và đề xuất sửa>"`.
- Kết thúc bằng lựa chọn bấm được: "Bạn muốn mình sửa luôn mấy chỗ này không?"
  - Nếu người dùng đồng ý: chạy skill `hoi-y-tuong` để thống nhất phương án (người dùng có thể chọn hoặc nói "bạn quyết giúp mình").
  - Tiến hành sửa bằng `sua-video` / `phu-de` (luôn kèm `--du-an "<dự án>"`).
  - Tự kiểm tra kết quả, rồi chốt bản hoàn thiện:
    `uv run python -m studio du-an chot "<dự án>" <file nháp> --ten "Bản đã sửa góp ý"`
  - Ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "Đã sửa video theo nhận xét biên tập viên."`.
  - Mở thư mục `Thành phẩm` cho người dùng: PowerShell `Invoke-Item "02-DU-AN\<dự án>\Thành phẩm"` (Mac: `open`).
- Gợi ý thêm 2–3 caption/tiêu đề phù hợp nội dung (skill `viet-content`).
