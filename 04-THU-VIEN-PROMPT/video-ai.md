# Thư viện prompt VIDEO AI (Veo / Sora / Kling / Runway)

> Biên soạn lại từ các bộ kỹ thuật góc máy, ánh sáng, đồng nhất nhân vật, video quảng cáo và quy trình người mẫu bán hàng. Prompt tiếng Anh cho kết quả tốt nhất; lời thoại tiếng Việt để trong ngoặc kép + "spoken in Vietnamese".

---

## 1. Khung prompt chuẩn (1 cảnh, 8 giây)
```
[SHOT] Medium close-up, slow push-in, eye level.
[SUBJECT] A Vietnamese woman in her late 20s, shoulder-length black hair, cream linen shirt, warm confident smile.
[ACTION] She lifts a glass jar of honey to the camera, turns it slowly so the label faces us, then nods.
[SETTING] Bright minimalist kitchen, morning, wooden counter with fresh lemons.
[LIGHT] Soft warm window light from the left, gentle highlights on the glass, shallow depth of field.
[AUDIO] Light acoustic music, soft clink of glass. She says: "Mật ong nguyên chất, ngọt dịu tự nhiên." (spoken in Vietnamese)
[STYLE] Photorealistic commercial, 4K, natural skin texture, no text on screen.
[FORMAT] 8 seconds, 9:16 vertical.
```

---

## 2. Chuyển động máy quay (chọn 1 cho mỗi cảnh)
| Kỹ thuật | Mô tả ngắn (dán vào [SHOT]) | Dùng khi |
|---|---|---|
| Static stillness | locked-off tripod shot, subject enters and moves while camera stays still, symmetrical framing | mở/kết video, cảnh tĩnh lặng, thương hiệu nhẹ nhàng |
| Fast cut-in | series of quick punch-in cuts toward the subject's details, energetic rhythm | hook 3 giây đầu, video năng động |
| Over-the-shoulder | camera behind the shoulder following what the subject sees or does | hướng dẫn, góc nhìn người dùng |
| Pull-back reveal | starts on a tight detail and slowly pulls back to reveal the full scene | tạo bất ngờ, giới thiệu không gian/sản phẩm |
| Push-in focus | slow dolly push-in toward the subject's face or product | khoảnh khắc cảm xúc, nhấn mạnh sản phẩm |
| Orbit shot | camera orbits 180° around the product/subject at constant distance | sản phẩm 360°, thời trang |
| Steady tracking | smooth tracking shot following the subject as they walk | người mẫu, review địa điểm |
| Crane up | slow crane rising upward revealing the landscape | cảnh hùng vĩ, kết video truyền cảm hứng |
| Handheld | subtle handheld movement, documentary feel | vlog, chân thực, UGC |

## 3. Ánh sáng & cảm xúc
| Cảm xúc | Mô tả ánh sáng |
|---|---|
| Ấm áp, bình yên | warm golden-hour light, soft shadows, amber tones |
| Sang trọng | low-key lighting, single soft key light, deep blacks, subtle rim light |
| Tươi mới, sạch | bright high-key lighting, soft diffused daylight, white tones |
| Xa cách, buồn | cold blue light, desaturated colors, soft overcast |
| Hồi hộp | flickering practical light, hard shadows, dim environment |
| Chi tiết sản phẩm | low ambient light with focused spotlight on the product's texture |
| Công nghệ | neon accents, cyan and magenta rim light, glossy reflections |

---

## 4. Giữ nhân vật / sản phẩm đồng nhất qua nhiều cảnh
1. Viết **Khóa nhân vật** 1 lần, dán nguyên văn vào đầu mọi prompt:
   `CHARACTER LOCK: [tên], Vietnamese man, 35, short side-parted black hair, thin rectangular glasses, navy polo shirt with small white logo on chest, silver watch on left wrist.`
2. Lặp lại **1 cử chỉ đặc trưng** ở các cảnh quan trọng (chỉnh kính, xoay nhẹ sản phẩm...) để người xem nhận ra.
3. Giữ cùng **bảng màu + kiểu ánh sáng + bối cảnh chính** giữa các cảnh.
4. Có ảnh nhân vật/sản phẩm → dùng chế độ **image-to-video / ingredients / reference** thay vì chỉ mô tả bằng chữ.
5. Nối cảnh: cảnh sau bắt đầu bằng đúng tư thế/khung hình cảnh trước kết thúc (dùng ảnh cuối cảnh trước làm khung đầu).

---

## 5. Mẫu quảng cáo ngắn
**Đếm ngược tiết lộ (countdown reveal)**
```
Fast-paced product reveal: three quick shots with on-screen motion counting 3, 2, 1, then the [product] lands in the center
of a clean [color] backdrop with a soft impact and floating particles. Punchy bass hit on reveal. 6 seconds, 9:16, 4K commercial.
```
**Vòng lặp cho mạng xã hội (seamless loop)**
```
Seamless looping shot: [product] rotating slowly on a turntable, steam/light rays drifting, the last frame matches the first frame exactly.
Calm ambient sound. 8 seconds, 1:1.
```
**Tương phản dừng lướt (scroll-stopping contrast)**
```
Split moment: left half dull, grey, messy [problem scene]; a hand swipes across and the frame becomes bright, colorful and tidy with [product].
Whoosh sound on the swipe. 6 seconds, 9:16.
```
**Kêu gọi hành động cuối video (CTA drop)**
```
[Product] drops into frame and bounces gently, background turns to brand color [#hex], space left empty at the top third for text overlay.
Upbeat sting sound. 4 seconds, 9:16.
```
(Chữ "Mua ngay / Link ở bio" chèn sau bằng `studio chu` để đúng chính tả.)

---

## 6. Người mẫu bán hàng: video xoay đồ 180° (khung đầu + khung cuối)
Đầu vào: ảnh móc treo mặt trước (start frame) + mặt sau (end frame) — tạo theo `anh-ai.md` mục 3.
```
Cinematic transition starting with a front view of the outfit held by a hand on a wooden hanger.
The hanger smoothly rotates 180 degrees horizontally to reveal the back of the outfit.
Bright modern room. Slow, fluid, stable motion; clothes stay centered; background stays consistent.
Photorealistic, 4K, seamless transformation from start frame to end frame.
```
**Chuyển động theo video mẫu (Kling Motion / motion transfer)** — đầu vào: ảnh người mẫu + video mẫu dáng đi/tạo dáng:
```
High-end fashion commercial, cinematic lighting, smooth camera movement. The character follows the motion of the reference video
perfectly while keeping outfit details and facial consistency. Photorealistic, 4K.
```

---

## 7. Video 8 giây truyền cảm hứng (mẫu nhanh)
`Create an 8-second cinematic video of [hình ảnh ẩn dụ]. Overlay text: '[câu ngắn]'. Add [âm thanh]. Use a [chuyển động máy]. 9:16.`
Ví dụ: hạt bồ công anh trôi trong vũ trụ rồi hóa thành thiên hà · ngọn hải đăng cắt qua sương mù giông bão · mầm xanh trồi lên khỏi đất nứt nẻ rồi thành ốc đảo.
(Chữ tiếng Việt: để AI tạo hình không chữ, rồi chèn chữ bằng `studio chu` cho đúng dấu.)

---

## 8. Phân tích ngược 1 video viral thành prompt
Đưa link/ảnh chụp video mẫu cho Gemini kèm câu:
```
Phân tích video này như một đạo diễn: nhân vật, bối cảnh, góc máy và chuyển động máy từng cảnh, ánh sáng, nhịp dựng, âm thanh, chữ trên màn hình.
Sau đó viết lại thành các prompt video riêng cho từng cảnh theo cấu trúc [SHOT][SUBJECT][ACTION][SETTING][LIGHT][AUDIO][STYLE][FORMAT],
thay nội dung bằng sản phẩm của tôi: [sản phẩm]. Không sao chép logo hay nhân vật của video gốc.
```
