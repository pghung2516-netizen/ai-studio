# Công cụ thêm (đã tích hợp)

> Người quản lý thêm công cụ mới bằng cách nói với Claude: **"thêm công cụ <link repo>"** (skill `them-cong-cu`).
> Claude đọc bảng này để biết có thể dùng thêm công cụ nào.

| Tên | Làm được gì | Người dùng nói gì để dùng | Cần mạng / API key? | Giấy phép | Skill |
|---|---|---|---|---|---|
| HyperFrames + GSAP + three.js | Video động dựng từ HTML: chữ chạy, intro logo, quảng cáo khuyến mãi, 3D xoay sản phẩm | "làm video chữ chạy", "làm intro logo", "video khuyến mãi 10 giây", "3D xoay sản phẩm" | Chỉ lúc cài (~530 MB; tải Chromium nếu máy không có Chrome). Dựng offline, không key | Apache-2.0 / GSAP Standard no-charge / MIT | `video-dong-html` |
| Remotion | Hàng loạt video từ bảng dữ liệu (mỗi dòng 1 video), mẫu video thương hiệu dùng lại | "làm hàng loạt video sản phẩm", "video từ bảng giá", "mẫu video dùng lại" | Lần cài đầu (~400 MB), sau đó offline; không key | Miễn phí cho cá nhân / công ty ≤3 người; công ty ≥4 người phải mua giấy phép | `video-remotion` |
| Manim | Video hoạt hình giải thích: sơ đồ, các bước, biểu đồ chạy số, công thức | "làm video giải thích bằng hoạt hình", "sơ đồ quy trình", "biểu đồ doanh thu chạy" | Lần chạy đầu (~150 MB), không key | MIT | `video-giai-thich` |
| OpenMontage (commit fecb9a1, chỉ dùng phần chạy offline) | Cắt video dài (livestream) thành nhiều clip ngắn; làm gọn video người nói (bỏ khoảng lặng, cắt khung dọc bám mặt); phân tích video mẫu (nhịp cắt, cảnh, khung hình chính) | "cắt livestream thành nhiều clip", "bỏ khoảng lặng", "video nói chuyện cho gọn", "làm video giống video này" | Chỉ lúc cài (~700 MB, `studio openmontage cai`), sau đó offline; không key. Công cụ online của nó bị chặn trong `studio openmontage cong-cu` | AGPL-3.0: dùng nội bộ thoải mái; **không** chép mã vào repo này, không sửa rồi phân phối lại / chạy thành dịch vụ web cho người khác (khi đó phải công khai mã) | `openmontage` |
| Blender MCP (mcp-for-blender 2.2.8) | Dựng cảnh 3D, ảnh sản phẩm 3D, video xoay 360° | "dựng cảnh 3D", "ảnh 3D cái hộp", "sản phẩm xoay 360" | Cần cài Blender (~400 MB). Tính năng AI online là tùy chọn, có thể tính phí, mặc định TẮT | MIT | `blender-3d` |
