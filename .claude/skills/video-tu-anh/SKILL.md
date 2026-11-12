---
name: video-tu-anh
description: Dựng video ngắn (TikTok/Reels/Shorts/YouTube) từ nhiều ảnh - hiệu ứng zoom chậm, chuyển cảnh, chữ từng cảnh, nhạc nền; kể cả quy trình video "người que"/minh họa theo kịch bản từng cảnh. Dùng khi người dùng muốn "làm video từ ảnh", "slideshow", "video sản phẩm từ hình", "video kể chuyện bằng tranh".
---

# Video từ ảnh

Lệnh: `uv run python -m studio anh-thanh-video <ảnh...|thư-mục> --du-an "<dự án>" [tùy chọn]`
Video nháp được lưu tự động trong `.cache/nhap/<dự án>/` và ảnh đầu vào được tìm trong `Gốc/` của dự án.

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
1. **Mở hoặc tạo dự án**:
   - Nếu làm tiếp: `uv run python -m studio du-an ds` / `du-an xem "<dự án>"`.
   - Nếu việc mới: `uv run python -m studio du-an moi "<Tên dự án>" [ảnh...] [--lay-hop-thu]`. File từ `01-DAU-VAO` (Hộp thư đến) được chuyển vào `Gốc/`; file từ chat/Downloads được chép vào `Gốc/`.
   - Nếu người dùng nói "lấy ảnh vừa tải về": `tim-file-moi --loai anh`.
2. **Hỏi ý tưởng** (skill `hoi-y-tuong`):
   - Đặt câu hỏi bằng các lựa chọn bấm được: loại video (sản phẩm 15s / feedback / tranh kể chuyện), tỷ lệ khung (9:16 dọc / 16:9 ngang), nhạc nền, chữ trên từng ảnh (đọc `03-THUONG-HIEU/thuong-hieu.md` để dùng đúng giọng văn). Người dùng có thể chọn hoặc nói "bạn quyết giúp mình".
   - Chốt brief và ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "<bản yêu cầu video từ ảnh>"`.
3. **Thực hiện**: chạy `anh-thanh-video` với `--du-an "<dự án>"`. Khoảng 10 ảnh mất 1–3 phút → báo trước thời gian.
4. **Tự kiểm tra**: `studio khung-hinh <kết quả> --du-an "<dự án>" --kiem-tra` → xem ảnh tổng hợp `_TONG-HOP.jpg` (xem chữ có bị che/tràn không, chuyển cảnh mượt không).
5. **Chốt bản cuối & mở thư mục**:
   - `uv run python -m studio du-an chot "<dự án>" <file nháp> --ten "<nhãn, vd TikTok>" [--ghi-chu "<vd 5 ảnh kèm nhạc>"]` → lưu vào `02-DU-AN/<dự án>/Thành phẩm/`.
   - Ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "<chi tiết các tham số video đã dựng>"`.
   - Mở thư mục `Thành phẩm` cho người dùng: PowerShell `Invoke-Item "02-DU-AN\<dự án>\Thành phẩm"` (Mac: `open`).
6. **Gợi ý bước tiếp / tùy chỉnh**: hỏi bằng lựa chọn bấm được (thêm phụ đề `phu-de`, gắn logo `logo`, đổi nhạc, hoặc đổi tốc độ).

## Công thức video hay dùng
- **Video sản phẩm 15 giây**: 5 ảnh × 3s, chữ: [Vấn đề] | [Sản phẩm] | [Điểm nổi bật 1] | [Điểm nổi bật 2] | [Giá + kêu gọi mua]. `--chuyen-canh ngau-nhien`.
- **Feedback khách hàng**: ảnh chụp màn hình feedback, `--kieu vua`, `--giay-moi-anh 3`, chữ nhấn mạnh 1 câu khen.
- **Video "người que"/minh họa kể chuyện** (theo quy trình kênh viral):
  1. Dùng skill `viet-content` → tiêu đề viral + kịch bản 15–30 cảnh, mỗi cảnh 1.5–2 giây: TỪ KHÓA (≤3 từ, in hoa) + LỜI ĐỌC + MÔ TẢ HÌNH.
  2. Dùng skill `prompt-anh-ai` → prompt ảnh người que cho từng cảnh (nền be #FDF6E3, nét đen, có chữ TỪ KHÓA).
  3. Người dùng tạo ảnh trên Gemini/ChatGPT, bỏ vào `01-DAU-VAO` → đưa vào `Gốc/` của dự án (`du-an them`).
  4. `anh-thanh-video <thư-mục> --du-an "<dự án>" --giay-moi-anh 2 --hieu-ung zoom --chuyen-canh fade` (+ `--nhac`).
  5. Lời đọc: người dùng tự thu âm hoặc dùng giọng AI (CapCut/Vbee), sau đó `studio nhac <video> <giọng-đọc.mp3> --du-an "<dự án>" --am-luong 1 --khong-giam-nhac`, rồi `phu-de`.
  6. `du-an chot` bản hoàn thiện cuối cùng.
