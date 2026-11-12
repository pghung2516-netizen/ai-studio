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
.claude/skills/           17 skill tiếng Việt + 3 skill Anthropic
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
| `video-dong-html` | Video động HTML (HyperFrames + GSAP + three.js), cài ở `05-CONG-CU-THEM/hyperframes/` |
| `video-remotion` | Hàng loạt video từ bảng dữ liệu (Remotion), cài ở `05-CONG-CU-THEM/remotion/` — giấy phép có điều kiện |
| `video-giai-thich` | Hoạt hình giải thích (Manim 0.22.1, chạy qua `uv run --with`, không thêm vào pyproject) |
| `blender-3d` | Dựng 3D qua Blender MCP (mcp-for-blender 2.2.8, add-on kèm trong skill) |
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
- v1.1 (2026-11-13) — thêm 4 skill dựng video không cần quay: `video-dong-html` (HyperFrames/GSAP/three.js), `video-remotion`, `video-giai-thich` (Manim), `blender-3d` (Blender MCP). Bảng chọn công cụ trong CLAUDE.md, menu mới. Đã render thử trên Mac (chưa test Windows; `blender-3d` chưa test với Blender thật).
  - Còn chờ người quản lý duyệt: quyền tự chạy lệnh trong `.claude/settings.json` và file `.mcp.json` cho Blender (Claude không được tự sửa file cấu hình).
- v1.1.1 (2026-11-13) — sửa issue #1: cài đặt trên máy bật Smart App Control và có antivirus quét HTTPS. Dùng Python có chữ ký từ python.org, kho chứng chỉ hệ thống (truststore, UV_SYSTEM_CERTS, NODE_USE_SYSTEM_CA), báo lỗi đúng nguyên nhân.
- v1.2 (2026-11-13) — lớp "app" (hướng A: vẫn dùng Claude Desktop làm giao diện):
  - Bộ icon `assets/icon/` (vẽ lại bằng `uv run python scripts/tao-icon.py`).
  - `CAI-DAT.bat` tự tạo 3 lối tắt trên Desktop và Start Menu (`scripts/tao-loi-tat.ps1`).
  - Trình mở `scripts/mo-ai-studio.ps1` (+ `MO-TTOMORROW-STUDIO.bat`): mở Claude Desktop, chép sẵn đường dẫn workspace, lần đầu mở `HUONG-DAN-NHANH.html`.
  - Các script chạy được cả khi PowerShell ở chế độ hạn chế (Constrained Language Mode, gặp trên máy bật Smart App Control).
  - Tên app nằm ở biến `$TenApp` trong 3 script + icon + trang hướng dẫn.
  - Chưa test trên Windows: xem mục E trong `KIEM-THU.md`.
- v1.2.1 (2026-11-13) — đổi tên app hiển thị thành **TTomorrow Studio** (lối tắt, trang hướng dẫn, bộ cài, `MO-TTOMORROW-STUDIO.bat`). Tên repo và tên file nội bộ (`mo-ai-studio.ps1`, `ai-studio.ico`) giữ nguyên.
- v1.3 (2026-11-13) — **Mỗi việc là một dự án** + **hỏi ý kiểu "grill me"**:
  - `02-DU-AN/<ngày> <Tên>/` gồm `Gốc/`, `Thành phẩm/` (chỉ bản cuối, tên có dấu, "bản N (ghi chú)"), `nhat-ky.md`; nháp ở `.cache/nhap/`. `01-DAU-VAO` thành Hộp thư đến: file được **chuyển** sang dự án (không sửa/xóa).
  - Lệnh mới: `studio du-an moi|them|ds|xem|ghi|chot`, tùy chọn chung `--du-an` cho mọi lệnh xử lý, `tim-file-moi` (Downloads, Desktop, Zalo, Pictures, Videos), `don-dep` (chuyển vào Thùng rác qua `send2trash`, luôn hỏi trước). Test: 44 ca.
  - Skill mới `hoi-y-tuong`: xem tư liệu → đề xuất 2–3 hướng → hỏi bằng lựa chọn bấm được → chốt bản yêu cầu → làm → hỏi tiếp để làm bản sau. 11 skill cũ chuyển sang quy trình dự án; `CLAUDE.md` có "Quy trình một việc".
  - Trình mở ưu tiên **IDE có Claude Code** (Antigravity / VS Code / Cursor) — mở thẳng workspace; chọn bằng `.cache/mo-bang.txt` (`tu-dong` | `ide` | `claude-desktop`). Lối tắt đổi tên: "Hộp thư đến", "Dự án của tôi".
  - Video mẫu Manim: bố cục dọc cân đối, tiêu đề không xuống dòng (helper `bo_cuc_doc()`).
  - Chưa test Windows: mục F trong `KIEM-THU.md`.
