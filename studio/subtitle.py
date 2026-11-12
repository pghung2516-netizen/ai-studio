"""Phụ đề: nghe giọng nói -> file .srt (offline, faster-whisper) và đốt phụ đề vào video."""
from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path

from .common import (AM_THANH_EXT, FONT_TEN, FONTS, VIDEO_EXT, LoiNguoiDung, bao, chay_ffmpeg, doc_thong_tin,
                     file_ra, ket_qua, tim_file)

MO_HINH = {"nhanh": "base", "vua": "small", "chuan": "medium", "tot-nhat": "large-v3"}


def _tg_srt(t: float) -> str:
    t = max(0.0, t)
    h, r = divmod(int(t * 1000), 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _doc_srt(p: Path) -> list[tuple[float, float, str]]:
    def to_s(x: str) -> float:
        h, m, s = x.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    cues = []
    for block in re.split(r"\n\s*\n", p.read_text(encoding="utf-8-sig").strip()):
        lines = block.strip().splitlines()
        for i, l in enumerate(lines):
            if "-->" in l:
                a, b = (x.strip() for x in l.split("-->"))
                cues.append((to_s(a), to_s(b.split()[0]), "\n".join(lines[i + 1:]).strip()))
                break
    return cues


def _ghi_srt(cues: list[tuple[float, float, str]], out: Path) -> None:
    out.write_text("\n".join(f"{i}\n{_tg_srt(a)} --> {_tg_srt(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1)),
                   encoding="utf-8")


def _gom_cau(words, toi_da_ky_tu: int) -> list[tuple[float, float, str]]:
    """Gom từng từ thành câu phụ đề ngắn, dễ đọc."""
    cues, cur, bd, kt = [], [], None, None
    for w in words:
        txt = w.word.strip()
        if not txt:
            continue
        nghi = bd is not None and kt is not None and w.start - kt > 0.7
        dai = len(" ".join(cur + [txt])) > toi_da_ky_tu
        if cur and (nghi or dai):
            cues.append((bd, kt, " ".join(cur)))
            cur, bd = [], None
        if bd is None:
            bd = w.start
        cur.append(txt)
        kt = w.end
        do_dai = len(" ".join(cur))
        if txt[-1] in ".?!…" or (txt[-1] in ",;:" and do_dai > toi_da_ky_tu * 0.5):
            cues.append((bd, kt, " ".join(cur)))
            cur, bd = [], None
    if cur:
        cues.append((bd, kt, " ".join(cur)))
    # gộp "từ mồ côi" (1 từ lẻ loi cuối câu) vào câu trước cho dễ đọc
    gon: list = []
    for a, b, t in cues:
        if gon and len(t.split()) == 1 and len(gon[-1][2]) + len(t) + 1 <= toi_da_ky_tu + 10 \
                and gon[-1][2][-1] not in ".?!…" and a - gon[-1][1] < 0.5:
            pa, _, pt = gon.pop()
            gon.append((pa, b, f"{pt} {t}"))
        else:
            gon.append((a, b, t))
    cues = gon
    # nối liền mạch: phụ đề hiện tới khi câu sau bắt đầu (nếu khoảng trống ngắn)
    out = []
    for i, (a, b, t) in enumerate(cues):
        if i + 1 < len(cues) and cues[i + 1][0] - b < 0.4:
            b = cues[i + 1][0]
        out.append((a, max(b, a + 0.4), t))
    return out


def _doc_am_thanh(p: Path):
    """Dùng ffmpeg đóng gói sẵn tách âm thanh 16kHz mono -> mảng số (không phụ thuộc thư viện PyAV)."""
    import subprocess

    import numpy as np

    from .common import ffmpeg_exe

    r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-nostdin", "-loglevel", "error", "-i", str(p), "-vn",
                        "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        raise LoiNguoiDung(f"Không đọc được âm thanh trong '{p.name}'. File có tiếng không?")
    return np.frombuffer(r.stdout, np.int16).astype(np.float32) / 32768.0


def nghe_thanh_chu(p: Path, ngon_ngu: str | None, muc: str, toi_da_ky_tu: int):
    try:
        from faster_whisper import WhisperModel
    except Exception as e:
        raise LoiNguoiDung(f"Chưa cài xong bộ nhận giọng nói ({e}). Hãy chạy lại CAI-DAT.bat.")
    ten = MO_HINH.get(muc, muc)
    bao(f"⏳ Đang nạp mô hình nghe giọng nói '{ten}' (lần đầu phải tải về, có thể mất vài phút)...")
    model = WhisperModel(ten, device="cpu", compute_type="int8")
    bao("⏳ Đang nghe và chép lời (video 1 phút mất khoảng 20-60 giây)...")
    segments, info = model.transcribe(_doc_am_thanh(p), language=ngon_ngu, vad_filter=True, word_timestamps=True,
                                      beam_size=5)
    words = [w for s in segments for w in (s.words or [])]
    if not words:
        raise LoiNguoiDung("Không nghe thấy giọng nói nào trong file này.")
    return _gom_cau(words, toi_da_ky_tu), info.language


KIEU = {
    # ASS: màu dạng &HAABBGGRR
    "tiktok": "Bold=1,PrimaryColour=&H0000E5FF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0",
    "don-gian": "Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1",
    "hop-den": "Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H90000000,BackColour=&H90000000,BorderStyle=3,Outline=5,Shadow=0",
    "trang-den": "Bold=1,PrimaryColour=&H00000000,OutlineColour=&H00FFFFFF,BorderStyle=1,Outline=3,Shadow=0",
}


def dot_phu_de(video: Path, srt: Path, kieu: str, vi_tri: str, co: str, in_hoa: bool) -> Path:
    info = doc_thong_tin(video)
    doc = info.cao > info.rong
    size = {"nho": 0.8, "vua": 1.0, "lon": 1.25}[co] * (15 if doc else 22)
    align = {"duoi": 2, "giua": 5, "tren": 8}[vi_tri]
    margin = (70 if doc else 18) if vi_tri == "duoi" else (40 if vi_tri == "tren" else 0)
    style = f"FontName={FONT_TEN},FontSize={size:.0f},{KIEU[kieu]},Alignment={align},MarginV={margin},MarginL=20,MarginR=20"
    # Đường dẫn trong filter ffmpeg rất dễ lỗi trên Windows (ổ C:, dấu cách, tiếng Việt)
    # -> chép phụ đề + font sang thư mục tạm tên đơn giản và chạy ffmpeg ngay tại đó.
    td = Path(tempfile.mkdtemp(prefix="studio_sub_"))
    try:
        cues = _doc_srt(srt)
        if in_hoa:
            cues = [(a, b, t.upper()) for a, b, t in cues]
        _ghi_srt(cues, td / "sub.srt")
        shutil.copytree(FONTS, td / "fonts", ignore=shutil.ignore_patterns("*.txt"))
        out = file_ra(video, "phu-de", ".mp4")
        maps = ["-map", "0:v"] + (["-map", "0:a"] if info.co_tieng else [])
        chay_ffmpeg(["-i", str(video), "-vf", f"subtitles=sub.srt:fontsdir=fonts:force_style='{style}'", *maps,
                     "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                     "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)],
                    cwd=td, mo_ta="Đốt phụ đề vào video")
        return out
    finally:
        shutil.rmtree(td, ignore_errors=True)


def lenh_phu_de(a) -> None:
    p = tim_file(a.video, VIDEO_EXT | AM_THANH_EXT)
    info = doc_thong_tin(p)
    doc = info.cao > info.rong
    toi_da = a.toi_da_ky_tu or (26 if doc else 42)
    cues, lang = nghe_thanh_chu(p, None if a.ngon_ngu == "tu-dong" else a.ngon_ngu, a.mo_hinh, toi_da)
    srt = file_ra(p, "phu-de", ".srt")
    _ghi_srt(cues, srt)
    txt = srt.with_suffix(".txt")
    txt.write_text(" ".join(t for _, _, t in cues), encoding="utf-8")
    bao(f"✅ Đã chép lời {len(cues)} câu (ngôn ngữ: {lang}).")
    outs = [srt, txt]
    if a.dot_vao and info.co_hinh:
        outs.append(dot_phu_de(p, srt, a.kieu, a.vi_tri, a.co, a.in_hoa))
    ket_qua(outs, so_cau=len(cues), ngon_ngu=lang)


def lenh_dot_phu_de(a) -> None:
    v = tim_file(a.video, VIDEO_EXT)
    s = tim_file(a.srt, {".srt"})
    ket_qua(dot_phu_de(v, s, a.kieu, a.vi_tri, a.co, a.in_hoa))
