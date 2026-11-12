---
name: video-tu-anh
description: Dựng video ngắn (TikTok/Reels/Shorts/YouTube) từ nhiều ảnh - hiệu ứng zoom chậm, chuyển cảnh, chữ từng cảnh, nhạc nền; kể cả quy trình video "người que"/minh họa theo kịch bản từng cảnh. Dùng khi người dùng muốn "làm video từ ảnh", "slideshow", "video sản phẩm từ hình", "video kể chuyện bằng tranh".
---

# Video từ ảnh

Lệnh: `uv run python -m studio anh-thanh-video <ảnh...|thư-mục> [tùy chọn]`

| Tùy chọn | Ý nghĩa | Mặc định |
|---|---|---|
| `--ti-le` | 9:16 (TikTok/Reels), 16:9 (YouTube), 1:1, 4:5 | 9:16 |
| `--giay-moi-anh` | số giây mỗi ảnh (video viral: 1.5–2.5; sản phẩm: 3–4) | 3 |
| `--kieu` | `nen-mo` giữ trọn ảnh + nền mờ / `cat` tràn khung | nen-mo |
| `--hieu-ung` | `zoom` (zoom chậm luân phiên vào/ra) / `khong` | zoom |
| `--chuyen-canh` | fade, slideleft, slideup, circleopen, dissolve, smoothleft, radial, `ngau-nhien` | fade |
| `--chu` | chữ từng ảnh, ngăn bằng `|`; để trống giữa 2 dấu `|` = ảnh đó không có chữ | — |
| `--nhac`, `--am-luong` | nhạc nền (tự cắt vừa + nhỏ dần cuối) | — |
| `--vi-tri`, `--co`, `--mau`, `--mau-nen` | kiểu chữ | dưới, vừa, trắng viền đen |

## Quy trình
1. Gom ảnh: thư mục người dùng chỉ định hoặc ảnh trong `01-DAU-VAO`. Thứ tự = thứ tự người dùng nói, hoặc theo tên file. Hỏi lại nếu thứ tự quan trọng mà không rõ.
2. Đề xuất nhanh (1 câu) nội dung chữ cho từng ảnh nếu là video bán hàng — dùng giọng văn trong `03-THUONG-HIEU/thuong-hieu.md`. Chữ ngắn: tối đa ~6–8 từ/ảnh.
3. Chạy lệnh. Khoảng 10 ảnh mất 1–3 phút → báo trước.
4. Tự kiểm tra bằng `khung-hinh <kết quả> --kiem-tra` (xem chữ có bị che/tràn không). Có thể bổ sung `phu-de`/`logo` sau.

## Công thức video hay dùng
- **Video sản phẩm 15 giây**: 5 ảnh × 3s, chữ: [Vấn đề] | [Sản phẩm] | [Điểm nổi bật 1] | [Điểm nổi bật 2] | [Giá + kêu gọi mua]. `--chuyen-canh ngau-nhien`.
- **Feedback khách hàng**: ảnh chụp màn hình feedback, `--kieu vua`, `--giay-moi-anh 3`, chữ nhấn mạnh 1 câu khen.
- **Video "người que"/minh họa kể chuyện** (theo quy trình kênh viral):
  1. Dùng skill `viet-content` → tiêu đề viral + kịch bản 15–30 cảnh, mỗi cảnh 1.5–2 giây: TỪ KHÓA (≤3 từ, in hoa) + LỜI ĐỌC + MÔ TẢ HÌNH.
  2. Dùng skill `prompt-anh-ai` → prompt ảnh người que cho từng cảnh (nền be #FDF6E3, nét đen, có chữ TỪ KHÓA).
  3. Người dùng tạo ảnh trên Gemini/ChatGPT, lưu theo tên `01.png, 02.png...` vào một thư mục con trong `01-DAU-VAO`.
  4. `anh-thanh-video <thư-mục> --giay-moi-anh 2 --hieu-ung zoom --chuyen-canh fade` (+ `--nhac`).
  5. Lời đọc: người dùng tự thu âm hoặc dùng giọng AI (CapCut/Vbee), sau đó `studio nhac <video> <giọng-đọc.mp3> --am-luong 1 --khong-giam-nhac`, rồi `phu-de`.
