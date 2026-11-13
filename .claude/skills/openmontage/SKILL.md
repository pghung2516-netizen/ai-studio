---
name: openmontage
description: Dùng công cụ thêm OpenMontage (chạy offline trên máy) cho 3 việc - (1) cắt video dài (livestream, buổi chia sẻ, phỏng vấn, video review dài) thành NHIỀU clip ngắn TikTok/Reels có phụ đề; (2) làm gọn video người nói trước camera - bỏ khoảng lặng, bỏ câu nói vấp, cắt khung dọc giữ mặt người ở giữa, chuẩn âm, phụ đề; (3) phân tích một video mẫu người dùng thích (nhịp cắt, câu mở đầu, kiểu chữ, nhạc) rồi đề xuất làm video tương tự cho shop. Dùng khi người dùng nói "cắt livestream thành nhiều clip", "chia video dài thành video ngắn", "lọc đoạn hay làm TikTok", "bỏ khoảng lặng", "cắt chỗ nói vấp", "video nói chuyện cho gọn", "làm video giống video này", "học theo video mẫu".
---

# OpenMontage - clip ngắn từ video dài, video người nói, học theo video mẫu

OpenMontage là công cụ mã nguồn mở (giấy phép AGPL-3.0). Nó được tải về máy ở lần dùng đầu vào `05-CONG-CU-THEM/openmontage` và **chạy hoàn toàn offline**: không cần API key, không gửi file đi đâu, không tốn tiền. Việc của nó là **phân tích + cắt + đổi khung**. Phụ đề, chữ, logo, nhạc và chốt bản vẫn làm bằng `studio` như mọi việc khác.

> Không dùng skill này cho việc 1 bước (cắt 1 đoạn, nén, xoay…) → dùng `sua-video`. Dự án CapCut → `capcut-cat-thong-minh`.

## Bước 0 - Sẵn sàng chưa?
```
uv run python -m studio openmontage trang-thai
```
- "chưa cài" → nói "Lần đầu dùng tính năng này, mình cần tải thêm khoảng 5–10 phút (~700MB) nhé", rồi chạy `uv run python -m studio openmontage cai`.
- Các tên công cụ hiện ra là tên kỹ thuật, **không đọc cho người dùng**.

## Cách gọi công cụ OpenMontage
```
uv run python -m studio openmontage cong-cu <tên> '<json>' --du-an "<dự án>"
```
- File vào (`input_path`, `source`, `audio_path`…) chỉ cần **tên file**; lệnh tự tìm trong nháp → `Gốc/` của dự án.
- Bỏ trống `output_path` thì kết quả tự vào nháp dự án. Dòng `KET QUA:` là file video ra; `THONG TIN.du_lieu` là file JSON đầy đủ (đọc khi cần chi tiết).
- PowerShell: bọc JSON trong nháy đơn, bên trong dùng nháy kép (giống skill CapCut).
- Chỉ công cụ offline mới chạy được. Link video (YouTube/TikTok) bị chặn có chủ ý: nhờ người dùng **lưu video về máy** rồi đưa vào dự án.

| Công cụ | Dùng để | Tham số hay dùng |
|---|---|---|
| `silence_cutter` | Bỏ khoảng lặng (hoặc tua nhanh chỗ lặng) | `mode`: `remove` / `speed_up`; `min_silence_duration` 0.5–1.0; `silence_threshold_db` -35 (ồn thì -30); `padding_seconds` 0.1 |
| `auto_reframe` | Đổi khung, **bám mặt người** để mặt luôn ở giữa | `target_aspect`: `portrait` (9:16) / `square` / `vertical_4_5` |
| `scene_detect` | Tìm các điểm chuyển cảnh | — |
| `video_analyzer` | Phân tích video mẫu: cảnh, nhịp cắt/phút, khung hình chính, độ sôi động âm thanh | `source`, `analysis_depth`: `standard` / `deep` |
| `audio_enhance` | Lọc ồn, làm rõ giọng | — |
| `transcriber` | Lời thoại có mốc từng chữ (JSON) | `model_size` `small`, `language` `vi` |

Lời thoại để đọc/chọn đoạn: ưu tiên `studio phu-de` (ra `.txt` + `.srt` dễ đọc). Chỉ dùng `transcriber` khi cần mốc **từng chữ** để cắt chính xác chỗ nói vấp.

---

## Việc 1 - Video dài → nhiều clip ngắn
1. **Mở dự án** (`du-an moi`), chạy `thong-tin`. Báo trước thời gian: nghe lời thoại mất khoảng 1/3 độ dài video (livestream 60 phút ≈ 20 phút).
2. **Nghe + xem**: `phu-de <file> --du-an …` (không đốt) → đọc `.txt`; `khung-hinh <file> --kiem-tra` → xem `_TONG-HOP.jpg`.
3. **Chọn đoạn**: đọc tiêu chí ở `05-CONG-CU-THEM/openmontage/skills/pipelines/clip-factory/script-director.md` (mục *Score Candidate Moments* và *Select The Final Batch*). Tóm lại một đoạn đáng làm clip khi:
   - **câu mở đầu giữ chân** trong 3 giây;
   - **tự hiểu được**, không cần xem phần trước;
   - có **một ý trọn vẹn** (mẹo, so sánh, giá, phản hồi khách, khoảnh khắc vui);
   - nói có năng lượng;
   - dài 15–60 giây.

   Mốc vào/ra phải rơi vào đầu/cuối câu, không cắt giữa chữ.
4. **Hỏi người dùng** (AskUserQuestion, `multiSelect: true`): liệt kê 4–8 đoạn đề xuất, mỗi đoạn gồm *tiêu đề gợi ý · mm:ss–mm:ss · câu mở đầu*. Thêm 1 câu hỏi về kiểu (phụ đề vàng TikTok / chữ tiêu đề đầu clip / logo) theo skill `hoi-y-tuong`, gợi ý đặt đầu.
5. **Làm từng clip** (mỗi bước lấy `KET QUA` của bước trước):
   1. `studio cat`
   2. `openmontage cong-cu silence_cutter` nếu clip có khoảng lặng > 1 giây
   3. `openmontage cong-cu auto_reframe` (`portrait`) nếu video gốc nằm ngang
   4. `studio chuan-am`
   5. `studio phu-de --dot-vao` (kiểu `tiktok`)
   6. tùy chọn: `studio chu` cho tiêu đề 3 giây đầu, `studio logo`
6. **Kiểm tra** `khung-hinh --kiem-tra` cho 1–2 clip đầu (mặt có bị cắt mất không, chữ có che mặt không).
7. **Chốt** từng clip: `du-an chot … --ten "clip 1 - <tiêu đề ngắn>"`. Ghi vào nhật ký danh sách mốc giờ đã dùng (lần sau "làm thêm 3 clip nữa" thì chọn đoạn khác).

## Việc 2 - Video người nói cho gọn
1. `thong-tin` + `khung-hinh --kiem-tra` + `phu-de` (đọc lời thoại).
2. Hỏi nhanh (hoi-y-tuong):
   - **Chỗ lặng:** cắt hẳn (gợi ý) hay tua nhanh?
   - **Khung:** dọc 9:16 bám mặt (gợi ý cho TikTok) hay giữ nguyên?
   - **Phụ đề:** có không?
3. `silence_cutter` (`remove`, `min_silence_duration` 0.6, `padding_seconds` 0.1).
4. **Câu nói vấp / nói lại** (bộ tự động không bắt được): đọc lời thoại tìm các câu lặp, **giữ lần nói CUỐI**. Lấy mốc từng chữ bằng `transcriber` trên bản đã bỏ lặng. Sau đó `studio cat` các đoạn giữ lại → `studio ghep`.
5. `auto_reframe` nếu cần dọc → `audio_enhance` nếu tiếng ồn → `studio chuan-am` → `studio phu-de --dot-vao`.
6. Kiểm tra (mặt ở giữa khung, không hụt chữ đầu câu) → chốt.

## Việc 3 - Học theo video mẫu
1. Người dùng đưa **file** video mẫu (đã lưu về máy) vào dự án.

   **Nhắc 1 lần:** chỉ học *cách làm* (nhịp, bố cục, kiểu chữ). Không chép nội dung, nhạc hay hình của người khác để đăng bán hàng.
2. Phân tích:
   - `openmontage cong-cu video_analyzer '{"source":"<file>","analysis_depth":"deep"}'`
   - `phu-de <file>` để lấy lời thoại
   - xem `_TONG-HOP.jpg` của `khung-hinh --kiem-tra`
   - mở vài ảnh trong thư mục `keyframes` mà công cụ tạo ra
3. Tóm tắt **bằng lời thường** (5–6 gạch đầu dòng), ví dụ:
   - 3 giây đầu làm gì;
   - bao lâu đổi cảnh một lần (từ `cuts_per_minute`);
   - chữ to/nhỏ, vị trí, màu;
   - có giọng nói hay chỉ nhạc;
   - nhạc sôi động hay nhẹ;
   - kết bằng lời kêu gọi gì.
4. Đề xuất 2–3 hướng làm cho shop theo `hoi-y-tuong`, chỉ rõ công cụ dựng:
   - có video thật → `sua-video` + Việc 2;
   - có ảnh → `video-tu-anh`;
   - không có tư liệu → `video-dong-html`.

   Người dùng chọn xong thì làm theo skill đó.

---

## Lưu ý
- **Không** chạy quy trình đầy đủ của OpenMontage (research → proposal → … → publish) và không đọc `AGENT_GUIDE.md` của nó. Quy trình đó viết cho người dùng biết kỹ thuật, nói tiếng Anh, và có nhiều bước gọi dịch vụ trả phí.
- Không tự thêm API key vào OpenMontage. Không dùng `openmontage chay` để gọi công cụ online.
- Lỗi "chưa cài" → `openmontage cai`. Lỗi lạ sau khi cài → `openmontage cai --cai-lai` (bản cũ được cất vào `.cache`, không xóa).
- `auto_reframe` báo `method: center_crop` nghĩa là không thấy mặt người, nên cắt giữa khung. Xem ảnh kiểm tra; nếu người đứng lệch, bị mất một phần thì dùng `studio khung --ti-le 9:16 --kieu nen-mo` (giữ trọn khung, nền mờ).
- Trên Mac có thể hiện cảnh báo `objc[...] Class AVF... implemented in both`: vô hại, bỏ qua.
