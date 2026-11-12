"""Xử lý video bằng ffmpeg đóng gói sẵn: cắt, ghép, đổi khung, nén, nhạc nền, logo, chữ, GIF, ảnh -> video."""
from __future__ import annotations

import random
import shutil
import tempfile
from pathlib import Path

from PIL import Image

from .common import (ANH_EXT, AM_THANH_EXT, VIDEO_EXT, LoiNguoiDung, bao, chay_ffmpeg, dinh_dang_tg, doc_thong_tin,
                     file_ra, kich_thuoc_ti_le, ket_qua, liet_ke, mau_rgb, thoi_gian, tim_file)
from .image import mo_anh, toa_do, ve_khoi_chu

MA_HOA = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
          "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart"]


def chan(x: float) -> int:
    x = int(round(x))
    return x - (x % 2)


def loc_khung(w: int, h: int, kieu: str, vao: str = "0:v", ra: str = "v") -> str:
    """Chuỗi filter đưa hình về đúng khung w x h."""
    if kieu == "cat":
        return f"[{vao}]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1[{ra}]"
    if kieu == "vua":
        return (f"[{vao}]scale={w}:{h}:force_original_aspect_ratio=decrease,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1[{ra}]")
    if kieu == "nen-mo":
        return (f"[{vao}]split[{ra}a][{ra}b];"
                f"[{ra}a]scale={w // 4}:{h // 4}:force_original_aspect_ratio=increase,crop={w // 4}:{h // 4},"
                f"boxblur=10:2,scale={w}:{h},eq=brightness=-0.06[{ra}bg];"
                f"[{ra}b]scale={w}:{h}:force_original_aspect_ratio=decrease[{ra}fg];"
                f"[{ra}bg][{ra}fg]overlay=(W-w)/2:(H-h)/2,setsar=1[{ra}]")
    raise LoiNguoiDung("Kiểu khung chỉ có: cat (lấp đầy, cắt bớt mép), vua (giữ trọn, viền đen), nen-mo (giữ trọn, nền mờ)")


def _video(duong_dan: str) -> Path:
    return tim_file(duong_dan, VIDEO_EXT)


# ---------------------------------------------------------------- thông tin
def lenh_thong_tin(a) -> None:
    from .image import thong_tin_anh

    p = tim_file(a.file)
    if p.is_dir():
        files = sorted(f for f in p.iterdir() if f.is_file() and not f.name.startswith("."))
    else:
        files = [p]
    for f in files:
        ext = f.suffix.lower()
        if ext in ANH_EXT:
            t = thong_tin_anh(f)
            bao(f"🖼️  {f.name}: ảnh {t['rong']}x{t['cao']}, {t['dung_luong_mb']} MB"
                + (", nền trong suốt" if t["trong_suot"] else ""))
        elif ext in VIDEO_EXT | AM_THANH_EXT:
            i = doc_thong_tin(f)
            if i.co_hinh:
                bao(f"🎬 {f.name}: video {i.rong}x{i.cao} ({i.ti_le}), dài {dinh_dang_tg(i.thoi_luong)}, "
                    f"{i.fps:g} fps, {'có' if i.co_tieng else 'KHÔNG có'} tiếng, {i.dung_luong_mb} MB")
            else:
                bao(f"🎵 {f.name}: âm thanh, dài {dinh_dang_tg(i.thoi_luong)}, {i.dung_luong_mb} MB")
        else:
            bao(f"📄 {f.name}")


# ---------------------------------------------------------------- cắt / ghép
def lenh_cat(a) -> None:
    p = _video(a.video)
    info = doc_thong_tin(p)
    bd = thoi_gian(a.tu) or 0.0
    kt = thoi_gian(a.den) or info.thoi_luong
    if a.dai:
        kt = bd + thoi_gian(a.dai)
    if kt <= bd:
        raise LoiNguoiDung("Mốc kết thúc phải sau mốc bắt đầu.")
    if bd >= info.thoi_luong:
        raise LoiNguoiDung(f"Video chỉ dài {dinh_dang_tg(info.thoi_luong)}, không cắt từ {dinh_dang_tg(bd)} được.")
    kt = min(kt, info.thoi_luong)
    out = file_ra(p, f"cat-{int(bd)}s-{int(kt)}s", ".mp4")
    chay_ffmpeg(["-ss", f"{bd:.3f}", "-i", str(p), "-t", f"{kt - bd:.3f}", *MA_HOA, str(out)],
                mo_ta=f"Cắt đoạn {dinh_dang_tg(bd)} → {dinh_dang_tg(kt)}")
    ket_qua(out, thoi_luong=round(kt - bd, 1))


def lenh_ghep(a) -> None:
    files: list[Path] = []
    for x in a.video:
        files += liet_ke(x, VIDEO_EXT)
    if len(files) < 2:
        raise LoiNguoiDung("Cần ít nhất 2 video để ghép (hoặc 1 thư mục chứa nhiều video).")
    infos = [doc_thong_tin(f) for f in files]
    if a.ti_le:
        w, h = kich_thuoc_ti_le(a.ti_le)
    else:
        w, h = chan(infos[0].rong), chan(infos[0].cao)
    args: list[str] = []
    for f in files:
        args += ["-i", str(f)]
    loc, chuoi = [], ""
    so_vao = len(files)
    for i, inf in enumerate(infos):
        loc.append(loc_khung(w, h, a.kieu, f"{i}:v", f"k{i}").replace(f"[k{i}]", f",fps=30,format=yuv420p[v{i}]"))
        if inf.co_tieng:
            loc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}]")
        else:
            args += ["-f", "lavfi", "-t", f"{inf.thoi_luong:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
            loc.append(f"[{so_vao}:a]anull[a{i}]")
            so_vao += 1
        chuoi += f"[v{i}][a{i}]"
    loc.append(f"{chuoi}concat=n={len(files)}:v=1:a=1[v][a]")
    out = file_ra(files[0], f"ghep-{len(files)}-video", ".mp4")
    chay_ffmpeg([*args, "-filter_complex", ";".join(loc), "-map", "[v]", "-map", "[a]", *MA_HOA, str(out)],
                mo_ta=f"Ghép {len(files)} video thành {w}x{h}")
    ket_qua(out, so_video=len(files), kich_thuoc=f"{w}x{h}")


def lenh_khung(a) -> None:
    p = _video(a.video)
    w, h = kich_thuoc_ti_le(a.ti_le)
    out = file_ra(p, f"khung-{a.ti_le.replace(':', 'x')}", ".mp4")
    info = doc_thong_tin(p)
    maps = ["-map", "[v]"] + (["-map", "0:a"] if info.co_tieng else [])
    chay_ffmpeg(["-i", str(p), "-filter_complex", loc_khung(w, h, a.kieu), *maps, *MA_HOA, str(out)],
                mo_ta=f"Đổi khung sang {a.ti_le} ({w}x{h}), kiểu {a.kieu}")
    ket_qua(out, kich_thuoc=f"{w}x{h}")


# ---------------------------------------------------------------- nén / tốc độ / âm thanh
def lenh_nen(a) -> None:
    p = _video(a.video)
    info = doc_thong_tin(p)
    vf = []
    if a.toi_da and min(info.rong, info.cao) > a.toi_da:
        vf.append(f"scale='if(gt(iw,ih),-2,{a.toi_da})':'if(gt(iw,ih),{a.toi_da},-2)'")
    args = ["-i", str(p)]
    if vf:
        args += ["-vf", ",".join(vf)]
    if a.toi_da_mb:
        kbps = int((a.toi_da_mb * 8 * 1024 * 0.93) / max(1.0, info.thoi_luong)) - 128
        if kbps < 150:
            raise LoiNguoiDung(f"Video dài {dinh_dang_tg(info.thoi_luong)} không thể nén xuống {a.toi_da_mb}MB "
                               "mà vẫn xem được. Hãy cắt ngắn hoặc tăng giới hạn dung lượng.")
        args += ["-c:v", "libx264", "-preset", "medium", "-b:v", f"{kbps}k", "-maxrate", f"{int(kbps * 1.3)}k",
                 "-bufsize", f"{kbps * 2}k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                 "-movflags", "+faststart"]
    else:
        crf = {"nhe": "23", "vua": "26", "manh": "30"}[a.muc]
        args += ["-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart"]
    out = file_ra(p, "nen", ".mp4")
    chay_ffmpeg([*args, str(out)], mo_ta="Nén video")
    sau = out.stat().st_size / 1048576
    bao(f"✅ {info.dung_luong_mb} MB → {sau:.1f} MB")
    ket_qua(out, truoc_mb=info.dung_luong_mb, sau_mb=round(sau, 1))


def _atempo(he_so: float) -> str:
    parts, x = [], he_so
    while x > 2.0:
        parts.append("atempo=2.0")
        x /= 2.0
    while x < 0.5:
        parts.append("atempo=0.5")
        x /= 0.5
    parts.append(f"atempo={x:.4f}")
    return ",".join(parts)


def lenh_toc_do(a) -> None:
    p = _video(a.video)
    if not 0.25 <= a.he_so <= 4:
        raise LoiNguoiDung("Hệ số tốc độ nên trong khoảng 0.25 (chậm 4 lần) đến 4 (nhanh 4 lần).")
    info = doc_thong_tin(p)
    loc = f"[0:v]setpts=PTS/{a.he_so}[v]" + (f";[0:a]{_atempo(a.he_so)}[a]" if info.co_tieng else "")
    maps = ["-map", "[v]"] + (["-map", "[a]"] if info.co_tieng else [])
    out = file_ra(p, f"toc-do-x{a.he_so:g}", ".mp4")
    chay_ffmpeg(["-i", str(p), "-filter_complex", loc, *maps, *MA_HOA, str(out)], mo_ta=f"Đổi tốc độ x{a.he_so:g}")
    ket_qua(out)


def lenh_nhac(a) -> None:
    p = _video(a.video)
    nhac = tim_file(a.nhac, AM_THANH_EXT | VIDEO_EXT)
    info = doc_thong_tin(p)
    D = info.thoi_luong
    fade = min(2.0, D / 4)
    loc = [f"[1:a]volume={a.am_luong},atrim=0:{D:.3f},afade=t=in:d=0.5,afade=t=out:st={D - fade:.3f}:d={fade:.3f}[m]"]
    if info.co_tieng and not a.bo_tieng_goc:
        if a.khong_giam_nhac:
            loc.append("[0:a][m]amix=inputs=2:duration=first:normalize=0[a]")
        else:  # tự giảm nhạc khi có người nói
            loc.append("[0:a]asplit[goc][sc]")
            loc.append("[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[md]")
            loc.append("[goc][md]amix=inputs=2:duration=first:normalize=0[a]")
    else:
        loc.append("[m]anull[a]")
    out = file_ra(p, "nhac-nen", ".mp4")
    chay_ffmpeg(["-i", str(p), "-stream_loop", "-1", "-i", str(nhac), "-filter_complex", ";".join(loc),
                 "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{D:.3f}",
                 "-movflags", "+faststart", str(out)], mo_ta="Chèn nhạc nền")
    ket_qua(out)


def lenh_chuan_am(a) -> None:
    p = _video(a.video)
    out = file_ra(p, "chuan-am", ".mp4")
    chay_ffmpeg(["-i", str(p), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                 "-movflags", "+faststart", str(out)], mo_ta="Cân bằng âm lượng chuẩn mạng xã hội (-14 LUFS)")
    ket_qua(out)


def lenh_tat_tieng(a) -> None:
    p = _video(a.video)
    out = file_ra(p, "tat-tieng", ".mp4")
    chay_ffmpeg(["-i", str(p), "-an", "-c:v", "copy", "-movflags", "+faststart", str(out)], mo_ta="Bỏ âm thanh")
    ket_qua(out)


def lenh_tach_am(a) -> None:
    p = _video(a.video)
    ext = "." + a.dinh_dang
    codec = {".mp3": ["-c:a", "libmp3lame", "-q:a", "2"], ".wav": ["-c:a", "pcm_s16le"],
             ".m4a": ["-c:a", "aac", "-b:a", "192k"]}[ext]
    out = file_ra(p, "am-thanh", ext)
    chay_ffmpeg(["-i", str(p), "-vn", *codec, str(out)], mo_ta="Tách âm thanh")
    ket_qua(out)


def lenh_xoay(a) -> None:
    p = _video(a.video)
    vf = {"phai": "transpose=1", "trai": "transpose=2", "180": "transpose=1,transpose=1", "lat-ngang": "hflip",
          "lat-doc": "vflip"}[a.huong]
    out = file_ra(p, f"xoay-{a.huong}", ".mp4")
    chay_ffmpeg(["-i", str(p), "-vf", vf, *MA_HOA, str(out)], mo_ta="Xoay video")
    ket_qua(out)


# ---------------------------------------------------------------- logo / chữ
def lenh_logo(a) -> None:
    logo = tim_file(a.logo, ANH_EXT)
    p = tim_file(a.file)
    if p.is_dir() or p.suffix.lower() in ANH_EXT:
        from .image import lenh_logo_anh

        outs = lenh_logo_anh(liet_ke(a.file, ANH_EXT), logo, a.vi_tri, a.ti_le, a.do_mo)
        ket_qua(outs, so_anh=len(outs))
        return
    info = doc_thong_tin(_video(a.file))
    lg = mo_anh(logo)
    lw = chan(info.rong * a.ti_le)
    lh = chan(lg.height * lw / lg.width)
    x, y = toa_do(info.rong, info.cao, lw, lh, a.vi_tri, int(min(info.rong, info.cao) * 0.03))
    loc = f"[1:v]scale={lw}:{lh},format=rgba,colorchannelmixer=aa={a.do_mo}[lg];[0:v][lg]overlay={x}:{y}[v]"
    maps = ["-map", "[v]"] + (["-map", "0:a"] if info.co_tieng else [])
    out = file_ra(p, "logo", ".mp4")
    chay_ffmpeg(["-i", str(p), "-i", str(logo), "-filter_complex", loc, *maps, *MA_HOA, str(out)], mo_ta="Chèn logo")
    ket_qua(out)


def _anh_chu_tam(text: str, rong: int, cao: int, a, thu_muc: Path, ten: str) -> Path:
    co = a.co_chu or max(24, int(min(rong, cao) * {"nho": 0.045, "vua": 0.065, "lon": 0.09}[a.co]))
    nen = (*mau_rgb(a.mau_nen), int(255 * a.do_mo_nen)) if a.mau_nen else None
    lop = ve_khoi_chu(text, int(rong * 0.88), co, mau_rgb(a.mau), mau_rgb(a.mau_vien), nen=nen)
    out = thu_muc / ten
    lop.save(out)
    return out


def lenh_chu(a) -> None:
    p = _video(a.video)
    info = doc_thong_tin(p)
    with tempfile.TemporaryDirectory() as td:
        png = _anh_chu_tam(a.noi_dung, info.rong, info.cao, a, Path(td), "chu.png")
        lw, lh = Image.open(png).size
        x, y = toa_do(info.rong, info.cao, lw, lh, a.vi_tri, int(min(info.rong, info.cao) * 0.06))
        bd = thoi_gian(a.tu) or 0.0
        kt = thoi_gian(a.den) or info.thoi_luong
        loc = f"[0:v][1:v]overlay={x}:{y}:enable='between(t,{bd:.3f},{kt:.3f})'[v]"
        maps = ["-map", "[v]"] + (["-map", "0:a"] if info.co_tieng else [])
        out = file_ra(p, "chu", ".mp4")
        chay_ffmpeg(["-i", str(p), "-i", str(png), "-filter_complex", loc, *maps, *MA_HOA, str(out)],
                    mo_ta="Chèn chữ vào video")
    ket_qua(out)


# ---------------------------------------------------------------- xem nhanh / GIF
def lenh_khung_hinh(a) -> None:
    """Trích N khung hình đều nhau + 1 ảnh tổng hợp có mốc thời gian (để Claude 'xem' video)."""
    from PIL import ImageDraw

    from .image import _font

    p = _video(a.video)
    info = doc_thong_tin(p)
    n = max(1, min(a.so, 60))
    D = info.thoi_luong
    moc = [D * (i + 0.5) / n for i in range(n)]
    if a.kiem_tra:  # ảnh để Claude tự kiểm tra -> để trong .cache, không làm rối thư mục kết quả
        from .common import CACHE, ten_an_toan

        out_dir = CACHE / "kiem-tra" / ten_an_toan(p.stem)
        shutil.rmtree(out_dir, ignore_errors=True)
    else:
        out_dir = file_ra(p, "khung-hinh", "").with_suffix("")
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    bao(f"⏳ Đang trích {n} khung hình...")
    for t in moc:
        f = out_dir / f"{int(t // 60):02d}m{t % 60:04.1f}s.jpg".replace(".", "_", 1)
        chay_ffmpeg(["-ss", f"{t:.3f}", "-i", str(p), "-frames:v", "1", "-vf", "scale=640:-2", "-q:v", "3", str(f)])
        if f.exists():
            frames.append((t, f))
    if not frames:
        raise RuntimeError("Không trích được khung hình nào.")
    th = Image.open(frames[0][1])
    tw, thh = 320, int(320 * th.height / th.width)
    cot = 4 if thh < tw else 6
    hang = (len(frames) + cot - 1) // cot
    sheet = Image.new("RGB", (cot * tw, hang * (thh + 28)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    font = _font(18, "dam")
    for i, (t, f) in enumerate(frames):
        r, c = divmod(i, cot)
        im = Image.open(f).convert("RGB").resize((tw, thh))
        sheet.paste(im, (c * tw, r * (thh + 28) + 28))
        d.text((c * tw + 6, r * (thh + 28) + 4), dinh_dang_tg(t), font=font, fill=(255, 214, 0))
    tong = out_dir / "_TONG-HOP.jpg"
    sheet.save(tong, quality=85)
    ket_qua(tong, thu_muc_khung=str(out_dir), so_khung=len(frames))


def lenh_gif(a) -> None:
    p = _video(a.video)
    bd = thoi_gian(a.tu) or 0.0
    info = doc_thong_tin(p)
    kt = thoi_gian(a.den) or min(info.thoi_luong, bd + 6)
    out = file_ra(p, "gif", ".gif")
    loc = (f"fps={a.fps},scale={a.rong}:-1:flags=lanczos,split[x][y];[x]palettegen=stats_mode=diff[p];"
           f"[y][p]paletteuse=dither=bayer:bayer_scale=4")
    chay_ffmpeg(["-ss", f"{bd:.3f}", "-t", f"{kt - bd:.3f}", "-i", str(p), "-filter_complex", loc, "-loop", "0",
                 str(out)], mo_ta="Tạo ảnh GIF")
    ket_qua(out, dung_luong_mb=round(out.stat().st_size / 1048576, 2))


# ---------------------------------------------------------------- ảnh -> video
CHUYEN_CANH = ["fade", "slideleft", "slideup", "circleopen", "smoothleft", "dissolve", "wipeleft", "radial"]


def lenh_anh_thanh_video(a) -> None:
    files: list[Path] = []
    for x in a.anh:
        files += liet_ke(x, ANH_EXT)
    if not files:
        raise LoiNguoiDung("Chưa có ảnh nào.")
    w, h = kich_thuoc_ti_le(a.ti_le)
    D = float(a.giay_moi_anh)
    T = min(0.6, D / 3) if len(files) > 1 else 0.0
    n = len(files)
    chu_ds = [c.strip() for c in a.chu.split("|")] if a.chu else []
    td = Path(tempfile.mkdtemp(prefix="studio_"))
    try:
        args, loc = [], []
        # chuẩn hóa ảnh (HEIC, xoay EXIF...) sang PNG tạm để ffmpeg đọc chắc chắn
        for i, f in enumerate(files):
            tmp = td / f"anh{i:03d}.png"
            mo_anh(f).convert("RGB").save(tmp)
            args += ["-loop", "1", "-framerate", "30", "-t", f"{D + T:.3f}", "-i", str(tmp)]
        so_vao = n
        W2, H2 = chan(w * 1.5), chan(h * 1.5)
        frames = int((D + T) * 30)
        for i in range(n):
            loc.append(loc_khung(W2, H2, a.kieu, f"{i}:v", f"k{i}"))
            if a.hieu_ung == "zoom":
                z = (f"min(1+0.10*on/{frames},1.10)" if i % 2 == 0 else f"max(1.10-0.10*on/{frames},1)")
                zp = (f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps=30")
            else:
                zp = f"scale={w}:{h},fps=30"
            nhan = f"z{i}" if i < len(chu_ds) and chu_ds[i] else f"s{i}"
            loc.append(f"[k{i}]{zp},trim=duration={D + T:.3f},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[{nhan}]")
            if nhan.startswith("z"):
                png = _anh_chu_tam(chu_ds[i], w, h, a, td, f"chu{i}.png")
                lw, lh = Image.open(png).size
                x, y = toa_do(w, h, lw, lh, a.vi_tri, int(min(w, h) * 0.08))
                args += ["-i", str(png)]
                loc.append(f"[z{i}][{so_vao}:v]overlay={x}:{y},format=yuv420p[s{i}]")
                so_vao += 1
        # nối bằng hiệu ứng chuyển cảnh
        if n == 1:
            loc.append("[s0]null[v]")
        else:
            truoc, offset = "s0", 0.0
            for i in range(1, n):
                offset += D
                kieu = a.chuyen_canh if a.chuyen_canh != "ngau-nhien" else random.choice(CHUYEN_CANH)
                ra = "v" if i == n - 1 else f"x{i}"
                # mỗi clip dài D+T; sau i lần nối, đoạn đã có dài i*D + T -> chuyển cảnh bắt đầu ở i*D
                loc.append(f"[{truoc}][s{i}]xfade=transition={kieu}:duration={T:.3f}:offset={offset:.3f}[{ra}]")
                truoc = ra
        tong = n * D + T
        maps = ["-map", "[v]"]
        if a.nhac:
            nhac = tim_file(a.nhac, AM_THANH_EXT | VIDEO_EXT)
            args += ["-stream_loop", "-1", "-i", str(nhac)]
            loc.append(f"[{so_vao}:a]atrim=0:{tong:.3f},afade=t=out:st={max(0, tong - 2):.3f}:d=2,volume={a.am_luong}[a]")
            maps += ["-map", "[a]"]
        out = file_ra(files[0], f"video-tu-{n}-anh", ".mp4")
        chay_ffmpeg([*args, "-filter_complex", ";".join(loc), *maps, "-t", f"{tong:.3f}", *MA_HOA, str(out)],
                    mo_ta=f"Dựng video {w}x{h} từ {n} ảnh (~{tong:.0f} giây, có thể mất 1-3 phút)")
        ket_qua(out, so_anh=n, thoi_luong=round(tong, 1))
    finally:
        shutil.rmtree(td, ignore_errors=True)
