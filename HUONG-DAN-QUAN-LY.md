# Hướng dẫn cho người quản lý workspace

## 1. Đưa lên GitHub (lần đầu)
```bash
cd "<thư mục workspace>"
git add -A
git commit -m "AI Studio v1.0"
gh repo create ai-studio --private --source=. --push      # hoặc tạo repo trên web rồi git remote add + git push
```
Mời người dùng: GitHub → repo → Settings → Collaborators → Add people (họ cần tài khoản GitHub để tải ZIP từ repo private).

`.gitignore` đã chặn: `.venv`, mô hình AI (`.cache`), file người dùng (`01-DAU-VAO`, `02-THANH-PHAM`, logo trong `03-THUONG-HIEU`), `.env`, và file PDF khóa học ở thư mục gốc. **Kiểm tra `git status` trước khi push lần đầu.**

## 2. Cấu trúc
```
CLAUDE.md                 Vai trò + quy tắc của Claude (luôn được nạp)
BAT-DAU-O-DAY.md          Hướng dẫn người dùng cuối
CAI-DAT.bat               Nhấp đúp để cài (gọi scripts/cai-dat.ps1)
MO-THANH-PHAM.bat         Nhấp đúp để mở thư mục kết quả
studio/                   Bộ lệnh Python: uv run python -m studio <lệnh>
  common.py  video.py  image.py  subtitle.py  doctor.py  cli.py
pyproject.toml, uv.lock   Thư viện (khóa phiên bản, có sẵn bản Windows)
.claude/settings.json     Quyền tự động cho lệnh an toàn, chặn sửa 01-DAU-VAO
.claude/skills/           13 skill tiếng Việt + 3 skill Anthropic
01..05-*/                 Thư mục làm việc của người dùng
assets/fonts/             Be Vietnam Pro (OFL) - font hiển thị đúng tiếng Việt
```

## 3. Skill có sẵn
| Skill | Việc |
|---|---|
| `menu` | Chào + menu việc làm được |
| `cai-dat` | Cài/sửa môi trường Windows |
| `sua-video` | Cắt, ghép, khung, nén, nhạc, logo, chữ, GIF... |
| `phu-de` | Phụ đề offline + sửa chính tả + đốt vào video |
| `video-tu-anh` | Dựng video từ ảnh (cả quy trình "người que") |
| `sua-anh` | Xóa nền, đổi cỡ theo kênh, chữ, logo, ghép ảnh |
| `nhan-xet-video` | Đánh giá video như biên tập viên MXH |
| `prompt-anh-ai` / `prompt-video-ai` | Viết prompt Gemini/ChatGPT/Veo/Sora/Kling (thư viện ở `04-THU-VIEN-PROMPT/`) |
| `viet-content` | Caption, kịch bản, lịch đăng |
| `thuong-hieu` | Thiết lập bộ nhận diện |
| `capcut-cat-thong-minh` | Cắt khoảng lặng/câu lặp trong dự án CapCut (thử nghiệm) |
| `them-cong-cu` | **Dành cho bạn**: tích hợp repo/công cụ mới |
| `canvas-design`, `slack-gif-creator`, `skill-creator` | Skill gốc của Anthropic (Apache-2.0) |

## 4. Thêm repo / công cụ mới
Mở workspace trong Claude Code và nói: **"thêm công cụ <link GitHub>"** → skill `them-cong-cu` đánh giá (Windows? GPU? phí? giấy phép? an toàn?), đóng gói thành skill, đăng ký vào `05-CONG-CU-THEM/DANH-SACH.md`.
Công cụ tạo ảnh/video AI chạy trên máy (nếu có) sẽ được ưu tiên thay cho cách "viết prompt dán web".

## 5. Thử nghiệm trên máy Mac của bạn
Mọi lệnh `studio` chạy được trên Mac: `uv sync` rồi `uv run python -m studio kiem-tra`. Chỉ `CAI-DAT.bat`/`.ps1` là riêng Windows.
Kiểm tra toàn bộ sau khi sửa code: `uv run python scripts/kiem-thu.py` (33 ca, ~1 phút, tự tạo file mẫu, báo cáo ở `.cache/kiem-thu/BAO-CAO.md`).
Quy trình test trên Windows và gửi kết quả về Mac qua GitHub Issue: xem **`KIEM-THU.md`**.

## 6. Cập nhật cho người dùng
- Họ dùng git: nói với Claude "cập nhật workspace" (Claude chạy `git pull` + `uv sync`).
- Họ dùng ZIP: gửi ZIP mới, giải nén đè (giữ `01-DAU-VAO`, `02-THANH-PHAM`, `03-THUONG-HIEU`), chạy lại `CAI-DAT.bat`.

## 7. Nguồn & giấy phép
- `studio/` — viết cho workspace này.
- Font **Be Vietnam Pro** — SIL Open Font License (`assets/fonts/OFL.txt`).
- `canvas-design`, `slack-gif-creator`, `skill-creator` — github.com/anthropics/skills, Apache-2.0 (giữ nguyên `LICENSE.txt` trong từng thư mục).
- `capcut-cat-thong-minh/scripts` — từ skill cộng đồng "capcut-smartcut" (gói "Bộ sưu tập kỹ năng Claude" trên Drive); đã rà soát mã: không gọi mạng, chỉ đọc/ghi thư mục dự án CapCut; bổ sung bước sao lưu. Tác giả gốc không ghi giấy phép → dùng nội bộ, không bán lại.
- Thư viện prompt `04-THU-VIEN-PROMPT/` — **viết lại/tóm lược** từ các tài liệu tham khảo (quy trình AI tạo banner, người que, người mẫu bán hàng, nhân vật 3D; bộ 250 visual code; bộ prompt góc máy/ánh sáng/đồng nhất/quảng cáo Veo; prompt Nano Banana). Không chép nguyên văn ebook; ebook/PDF gốc không đưa vào repo.
- Các skill YouTube dùng dịch vụ Higgsfield (trả phí) trong gói skill Drive **không** đưa vào — có thể thêm sau bằng `them-cong-cu` nếu người dùng có tài khoản Higgsfield.

## 8. Đã kiểm thử
- Trên macOS (Apple Silicon): toàn bộ lệnh `studio` (video, ảnh, phụ đề tiếng Việt, xóa nền, ảnh → video), kết quả được xem lại bằng ảnh khung hình.
- Windows: đã xác minh `uv.lock` có bản cài sẵn (wheel) cho Windows của mọi thư viện nặng, và bản ffmpeg Windows có libass/x264/mp3. **Chưa chạy thử `CAI-DAT.bat` trên máy Windows thật** → nên thử 1 lần trên máy Windows trước khi gửi người dùng.

## Lịch sử thay đổi
- v1.0 — bản đầu tiên.
