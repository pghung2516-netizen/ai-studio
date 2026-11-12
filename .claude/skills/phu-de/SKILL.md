---
name: phu-de
description: Làm phụ đề tiếng Việt (hoặc ngôn ngữ khác) cho video bằng AI chạy trên máy, sửa chính tả phụ đề, đốt phụ đề vào video theo kiểu TikTok, chép lời video thành văn bản. Dùng khi người dùng nói "phụ đề", "sub", "caption chạy chữ", "chép lời", "gỡ băng", "transcript".
---

# Phụ đề

## Quy trình chuẩn (chất lượng cao)
1. `uv run python -m studio phu-de <video>` → tạo `..._phu-de.srt` và `..._phu-de.txt` (lời thoại liền mạch).
   - Mặc định tiếng Việt, mô hình `vua`. Người nói tiếng Anh → `--ngon-ngu en`; không rõ → `--ngon-ngu tu-dong`.
   - Giọng địa phương nặng / nhiều tạp âm → `--mo-hinh chuan` (chính xác hơn, chậm hơn ~3 lần; lần đầu tải thêm ~1.5 GB).
2. **Đọc file .srt và tự sửa lỗi chính tả** bằng công cụ Edit (chỉ sửa chữ, **giữ nguyên số thứ tự và dòng thời gian**):
   - Tên riêng, tên sản phẩm, thương hiệu (đối chiếu `03-THUONG-HIEU/thuong-hieu.md`).
   - Từ nghe nhầm phổ biến (vd "trí tội" → "trí tuệ"), dấu câu, viết hoa đầu câu.
   - Không thêm/bớt ý của người nói.
3. Đốt vào video: `studio dot-phu-de <video> <file.srt>` với kiểu phù hợp:
   - `--kieu tiktok` (chữ vàng viền đen, mặc định — hợp video ngắn bán hàng)
   - `--kieu don-gian` (chữ trắng viền đen — lịch sự, hợp YouTube/hướng dẫn)
   - `--kieu hop-den` (chữ trắng trên hộp đen mờ — dễ đọc trên nền rối)
   - `--kieu trang-den` (chữ đen viền trắng)
   - Thêm `--in-hoa` cho phong cách TikTok mạnh; `--co lon` khi xem trên điện thoại; `--vi-tri giua` nếu phía dưới có chữ/sản phẩm.
4. Tự kiểm tra: `studio khung-hinh <kết quả> --so 6 --kiem-tra` → xem `_TONG-HOP.jpg` (chữ có che mặt/sản phẩm không, có tràn mép không).
5. Báo kết quả. Nhắc: file `.srt` có thể tải riêng lên YouTube/Facebook làm phụ đề bật/tắt được.

## Làm nhanh (khi người dùng vội)
`studio phu-de <video> --dot-vao` (nghe + đốt luôn, bỏ qua bước sửa chính tả) — nói rõ là bản nhanh, có thể sai vài chữ.

## Chép lời / gỡ băng
Chỉ cần bước 1, đưa nội dung file `.txt` (đã sửa chính tả, chia đoạn hợp lý) cho người dùng. Có thể tóm tắt, rút ý chính, hoặc chuyển thành bài viết nếu họ muốn (xem skill `viet-content`).

## Lưu ý
- Video không có tiếng nói (chỉ nhạc) → báo lại, gợi ý chèn chữ bằng `studio chu` hoặc `video-tu-anh --chu`.
- Video > 10 phút: báo trước sẽ mất vài phút.
