---
name: them-cong-cu
description: Dành cho NGƯỜI QUẢN LÝ workspace - tích hợp thêm một công cụ/repo mã nguồn mở (agent sửa video, tạo ảnh/video AI chạy local, phần mềm edit) hoặc một skill mới vào workspace sao cho người dùng cuối chỉ cần nói chuyện là dùng được. Dùng khi có yêu cầu "thêm công cụ", "cài repo này", "tích hợp", "thêm skill".
---

# Thêm công cụ / repo mới

Mục tiêu: người dùng cuối (không biết IT) **không phải cài hay gõ gì thêm** — mọi thứ được đóng gói thành skill + ghi trong danh sách.

## Bước 1 — Đánh giá trước khi thêm (báo lại cho người quản lý)
- Đọc README, giấy phép (LICENSE), yêu cầu hệ thống. **Không chạy script cài đặt nào trước khi đọc nội dung của nó.**
- Kiểm tra: chạy được trên **Windows** không? Cần GPU/NVIDIA không? Cần API key trả phí không? Dung lượng tải về? Có gửi dữ liệu ra ngoài không?
- Giấy phép cho dùng thương mại không (MIT/Apache = thoải mái; GPL = được dùng, chú ý khi phân phối lại; "non-commercial" = báo rõ).
- Có dấu hiệu đáng ngờ (tải file .exe lạ, mã hóa/che giấu code, đòi mật khẩu) → **dừng và báo**.

## Bước 2 — Đặt công cụ vào workspace
- Repo Python: ưu tiên thêm thành **dependency** trong `pyproject.toml` (`uv add <gói>`) nếu có trên PyPI; nếu không → clone vào `05-CONG-CU-THEM/<ten-cong-cu>/` (thư mục con này nằm trong `.gitignore` nếu nặng; khi đó ghi lệnh clone vào skill để máy mới tự tải).
- Phần mềm Windows cài đặt riêng (.exe): ghi hướng dẫn tải + cài từng bước có ảnh/tên nút vào skill; kiểm tra có bản portable (không cần cài) thì ưu tiên.
- Model AI tải về: đặt cache trong `.cache/` của workspace.

## Bước 3 — Tạo skill bọc công cụ
- Dùng skill `skill-creator` để viết `.claude/skills/<ten-khong-dau>/SKILL.md`:
  - `description` nêu rõ **người dùng sẽ nói gì** để kích hoạt (tiếng Việt đời thường).
  - Hướng dẫn Claude: kiểm tra công cụ đã sẵn sàng chưa → nếu chưa thì tự cài → chạy → lưu kết quả vào `02-THANH-PHAM/<ngày>/` → tự kiểm tra kết quả → báo người dùng.
  - Ghi rõ lỗi thường gặp + cách xử lý.
- Nếu công cụ có lệnh dòng lệnh: thêm quyền chạy vào `.claude/settings.json` (`allow`, cả dạng `Bash(...)` và `PowerShell(...)`), **chỉ** đúng lệnh cần thiết.

## Bước 4 — Đăng ký & kiểm thử
- Thêm 1 dòng vào `05-CONG-CU-THEM/DANH-SACH.md` (tên, làm được gì, câu nói kích hoạt, cần mạng/key không, giấy phép).
- Nếu công cụ thay thế việc "viết prompt để dán web" (tạo ảnh/video AI chạy local) → cập nhật skill `prompt-anh-ai` / `prompt-video-ai` để ưu tiên công cụ mới.
- Thử như người dùng thật: nói câu kích hoạt bằng tiếng Việt, kiểm tra từ đầu đến cuối trên máy Windows sạch nếu có thể.
- Cập nhật `HUONG-DAN-QUAN-LY.md` (mục Lịch sử thay đổi).
