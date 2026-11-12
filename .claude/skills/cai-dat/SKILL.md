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
2. **Cài Python 3.12 chính thức + thư viện**:
   `winget install --id Python.Python.3.12 -e --source winget --scope user --silent`
   Sau đó đặt `UV_PYTHON_DOWNLOADS=never`, tìm `python.exe` và chạy:
   `uv sync --python "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" --system-certs`
   - Lần đầu tải khoảng 300–600 MB, mất 3–10 phút tùy mạng.
3. **Tải trước mô hình AI** (phụ đề + xóa nền, ~650 MB) để lần dùng đầu không phải chờ:
   `uv run python -m studio tai-mo-hinh`
4. **Kiểm tra**: `uv run python -m studio kiem-tra` → phải thấy "🎉 MỌI THỨ ĐÃ SẴN SÀNG".

## Sửa lỗi thường gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `uv` không được nhận dạng | Bước 1. Sau khi cài phải mở lại Claude, hoặc gọi đường dẫn đầy đủ. |
| `No module named ...` / thiếu thư viện | Chạy lại `uv sync --python "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" --system-certs`. Nếu vẫn lỗi: xóa `.venv` (hỏi người dùng trước) rồi chạy lại lệnh này. |
| `4551` / `Application Control policy has blocked` | Smart App Control đang chặn Python do uv tự tải. **Không bao giờ bảo người dùng tắt Smart App Control**. Cài Python 3.12 chính thức bằng `winget install --id Python.Python.3.12 -e --source winget --scope user`, đặt `UV_PYTHON_DOWNLOADS=never`, rồi `uv sync --python "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" --system-certs`. |
| `UnknownIssuer` / `CERTIFICATE_VERIFY_FAILED` / SSL | Antivirus có thể đang quét HTTPS. Đặt `UV_SYSTEM_CERTS=1` và `NODE_USE_SYSTEM_CA=1`; nếu vẫn lỗi, chỉ tạm tắt Web Shield/HTTPS scanning trong lúc cài rồi bật lại. |
| Winget báo `0x8a15005e` ở nguồn msstore | Luôn thêm `--source winget` vào lệnh cài. |
| Timeout / DNS khi `uv sync` / tải mô hình | Kiểm tra kết nối; chỉ đề nghị đổi mạng khi log thật sự báo timeout, DNS hoặc không kết nối được. |
| `kiem-tra` cảnh báo **OneDrive** | Khuyên người dùng chép cả thư mục sang `C:\TTomorrow-Studio` (OneDrive đồng bộ video nặng rất chậm, dễ lỗi). |
| Đường dẫn quá dài / ký tự lạ | Khuyên đặt workspace ở `C:\TTomorrow-Studio` (ngắn, không dấu, không khoảng trắng). |
| Ổ đĩa đầy | Chạy `studio don-dep` (chỉ báo cáo) → hỏi người dùng → `don-dep --xac-nhan` (chuyển dự án cũ vào Thùng rác). |
| Phụ đề/xóa nền chậm lần đầu | Bình thường — đang tải mô hình. Các lần sau nhanh. |
| Antivirus chặn `uv.exe`/`ffmpeg` | Nhờ người dùng bấm "Allow/Cho phép" trong cảnh báo Windows Security. |

## Cập nhật workspace (khi người quản lý báo có bản mới)
- Nếu thư mục là git clone: `git pull` rồi `uv sync`.
- Nếu tải bằng file ZIP: hướng dẫn người dùng tải ZIP mới, giải nén đè lên (giữ nguyên `01-DAU-VAO`, `02-DU-AN`, `02-THANH-PHAM`, `03-THUONG-HIEU`), rồi chạy `uv sync`.
