---
name: phu-de
description: Làm phụ đề tiếng Việt (hoặc ngôn ngữ khác) cho video bằng AI chạy trên máy, sửa chính tả phụ đề, đốt phụ đề vào video theo kiểu TikTok, chép lời video thành văn bản. Dùng khi người dùng nói "phụ đề", "sub", "caption chạy chữ", "chép lời", "gỡ băng", "transcript".
---

# Phụ đề

Mọi lệnh chạy qua `uv run python -m studio <lệnh> --du-an "<dự án>"`. Các file phụ đề và video nháp tự động lưu trong `.cache/nhap/<dự án>/`.

## Quy trình chuẩn (chất lượng cao)
1. **Mở hoặc tạo dự án**:
   - Nếu làm tiếp video trong dự án: `uv run python -m studio du-an ds` / `du-an xem "<dự án>"`.
   - Nếu việc mới: `uv run python -m studio du-an moi "<Tên dự án>" [video] [--lay-hop-thu]`. File từ `01-DAU-VAO` (Hộp thư đến) được chuyển vào `Gốc/`.
   - Nếu người dùng nói "lấy video vừa tải về": `tim-file-moi --loai video`.
2. **Hỏi ý tưởng** (khi làm video hoàn thiện cho kênh mạng xã hội): nếu chưa rõ phong cách, chạy skill `hoi-y-tuong` (hỏi bằng lựa chọn bấm được: kiểu chữ TikTok/YouTube, màu sắc, vị trí) → ghi brief bằng `uv run python -m studio du-an ghi "<dự án>" "<bản yêu cầu phụ đề>"`. Nếu chỉ yêu cầu kỹ thuật đơn giản thì dùng mặc định tốt.
3. **Tạo phụ đề**: `uv run python -m studio phu-de <video> --du-an "<dự án>"` → tạo `..._phu-de.srt` và `..._phu-de.txt` (lời thoại liền mạch) trong thư mục nháp của dự án.
   - Mặc định tiếng Việt, mô hình `vua`. Người nói tiếng Anh → `--ngon-ngu en`; không rõ → `--ngon-ngu tu-dong`.
   - Giọng địa phương nặng / nhiều tạp âm → `--mo-hinh chuan` (chính xác hơn, chậm hơn ~3 lần; lần đầu tải thêm ~1.5 GB).
4. **Đọc file .srt và tự sửa lỗi chính tả** bằng công cụ Edit (chỉ sửa chữ, **giữ nguyên số thứ tự và dòng thời gian**):
   - Tên riêng, tên sản phẩm, thương hiệu (đối chiếu `03-THUONG-HIEU/thuong-hieu.md`).
   - Từ nghe nhầm phổ biến (vd "trí tội" → "trí tuệ"), dấu câu, viết hoa đầu câu.
   - Không thêm/bớt ý của người nói.
5. **Đốt vào video**: `uv run python -m studio dot-phu-de <video> <file.srt> --du-an "<dự án>"` với kiểu phù hợp:
   - `--kieu tiktok` (chữ vàng viền đen, mặc định — hợp video ngắn bán hàng)
   - `--kieu don-gian` (chữ trắng viền đen — lịch sự, hợp YouTube/hướng dẫn)
   - `--kieu hop-den` (chữ trắng trên hộp đen mờ — dễ đọc trên nền rối)
   - `--kieu trang-den` (chữ đen viền trắng)
   - Thêm `--in-hoa` cho phong cách TikTok mạnh; `--co lon` khi xem trên điện thoại; `--vi-tri giua` nếu phía dưới có chữ/sản phẩm.
6. **Tự kiểm tra**: `uv run python -m studio khung-hinh <kết quả> --du-an "<dự án>" --so 6 --kiem-tra` → xem `_TONG-HOP.jpg` (chữ có che mặt/sản phẩm không, có tràn mép không).
7. **Chốt bản cuối & mở thư mục**:
   - `uv run python -m studio du-an chot "<dự án>" <video nháp> --ten "Phụ đề TikTok" --kem-phu-de` → xuất bản hoàn thiện vào `02-DU-AN/<dự án>/Thành phẩm/` kèm file `.srt` để người dùng có thể tải riêng lên YouTube/Facebook.
   - Ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "Đã tạo phụ đề, sửa chính tả và đốt vào video."`.
   - Mở thư mục `Thành phẩm` cho người dùng: PowerShell `Invoke-Item "02-DU-AN\<dự án>\Thành phẩm"` (Mac: `open`).
8. **Gợi ý bước tiếp / chỉnh sửa**: hỏi bằng lựa chọn bấm được (đổi kiểu chữ, đổi vị trí, thêm nhạc nền).

## Làm nhanh (khi người dùng vội)
`uv run python -m studio phu-de <video> --du-an "<dự án>" --dot-vao` (nghe + đốt luôn, bỏ qua bước sửa chính tả) — nói rõ là bản nhanh, có thể sai vài chữ. Sau đó `du-an chot` bản này.

## Chép lời / gỡ băng
Chỉ cần bước 1 và 3, đưa nội dung file `.txt` (đã sửa chính tả, chia đoạn hợp lý) cho người dùng trong chat. Lưu bản chép lời vào dự án: lưu file text nháp rồi `du-an chot "<dự án>" <file.txt> --ten "Bản gỡ băng"`. Có thể tóm tắt hoặc chuyển thành bài viết nếu họ muốn (xem skill `viet-content`).

## Lưu ý
- Video không có tiếng nói (chỉ nhạc) → báo lại, gợi ý chèn chữ bằng `studio chu` hoặc `video-tu-anh --chu`.
- Video > 10 phút: báo trước sẽ mất vài phút.
