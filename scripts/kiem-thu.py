"""Kiểm thử tự động toàn bộ lệnh `studio` - chạy được trên Windows và Mac.

    uv run python scripts/kiem-thu.py            # chạy tất cả
    uv run python scripts/kiem-thu.py cat logo   # chỉ chạy các ca có tên chứa 'cat' hoặc 'logo'

- Tự tạo file mẫu trong thư mục có dấu tiếng Việt + dấu cách (giống máy người dùng thật).
- Kết quả ghi vào .cache/kiem-thu/ (KHÔNG đụng 01-DAU-VAO / 02-THANH-PHAM).
- In ra báo cáo markdown gọn và lưu ở .cache/kiem-thu/BAO-CAO.md
- Ảnh .cache/kiem-thu/_XEM-MAT.jpg ghép khung hình các kết quả có chữ tiếng Việt -> mở ra xem dấu có lỗi không.
"""
from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

GOC = ROOT / ".cache" / "kiem-thu"
MAU = GOC / "Mẫu thử có dấu"          # đường dẫn khó: tiếng Việt + dấu cách
KQ = GOC / "ket-qua"
os.environ["STUDIO_THANH_PHAM"] = str(KQ)

from studio.common import bat_utf8, chay_ffmpeg, doc_thong_tin, ffmpeg_exe  # noqa: E402

bat_utf8()


# ------------------------------------------------------------------ tạo file mẫu
def tao_mau() -> dict[str, Path]:
    shutil.rmtree(GOC, ignore_errors=True)
    MAU.mkdir(parents=True)
    from PIL import Image, ImageDraw

    m = {
        "video": MAU / "video gốc ngang.mp4",
        "video_doc": MAU / "video dọc.mp4",
        "nhac": MAU / "nhạc nền.mp3",
        "anh": MAU / "ảnh sản phẩm.jpg",
        "anh2": MAU / "ảnh 2.png",
        "logo": MAU / "logo.png",
        "srt": MAU / "phụ đề.srt",
    }
    chay_ffmpeg(["-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30:duration=8",
                 "-f", "lavfi", "-i", "sine=frequency=440:duration=8",
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(m["video"])])
    chay_ffmpeg(["-f", "lavfi", "-i", "testsrc2=size=720x1280:rate=30:duration=5",
                 "-f", "lavfi", "-i", "sine=frequency=660:duration=5",
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(m["video_doc"])])
    chay_ffmpeg(["-f", "lavfi", "-i", "sine=frequency=330:duration=4", "-c:a", "libmp3lame", str(m["nhac"])])

    im = Image.new("RGB", (1200, 900), (235, 235, 235))
    d = ImageDraw.Draw(im)
    d.ellipse((350, 200, 850, 700), fill=(220, 60, 60))
    d.rectangle((520, 90, 680, 220), fill=(60, 60, 200))
    im.save(m["anh"], quality=92)
    im2 = Image.new("RGB", (900, 1200), (40, 120, 90))
    ImageDraw.Draw(im2).rectangle((200, 300, 700, 900), fill=(250, 210, 40))
    im2.save(m["anh2"])
    lg = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    ImageDraw.Draw(lg).ellipse((20, 20, 380, 380), fill=(255, 140, 0, 255))
    lg.save(m["logo"])
    m["srt"].write_text(
        "1\n00:00:00,500 --> 00:00:03,500\nXin chào cả nhà! Hôm nay giảm giá đặc biệt\n\n"
        "2\n00:00:04,000 --> 00:00:07,500\nĐừng bỏ lỡ ưu đãi: ăn ở, đường phố, nghỉ ngơi\n",
        encoding="utf-8")

    # giọng nói tiếng Anh tạo bằng TTS có sẵn của hệ điều hành -> để thử nghe phụ đề
    loi = "Hello everyone. Today we have a special discount on all products. Thank you for watching."
    wav = MAU / "giọng nói.wav"
    try:
        if sys.platform == "win32":
            ps = ("Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                  f"$s.SetOutputToWaveFile('{wav}'); $s.Speak('{loi}'); $s.Dispose()")
            subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, timeout=60)
        elif sys.platform == "darwin":
            aiff = MAU / "giong.aiff"
            subprocess.run(["say", "-o", str(aiff), loi], capture_output=True, timeout=60)
            if aiff.exists():
                chay_ffmpeg(["-i", str(aiff), str(wav)])
    except Exception:  # noqa: BLE001
        pass
    if wav.exists() and wav.stat().st_size > 10000:
        m["giong"] = wav
    return m


# ------------------------------------------------------------------ chạy 1 ca
def chay(args: list[str], timeout: int = 300) -> tuple[int, str, float]:
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, "-m", "studio", *args], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or ""), time.time() - t0
    except subprocess.TimeoutExpired:
        return -9, f"QUÁ THỜI GIAN {timeout}s", time.time() - t0


def ket_qua_cua(out: str) -> list[Path]:
    return [Path(x.strip()) for x in re.findall(r"^KET QUA: (.+)$", out, re.M)]


def kt_video(dai=None, rong=None, cao=None, tieng=None, hinh=True):
    """Trả về hàm kiểm tra file kết quả đầu tiên."""
    def f(files: list[Path]) -> str | None:
        p = files[0]
        i = doc_thong_tin(p)
        if hinh and not i.co_hinh:
            return "không có hình"
        if dai is not None and abs(i.thoi_luong - dai) > 0.6:
            return f"độ dài {i.thoi_luong:.2f}s, mong đợi {dai}s"
        if rong and (i.rong, i.cao) != (rong, cao):
            return f"khung {i.rong}x{i.cao}, mong đợi {rong}x{cao}"
        if tieng is not None and i.co_tieng != tieng:
            return f"có tiếng={i.co_tieng}, mong đợi {tieng}"
        return None
    return f


def kt_anh(rong=None, cao=None, alpha=None, ext=None):
    def f(files: list[Path]) -> str | None:
        from PIL import Image
        p = files[0]
        if ext and p.suffix.lower() != ext:
            return f"đuôi {p.suffix}, mong đợi {ext}"
        im = Image.open(p)
        if rong and im.size != (rong, cao):
            return f"cỡ {im.size}, mong đợi {(rong, cao)}"
        if alpha is not None and ("A" in im.getbands()) != alpha:
            return f"kênh trong suốt={'A' in im.getbands()}, mong đợi {alpha}"
        return None
    return f


def kt_file(*duoi):
    def f(files: list[Path]) -> str | None:
        co = {p.suffix.lower() for p in files}
        thieu = [d for d in duoi if d not in co]
        return f"thiếu file {thieu}" if thieu else None
    return f


# ------------------------------------------------------------------ danh sách ca kiểm thử
def danh_sach_ca(m: dict[str, Path]) -> list[tuple]:
    v, vd, s = str(m["video"]), str(m["video_doc"]), str
    ca = [
        # (tên, args, hàm kiểm tra | None, timeout, xem_mat)
        ("kiem-tra", ["kiem-tra"], None, 120, False),
        ("thong-tin", ["thong-tin", v], None, 60, False),
        ("cat", ["cat", v, "--tu", "0:01", "--den", "0:04"], kt_video(dai=3, tieng=True), 300, False),
        ("ghep", ["ghep", v, vd, "--ti-le", "16:9"], kt_video(dai=13, rong=1920, cao=1080), 300, False),
        ("khung-9:16-nen-mo", ["khung", v, "--ti-le", "9:16"], kt_video(dai=8, rong=1080, cao=1920), 300, False),
        ("khung-1:1-cat", ["khung", v, "--ti-le", "vuong", "--kieu", "cat"], kt_video(rong=1080, cao=1080), 300, False),
        ("nen", ["nen", v, "--muc", "vua", "--toi-da", "480"], kt_video(dai=8), 300, False),
        ("nen-toi-da-mb", ["nen", v, "--toi-da-mb", "1"], kt_video(dai=8), 300, False),
        ("toc-do-x2", ["toc-do", v, "--he-so", "2"], kt_video(dai=4, tieng=True), 300, False),
        ("nhac", ["nhac", v, s(m["nhac"])], kt_video(dai=8, tieng=True), 300, False),
        ("chuan-am", ["chuan-am", v], kt_video(dai=8, tieng=True), 300, False),
        ("tat-tieng", ["tat-tieng", v], kt_video(dai=8, tieng=False), 300, False),
        ("tach-am", ["tach-am", v], kt_file(".mp3"), 300, False),
        ("xoay", ["xoay", v, "--huong", "phai"], kt_video(rong=720, cao=1280), 300, False),
        ("logo-video", ["logo", v, s(m["logo"])], kt_video(dai=8), 300, True),
        ("chu-video", ["chu", v, "--noi-dung", "Giảm giá 50% – Đặc biệt hôm nay!", "--tu", "0", "--den", "6"],
         kt_video(dai=8), 300, True),
        ("khung-hinh", ["khung-hinh", v, "--so", "6", "--kiem-tra"], kt_file(".jpg"), 300, False),
        ("gif", ["gif", v, "--tu", "0", "--den", "2"], kt_file(".gif"), 300, False),
        ("anh-thanh-video", ["anh-thanh-video", s(m["anh"]), s(m["anh2"]), "--giay-moi-anh", "2",
                             "--chu", "Ưu đãi sốc|Mua ngay hôm nay", "--nhac", s(m["nhac"])],
         kt_video(rong=1080, cao=1920, tieng=True), 600, True),
        ("dot-phu-de", ["dot-phu-de", v, s(m["srt"])], kt_video(dai=8), 300, True),
        ("dot-phu-de-doc-hop-den", ["dot-phu-de", vd, s(m["srt"]), "--kieu", "hop-den", "--in-hoa"],
         kt_video(rong=720, cao=1280), 300, True),
        ("doi-co-shopee", ["doi-co", s(m["anh"]), "--kenh", "shopee"], kt_anh(1024, 1024), 120, False),
        ("doi-co-thu-muc", ["doi-co", s(MAU), "--kenh", "tiktok", "--kieu", "nen-mo"], kt_anh(1080, 1920), 120, False),
        ("xoa-nen", ["xoa-nen", s(m["anh"])], kt_anh(alpha=True), 600, False),
        ("xoa-nen-trang", ["xoa-nen", s(m["anh"]), "--nen", "trang", "--cat-sat"], None, 600, False),
        ("chu-anh", ["chu-anh", s(m["anh"]), "--noi-dung", "Tiếng Việt: ăn ở, đường phố – ỨNG DỤNG",
                     "--mau-nen", "do"], None, 120, True),
        ("nen-anh", ["nen-anh", s(m["anh"]), "--dinh-dang", "webp"], kt_anh(ext=".webp"), 120, False),
        ("ghep-anh-luoi", ["ghep-anh", s(m["anh"]), s(m["anh2"]), s(m["anh"])], None, 120, False),
        ("ghep-anh-truoc-sau", ["ghep-anh", s(m["anh"]), s(m["anh2"]), "--kieu", "truoc-sau", "--nhan", "TRƯỚC|SAU"],
         None, 120, True),
        ("doi-dinh-dang", ["doi-dinh-dang", s(m["anh2"]), "--sang", "jpg"], kt_anh(ext=".jpg"), 120, False),
        ("logo-anh", ["logo", s(m["anh"]), s(m["logo"])], None, 120, False),
        ("loi-file-khong-co (mong đợi mã 2)", ["cat", "khong-ton-tai.mp4", "--dai", "3"], "MA2", 60, False),
    ]
    if "giong" in m:
        ca.append(("phu-de-nghe (tiếng Anh)", ["phu-de", s(m["giong"]), "--ngon-ngu", "en", "--mo-hinh", "nhanh"],
                   kt_file(".srt", ".txt"), 900, False))
    return ca


# ------------------------------------------------------------------ ảnh xem bằng mắt
def anh_xem_mat(muc: list[tuple[str, Path]]) -> Path | None:
    from PIL import Image, ImageDraw
    from studio.image import _font

    thumbs = []
    for ten, p in muc:
        j = GOC / "xem" / f"{len(thumbs)}.jpg"
        j.parent.mkdir(parents=True, exist_ok=True)
        try:
            if p.suffix.lower() in {".mp4", ".mov"}:
                info = doc_thong_tin(p)
                t = 1.5 if info.thoi_luong > 2 else info.thoi_luong / 2
                chay_ffmpeg(["-ss", f"{t:.2f}", "-i", str(p), "-frames:v", "1", "-vf", "scale=480:-2", str(j)])
                im = Image.open(j).convert("RGB")
            else:
                im = Image.open(p).convert("RGB")
            im.thumbnail((480, 480))
            thumbs.append((ten, im))
        except Exception:  # noqa: BLE001
            continue
    if not thumbs:
        return None
    o = 480
    sheet = Image.new("RGB", (o * len(thumbs), o + 36), (25, 25, 25))
    d = ImageDraw.Draw(sheet)
    f = _font(20, "dam")
    for i, (ten, im) in enumerate(thumbs):
        sheet.paste(im, (i * o + (o - im.width) // 2, 36 + (o - im.height) // 2))
        d.text((i * o + 8, 6), ten, font=f, fill=(255, 214, 0))
    out = GOC / "_XEM-MAT.jpg"
    sheet.save(out, quality=88)
    return out


# ------------------------------------------------------------------ main
def main() -> int:
    loc = [a.lower() for a in sys.argv[1:]]
    t_bd = time.time()
    print("⏳ Đang tạo file mẫu...", flush=True)
    m = tao_mau()
    ca = [c for c in danh_sach_ca(m) if not loc or any(x in c[0].lower() for x in loc)]

    rows, loi, xem = [], [], []
    for i, (ten, args, kt, to, xm) in enumerate(ca, 1):
        print(f"[{i}/{len(ca)}] {ten} ...", end=" ", flush=True)
        code, out, dt = chay(args, to)
        ly_do = None
        files = ket_qua_cua(out)
        if kt == "MA2":
            ly_do = None if code == 2 else f"mã thoát {code}, mong đợi 2"
        elif code != 0:
            ly_do = f"mã thoát {code}"
        elif args[0] not in ("kiem-tra", "thong-tin") and not files:
            ly_do = "không có dòng KET QUA"
        elif files and not all(p.exists() for p in files):
            ly_do = "file KET QUA không tồn tại"
        elif kt and files:
            try:
                ly_do = kt(files)
            except Exception as e:  # noqa: BLE001
                ly_do = f"lỗi khi kiểm tra kết quả: {e}"
        ok = ly_do is None
        print(("✅" if ok else "❌") + f" {dt:.1f}s", flush=True)
        rows.append((ten, ok, dt, ly_do or ""))
        if not ok:
            loi.append((ten, args, code, out))
        elif xm and files:
            xem.append((ten, files[0]))

    sheet = anh_xem_mat(xem)

    # ---- thông tin máy
    try:
        r = subprocess.run([ffmpeg_exe(), "-version"], capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        ffv = r.stdout.splitlines()[0][:60]
    except Exception as e:  # noqa: BLE001
        ffv = f"lỗi: {e}"
    dat = sum(1 for r in rows if r[1])
    L = [
        f"# Kiểm thử studio – {platform.system()} – {dat}/{len(rows)} đạt",
        "",
        f"- Máy: {platform.platform()} | {platform.machine()} | Python {sys.version.split()[0]}",
        f"- ffmpeg: {ffv}",
        f"- Thư mục workspace: `{ROOT}` (OneDrive: {'CÓ' if 'onedrive' in str(ROOT).lower() else 'không'})",
        f"- Mã hóa console: stdout={sys.stdout.encoding}, locale={__import__('locale').getpreferredencoding(False)}",
        f"- Có giọng TTS để thử phụ đề: {'có' if 'giong' in m else 'KHÔNG (bỏ qua ca phu-de-nghe)'}",
        f"- Tổng thời gian: {time.time() - t_bd:.0f}s",
        "",
        "| Ca | Kết quả | Thời gian | Ghi chú |",
        "|---|---|---|---|",
    ]
    L += [f"| {t} | {'✅' if ok else '❌'} | {dt:.1f}s | {g} |" for t, ok, dt, g in rows]
    if loi:
        L += ["", "## Chi tiết lỗi"]
        for ten, args, code, out in loi:
            duoi = "\n".join(out.strip().splitlines()[-15:])
            L += ["", f"### {ten} (mã {code})", f"`studio {' '.join(json.dumps(a, ensure_ascii=False) if ' ' in a else a for a in args)}`",
                  "```", duoi, "```"]
    L += ["", f"Ảnh xem bằng mắt (chữ tiếng Việt, logo, phụ đề): `{sheet}`" if sheet else ""]
    bc = "\n".join(L).rstrip() + "\n"
    (GOC / "BAO-CAO.md").write_text(bc, encoding="utf-8")
    print("\n" + bc)
    print(f"BAO CAO: {GOC / 'BAO-CAO.md'}")
    return 0 if dat == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
