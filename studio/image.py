"""Xử lý ảnh: đổi cỡ theo kênh, xóa nền, chèn chữ/logo, nén, ghép ảnh."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from .common import (ANH_EXT, FONT_DAM, FONT_RAT_DAM, FONT_THUONG, LoiNguoiDung, bao, file_ra, ket_qua, liet_ke,
                     mau_rgb, tim_file)

try:  # đọc được ảnh HEIC từ iPhone
    import pillow_heif

    pillow_heif.register_heif_opener()
except Exception:  # pragma: no cover
    pass

# Kích thước chuẩn theo kênh (rộng x cao)
KENH = {
    "facebook-post": (1080, 1350), "facebook-vuong": (1080, 1080), "facebook-cover": (1640, 624),
    "facebook-ads": (1080, 1080), "instagram-post": (1080, 1350), "instagram-vuong": (1080, 1080),
    "story": (1080, 1920), "reels": (1080, 1920), "tiktok": (1080, 1920), "zalo-story": (1080, 1920),
    "youtube-thumbnail": (1280, 720), "youtube-banner": (2560, 1440), "youtube-shorts": (1080, 1920),
    "shopee": (1024, 1024), "lazada": (1024, 1024), "tiktok-shop": (1024, 1024),
    "zalo-oa": (1280, 720), "linkedin": (1200, 627), "banner-web": (1920, 600), "avatar": (800, 800),
    "a4-doc": (2480, 3508), "a4-ngang": (3508, 2480),
}
KENH_ALIAS = {"thumbnail": "youtube-thumbnail", "thumb": "youtube-thumbnail", "fb": "facebook-post",
              "ig": "instagram-post", "san-pham": "shopee", "san-pham-tmdt": "shopee", "zalo": "zalo-oa"}


def mo_anh(p: Path) -> Image.Image:
    try:
        im = Image.open(p)
        im = ImageOps.exif_transpose(im)  # xoay đúng chiều ảnh điện thoại
        return im
    except Exception as e:
        raise LoiNguoiDung(f"Không mở được ảnh '{p.name}': {e}")


def luu_anh(im: Image.Image, out: Path, chat_luong: int = 92) -> Path:
    ext = out.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        if im.mode in ("RGBA", "LA", "P"):
            nen = Image.new("RGB", im.size, (255, 255, 255))
            im2 = im.convert("RGBA")
            nen.paste(im2, mask=im2.split()[-1])
            im = nen
        im.convert("RGB").save(out, quality=chat_luong, optimize=True, progressive=True)
    elif ext == ".webp":
        im.save(out, quality=chat_luong, method=6)
    else:
        im.save(out, optimize=True)
    return out


def _ext_ra(goc: Path, ep: str | None = None, can_trong_suot: bool = False) -> str:
    if ep:
        return "." + ep.lower().lstrip(".").replace("jpeg", "jpg")
    if can_trong_suot:
        return ".png"
    return ".jpg" if goc.suffix.lower() in (".heic", ".heif", ".bmp", ".tif", ".tiff") else goc.suffix.lower()


def phong(im: Image.Image, w: int, h: int, kieu: str, mau_nen=(255, 255, 255)) -> Image.Image:
    """Đưa ảnh về đúng khung w x h. kieu: cat (lấp đầy, cắt bớt) | vua (giữ trọn, thêm nền) | nen-mo (giữ trọn, nền mờ)."""
    im = im.convert("RGBA")
    if kieu == "cat":
        return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.45))
    fg = ImageOps.contain(im, (w, h), Image.LANCZOS)
    if kieu == "nen-mo":
        bg = ImageOps.fit(im, (w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(max(w, h) // 30))
        toi = Image.new("RGBA", (w, h), (0, 0, 0, 70))
        bg = Image.alpha_composite(bg, toi)
    else:
        bg = Image.new("RGBA", (w, h), (*mau_nen, 255))
    bg.alpha_composite(fg, ((w - fg.width) // 2, (h - fg.height) // 2))
    return bg


# ---------------------------------------------------------------- chữ
def _font(size: int, dam: str = "dam") -> ImageFont.FreeTypeFont:
    f = {"thuong": FONT_THUONG, "dam": FONT_DAM, "rat-dam": FONT_RAT_DAM}.get(dam, FONT_DAM)
    return ImageFont.truetype(str(f), size)


def _ngat_dong(draw: ImageDraw.ImageDraw, text: str, font, rong_toi_da: int) -> list[str]:
    dong_ra: list[str] = []
    for doan in text.split("\n"):
        tu = doan.split()
        if not tu:
            dong_ra.append("")
            continue
        cur = tu[0]
        for t in tu[1:]:
            thu = f"{cur} {t}"
            if draw.textlength(thu, font=font) <= rong_toi_da:
                cur = thu
            else:
                dong_ra.append(cur)
                cur = t
        dong_ra.append(cur)
    return dong_ra


def ve_khoi_chu(text: str, rong_toi_da: int, co_chu: int, mau=(255, 255, 255), vien=(0, 0, 0),
                do_day_vien: int | None = None, nen: tuple | None = None, dam: str = "rat-dam",
                can: str = "giua") -> Image.Image:
    """Tạo ảnh trong suốt chứa khối chữ tiếng Việt (tự xuống dòng, có viền/nền)."""
    font = _font(co_chu, dam)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    pad = int(co_chu * 0.45) if nen else 0
    lines = _ngat_dong(tmp, text, font, rong_toi_da - 2 * pad)
    vien_px = do_day_vien if do_day_vien is not None else (0 if nen else max(2, co_chu // 14))
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * 1.12)
    w = max(int(tmp.textlength(l, font=font)) for l in lines) + 2 * pad + 2 * vien_px
    h = lh * len(lines) + 2 * pad + 2 * vien_px
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if nen:
        r = int(co_chu * 0.35)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=nen)
    for i, line in enumerate(lines):
        lw = d.textlength(line, font=font)
        x = {"trai": pad + vien_px, "phai": w - pad - vien_px - lw}.get(can, (w - lw) / 2)
        y = pad + vien_px + i * lh
        d.text((x, y), line, font=font, fill=(*mau, 255), stroke_width=vien_px,
               stroke_fill=(*vien, 255) if vien_px else None)
    return im


VI_TRI = ["tren", "giua", "duoi", "trai", "phai", "tren-trai", "tren-phai", "duoi-trai", "duoi-phai"]


def toa_do(W: int, H: int, w: int, h: int, vi_tri: str, le: int) -> tuple[int, int]:
    parts = vi_tri.lower().split("-")
    if vi_tri not in VI_TRI:
        raise LoiNguoiDung(f"Vị trí '{vi_tri}' không hợp lệ. Chọn: {', '.join(VI_TRI)}")
    ngang = next((p for p in parts if p in ("trai", "phai")), "giua")
    doc = next((p for p in parts if p in ("tren", "duoi")), "giua")
    x = {"trai": le, "phai": W - w - le}.get(ngang, (W - w) // 2)
    y = {"tren": le, "duoi": H - h - le}.get(doc, (H - h) // 2)
    return max(0, x), max(0, y)


def dat_vao(nen: Image.Image, lop: Image.Image, vi_tri: str, le: int) -> Image.Image:
    """vi_tri: tren, giua, duoi, trai, phai, tren-trai, tren-phai, duoi-trai, duoi-phai."""
    W, H = nen.size
    w, h = lop.size
    x, y = toa_do(W, H, w, h, vi_tri, le)
    out = nen.convert("RGBA")
    out.alpha_composite(lop, (max(0, x), max(0, y)))
    return out


# ---------------------------------------------------------------- lệnh
def lenh_doi_co(a) -> None:
    files = liet_ke(a.anh, ANH_EXT)
    if a.kenh:
        k = KENH_ALIAS.get(a.kenh, a.kenh)
        if k not in KENH:
            raise LoiNguoiDung("Kênh chưa có. Các kênh hỗ trợ: " + ", ".join(sorted(KENH)))
        w, h = KENH[k]
        nhan = k
    elif a.kich_thuoc:
        try:
            w, h = (int(x) for x in a.kich_thuoc.lower().replace("*", "x").split("x"))
        except ValueError:
            raise LoiNguoiDung("Kích thước ghi dạng RỘNGxCAO, ví dụ 1080x1350")
        nhan = f"{w}x{h}"
    else:
        raise LoiNguoiDung("Cần chọn --kenh (ví dụ shopee, tiktok, youtube-thumbnail) hoặc --kich-thuoc 1080x1350")
    outs = []
    for f in files:
        im = phong(mo_anh(f), w, h, a.kieu, mau_rgb(a.mau_nen))
        out = file_ra(f, nhan, _ext_ra(f, a.dinh_dang))
        outs.append(luu_anh(im, out))
        bao(f"✅ {f.name} -> {w}x{h}")
    ket_qua(outs, kich_thuoc=f"{w}x{h}", so_anh=len(outs))


def lenh_xoa_nen(a) -> None:
    files = liet_ke(a.anh, ANH_EXT)
    bao("⏳ Đang xóa nền (lần đầu sẽ chậm hơn vì cần nạp mô hình AI)...")
    try:
        from rembg import new_session, remove
    except Exception as e:
        raise LoiNguoiDung(f"Chưa cài xong bộ xóa nền ({e}). Hãy chạy lại CAI-DAT.bat.")
    session = new_session(a.mo_hinh)
    outs = []
    for f in files:
        im = mo_anh(f).convert("RGBA")
        cut = remove(im, session=session, post_process_mask=True)
        if a.cat_sat:
            bbox = cut.getbbox()
            if bbox:
                cut = cut.crop(bbox)
        if a.nen:
            if a.nen in ("mo", "nen-mo"):
                bg = mo_anh(f).convert("RGBA").resize(cut.size).filter(ImageFilter.GaussianBlur(25))
            else:
                bg = Image.new("RGBA", cut.size, (*mau_rgb(a.nen), 255))
            bg.alpha_composite(cut)
            cut = bg
        out = file_ra(f, "xoa-nen", ".png")
        outs.append(luu_anh(cut, out))
        bao(f"✅ {f.name}")
    ket_qua(outs, so_anh=len(outs))


def lenh_chu_anh(a) -> None:
    files = liet_ke(a.anh, ANH_EXT)
    outs = []
    for f in files:
        im = mo_anh(f).convert("RGBA")
        W, H = im.size
        co = a.co_chu or max(18, int(min(W, H) * {"nho": 0.045, "vua": 0.07, "lon": 0.1}[a.co]))
        nen = (*mau_rgb(a.mau_nen), int(255 * a.do_mo_nen)) if a.mau_nen else None
        lop = ve_khoi_chu(a.noi_dung, int(W * 0.9), co, mau_rgb(a.mau), mau_rgb(a.mau_vien), nen=nen)
        out_im = dat_vao(im, lop, a.vi_tri, int(min(W, H) * 0.05))
        out = file_ra(f, "chu", _ext_ra(f, a.dinh_dang))
        outs.append(luu_anh(out_im, out))
    ket_qua(outs, so_anh=len(outs))


def lenh_logo_anh(files: list[Path], logo: Path, vi_tri: str, ti_le: float, do_mo: float) -> list[Path]:
    lg = mo_anh(logo).convert("RGBA")
    outs = []
    for f in files:
        if f.resolve() == logo.resolve():
            continue  # không chèn logo vào chính file logo
        im = mo_anh(f).convert("RGBA")
        W, H = im.size
        lw = max(16, int(W * ti_le))
        l2 = lg.resize((lw, max(1, int(lg.height * lw / lg.width))), Image.LANCZOS)
        if do_mo < 1:
            alpha = l2.split()[-1].point(lambda v: int(v * do_mo))
            l2.putalpha(alpha)
        out_im = dat_vao(im, l2, vi_tri, int(min(W, H) * 0.03))
        out = file_ra(f, "logo", _ext_ra(f))
        outs.append(luu_anh(out_im, out))
    return outs


def lenh_nen_anh(a) -> None:
    files = liet_ke(a.anh, ANH_EXT)
    outs, truoc, sau = [], 0, 0
    for f in files:
        im = mo_anh(f)
        if a.rong_toi_da and max(im.size) > a.rong_toi_da:
            im.thumbnail((a.rong_toi_da, a.rong_toi_da), Image.LANCZOS)
        ext = "." + a.dinh_dang.lower().replace("jpeg", "jpg")
        if ext == ".jpg" and im.mode in ("RGBA", "LA", "P"):
            pass  # luu_anh tự xử lý nền trắng
        out = file_ra(f, "nen", ext)
        luu_anh(im, out, a.chat_luong)
        truoc += f.stat().st_size
        sau += out.stat().st_size
        outs.append(out)
    giam = 100 - (sau * 100 // max(1, truoc))

    def dl(b: int) -> str:
        return f"{b / 1048576:.1f} MB" if b >= 1048576 else f"{b / 1024:.0f} KB"

    bao(f"✅ Giảm dung lượng ~{giam}% ({dl(truoc)} → {dl(sau)})")
    ket_qua(outs, so_anh=len(outs), giam_phan_tram=giam)


def lenh_ghep_anh(a) -> None:
    files: list[Path] = []
    for x in a.anh:
        files += liet_ke(x, ANH_EXT)
    if len(files) < 2:
        raise LoiNguoiDung("Cần ít nhất 2 ảnh để ghép.")
    gap = a.khoang_cach
    nen = (*mau_rgb(a.mau_nen), 255)
    if a.kieu == "truoc-sau":
        a1, a2 = (mo_anh(p).convert("RGBA") for p in files[:2])
        h = min(a1.height, a2.height, 1600)
        a1 = a1.resize((int(a1.width * h / a1.height), h), Image.LANCZOS)
        a2 = a2.resize((int(a2.width * h / a2.height), h), Image.LANCZOS)
        out_im = Image.new("RGBA", (a1.width + a2.width + gap * 3, h + gap * 2), nen)
        out_im.alpha_composite(a1, (gap, gap))
        out_im.alpha_composite(a2, (a1.width + gap * 2, gap))
        nhan = (a.nhan or "TRƯỚC|SAU").split("|")
        co = max(20, h // 14)
        for i, (txt, x0, wd) in enumerate([(nhan[0], gap, a1.width), (nhan[-1], a1.width + gap * 2, a2.width)]):
            lop = ve_khoi_chu(txt, wd, co, (255, 255, 255), nen=(0, 0, 0, 160))
            out_im.alpha_composite(lop, (x0 + (wd - lop.width) // 2, gap + h - lop.height - co // 2))
    else:
        import math

        n = len(files)
        cot = a.so_cot or math.ceil(math.sqrt(n))
        hang = math.ceil(n / cot)
        o = a.co_o
        out_im = Image.new("RGBA", (cot * o + (cot + 1) * gap, hang * o + (hang + 1) * gap), nen)
        for i, p in enumerate(files):
            tile = ImageOps.fit(mo_anh(p).convert("RGBA"), (o, o), Image.LANCZOS)
            r, c = divmod(i, cot)
            out_im.alpha_composite(tile, (gap + c * (o + gap), gap + r * (o + gap)))
    out = file_ra(files[0], "ghep-" + a.kieu, ".jpg")
    luu_anh(out_im, out)
    ket_qua(out, so_anh=len(files))


def lenh_doi_dinh_dang(a) -> None:
    files = liet_ke(a.anh, ANH_EXT)
    ext = "." + a.sang.lower().replace("jpeg", "jpg")
    outs = [luu_anh(mo_anh(f), file_ra(f, ext.strip("."), ext)) for f in files]
    ket_qua(outs, so_anh=len(outs))


def thong_tin_anh(p: Path) -> dict:
    im = mo_anh(p)
    return {"file": p.name, "rong": im.width, "cao": im.height, "che_do": im.mode,
            "dung_luong_mb": round(p.stat().st_size / 1048576, 2), "trong_suot": im.mode in ("RGBA", "LA", "P")}
