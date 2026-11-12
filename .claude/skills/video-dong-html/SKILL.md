---
name: video-dong-html
description: Tạo video chuyển động đồ họa từ con số 0 bằng code HTML + GSAP + three.js (HyperFrames) - video chữ chạy, intro/outro logo, video khuyến mãi/quảng cáo động, hiệu ứng 3D xoay sản phẩm, đếm số, bảng giá động. Dùng khi người dùng nói "làm video chữ chạy", "làm intro logo", "video động quảng cáo khuyến mãi", "video giảm giá 10 giây", "hiệu ứng 3D xoay sản phẩm", "motion graphics", "video không cần quay".
---

# Video động dựng từ HTML (HyperFrames)

Mình viết một trang HTML có chuyển động (GSAP, three.js cho 3D) rồi HyperFrames quay màn hình từng khung và đóng thành MP4. Chạy **offline** trên máy, không gửi gì lên mạng.

## Dùng skill nào?
| Người dùng muốn | Skill |
|---|---|
| Sửa/cắt video **quay thật** | `sua-video` |
| Video từ **nhiều ảnh** (slideshow, zoom ảnh) | `video-tu-anh` |
| Phụ đề cho video | `phu-de` |
| Video **tạo từ đầu**: chữ chạy, intro logo, quảng cáo khuyến mãi, 3D, số đếm | **skill này** |
| AI sinh cảnh quay điện ảnh | `prompt-video-ai` |

## 1. Kiểm tra / cài đặt (chỉ lần đầu)
Kiểm tra: thư mục `05-CONG-CU-THEM/hyperframes/node_modules` có chưa. Có rồi → sang mục 2.

Chưa có → báo người dùng "mình cài công cụ làm video động, khoảng 3–5 phút, cần mạng một lần" rồi tự chạy (PowerShell, tại thư mục gốc workspace):
```powershell
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements }
# Sau khi cài Node lần đầu cần mở cửa sổ PowerShell MỚI (hoặc nạp lại PATH) rồi chạy tiếp:
New-Item -ItemType Directory -Force 05-CONG-CU-THEM\hyperframes | Out-Null
Set-Location 05-CONG-CU-THEM\hyperframes
npm init -y
npm install hyperframes@0.9.39 gsap@3.15.1 three@0.160.0 ffmpeg-static@5.3.0 ffprobe-static@3.1.0
npx hyperframes telemetry disable
```
- Cần Node.js **22 trở lên** (`node -v`). `winget` có sẵn trên Windows 10/11; nếu không có → nhờ người dùng cài Node.js LTS từ nodejs.org (bấm Next hết).
- `ffmpeg-static`/`ffprobe-static` là bản ffmpeg nằm gọn trong thư mục này, không cài vào hệ thống.
- Trình duyệt dựng hình: dùng Chrome/Edge có sẵn; nếu máy không có, lần render đầu HyperFrames tự tải Chromium (~150 MB, cần mạng).
- Dung lượng ~530 MB. Từ sau đó **không cần mạng**.
- Mac (người quản lý): cùng lệnh, thay bước winget bằng `brew install node`.
- Phiên bản đã ghim (0.9.39 / gsap 3.15.1 / three 0.160.0). `three@0.160.0` cố ý: bản mới hơn không còn file `three.min.js` dạng script thường.

## 2. Quy trình làm việc
1. Đọc `03-THUONG-HIEU/thuong-hieu.md` (màu, logo, tên shop, giọng văn). Còn trống → dùng màu mặc định của mẫu.
2. Hỏi tối đa 1–2 câu nếu thiếu: nội dung chữ, khung (dọc 9:16 / ngang 16:9), có logo/ảnh sản phẩm không. Đủ thì làm luôn. Chữ ngắn gọn, giọng thương hiệu.
3. Tạo thư mục làm việc từ mẫu (tự chép gsap, three.js, font Be Vietnam Pro vào):
   `node .claude/skills/video-dong-html/video-dong-html.mjs tao <ten-ngan>` → in `KET QUA: <thư mục dự án>` (nằm trong `.cache/hyperframes-work/`).
4. Chép logo / ảnh sản phẩm của người dùng vào thư mục `assets/` của dự án (chép, không di chuyển file gốc). Sửa **khối `CFG`** đầu phần `<script>` trong `index.html` (chữ, đường dẫn logo/ảnh, màu hộp 3D) và màu ở khối `:root`. Muốn đổi cảnh/nhịp → sửa timeline GSAP (xem mục 4).
5. Xem thử nhanh 1 vài khung trước khi dựng thật: `node .claude/skills/video-dong-html/video-dong-html.mjs xuat <thư mục dự án> <ten-file> --nhanh` (bản nháp), hài lòng mới bỏ `--nhanh`.
   Lệnh `xuat` tự kiểm tra bố cục → dựng → lưu `02-THANH-PHAM/<hôm nay>/<ten-file>.mp4`, trùng tên thì tự thêm `_2`, `_3`. Mẫu 8 giây mất khoảng 30–60 giây → báo trước "khoảng 1 phút nhé".
6. Kiểm tra: `uv run python -m studio thong-tin <mp4>` (đúng độ dài, khung) rồi `uv run python -m studio khung-hinh <mp4> --kiem-tra` và **xem ảnh `_TONG-HOP.jpg`**: dấu tiếng Việt đúng, chữ không tràn/bị che, 3D có hiện. Sai → sửa `index.html`, dựng lại (đặt tên mới).
7. Báo kết quả ở đâu, mở thư mục (`explorer`/`Invoke-Item`), gợi ý bước tiếp: thêm nhạc (`sua-video`: `nhac`), thêm logo, hoặc làm bản 16:9/vuông.

## 3. Mẫu có sẵn (`templates/`)
- `khuyen-mai-doc/`: 9:16 1080x1920, 8 giây, 30fps. Chữ chạy từng ký tự, số to "50%", hộp 3D xoay (three.js), dòng "Chỉ hôm nay!", nút "MUA NGAY". Tham số: `tenShop`, `logo`, `dongTren`, `soTo`, `dongDuoi`, `dongPhu`, `nut`, `anhSanPham` (dán lên hộp 3D), `mauHop`, `hien3D`.
- Khung ngang 16:9 hoặc vuông: sửa 4 chỗ cho khớp: `data-resolution`, `<meta viewport>`, `html/body/#root` width-height trong CSS, và `data-width/data-height` ở `#root` (1920x1080 hoặc 1080x1080), rồi canh lại vị trí `top` các khối.
- Đổi độ dài: sửa `data-duration` ở `#root` và vị trí thời gian trong timeline (số cuối mỗi dòng `tl.…`). Tối đa nên ≤ 30 giây (render càng dài càng lâu).
- Làm mẫu mới (intro logo, chữ chạy, đếm số): copy `khuyen-mai-doc` sang `templates/<ten-moi>/` rồi sửa. Giữ nguyên các quy tắc ở mục 4.

## 4. Quy tắc viết HTML để dựng đúng (rất quan trọng)
- Mọi chuyển động nằm trên **một timeline GSAP `paused: true`**, đăng ký `window.__timelines["main"] = tl` (khóa trùng `data-composition-id`). HyperFrames tua từng khung hình → **không dùng** `setTimeout`, `requestAnimationFrame`, `Math.random()`, CSS animation, `Date.now()`, video/GIF tự chạy.
- Phần tử xuất hiện đúng lúc: dùng `tl.fromTo(sel, {…}, {…}, <giây bắt đầu>)`. Vị trí tuyệt đối tính bằng giây (đối số thứ 3).
- Chữ: chỉ dùng `font-family: "BeVN"` (đã `@font-face` từ `./fonts/` = Be Vietnam Pro). Font khác dễ lỗi dấu. Font riêng của shop trong `03-THUONG-HIEU/` thì chép vào `fonts/` và thêm `@font-face`.
- **three.js**: scene tạo bình thường, nhưng **chỉ vẽ trong `onUpdate` của tween GSAP** (mẫu: đối tượng `spin` chạy 0→8 giây, hàm `draw()` đọc `spin.t` để xoay). Không dùng `clock`/`requestAnimationFrame`. Giữ `preserveDrawingBuffer: true`, `setPixelRatio(1)`. Ảnh làm texture phải ở trong thư mục dự án (đường dẫn tương đối).
- Màu chữ phải đọc được trên nền (lệnh kiểm tra sẽ cảnh báo tương phản). Chữ trong vùng an toàn: cách mép trên/dưới ~150px với video TikTok (nút giao diện che).
- Hiệu ứng hay dùng: `back.out(2)` (nảy), `power3.out` (trượt mượt), `stagger` (chữ chạy lần lượt), `yoyo + repeat` (nhấp nháy/nhịp), `scale` + `opacity` (hiện dần). Mỗi cảnh 2–3 giây, 3 giây đầu phải có chữ chính (hook).
- Cảnh báo `panel_out_of_canvas` (khối mờ tràn mép) là chủ ý, bỏ qua được. Lỗi (error) thì phải sửa.
- Tra cứu thêm bằng máy: `node 05-CONG-CU-THEM/hyperframes/node_modules/hyperframes/bin/hyperframes.mjs docs gsap` (topics: gsap, data-attributes, compositions, rendering, troubleshooting).
- Bộ skill chính hãng của HyperFrames (~450 khối dựng sẵn như chuyển cảnh, biểu đồ, bản đồ) cài bằng `npx hyperframes skills update` (cần mạng; người quản lý quyết định có cài hay không, mặc định không).

## 5. Lỗi thường gặp
| Hiện tượng | Cách xử lý (mình tự làm) |
|---|---|
| `node` không nhận / phiên bản < 22 | Cài lại Node LTS bằng winget (mục 1), mở cửa sổ mới |
| Báo thiếu ffmpeg/ffprobe | Chạy lại `npm install` trong `05-CONG-CU-THEM/hyperframes` (dùng `video-dong-html.mjs` thì PATH tự thêm) |
| Lần dựng đầu rất lâu / tải trình duyệt | Bình thường nếu máy chưa có Chrome; chờ, cần mạng |
| Video đen / 3D không hiện | Kiểm tra đã gọi `draw()` trong `onUpdate`; thử `--no-browser-gpu` ở lệnh render (máy yếu không có WebGL) |
| Chữ vuông ô / sai dấu | Chưa dùng `font-family: "BeVN"` hoặc thiếu thư mục `fonts/` |
| Chữ tràn khung | Giảm `font-size`, ngắt dòng, kiểm tra lại bằng `khung-hinh` |
| Hết bộ nhớ (RAM < 4 GB trống) | Tắt bớt phần mềm; thêm `-w 1` vào lệnh render |
| Muốn chạy tay | `cd <dự án>` rồi `node ..\..\..\05-CONG-CU-THEM\hyperframes\node_modules\hyperframes\bin\hyperframes.mjs render -o <đường dẫn.mp4>` (đặt PATH có ffmpeg-static trước) |

### Lỗi trên Windows (Smart App Control, diệt virus)
- **Lỗi chứng chỉ khi `npm install` hoặc tải Chromium** (`CERTIFICATE_VERIFY_FAILED`, `UNABLE_TO_GET_ISSUER_CERT_LOCALLY`, `UnknownIssuer`): Do trình diệt virus (như Avast) quét HTTPS. Đảm bảo biến môi trường `NODE_USE_SYSTEM_CA=1` (Node ≥ 22.15). Tạm đặt trong PowerShell hiện tại: `$env:NODE_USE_SYSTEM_CA='1'` rồi thử lại. Biện pháp cuối: nhờ người dùng tạm dừng "Web Shield / Quét HTTPS" của diệt virus chỉ trong lúc tải.
- **Lỗi 4551 / "Application Control policy" (Smart App Control chặn file chưa ký)**:
  - File có thể bị chặn: `ffmpeg-static` và `ffprobe-static` trong `05-CONG-CU-THEM/hyperframes/node_modules/`.
  - Cách xử lý: Script `video-dong-html.mjs` tự động tìm ffmpeg theo thứ tự: biến môi trường → PATH hệ thống → ffmpeg có sẵn của gói `imageio-ffmpeg` trong workspace (đã ký, không bị chặn) → mới đến `ffmpeg-static`. Nếu `ffprobe-static` bị chặn, cài ffmpeg/ffprobe chuẩn có chữ ký vào hệ thống:
    ```powershell
    winget install --id Gyan.FFmpeg.Essentials -e --source winget
    ```
    Lệnh này đưa cả `ffmpeg` và `ffprobe` lên PATH, script sẽ tự nhận diện.
  - **Tuyệt đối không** khuyên người dùng tắt Smart App Control (tắt là vĩnh viễn, không bật lại được nếu không cài lại Windows).

Telemetry: HyperFrames mặc định có thể gửi thống kê ẩn danh; script đã tắt (`HYPERFRAMES_NO_TELEMETRY=1`). Dựng hình chạy hoàn toàn trên máy, không gửi file lên web.

## 6. Giấy phép (nhắc khi cần)
- HyperFrames (HeyGen): Apache-2.0, dùng thương mại được, giữ thông báo bản quyền khi phân phối lại mã.
- GSAP: giấy phép GSAP Standard "no charge" của GSAP/Webflow, miễn phí kể cả thương mại; chỉ cấm dùng để dựng sản phẩm cạnh tranh với chính công cụ no-code/animation của GSAP/Webflow. Video do người dùng làm ra không bị ràng buộc.
- three.js: MIT. Be Vietnam Pro: OFL (`assets/fonts/OFL.txt`).
- Video làm xong thuộc về người dùng. Không dùng ảnh/nhạc/logo của người khác khi chưa được phép.
