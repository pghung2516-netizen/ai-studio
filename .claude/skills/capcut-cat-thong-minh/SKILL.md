---
name: capcut-cat-thong-minh
description: Cắt thông minh dự án CapCut trên máy - bỏ khoảng lặng, bỏ câu nói lặp/nói vấp (giữ lần nói cuối), sửa/tách/gộp phụ đề tự động của CapCut. Dùng khi người dùng nói "cắt khoảng lặng", "smart cut", "cắt dự án CapCut", "sửa phụ đề CapCut", "xem các dự án CapCut".
---

# CapCut – cắt thông minh

> Dựa trên skill mã nguồn mở "capcut-smartcut", đã bổ sung bước **tự sao lưu** trước khi sửa. Chạy offline, không cần API key.
> ⚠️ Tính năng thử nghiệm: CapCut thay đổi định dạng dự án theo phiên bản. Nếu báo lỗi đọc dự án → bản CapCut đó chưa hỗ trợ; dùng cách thay thế ở cuối.

Lệnh: `uv run python .claude/skills/capcut-cat-thong-minh/scripts/cli.py <lệnh> --args '<json>'`
(PowerShell: bọc JSON trong nháy đơn; bên trong dùng nháy kép.)

| Lệnh | Việc | `--args` chính |
|---|---|---|
| `list` | Liệt kê dự án CapCut | — |
| `open` | Xem dự án: đoạn video + phụ đề (kèm thời gian từng chữ) | `project_name` |
| `smart-cut` | Cắt khoảng lặng + lần nói lặp (lượt đầu, tự động) | `project_name`, `silence_threshold_sec` (mặc định 1.0) |
| `cut-ranges` | Cắt chính xác các khoảng bạn tự xác định | `project_name`, `ranges`: `[{"start_sec":..,"end_sec":..}]` |
| `edit-subtitle` / `split-subtitle` / `merge-subtitles` / `batch-edit` | Sửa phụ đề | xem `--help` |

## Quy trình bắt buộc
1. Người dùng chuẩn bị (hướng dẫn bằng lời thường): mở CapCut → nhập video → **Văn bản → Phụ đề tự động** (Text → Auto captions) → lưu → **ĐÓNG HẲN CapCut**. Hỏi xác nhận đã đóng CapCut.
2. `list` → xác nhận đúng dự án với người dùng.
3. **Sao lưu**: `uv run python -m studio capcut-sao-luu "<tên dự án>"` (bắt buộc, không được bỏ qua).
4. `smart-cut` với dự án đó → báo đã cắt bao nhiêu đoạn / bao nhiêu giây.
5. **Rà soát lời thoại (bắt buộc — bộ tự động bỏ sót)**: `open` và **đọc toàn bộ phụ đề còn lại**, tìm:
   - Câu nói lặp: xóa các lần trước, **luôn giữ lần nói CUỐI** (người nói thử lại tới khi nói chuẩn).
   - Câu bỏ dở rồi nói lại; lặp trong cùng 1 câu ("hôm nay hôm nay"); từ đệm lẻ loi ("ờ", "à", "thì thì").
   - Tính khoảng `{start_sec, end_sec}` (từ đầu chữ thừa đến đầu chữ giữ lại, dùng thời gian từng chữ) → `cut-ranges` **1 lần cho tất cả**.
6. `open` lại, đọc lại; còn lặp → lặp lại bước 5. Mỗi lần cắt xong, mốc thời gian cũ không còn đúng → luôn `open` lại trước khi tính tiếp.
7. Nhắc người dùng mở lại CapCut để xem (nếu chưa thấy thay đổi → tắt hẳn rồi mở lại). Không ưng → chép thư mục sao lưu đè lại (bạn hướng dẫn hoặc làm giúp).

## Cách thay thế khi CapCut không đọc được
Xuất video từ CapCut ra file MP4 → `studio phu-de` để có lời thoại + mốc giờ → xác định đoạn thừa → cắt bằng `studio cat` các đoạn cần giữ rồi `studio ghep` lại.
