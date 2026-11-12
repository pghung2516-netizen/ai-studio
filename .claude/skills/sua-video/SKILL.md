---
name: sua-video
description: Sửa video thật (quay bằng điện thoại/máy quay) - cắt đoạn, ghép nhiều clip, đổi khung dọc 9:16/ngang 16:9/vuông, nén nhẹ, tua nhanh/chậm, chèn nhạc nền, logo, chữ, xoay, tách/bỏ âm thanh, chuẩn âm lượng, làm GIF. Dùng cho mọi yêu cầu chỉnh sửa video có sẵn.
---

# Sửa video

Luôn dùng `uv run python -m studio <lệnh>` (xem `--help` của từng lệnh khi cần). Tất cả lệnh tự lưu vào `02-THANH-PHAM/<ngày>/`, không ghi đè.

## Quy trình
1. **Xác định file**: tên file người dùng nói / file mới nhất trong `01-DAU-VAO` (`studio danh-sach`). Không chắc → hỏi kèm danh sách để chọn.
2. **Đọc thông tin**: `studio thong-tin <file>` → biết độ dài, khung, có tiếng không.
3. **Làm** theo bảng dưới. Việc nhiều bước → nối tiếp, mỗi bước dùng file `KET QUA` của bước trước.
4. **Tự kiểm tra**: `thong-tin` file kết quả; nếu có chữ/logo/đổi khung → `khung-hinh <file> --so 6 --kiem-tra` và **xem ảnh `_TONG-HOP.jpg`**.
5. **Báo kết quả** + mở thư mục (PowerShell: `Invoke-Item "<thư mục>"`), gợi ý bước tiếp.

## Bảng ánh xạ yêu cầu → lệnh

| Người dùng nói | Lệnh |
|---|---|
| "cắt từ 0:10 đến 0:40", "lấy 30 giây đầu" | `cat <v> --tu 0:10 --den 0:40` / `cat <v> --dai 30` |
| "bỏ 5 giây đầu" | `cat <v> --tu 5` |
| "ghép các video" | `ghep <v1> <v2> ...` hoặc `ghep <thư-mục>` (+ `--ti-le 9:16` nếu cần đồng nhất) |
| "đổi sang dọc / TikTok / Reels / Shorts" | `khung <v> --ti-le 9:16` (mặc định `--kieu nen-mo`: giữ trọn hình, nền mờ. Muốn tràn màn hình → `--kieu cat`, mất 2 bên mép) |
| "đổi sang ngang YouTube" / "vuông" / "4:5 Facebook" | `khung <v> --ti-le 16:9` / `1:1` / `4:5` |
| "nén nhẹ", "gửi Zalo/email không được" | `nen <v>`; Zalo/email giới hạn → `nen <v> --toi-da-mb 25`; muốn nhẹ hơn nữa `--toi-da 720` |
| "tua nhanh 2 lần" / "làm chậm" | `toc-do <v> --he-so 2` / `--he-so 0.5` |
| "thêm nhạc nền" | `nhac <v> <nhạc>` (tự lặp/cắt vừa video, tự nhỏ nhạc khi có người nói). Nhạc to/nhỏ → `--am-luong 0.15..0.5`. Chỉ giữ nhạc → `--bo-tieng-goc` |
| "âm thanh lúc to lúc nhỏ", "tiếng nhỏ quá" | `chuan-am <v>` |
| "bỏ tiếng" / "lấy nhạc/tiếng ra file mp3" | `tat-tieng <v>` / `tach-am <v>` |
| "chèn logo" | `logo <v> <logo.png> --vi-tri tren-phai --ti-le 0.15` (logo lấy từ `03-THUONG-HIEU/` nếu có) |
| "chèn chữ / tiêu đề / giá" | `chu <v> --noi-dung "..." [--tu 0 --den 3] [--vi-tri tren] [--mau-nen "#E53935"]` |
| "video bị ngược / nằm ngang" | `xoay <v> --huong phai` (hoặc `trai`, `180`, `lat-ngang`) |
| "làm GIF" | `gif <v> --tu 2 --den 5` |
| "xem trong video có gì" | `khung-hinh <v> --so 12` → xem `_TONG-HOP.jpg` |

## Mặc định thông minh (dùng khi người dùng không nói)
- Đăng TikTok/Reels/Shorts → 9:16, thường kèm `phu-de` + `chuan-am` (gợi ý, không tự làm nếu họ không muốn).
- Logo: góc trên-phải, 15% chiều rộng, độ rõ 0.9.
- Màu chữ/hộp nền: lấy từ `03-THUONG-HIEU/thuong-hieu.md` nếu có.
- Video bán hàng: nhắc khéo nếu nhạc người dùng đưa là nhạc nổi tiếng có bản quyền (dễ bị tắt tiếng/đánh gậy).

## Khi gặp lỗi
- Đọc dòng `❌` (lỗi đầu vào) → sửa tham số và chạy lại, chỉ hỏi người dùng nếu thật sự cần.
- Lỗi kỹ thuật ffmpeg → thử lại với file đã chuyển chuẩn trước: `nen <v> --muc nhe` rồi làm tiếp trên file đó. Vẫn lỗi → skill `cai-dat`.
- Video rất dài (> 20 phút): báo trước thời gian xử lý, gợi ý cắt đoạn cần dùng trước.
