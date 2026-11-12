---
name: sua-anh
description: Chỉnh sửa ảnh thật - xóa nền ảnh sản phẩm/chân dung, thay nền, đổi cỡ đúng chuẩn từng kênh (Shopee, TikTok Shop, Facebook, Instagram, YouTube thumbnail, banner web), chèn chữ khuyến mãi, chèn logo/watermark hàng loạt, nén ảnh, đổi HEIC sang JPG, ghép ảnh lưới hoặc trước-sau. Dùng cho mọi yêu cầu sửa ảnh có sẵn.
---

# Sửa ảnh

Lệnh: `uv run python -m studio <lệnh> <ảnh-hoặc-thư-mục> [tùy chọn]` — **mọi lệnh ảnh nhận cả thư mục** (làm hàng loạt).

| Người dùng nói | Lệnh |
|---|---|
| "xóa nền", "tách nền sản phẩm" | `xoa-nen <ảnh>` → PNG nền trong suốt. Thêm `--cat-sat` để cắt sát. |
| "xóa nền rồi để nền trắng" (chuẩn sàn TMĐT) | `xoa-nen <ảnh> --nen trang --cat-sat` rồi `doi-co <kết quả> --kenh shopee --kieu vua` |
| "thay nền màu thương hiệu" | `xoa-nen <ảnh> --nen "#mã-màu"` |
| ảnh chân dung người | `xoa-nen <ảnh> --mo-hinh u2net_human_seg` (tóc đẹp hơn) |
| "đổi cỡ cho Shopee / Facebook / TikTok / YouTube" | `doi-co <ảnh> --kenh <kênh>` |
| "cỡ 1200x628" | `doi-co <ảnh> --kich-thuoc 1200x628` |
| "chèn chữ sale / giá" | `chu-anh <ảnh> --noi-dung "..." --vi-tri duoi --co lon [--mau vang] [--mau-nen "#E53935"]` |
| "đóng logo / watermark cả thư mục" | `logo <thư-mục> <logo.png> --vi-tri duoi-phai --ti-le 0.18 --do-mo 0.7` |
| "ảnh nặng quá", "giảm dung lượng" | `nen-anh <ảnh> [--dinh-dang webp] [--rong-toi-da 1600]` |
| "ảnh iPhone không mở được" (HEIC) | `doi-dinh-dang <ảnh/thư-mục> --sang jpg` |
| "ghép ảnh trước – sau" | `ghep-anh <trước> <sau> --kieu truoc-sau [--nhan "TRƯỚC|SAU"]` |
| "ghép nhiều ảnh thành 1" | `ghep-anh <ảnh...> --kieu luoi [--so-cot 3]` |

**Kênh có sẵn (`--kenh`)**: facebook-post (1080x1350), facebook-vuong, facebook-cover, facebook-ads, instagram-post, instagram-vuong, story / reels / tiktok / zalo-story (1080x1920), youtube-thumbnail (1280x720), youtube-banner, youtube-shorts, shopee / lazada / tiktok-shop (1024x1024), zalo-oa, linkedin, banner-web (1920x600), avatar, a4-doc, a4-ngang.

**Kiểu đổi cỡ (`--kieu`)**: `vua` = giữ trọn ảnh, thêm nền (màu `--mau-nen`) · `cat` = lấp đầy, cắt bớt mép · `nen-mo` = giữ trọn, nền là chính ảnh làm mờ (đẹp cho story/tiktok).

## Quy trình
1. Xác định ảnh + mục đích dùng (đăng đâu?) → chọn kênh phù hợp, không cần hỏi nếu đã rõ.
2. Chạy lệnh; với chuỗi nhiều bước dùng `KET QUA` bước trước.
3. **Xem lại ảnh kết quả** (mở bằng công cụ Read) — đặc biệt xóa nền (viền có sạch không) và chữ (có che sản phẩm không). Không đạt → thử mô hình khác / vị trí khác.
4. Báo kết quả, mở thư mục.

## Khi người dùng muốn thiết kế MỚI (poster, banner, ảnh quảng cáo)
- Ảnh có sản phẩm thật + bố cục đơn giản → kết hợp `xoa-nen` + `doi-co` + `chu-anh` + `logo`.
- Poster nghệ thuật/đồ họa → skill `canvas-design` (chữ tiếng Việt phải dùng font `assets/fonts/BeVietnamPro-*.ttf`).
- Ảnh studio/người mẫu/bối cảnh do AI vẽ → skill `prompt-anh-ai` (người dùng dán prompt vào Gemini/ChatGPT), sau đó quay lại đây để đổi cỡ/chèn logo.
