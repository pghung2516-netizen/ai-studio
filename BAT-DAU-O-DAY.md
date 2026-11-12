# 🎬 AI STUDIO — Hướng dẫn bắt đầu (dành cho người không rành máy tính)

Workspace này biến ứng dụng **Claude** thành trợ lý biên tập video, sửa ảnh và viết content cho bạn.
Bạn **chỉ cần nói chuyện bằng tiếng Việt** — không cần biết lập trình hay gõ lệnh.

---

## Bạn cần có
- Máy tính **Windows 10 hoặc 11**, còn trống ít nhất **5 GB** ổ đĩa.
- Tài khoản **Claude Pro** trở lên (đăng ký tại claude.ai).
- Mạng Internet ổn định cho lần cài đặt đầu tiên.

---

## Cài đặt lần đầu (khoảng 15–20 phút, chỉ làm 1 lần)

### Bước 1 — Cài ứng dụng Claude
1. Vào **claude.ai/download** → bấm **Download for Windows**.
2. Mở file vừa tải → cài đặt → **đăng nhập** tài khoản Claude của bạn.

### Bước 2 — Lấy thư mục workspace về máy
1. Mở đường link GitHub mà người quản lý gửi cho bạn (đăng nhập GitHub bằng tài khoản đã được mời).
2. Bấm nút xanh **`<> Code`** → chọn **Download ZIP**.
3. Mở thư mục *Downloads* → bấm chuột phải vào file ZIP → **Extract All… (Giải nén tất cả)**.
4. Đổi tên thư mục vừa giải nén thành **`AI-Studio`** và **kéo nó vào ổ `C:`** → bạn có `C:\AI-Studio`.
   > ⚠️ Không để trong *Desktop* hoặc *Documents* nếu máy bạn bật OneDrive — video nặng sẽ bị đồng bộ, rất chậm.

### Bước 3 — Nhấp đúp file `CAI-DAT.bat`
1. Mở `C:\AI-Studio` → **nhấp đúp `CAI-DAT.bat`**.
2. Nếu Windows hiện khung xanh *"Windows protected your PC"* → bấm **More info** → **Run anyway**.
3. Một cửa sổ đen hiện chữ chạy — **cứ để nó tự chạy** (5–15 phút, tùy mạng). Đừng tắt.
4. Khi thấy chữ **XONG! Workspace da san sang** → bấm phím bất kỳ để đóng.

### Bước 4 — Mở workspace trong Claude
1. Mở ứng dụng **Claude** → chọn tab **Code** (phía trên).
2. Bấm chọn thư mục → chọn **`C:\AI-Studio`**.
3. Nếu Claude hỏi *"Do you trust the files in this folder?" / "Tin tưởng thư mục này?"* → bấm **Yes / Trust** (bắt buộc — có bước này Claude mới dùng được bộ công cụ có sẵn mà không hỏi đi hỏi lại).
4. Gõ: **`menu`** rồi Enter. Claude sẽ chào và cho bạn xem những việc làm được. 🎉

> Thỉnh thoảng Claude hỏi *"Allow / Cho phép ... ?"* khi chạy một công cụ mới → bấm **Allow** (hoặc *Allow always* nếu có). Đó là Claude xin phép dùng công cụ ngay trên máy bạn.

---

## Dùng hằng ngày (3 bước)

1. **Bỏ file** (video, ảnh, nhạc, logo) vào thư mục **`01-DAU-VAO`** — hoặc kéo thả thẳng vào khung chat.
2. **Nói việc bạn muốn**, ví dụ:
   - *"Cắt video ban-hang.mp4 lấy từ giây 5 đến giây 35, đổi sang dọc cho TikTok rồi thêm phụ đề."*
   - *"Xóa nền 10 ảnh sản phẩm trong thư mục ao-thun, để nền trắng cho Shopee."*
   - *"Làm video 15 giây từ 5 tấm ảnh này, có chữ giới thiệu và nhạc nền."*
   - *"Viết 3 caption Facebook bán nến thơm, giọng nhẹ nhàng."*
   - *"Viết prompt để Gemini tạo ảnh người mẫu mặc chiếc áo này."*
   - *"Xem video này có gì cần sửa để nhiều view hơn không."*
3. **Nhận kết quả** trong thư mục **`02-THANH-PHAM`** (chia theo ngày). Claude sẽ tự mở thư mục cho bạn — hoặc nhấp đúp **`MO-THANH-PHAM.bat`**.

💡 **Làm 1 lần cho đáng:** gõ *"thiết lập thương hiệu"* — Claude hỏi bạn vài câu về shop (tên, màu, giọng văn, logo) để mọi content và thiết kế sau này đúng chất của bạn.

---

## Các thư mục

| Thư mục | Ý nghĩa |
|---|---|
| `01-DAU-VAO` | Bạn bỏ file gốc vào đây. Claude **không bao giờ** sửa/xóa file gốc. |
| `02-THANH-PHAM` | Kết quả, chia theo ngày. |
| `03-THUONG-HIEU` | Thông tin shop, logo, màu sắc của bạn. |
| `04-THU-VIEN-PROMPT` | Mẫu câu lệnh tạo ảnh/video AI và mẫu content. |
| Các thư mục khác | Phần máy móc — không cần mở. |

---

## Gặp trục trặc?

| Chuyện gì xảy ra | Làm gì |
|---|---|
| Claude báo thiếu công cụ / lỗi lạ | Gõ: **"kiểm tra cài đặt giúp mình"** — Claude tự sửa. |
| Cửa sổ `CAI-DAT.bat` báo LỖI | Kiểm tra mạng (thử phát 4G từ điện thoại), chạy lại. Vẫn lỗi → mở Claude, gõ *"cài đặt bị lỗi"*. |
| Phụ đề / xóa nền lần đầu rất chậm | Bình thường — máy đang tải mô hình AI (1 lần). |
| Windows Security cảnh báo `uv.exe` hoặc `ffmpeg` | Bấm **Allow / Cho phép** — đây là công cụ của workspace. |
| Video ra không như ý | Nói cụ thể điều chưa ưng: *"chữ to hơn"*, *"nhạc nhỏ lại"*, *"cắt sớm hơn 2 giây"*. |
| Muốn cập nhật bản mới | Hỏi người quản lý, hoặc gõ *"cập nhật workspace"*. |

---

## Lưu ý an toàn
- Không đưa **CCCD, số tài khoản, mật khẩu, thông tin khách hàng** vào nội dung nhờ AI viết.
- Nhạc nền video bán hàng: dùng nhạc **miễn phí bản quyền** (YouTube Audio Library, Pixabay) hoặc nhạc có sẵn trong TikTok/CapCut.
- Ảnh/video AI tạo ra: không giả mạo người thật hay thương hiệu khác.
