# Quy trình kiểm thử Windows ↔ Mac

> File này dành cho **người quản lý** và Claude Code của họ, không dành cho người dùng cuối.
> Khi làm theo file này, Claude đang làm việc với người quản lý (biết kỹ thuật): được dùng thuật ngữ, lệnh, mã lỗi.
> Các quy tắc giao tiếp "cho người không biết IT" trong CLAUDE.md **không áp dụng** trong lúc kiểm thử.

## Phân vai

| Máy | Vai trò | Được làm | Không làm |
|---|---|---|---|
| **Windows** | Người kiểm thử | Clone/pull repo, cài đặt, chạy test, **báo kết quả qua GitHub Issue** | Không sửa code, không commit/push (settings đã chặn `git push`) |
| **Mac** | Người sửa code | Đọc issue, sửa code, commit, push, trả lời issue | — |

Kênh liên lạc duy nhất: **GitHub Issues có nhãn `kiem-thu-windows`**. Mỗi đợt test là 1 issue; test lại là comment trong issue đó.
Lý do: Windows không push code → không bao giờ xung đột git; Mac chỉ đọc đúng phần báo cáo gọn → ít token.

---

## A. Bên Windows (Claude Code trên Windows)

### Lần đầu
1. Cài: Git, GitHub CLI (`winget install GitHub.cli`), Claude Code. Đăng nhập `gh auth login`.
2. Clone repo ra thư mục **không nằm trong OneDrive** và **có dấu tiếng Việt** để test giống người dùng thật, ví dụ `C:\AI Studio thử\`:
   `gh repo clone <chủ-repo>/ai-studio "C:\AI Studio thử"`
3. Người quản lý **tự nhấp đúp `CAI-DAT.bat`** (đây là bài test quan trọng nhất – người dùng thật sẽ làm đúng như vậy). Ghi lại: có lỗi không, mất bao lâu, thông báo có dễ hiểu không.

### Mỗi đợt test
```powershell
git pull
uv sync
uv run python scripts/kiem-thu.py            # tất cả (~1-5 phút)
uv run python scripts/kiem-thu.py cat logo   # hoặc chỉ các ca cần test lại
```
Sau đó Claude:
1. Mở `.cache\kiem-thu\_XEM-MAT.jpg` để xem — chữ tiếng Việt có đủ dấu không, logo/phụ đề có đúng chỗ không. Ghi nhận xét 1–3 dòng.
2. Gửi báo cáo:
   - **Đợt mới:**
     `gh issue create --label kiem-thu-windows --title "Windows <ngày>: X/Y đạt" --body-file .cache\kiem-thu\BAO-CAO.md`
     rồi `gh issue comment <số> --body "<nhận xét ảnh + kết quả CAI-DAT.bat + thử hội thoại (mục C)>"`
   - **Test lại sau khi Mac sửa:** `gh issue comment <số> --body-file .cache\kiem-thu\BAO-CAO.md`
   - Tất cả đạt → `gh issue close <số>`.
3. **Chỉ báo cáo, không tự sửa code.** Có thể ghi đề xuất ("nghi do đường dẫn có dấu trong filter ffmpeg ở video.py:…").

### C. Thử hội thoại (tùy chọn, sau khi script đạt hết)
Bỏ vài file thật vào `01-DAU-VAO`, mở **phiên Claude Code mới** rồi nói như người dùng:
- "chào" → phải hiện menu
- "cắt 10 giây đầu video <tên> rồi đổi sang dọc TikTok"
- "làm phụ đề cho video <tên>"
- "xóa nền ảnh <tên> rồi đổi cỡ cho Shopee"
Ghi lại: có hỏi xin quyền chạy lệnh không (lẽ ra không), có mở thư mục kết quả không, lời lẽ có dễ hiểu không.

---

## B. Bên Mac (Claude Code trên Mac)

```bash
gh issue list --label kiem-thu-windows --state open
gh issue view <số> --comments
```
1. Đọc bảng ❌ + "Chi tiết lỗi". Tái hiện trên Mac nếu được: `uv run python scripts/kiem-thu.py <tên-ca>`.
2. Sửa code → chạy lại script trên Mac (phải vẫn đạt hết) → commit + push.
3. `gh issue comment <số> --body "Đã sửa ở <commit>: <tóm tắt>. Test lại: uv run python scripts/kiem-thu.py <ca>"`
4. Ghi vào "Lịch sử thay đổi" trong HUONG-DAN-QUAN-LY.md nếu là sửa đáng kể.

### D. Công cụ dựng video mới (v1.1) — test bằng hội thoại trong phiên Claude mới
Mỗi câu dưới đây phải chạy từ máy chưa cài gì thêm (để test luôn bước tự cài Node/Manim). Ghi lại: thời gian cài lần đầu, dung lượng, lỗi, và **xem ảnh khung hình** xem dấu tiếng Việt có đúng không.
| Skill | Câu nói thử | Điểm dễ lỗi trên Windows |
|---|---|---|
| `video-dong-html` | "làm video chữ chạy giảm giá 50% chỉ hôm nay, dọc TikTok" | đường dẫn ffprobe-static theo win32/x64; tìm Chrome |
| `video-remotion` | "làm 2 video sản phẩm từ bảng giá mẫu" | tải Chrome Headless Shell (antivirus chặn?); `npx` trong PowerShell |
| `video-giai-thich` | "làm video hoạt hình 3 bước đặt hàng, dọc" | `manimpango.register_font` với font trong đường dẫn có dấu |
| `blender-3d` | (cần cài Blender) "dựng ảnh 3D hộp quà màu đỏ" | `cmd /c uvx` trong `.mcp.json`; add-on "Install from Disk" trên Blender 4.2+ |

### E. Lớp "app" (v1.2): icon, lối tắt, trình mở
Sau khi `CAI-DAT.bat` chạy xong, kiểm tra và ghi lại kèm ảnh chụp màn hình:
- Trên Desktop và trong Start Menu có 3 lối tắt: **TTomorrow Studio**, **TTomorrow Studio - Hộp thư đến**, **TTomorrow Studio - Dự án của tôi**. Icon có đúng không? Tên có dấu có hiển thị đúng không?
- PowerShell chạy ở chế độ nào? Chạy lệnh `$ExecutionContext.SessionState.LanguageMode` trong cửa sổ PowerShell thường. Nếu ra `ConstrainedLanguage` thì đây là máy bị hạn chế, lúc đó lối tắt thư mục sẽ là file `.url`, và **không có** lối tắt TTomorrow Studio.
- Nhấp đúp **TTomorrow Studio**: Claude Desktop có mở không? Có nháy cửa sổ đen không? Lần đầu có mở `HUONG-DAN-NHANH.html` không? Nhấn Ctrl+V xem đường dẫn workspace có nằm sẵn trong clipboard không?
- Máy **chưa cài** Claude Desktop: phải mở trang claude.com/download và trang hướng dẫn.

### F. Dự án + hỏi ý (v1.3) — test bằng hội thoại như người dùng thật
- **Trình mở:** nhấp **TTomorrow Studio** → phải mở **Antigravity IDE đúng thư mục workspace** (máy có Claude Code trong IDE). Ghi nội dung `%TEMP%\ttomorrow-studio.log` (dòng chọn ứng dụng nào, vì sao).
- **3 cách đưa file:**
  1. Bỏ 1 video vào **Hộp thư đến** → nói "làm video TikTok từ video mình vừa bỏ vào" → phải tạo dự án, **file biến khỏi Hộp thư đến và nằm trong `Gốc/`**.
  2. **Kéo thả 1 video vào khung chat** → Claude có nhận được đường dẫn file không? (ghi rõ: thấy đường dẫn / chỉ thấy ảnh / không nhận) → file phải được **chép** vào `Gốc/`, bản gốc vẫn còn chỗ cũ.
  3. Tải 1 ảnh về Downloads rồi nói "lấy ảnh mình vừa tải về" → Claude hiện danh sách đánh số để chọn.
- **Hỏi ý kiểu "grill me":** với yêu cầu sáng tạo, Claude có xem tư liệu trước, đưa 2–3 hướng, hỏi bằng **nút bấm** (AskUserQuestion có hiện trong Antigravity IDE không?), chốt "bản yêu cầu" trước khi làm không? Việc máy móc (nén video) thì phải làm luôn, không hỏi.
- **Thành phẩm:** chỉ bản cuối nằm trong `Thành phẩm/`, tên có dấu "… - bản 1"; yêu cầu chỉnh thêm → "bản 2 (…)"; file nháp không lộ ra. Lối tắt **Dự án của tôi** mở `02-DU-AN`.
- **Làm tiếp ở phiên mới:** mở phiên Claude mới, nói "làm tiếp dự án áo thun" → Claude đọc nhật ký và biết đã làm gì.
- **Dọn dẹp:** nói "dọn dự án cũ" → Claude phải báo cáo trước và **hỏi** trước khi chuyển vào Thùng rác.

### G. OpenMontage (v1.4) — test bằng hội thoại
- Nói "cắt video này thành mấy clip TikTok" với 1 video nói chuyện dài 3–10 phút. Lần đầu Claude phải báo trước rồi tự chạy `studio openmontage cai`. Ghi lại: thời gian cài, dung lượng, có bị Smart App Control / antivirus chặn `ffprobe.exe` / `ffmpeg.exe` trong `05-CONG-CU-THEM\openmontage\_bin` không.
- Claude phải đưa danh sách đoạn đề xuất để **chọn nhiều** bằng nút bấm. Clip ra có khung dọc, mặt người ở giữa, phụ đề đúng dấu.
- Nói "bỏ khoảng lặng video này" → có bản ngắn hơn, không bị hụt chữ đầu câu.
- Nói "làm video giống video mẫu này" với 1 video đã lưu về máy → có phần tóm tắt nhịp/cảnh bằng lời thường + 2–3 hướng làm.

## Script kiểm thử làm gì
`scripts/kiem-thu.py` tự tạo file mẫu trong `.cache\kiem-thu\Mẫu thử có dấu\` (video ngang/dọc, nhạc, ảnh, logo, phụ đề tiếng Việt, giọng nói TTS tiếng Anh), chạy ~46 ca phủ mọi lệnh `studio`, kiểm tra mã thoát + độ dài + khung hình + có/không tiếng, rồi xuất `BAO-CAO.md` (gọn, chỉ in 15 dòng cuối của ca lỗi) và `_XEM-MAT.jpg`. Kết quả nằm trong `.cache\` (không lên git, không làm rối `02-THANH-PHAM`).
