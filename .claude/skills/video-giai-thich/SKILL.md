---
name: video-giai-thich
description: Làm video hoạt hình giải thích bằng Manim - sơ đồ quy trình, các bước đặt hàng/sử dụng, biểu đồ cột doanh thu chạy số, minh họa ý tưởng, video dạy học/công thức, chữ tiếng Việt chuyển động (dọc 9:16 hoặc ngang 16:9). Dùng khi người dùng nói "làm video giải thích bằng hoạt hình", "video sơ đồ quy trình", "biểu đồ doanh thu chạy", "minh họa các bước", "video dạy toán/công thức", "infographic động".
---

# Video giải thích bằng hoạt hình (Manim)

Mình tự viết "kịch bản chuyển động" bằng mã rồi xuất ra MP4 — **không có tiếng**, chạy hoàn toàn trên máy, không cần mạng sau lần cài đầu. Người dùng chỉ cần nói nội dung muốn giải thích.

## Chọn đúng công cụ
| Người dùng muốn | Dùng |
|---|---|
| Video quay thật (cắt, ghép, chèn nhạc/chữ) | skill `sua-video` |
| Video quảng cáo chữ/ảnh chuyển động kiểu motion graphics, banner động | skill `video-dong-html` |
| Video từ nhiều ảnh (slideshow) | skill `video-tu-anh` |
| **Giải thích bằng sơ đồ, các bước, biểu đồ chạy, số liệu, công thức, ý tưởng** | **skill này** |

## Lần đầu: kiểm tra & cài (mình tự làm, người dùng không phải gõ)
Công cụ nằm ngoài môi trường chính của workspace (không đụng `pyproject.toml`), chạy qua `uv` với phiên bản cố định **manim 0.22.1** (giấy phép MIT, không gửi dữ liệu nào ra ngoài).

Kiểm tra (PowerShell, tại thư mục gốc workspace):
```
uv run --no-project --python 3.12 --with manim==0.22.1 manim --version
```
- In ra `Manim Community v0.22.1` là xong. **Lần đầu mất 1–3 phút** vì tải ~150–250 MB thư viện (báo trước: "mình cài công cụ hoạt hình, khoảng 2 phút nhé"). Các lần sau chạy ngay.
- Windows có sẵn bản cài đặt sẵn cho mọi thư viện cần thiết (pycairo, manimpango, PyAV), **không cần cài ffmpeg riêng, không cần Visual Studio**.
- **Lưu ý Windows**: Các biến môi trường `UV_SYSTEM_CERTS=1`, `UV_PYTHON_DOWNLOADS=never`, `UV_NO_MANAGED_PYTHON=1` giúp `uv` dùng Python 3.12 chính thức đã ký từ python.org. Kiểm tra: `uv python find 3.12` phải in ra đường dẫn dưới `AppData\Local\Programs\Python\Python312`.
- Nếu `uv` không chạy → làm theo skill `cai-dat`.
- **Máy Mac (người quản lý thử nghiệm)**: cần cài một lần `brew install pkg-config cairo pango`.
- **Công thức toán dạng LaTeX (MathTex/Tex) cần cài MiKTeX — KHÔNG bắt buộc**, mặc định không dùng. Công thức đơn giản viết bằng chữ thường: `chu("S = π × r²")`, `chu("(a + b)² = a² + 2ab + b²")` (dùng ký tự ², ³, ×, ÷, √, π, ≈, ≠, ≤, ≥, →). Chỉ khi cần phân số/căn/tích phân đẹp mới hỏi người dùng cài MiKTeX (miễn phí, ~300 MB); lúc đó mới được dùng `MathTex`.

## Bộ dựng sẵn: `nen_tang.py`
Nằm cạnh file này. Đã lo sẵn: font Be Vietnam Pro (dấu tiếng Việt chuẩn), khung 9:16 (1080×1920) / 16:9 (1920×1080) 30fps, màu lấy từ `03-THUONG-HIEU/thuong-hieu.md` (không có thì dùng màu mặc định, dict `MAU`: chinh, phu, nhan, nen, chu).

| Hàm | Làm gì |
|---|---|
| `dung_khung("9:16" hoặc "16:9")` | Đặt khung hình — gọi ngay sau import, trước khi tạo `Scene` |
| `chu("Nội dung", co=44, mau=None, dam=False, rong_toi_da=None)` | Chữ tiếng Việt (luôn dùng hàm này thay `Text` trần). `rong_toi_da` = số ký tự mỗi dòng |
| `the_tieu_de(tieu_de, phu_de)` | Thẻ tiêu đề + vạch nhấn. Dùng `self.play(FadeIn(...))` |
| `danh_sach_buoc(self, [..], tieu_de)` | Các bước hiện lần lượt với số tròn |
| `so_do_luong(self, [..], tieu_de)` | Ô → mũi tên → ô (dọc: trên xuống, ngang: trái sang phải) |
| `bieu_do_cot(self, nhan, gia_tri, tieu_de, don_vi)` | Cột mọc dần kèm số liệu |
| `chay(LopCanh, "9:16", "ten-video")` | Xuất video (xem bên dưới) |

Mọi thứ khác của Manim dùng bình thường (`Circle`, `Arrow`, `Transform`, `Write`, `FadeIn`, `VGroup`...). Cỡ chữ theo thang 16:9: tiêu đề ~56–64, nội dung ~36–44, nhãn nhỏ ≥ 30 (xem trên điện thoại phải đọc được). Bố cục khung dọc hẹp: mỗi dòng chữ ≤ ~14 ký tự.

Hai ví dụ chạy được ngay: `vi-du/3-buoc-dat-hang.py` (dọc, sơ đồ 3 bước) và `vi-du/doanh-thu-4-thang.py` (ngang, biểu đồ cột). Copy và sửa chữ/số là ra video mới.

## Quy trình làm việc
1. **Hỏi tối đa 1–2 câu** nếu thiếu: nội dung/số liệu, và "TikTok (dọc) hay YouTube (ngang)?". Đủ thì làm luôn. Không dùng số liệu bịa cho việc thật — hỏi số thật.
2. **Viết cảnh** vào `.cache/video-giai-thich/<ten-ngan>.py` (thư mục tạm của mình, tạo nếu chưa có), mẫu:
   ```python
   import sys
   sys.path.insert(0, r"<đường dẫn tuyệt đối tới .claude/skills/video-giai-thich>")
   from nen_tang import *
   dung_khung("9:16")
   class Canh(Scene):
       def construct(self):
           ...
   if __name__ == "__main__":
       chay(Canh, "9:16", "ten-video")
   ```
   Ngắn gọn: video TikTok 15–30 giây, mỗi ý 2–4 giây, chữ ít. Dùng `self.wait(1)` cuối mỗi ý cho người xem kịp đọc.
3. **Xem thử nhanh trước** (nửa độ phân giải, vài giây):
   ```
   uv run --no-project --python 3.12 --with manim==0.22.1 python -W ignore ".cache\video-giai-thich\ten-ngan.py" --xem-truoc
   ```
   Lấy dòng `KET QUA:` rồi `uv run python -m studio khung-hinh <file> --kiem-tra`, **xem ảnh `_TONG-HOP.jpg`**: chữ có tràn khung/chồng nhau không, dấu tiếng Việt đúng chưa, mốc giờ có hợp lý không. Sửa đến khi ổn.
4. **Xuất bản chính thức** (đủ nét, 30fps) và chép thẳng vào thư mục kết quả của ngày (không bao giờ ghi đè — nếu trùng tên tự thêm `_2`, `_3`):
   ```
   uv run --no-project --python 3.12 --with manim==0.22.1 python -W ignore ".cache\video-giai-thich\ten-ngan.py" --ra "02-THANH-PHAM\<YYYY-MM-DD hôm nay>"
   ```
   Thường 5–60 giây tùy độ dài (báo trước nếu video dài hơn 1 phút).
5. **Kiểm tra** bằng `studio thong-tin <file>` (đúng khung 1080×1920 hoặc 1920×1080, đúng độ dài) và xem lại `khung-hinh --kiem-tra` bản chính thức.
6. **Báo kết quả**: nói tên file + nằm ở `02-THANH-PHAM` → ngày hôm nay, rồi mở thư mục (Windows: `Invoke-Item "02-THANH-PHAM\<ngày>"`; Mac: `open`). Gợi ý 1 bước tiếp theo (thêm giọng đọc/nhạc, hoặc phụ đề).

## Thêm giọng đọc, nhạc, phụ đề sau khi xong
Video Manim không có tiếng. Muốn có tiếng:
- Nhạc nền: `uv run python -m studio nhac <video> <nhac.mp3>` (nhạc mẫu trong `assets/nhac-mau/`; nhắc bản quyền nếu là nhạc nổi tiếng).
- Giọng đọc: viết lời đọc bằng skill `viet-content` (khớp từng cảnh); người dùng tự thu âm hoặc tạo giọng AI (CapCut/Vbee) rồi bỏ file vào `01-DAU-VAO`. Ghép: `studio nhac <video> <giong-doc.mp3> --am-luong 1 --khong-giam-nhac`.
- Đồng bộ: nếu đã có giọng đọc, đo độ dài từng câu rồi chỉnh `self.wait(...)` cho khớp trước khi xuất bản chính thức.
- Phụ đề cứng: skill `phu-de` sau khi đã có giọng đọc.

## Lỗi thường gặp
| Dấu hiệu | Cách xử lý (mình tự làm) |
|---|---|
| `uv is not recognized` | Skill `cai-dat` |
| Lần đầu chạy rất lâu / báo đang tải | Bình thường (tải thư viện một lần). Đợi, đừng ngắt |
| Máy Mac: lỗi `pycairo`/`pkg-config` | `brew install pkg-config cairo pango` rồi chạy lại |
| Chữ mất dấu / xấu | Dùng `chu(...)`, không dùng `Text(...)` trần; kiểm tra `assets/fonts/BeVietnamPro-*.ttf` còn đủ |
| Chữ tràn khung / chồng nhau | Giảm `co`, thêm `rong_toi_da`, chia thành 2 cảnh; khung dọc ≤ ~14 ký tự/dòng |
| `latex ... not found` / `MathTex` lỗi | Không dùng `MathTex/Tex`; viết công thức bằng `chu("...")` hoặc nhờ người dùng cài MiKTeX |
| `ModuleNotFoundError: nen_tang` | Dòng `sys.path.insert` sai đường dẫn tới thư mục skill |
| File `.mp4` đang mở/khóa | Nhờ người dùng đóng trình phát video rồi chạy lại (kết quả tự đổi tên, không ghi đè) |
| Dòng lệnh quá chậm | Dùng `--xem-truoc`; giảm số `self.play` / thời lượng `wait` |

### Lỗi trên Windows (Smart App Control, diệt virus)
- **Lỗi chứng chỉ khi tải thư viện (`uv run --with ...`)** (`CERTIFICATE_VERIFY_FAILED`, `UnknownIssuer`): Do trình diệt virus (như Avast) quét HTTPS. Đảm bảo biến `UV_SYSTEM_CERTS=1` đã được thiết lập. Tạm đặt trong PowerShell hiện tại: `$env:UV_SYSTEM_CERTS='1'` rồi thử lại. Biện pháp cuối: nhờ người dùng tạm dừng "Web Shield / Quét HTTPS" của diệt virus chỉ trong lúc tải.
- **Lỗi 4551 / "Application Control policy has blocked this file"**:
  - Do Smart App Control chặn bản Python chưa ký số do uv tự tải về.
  - Cách xử lý: Cài bản Python 3.12 chính thức từ python.org (đã có chữ ký số) và đảm bảo các biến `UV_NO_MANAGED_PYTHON=1`, `UV_PYTHON_DOWNLOADS=never`. Kiểm tra:
    ```powershell
    uv python find 3.12
    ```
    Kết quả phải in ra đường dẫn dưới `AppData\Local\Programs\Python\Python312`.
  - **Tuyệt đối không** khuyên người dùng tắt Smart App Control (không thể bật lại nếu không cài lại Windows).

## Lưu ý
- Chữ chỉ dùng font Be Vietnam Pro (hàm `chu` lo sẵn). Không đưa dữ liệu Đỏ (SĐT, số tài khoản khách) lên video công khai.
- Số liệu kinh doanh nội bộ (loại Vàng) → nhắc người dùng cân nhắc trước khi đăng.
- Ý tưởng hay: "3 bước đặt hàng", "quy trình đổi trả", "doanh thu tháng chạy cột", "so sánh trước–sau", "mẹo 5 bước", "giải thích công thức tính giá/lãi".
