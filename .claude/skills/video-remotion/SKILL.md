---
name: video-remotion
description: Làm video hàng loạt từ bảng dữ liệu (Excel/CSV/danh sách sản phẩm - mỗi dòng ra 1 video), mẫu video thương hiệu dùng lại nhiều lần, video chạy chữ khớp phụ đề, cảnh 3D bằng code (Remotion - React). Dùng khi người dùng nói "làm hàng loạt video sản phẩm", "20 sản phẩm làm 20 video", "video từ bảng giá", "mẫu video thương hiệu dùng lại", "đổi tên/giá là ra video mới", "video có cảnh 3D".
---

# Video hàng loạt & mẫu dùng lại (Remotion)

Remotion = viết video bằng code React, **dữ liệu thay đổi → video mới**. Mình tự cài, tự chạy; người dùng chỉ đưa bảng sản phẩm.

## Chọn đúng công cụ (quan trọng)
| Người dùng muốn | Dùng |
|---|---|
| 1 video đồ họa chuyển động đẹp (intro, quảng cáo, chữ động) | skill `video-dong-html` (HyperFrames, **mặc định**) |
| Video từ vài tấm ảnh có sẵn, nhanh | skill `video-tu-anh` |
| Sửa video đã quay | skill `sua-video` |
| **Nhiều video cùng kiểu, khác dữ liệu** (mỗi sản phẩm/dòng bảng = 1 video) | **skill này** |
| Mẫu thương hiệu dùng lại hằng tuần (đổi chữ/giá/ảnh) | **skill này** |
| Chữ chạy khớp từng câu phụ đề / cảnh 3D (three.js) | **skill này** |
Chỉ làm 1 video đồ họa đơn lẻ → đừng dùng skill này (nặng hơn, lần đầu tải ~150 MB).

## Giấy phép - nói với người dùng MỘT LẦN (lần đầu dùng)
Remotion miễn phí cho **cá nhân, công ty/nhóm tối đa 3 người, tổ chức phi lợi nhuận** (kể cả bán hàng thương mại). Công ty **vì lợi nhuận từ 4 người trở lên** phải mua giấy phép công ty (từ ~25 USD/tháng/người dùng hoặc theo số lượt render - xem remotion.dev/docs/license). Hỏi: "Shop bạn có tối đa 3 người làm không?" Nếu không → nói rõ cần mua giấy phép, **không tự mua/nhập thẻ**; hướng dẫn họ vào trang đó. Nếu họ có khóa (bắt đầu `rm_sec_`) → đặt biến `REMOTION_LICENSE_KEY` khi chạy lô. Ghi lại câu trả lời để không hỏi lại.

## Bước 0 - Kiểm tra & cài (tự làm, không bắt người dùng gõ)
Thư mục làm việc: `05-CONG-CU-THEM/remotion/` (không nằm trong git). Đã sẵn sàng nếu có `05-CONG-CU-THEM/remotion/node_modules` và `public/fonts`.

Nếu chưa có (máy mới), PowerShell tại thư mục gốc workspace:
```powershell
node -v   # cần v18 trở lên; nếu lỗi:
winget install OpenJS.NodeJS.LTS   # xong phải mở lại cửa sổ lệnh/phiên Claude để nhận node
New-Item -ItemType Directory -Force 05-CONG-CU-THEM\remotion | Out-Null
Copy-Item -Recurse -Force .claude\skills\video-remotion\template\* 05-CONG-CU-THEM\remotion\
New-Item -ItemType Directory -Force 05-CONG-CU-THEM\remotion\public\fonts | Out-Null
Copy-Item assets\fonts\*.ttf 05-CONG-CU-THEM\remotion\public\fonts\
cd 05-CONG-CU-THEM\remotion; npm install --no-audit --no-fund
```
(Mac: giống vậy với `cp -R`, `brew install node` nếu thiếu node.)
- Cần mạng: lần cài đầu (~260 MB gói + ~140 MB trình duyệt Chrome Headless Shell, tải tự động ở lần render đầu, tốn 2-6 phút). Sau đó **chạy offline**.
- Báo trước: "Lần đầu mình cần cài thêm công cụ, khoảng 5 phút nhé."
- Remotion có gửi thống kê đếm số lượt render **chỉ khi** có khóa giấy phép; không có khóa thì không gửi gì.

## Quy trình
1. **Mở hoặc tạo dự án**:
   - Nếu làm tiếp: `uv run python -m studio du-an ds` / `du-an xem "<dự án>"`.
   - Nếu việc mới: `uv run python -m studio du-an moi "<Tên dự án>" [file bảng dữ liệu, ảnh...] [--lay-hop-thu]`. File từ `01-DAU-VAO` (Hộp thư đến) được chuyển vào `Gốc/`.
   - Nếu người dùng nói "lấy file vừa tải về": `tim-file-moi`.
2. **Hỏi ý tưởng** (skill `hoi-y-tuong`):
   - Đọc `03-THUONG-HIEU/thuong-hieu.md` → lấy tên shop, màu chính/nền/chữ, giọng văn, CTA.
   - Hỏi bằng lựa chọn bấm được: kiểu mẫu video hiển thị (thẻ sản phẩm, giá sale, kiểu hiện đại), thời lượng mỗi video, các trường thông tin cần đưa vào.
   - Nhắc giấy phép 1 lần nếu là công ty từ 4 người trở lên.
   - Chốt brief và ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "<bản yêu cầu video hàng loạt Remotion>"`.
3. **Chuẩn bị dữ liệu**:
   - Bảng người dùng đưa (Excel / CSV / danh sách) → tạo `.cache/remotion-work/<dự án>/san-pham.json` (hoặc .csv, **UTF-8**). Mỗi dòng: `ten-file` (tên file nháp), `name`, `price`, `oldPrice`, `tagline`, `cta`, `image`. Ảnh lấy từ `Gốc/` của dự án (hoặc đường dẫn ngoài). Có thể dùng `sua-anh` xóa nền ảnh trước nếu cần.
   - Màu/tên shop chung ghi vào `.cache/remotion-work/<dự án>/chung.json`.
4. **Thử 1 video trước trong nháp**:
   - Dựng thử 1 video vào thư mục nháp của dự án `.cache/nhap/<dự án>/`:
     ```powershell
     cd 05-CONG-CU-THEM\remotion
     npx remotion render src/index.ts ProductCard "..\..\.cache\nhap\<dự án>\thu-nghiem.mp4" --props="..\..\.cache\remotion-work\<dự án>\san-pham-1.json"
     ```
   - Tự kiểm tra bằng `uv run python -m studio thong-tin` và `studio khung-hinh --du-an "<dự án>" --kiem-tra` → xem `_TONG-HOP.jpg` (dấu tiếng Việt, giá, bố cục).
   - Cho người dùng duyệt mẫu trước khi chạy cả lô. Báo thời gian: mỗi video ~6 giây mất khoảng 30-60 giây.
5. **Chạy lô vào thư mục nháp của dự án**:
   - Chạy script render batch xuất thẳng vào `.cache/nhap/<dự án>`:
     ```powershell
     cd 05-CONG-CU-THEM\remotion
     node scripts/render-batch.mjs "..\..\.cache\remotion-work\<dự án>\san-pham.json" "..\..\.cache\nhap\<dự án>" "--chung=@..\..\.cache\remotion-work\<dự án>\chung.json"
     ```
   - Đầu ra in danh sách các file video nháp đã tạo.
6. **Chốt bản cuối vào Thành phẩm & mở thư mục**:
   - Duyệt các video nháp hoàn thiện và chốt từng file vào `Thành phẩm/`:
     `uv run python -m studio du-an chot "<dự án>" ".cache/nhap/<dự án>/<ten-file>.mp4" --ten "<tên sản phẩm>"`
   - Ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "Đã hoàn thành và chốt lô N video sản phẩm vào Thành phẩm."`.
   - Mở thư mục `Thành phẩm` cho người dùng: PowerShell `Invoke-Item "02-DU-AN\<dự án>\Thành phẩm"` (Mac: `open`).
7. **Gợi ý bước tiếp / tùy chỉnh**: hỏi bằng lựa chọn bấm được: thêm nhạc nền (`sua-video`), viết caption cho từng video (`viet-content`).

## Tùy biến mẫu
- Mẫu gốc: `.claude/skills/video-remotion/template/` (9:16, 6s, tên + giá + nút CTA). Sửa bản trong `05-CONG-CU-THEM/remotion/src/`; muốn giữ lâu dài cho thương hiệu thì cập nhật cả bản template cho cùng.
- Đổi độ dài/khung: `src/Root.tsx` (`durationInFrames`, `width`, `height`). Thêm trường mới: thêm vào kiểu `ProductCardProps` rồi dùng trong `ProductCard.tsx`; cột mới trong bảng tự thành props.
- Cảnh 3D: `npm install three @react-three/fiber @remotion/three` (đúng cùng phiên bản `remotion`: 4.0.543), dùng `<ThreeCanvas>`; đọc docs remotion.dev/docs/three. Chỉ cài khi người dùng thật sự cần 3D.
- Chữ khớp phụ đề: dùng file `.srt` từ skill `phu-de`, đọc bằng `@remotion/captions` (`parseSrt`).

## Quy tắc viết code Remotion (rút gọn từ Remotion Agent Skills chính thức, github.com/remotion-dev/skills - viết lại theo ý, không chép nguyên văn)
- Mọi chuyển động phải dùng `useCurrentFrame()` + `interpolate()`/`spring()`. **Không dùng CSS transition/animation** hay class animation của Tailwind - render sẽ sai.
- Giây → frame: lấy `fps` từ `useVideoConfig()` (`2 * fps`), đừng gõ cứng số frame.
- Dùng `scale`, `translate`, `rotate` thay vì `transform`; đặt `interpolate()` ngay trong `style`.
- Font: nạp bằng `FontFace` + `delayRender/continueRender` (như mẫu), chỉ Be Vietnam Pro từ `assets/fonts` (đã chép vào `public/fonts`); ảnh/video dùng `<Img>`, `staticFile()`.
- Test render không muốn bị tính phí (công ty có khóa): thêm `--is-production=false`.
- Dùng ảnh/nhạc có bản quyền của người khác để bán hàng thì nhắc người dùng như quy tắc chung.

## Lỗi thường gặp
| Triệu chứng | Cách xử lý |
|---|---|
| `node`/`npm` is not recognized | `winget install OpenJS.NodeJS.LTS`, mở lại phiên rồi thử lại |
| Treo lâu ở "Getting Headless Shell" | Đang tải trình duyệt ~140 MB lần đầu, chờ; mất mạng thì chạy lại khi có mạng |
| Chữ mất dấu / sai font | Thiếu `public/fonts/*.ttf` → chép lại từ `assets/fonts` |
| Ảnh sản phẩm không hiện | Đường dẫn ảnh sai/ có dấu cách không đặt trong ngoặc kép; file phải là jpg/png/webp |
| "Invalid --license-key" | Chỉ nhận khóa `rm_sec_...`; không có khóa thì bỏ tham số này |
| CSV lỗi font tiếng Việt | Lưu lại dạng "CSV UTF-8"; hoặc chuyển sang JSON |
| Chạy chậm/đơ máy | Thêm `--concurrency=2` vào lệnh `npx remotion render`; đóng bớt chương trình |
| "Cannot find module" | Chạy lại `npm install` trong `05-CONG-CU-THEM\remotion` |
| Máy cài chậm do diệt virus chặn | Báo người dùng thêm thư mục workspace vào ngoại lệ Windows Security |

### Lỗi trên Windows (Smart App Control, diệt virus)
- **Lỗi chứng chỉ khi `npm install` hoặc tải Chrome Headless Shell** (`CERTIFICATE_VERIFY_FAILED`, `UNABLE_TO_GET_ISSUER_CERT_LOCALLY`, `UnknownIssuer`): Do trình diệt virus (như Avast) quét HTTPS. Đảm bảo biến môi trường `NODE_USE_SYSTEM_CA=1` (Node ≥ 22.15). Tạm đặt trong PowerShell hiện tại: `$env:NODE_USE_SYSTEM_CA='1'` rồi chạy lại lệnh. Biện pháp cuối: nhờ người dùng tạm dừng "Web Shield / Quét HTTPS" của diệt virus chỉ trong lúc tải.
- **Lỗi 4551 / "Application Control policy" (Smart App Control chặn file chưa ký)**:
  - File có thể bị chặn: file nhị phân `@remotion/compositor-win32-x64-msvc` và `Chrome Headless Shell`.
  - Cách xử lý: Nếu Remotion compositor bị chặn, phía người dùng không thể tự khắc phục trực tiếp → báo cho người quản trị workspace (workspace admin) và chuyển sang dùng skill `video-dong-html` (HyperFrames) để tạo video thay thế.
  - **Tuyệt đối không** bảo người dùng tắt Smart App Control (không thể bật lại nếu không cài lại Windows).
