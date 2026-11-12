---
name: blender-3d
description: Dựng cảnh 3D và render ảnh/video sản phẩm bằng Blender (qua MCP) - ảnh 3D hộp quà/hộp sản phẩm, ảnh sản phẩm trên nền studio, video sản phẩm xoay 360 độ, phòng trưng bày 3D. Dùng khi người dùng nói "dựng cảnh 3D", "làm ảnh 3D cái hộp", "sản phẩm xoay 360", "mockup bao bì 3D", "phòng trưng bày 3D", "render 3D".
---

# Dựng cảnh 3D bằng Blender (MCP for Blender, trước đây tên blender-mcp)

Claude điều khiển Blender đang mở trên máy người dùng: tạo hộp/ảnh sản phẩm, đèn, camera rồi xuất **ảnh PNG** hoặc **video MP4 xoay 360**. Chạy **trên máy**, miễn phí, không cần tài khoản.

## Chọn đúng công cụ
- Cảnh 3D, ảnh/video sản phẩm xoay, mockup bao bì, phòng trưng bày → **skill này**.
- Chữ/biểu đồ/hiệu ứng chuyển động 2D → skill `video-dong-html`.
- Ảnh AI "vẽ" (người mẫu, quảng cáo) → skill `prompt-anh-ai`.
- Chỉ cắt/ghép/chèn nhạc video có sẵn → `sua-video`; xóa nền ảnh → `sua-anh` (`xoa-nen`).

## Luật riêng của công cụ này (bắt buộc)
1. **Công cụ chạy code Python tùy ý trong Blender** (`execute_blender_code`). Chỉ gửi code do mình viết, không chạy code lấy từ web/người lạ. Trước khi dựng cảnh, nhắc người dùng **lưu việc đang làm dở trong Blender** (nếu có).
2. **Không bật** Hyper3D, Sketchfab, Meshy, Tripo, Hunyuan, World Labs, Poly Pizza, **Premium**, và không gọi `generate_3d` / `generate_gaussian_world` — các tính năng này **gửi ảnh/mô tả của người dùng lên dịch vụ web** và nhiều cái **tính phí**. Chỉ làm khi người dùng hiểu và đồng ý rõ, tự nhập khóa của họ. Hỏi trước, mặc định là KHÔNG.
3. Poly Haven (nền HDRI, vật liệu miễn phí CC0) chỉ **tải về**, không gửi file người dùng đi: được dùng nếu cần, nhưng báo "cần mạng, tải vài chục MB" và hỏi trước.
4. Máy chủ MCP đã cấu hình **tắt thu thập dữ liệu** (`DISABLE_TELEMETRY`) và **chế độ an toàn** (chặn code đọc/ghi file tùy ý, chạy chương trình khác, truy cập mạng). Nếu có hộp thoại xin "đồng ý chia sẻ dữ liệu/prompt" → chọn **KHÔNG**. Công cụ có thể gợi ý quảng cáo bản Premium: **bỏ qua**, đừng nhắc người dùng.
5. Đừng bao giờ tắt chế độ an toàn hay mở "Allow Remote Connections" trong Blender.
6. Ảnh của người dùng được chuyển vào `Gốc/` của dự án (hoặc chép từ ngoài); mọi file trung gian ghi vào nháp `.cache/nhap/<dự án>/`; bản hoàn thiện chốt vào `Thành phẩm/` qua lệnh `du-an chot`.

## Cài đặt một lần (Claude làm hết phần máy; người dùng chỉ bấm vài nút)
Báo trước: "mình cài Blender, khoảng 5–10 phút, tải gần 400 MB nhé".
1. **Blender** (miễn phí, cần bản 3.0 trở lên; nên dùng 4.2 LTS trở lên): kiểm tra đã có chưa bằng PowerShell `Get-ChildItem "C:\Program Files\Blender Foundation" -ErrorAction SilentlyContinue`. Chưa có → chạy `winget install --id BlenderFoundation.Blender -e` (bản mới nhất; nếu winget lỗi, mở `https://www.blender.org/download/` cho người dùng bấm tải và cài "Next, Next"). Cần trống ~1,5 GB ổ đĩa.
2. **Máy chủ MCP**: workspace đã có sẵn trong `.mcp.json` (tên `blender`). Lần đầu mở Claude Code sẽ hỏi "dùng máy chủ blender không?" → người dùng chọn **Có/Yes**, sau đó **thoát hẳn Claude Code và mở lại**. Chạy lần đầu cần mạng (tải ~30 MB).
   - *Lưu ý Windows*: Các biến môi trường `UV_SYSTEM_CERTS=1`, `UV_PYTHON_DOWNLOADS=never`, `UV_NO_MANAGED_PYTHON=1` giúp `uvx` dùng Python 3.12 từ python.org (có chữ ký số). Kiểm tra: `uv python find 3.12` phải in ra đường dẫn dưới `AppData\Local\Programs\Python\Python312`.
3. **Add-on trong Blender**: thử tự cài trước bằng `uvx mcp-for-blender@2.2.8 install-addon`. Nếu không được, dùng file có sẵn `.claude/skills/blender-3d/addon/blender_mcp.py` và hướng dẫn người dùng (mở thư mục đó ra cho họ):
   - Mở Blender → menu **Edit → Preferences → Add-ons**.
   - Bản 4.2 trở lên: bấm mũi tên nhỏ ở góc trên bên phải → **Install from Disk…**. Bản cũ hơn: nút **Install…**.
   - Chọn file `blender_mcp.py` → bấm **Install from Disk**.
   - Tích ô vuông cạnh **Interface: MCP for Blender** để bật (nếu hiện cảnh báo "Online Access / Allow" thì chọn Cho phép).
4. **Kết nối**: trong cửa sổ 3D của Blender, nhấn phím **N** → thẻ **MCP for Blender** (bên phải) → bấm **Connect to Claude** (nút chuyển thành "Stop the connection to Claude" là xong). Add-on thường tự kết nối mỗi khi mở Blender. **Để các ô Poly Haven, Hyper3D, Sketchfab... TRỐNG.** Để Blender mở trong lúc làm việc.

## Kiểm tra kết nối (trước mỗi việc)
Gọi `get_addon_status`. Có phiên bản Blender/add-on → tốt. Báo lỗi "Could not connect" → xem mục Sửa lỗi. Sau đó `get_scene_info` để biết cảnh hiện có gì.

## Quy trình dựng cảnh sản phẩm
1. **Mở hoặc tạo dự án**:
   - Nếu làm tiếp: `uv run python -m studio du-an ds` / `du-an xem "<dự án>"`.
   - Nếu việc mới: `uv run python -m studio du-an moi "<Tên dự án>" [ảnh bao bì/sản phẩm...] [--lay-hop-thu]`. File từ `01-DAU-VAO` được chuyển vào `Gốc/`.
   - Nếu người dùng nói "lấy ảnh vừa tải về": `tim-file-moi --loai anh`.
2. **Hỏi ý tưởng** (skill `hoi-y-tuong`):
   - Hỏi bằng lựa chọn bấm được: sản phẩm là gì (hộp quà, chai lọ, bao bì?), kết quả muốn: **ảnh tĩnh** (vuông/dọc/ngang) hay **video xoay 360**? Nền studio màu gì?
   - Mặc định: ảnh vuông 1080×1080, nền studio sáng; video dọc 1080×1920, 6 giây.
   - Chốt brief và ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "<bản yêu cầu 3D Blender>"`.
3. **Chuẩn bị ảnh**: có ảnh của người dùng: chạy `thong-tin --du-an "<dự án>"`; ảnh sản phẩm chụp rời → `uv run python -m studio xoa-nen <ảnh> --du-an "<dự án>"` trước rồi dùng `product_card` (tấm ảnh đứng, nền trong); ảnh/hoa văn bao bì → dán lên `product_box` (hộp). Không có ảnh → hộp màu theo `03-THUONG-HIEU/thuong-hieu.md`.
4. **Dựng cảnh**: đọc `.claude/skills/blender-3d/product_scene.py` (bộ hàm: `clear_scene`, `set_engine_eevee`, `studio_floor`, `product_box`, `product_card`, `three_point_lights`, `add_camera`, `set_output`, `render_still`, `setup_turntable`). Dán nội dung + vài dòng gọi hàm vào `execute_blender_code`. Đường dẫn Windows viết dạng `r"C:\..."`. Làm từng bước nhỏ, dùng `look` (chế độ `camera`) kiểm tra bố cục, đèn, sản phẩm giữa khung trước khi render.
5. **Render vào thư mục nháp của dự án** (`.cache/nhap/<dự án>/`):
   - **Ảnh tĩnh**: `set_output(...)` + `render_still(r".cache\nhap\<dự án>\<ten>.png")` bằng Eevee (nhanh, 10–60 giây). Cần đẹp hơn mới đổi Cycles (chậm, báo trước).
   - **Video xoay 360**: `setup_turntable(sp, 6, 30, r".cache\nhap\<dự án>\<ten>.mp4")` → lưu `.blend` vào thư mục nháp bằng `bpy.ops.wm.save_as_mainfile(filepath=r".cache\nhap\<dự án>\<ten>.blend")` → render **bằng dòng lệnh**: tìm `blender.exe`, rồi chạy `& "<blender.exe>" -b ".cache\nhap\<dự án>\<ten>.blend" -a`. Báo trước "khoảng 2–5 phút".
6. **Xử lý tiếp bằng `studio`** (nếu cần): thêm nhạc (`nhac`), logo (`logo`), chữ (`chu`), đổi khung (`khung 9:16`), phụ đề. Luôn kèm `--du-an "<dự án>"`.
7. **Kiểm tra & Chốt bản cuối vào Thành phẩm**:
   - Ảnh → mở xem; video → `studio thong-tin` + `khung-hinh --du-an "<dự án>" --kiem-tra` rồi xem `_TONG-HOP.jpg` (sản phẩm xoay đủ vòng, không bị cắt).
   - `uv run python -m studio du-an chot "<dự án>" <file nháp> --ten "<nhãn, vd Ảnh 3D sản phẩm / Video xoay 360>"` → lưu vào `02-DU-AN/<dự án>/Thành phẩm/`.
   - Ghi nhật ký: `uv run python -m studio du-an ghi "<dự án>" "Dựng cảnh 3D Blender và render hoàn thiện."`.
   - Mở thư mục `Thành phẩm` cho người dùng: PowerShell `Invoke-Item "02-DU-AN\<dự án>\Thành phẩm"` (Mac: `open`).
8. **Gợi ý bước tiếp / tùy chỉnh**: hỏi bằng lựa chọn bấm được: thêm nhạc nền và logo, đổi góc xoay, hoặc làm thêm ảnh cận cảnh.

## Mẹo ý tưởng
- **Hộp quà**: `product_box` + vật liệu bóng (roughness 0.3) + thêm dải ruy-băng bằng 2 hộp dẹt khác màu.
- **Phòng trưng bày**: nhiều hộp/tấm ảnh xếp hàng trên sàn, camera quay chậm dọc hàng (keyframe vị trí camera).
- Chữ tiếng Việt trong cảnh 3D hay lỗi dấu → đừng tạo chữ bằng Blender; chèn chữ sau bằng `studio chu`/`chu-anh` với font trong `assets/fonts/`.
- Blender không có mô hình thật của sản phẩm: nói rõ đây là mockup đơn giản (hộp/tấm ảnh). Muốn mô hình chi tiết → người dùng chụp nhiều góc hoặc thuê dựng; AI tạo 3D online chỉ khi họ đồng ý (luật 2).

## Sửa lỗi (nói bằng lời thường, tự thử trước)
| Hiện tượng | Cách xử lý |
|---|---|
| "Could not connect to Blender" | Blender chưa mở, hoặc chưa bấm **Connect to Claude** trong thẻ MCP for Blender (phím N). Nhờ người dùng mở Blender và bấm nút đó. |
| Có nút nhưng vẫn không nối | Bấm **Stop** rồi **Connect** lại; thoát hẳn Claude Code và mở lại. Thử `get_addon_status` lần nữa (lần đầu đôi khi trượt, lần sau được). |
| Cổng 9876 bị chiếm | Có một Blender/ứng dụng khác đang dùng: đóng các cửa sổ Blender thừa. Chưa hết → khởi động lại máy. Chỉ đổi cổng khi bất khả kháng (phải đổi cả trong `.mcp.json` lẫn thẻ Blender). |
| Claude Code không thấy công cụ blender | Chưa duyệt máy chủ trong `.mcp.json` hoặc `uvx` không chạy: kiểm tra `uv --version`; làm skill `cai-dat`; thoát và mở lại Claude Code. |
| Add-on không hiện / lỗi khi bật | Blender quá cũ (cần 3.0+; nên 4.2 LTS+) → cài bản mới. Xóa add-on cũ rồi cài lại từ file `blender_mcp.py`. |
| Hết giờ (timeout) / Blender đứng | Cảnh quá nặng hoặc render trực tiếp quá lâu: giảm độ phân giải/số mẫu, chia việc nhỏ, render video bằng dòng lệnh. |
| Ảnh ra đen / quá tối / sản phẩm lọt khỏi khung | Dùng `look` xem camera; tăng `power` đèn, lùi `distance` camera. |
| Báo "Rejected by safe mode" | Viết lại code theo lời nhắn (không dùng `os`, `open`, mạng). Không tắt chế độ an toàn. |
| Lỗi `BLENDER_EEVEE_NEXT` / tên engine / `fcurves` | Hàm trong `product_scene.py` đã thử nhiều tên; vẫn lỗi thì xem số bản Blender (`get_addon_status`) và sửa nhẹ lệnh gọi. |

### Lỗi trên Windows (Smart App Control, diệt virus)
- **Lỗi chứng chỉ khi chạy `uvx`** (`CERTIFICATE_VERIFY_FAILED`, `UnknownIssuer`): Do trình diệt virus (như Avast) quét HTTPS. Đảm bảo biến `UV_SYSTEM_CERTS=1` đã được thiết lập. Tạm đặt trong PowerShell hiện tại: `$env:UV_SYSTEM_CERTS='1'` rồi thử lại. Biện pháp cuối: nhờ người dùng tạm dừng "Web Shield / Quét HTTPS" của diệt virus trong lúc cài.
- **Lỗi 4551 / "Application Control policy has blocked this file"**:
  - Do Smart App Control chặn bản Python chưa ký số do uv tự tải về.
  - Cách xử lý: Cài bản Python 3.12 chính thức từ python.org (đã có chữ ký số) và đảm bảo các biến `UV_NO_MANAGED_PYTHON=1`, `UV_PYTHON_DOWNLOADS=never`. Kiểm tra:
    ```powershell
    uv python find 3.12
    ```
    Kết quả phải in ra đường dẫn dưới `AppData\Local\Programs\Python\Python312`.
  - **Tuyệt đối không** khuyên người dùng tắt Smart App Control (không thể bật lại nếu không cài lại Windows).

## Cập nhật / gỡ
Cập nhật: `uvx mcp-for-blender@latest update` rồi cập nhật file add-on trong thư mục skill (ghi chú lại bản đã thử). Gỡ: tắt add-on trong Preferences; xóa mục `blender` khỏi `.mcp.json`. Giấy phép MIT (xem `addon/LICENSE`); điều khoản dữ liệu ở `addon/TERMS_AND_CONDITIONS.md`.
