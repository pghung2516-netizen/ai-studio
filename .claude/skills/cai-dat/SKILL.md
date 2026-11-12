---
name: cai-dat
description: Cài đặt / sửa môi trường của workspace trên Windows (uv, Python, thư viện, ffmpeg, mô hình AI) và xử lý lỗi kiểu "uv is not recognized", "No module named", "ffmpeg", thiếu .venv. Dùng khi người dùng nói "cài đặt", "setup", lần đầu mở workspace, hoặc khi lệnh studio báo lỗi môi trường.
---

# Cài đặt & sửa môi trường

Người dùng không biết IT → **bạn tự chạy mọi lệnh**, chỉ báo tiến độ bằng lời thường ("đang tải công cụ, khoảng 3–5 phút..."). Không cần quyền Administrator.

## Cách nhanh nhất
Người dùng có thể **nhấp đúp `CAI-DAT.bat`** ở thư mục gốc — file này làm toàn bộ các bước dưới. Nếu họ đã chạy mà vẫn lỗi, hoặc muốn bạn làm hộ → làm theo các bước sau.

## Các bước (Windows, chạy trong PowerShell tại thư mục gốc workspace)

1. **Kiểm tra uv**: `uv --version`
   - Nếu báo không nhận ra lệnh → cài uv (chỉ cho người dùng hiện tại, không cần admin):
     `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - uv được cài vào `%USERPROFILE%\.local\bin`. Trong phiên hiện tại, nếu `uv` vẫn chưa nhận → gọi thẳng `"$env:USERPROFILE\.local\bin\uv.exe"` thay cho `uv` ở các bước sau, và nhắc người dùng **đóng mở lại ứng dụng Claude** sau khi xong.
2. **Cài Python + thư viện** (uv tự tải Python 3.12, không đụng Python khác trên máy):
   `uv sync`
   - Lần đầu tải khoảng 300–600 MB, mất 3–10 phút tùy mạng.
3. **Tải trước mô hình AI** (phụ đề + xóa nền, ~650 MB) để lần dùng đầu không phải chờ:
   `uv run python -m studio tai-mo-hinh`
4. **Kiểm tra**: `uv run python -m studio kiem-tra` → phải thấy "🎉 MỌI THỨ ĐÃ SẴN SÀNG".

## Sửa lỗi thường gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `uv` không được nhận dạng | Bước 1. Sau khi cài phải mở lại Claude, hoặc gọi đường dẫn đầy đủ. |
| `No module named ...` / thiếu thư viện | `uv sync` lại. Nếu vẫn lỗi: xóa thư mục `.venv` (hỏi người dùng trước) rồi `uv sync`. |
| Lỗi mạng khi `uv sync` / tải mô hình | Mạng công ty/wifi chặn. Thử lại; nếu vẫn lỗi, nhờ người dùng đổi mạng (vd phát 4G từ điện thoại). |
| `kiem-tra` cảnh báo **OneDrive** | Khuyên người dùng chép cả thư mục sang `C:\AI-Studio` (OneDrive đồng bộ video nặng rất chậm, dễ lỗi). |
| Đường dẫn quá dài / ký tự lạ | Khuyên đặt workspace ở `C:\AI-Studio` (ngắn, không dấu, không khoảng trắng). |
| Ổ đĩa đầy | Gợi ý xóa bớt kết quả cũ trong `02-THANH-PHAM` (hỏi trước khi xóa). |
| Phụ đề/xóa nền chậm lần đầu | Bình thường — đang tải mô hình. Các lần sau nhanh. |
| Antivirus chặn `uv.exe`/`ffmpeg` | Nhờ người dùng bấm "Allow/Cho phép" trong cảnh báo Windows Security. |

## Cập nhật workspace (khi người quản lý báo có bản mới)
- Nếu thư mục là git clone: `git pull` rồi `uv sync`.
- Nếu tải bằng file ZIP: hướng dẫn người dùng tải ZIP mới, giải nén đè lên (giữ nguyên `01-DAU-VAO`, `02-THANH-PHAM`, `03-THUONG-HIEU`), rồi chạy `uv sync`.
