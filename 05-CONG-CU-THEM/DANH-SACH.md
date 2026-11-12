# Công cụ thêm (đã tích hợp)

> Người quản lý thêm công cụ mới bằng cách nói với Claude: **"thêm công cụ <link repo>"** (skill `them-cong-cu`).
> Claude đọc bảng này để biết có thể dùng thêm công cụ nào.

| Tên | Làm được gì | Người dùng nói gì để dùng | Cần mạng / API key? | Giấy phép | Skill |
|---|---|---|---|---|---|
| HyperFrames + GSAP + three.js | Video động dựng từ HTML: chữ chạy, intro logo, quảng cáo khuyến mãi, 3D xoay sản phẩm | "làm video chữ chạy", "làm intro logo", "video khuyến mãi 10 giây", "3D xoay sản phẩm" | Chỉ lúc cài (~530 MB; tải Chromium nếu máy không có Chrome). Dựng offline, không key | Apache-2.0 / GSAP Standard no-charge / MIT | `video-dong-html` |
| Remotion | Hàng loạt video từ bảng dữ liệu (mỗi dòng 1 video), mẫu video thương hiệu dùng lại | "làm hàng loạt video sản phẩm", "video từ bảng giá", "mẫu video dùng lại" | Lần cài đầu (~400 MB), sau đó offline; không key | Miễn phí cho cá nhân / công ty ≤3 người; công ty ≥4 người phải mua giấy phép | `video-remotion` |
| Manim | Video hoạt hình giải thích: sơ đồ, các bước, biểu đồ chạy số, công thức | "làm video giải thích bằng hoạt hình", "sơ đồ quy trình", "biểu đồ doanh thu chạy" | Lần chạy đầu (~150 MB), không key | MIT | `video-giai-thich` |
| Blender MCP (mcp-for-blender 2.2.8) | Dựng cảnh 3D, ảnh sản phẩm 3D, video xoay 360° | "dựng cảnh 3D", "ảnh 3D cái hộp", "sản phẩm xoay 360" | Cần cài Blender (~400 MB). Tính năng AI online là tùy chọn, có thể tính phí, mặc định TẮT | MIT | `blender-3d` |
