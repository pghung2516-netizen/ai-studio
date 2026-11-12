"""Vẽ bộ icon của app: uv run python scripts/tao-icon.py
Kết quả: assets/icon/{ai-studio,dau-vao,thanh-pham}.ico + .png (256px) + ai-studio-1024.png
Đổi màu thương hiệu ở 2 dòng MAU_* bên dưới rồi chạy lại.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "icon"
MAU_1 = (91, 46, 229)    # tím  #5B2EE5
MAU_2 = (255, 107, 74)   # cam san hô #FF6B4A
VANG = (255, 209, 102)   # #FFD166
S = 1024 * 2             # vẽ gấp đôi rồi thu nhỏ cho mịn


def nen() -> Image.Image:
    """Ô vuông bo góc, chuyển màu chéo + lớp sáng phía trên."""
    y, x = np.mgrid[0:S, 0:S].astype(np.float32) / (S - 1)
    t = np.clip((x * 0.55 + y * 0.45), 0, 1)[..., None]
    rgb = (np.array(MAU_1) * (1 - t) + np.array(MAU_2) * t).astype(np.uint8)
    img = Image.fromarray(rgb, "RGB").convert("RGBA")
    # lớp sáng mềm ở nửa trên
    gloss = Image.new("L", (S, S), 0)
    ImageDraw.Draw(gloss).ellipse((-S * 0.3, -S * 0.85, S * 1.3, S * 0.4), fill=30)
    gloss = gloss.filter(ImageFilter.GaussianBlur(S * 0.1))
    img = Image.composite(Image.new("RGBA", (S, S), (255, 255, 255, 255)), img, gloss)
    mask = Image.new("L", (S, S), 0)
    m = int(S * 0.035)
    ImageDraw.Draw(mask).rounded_rectangle((m, m, S - m, S - m), radius=int(S * 0.225), fill=255)
    img.putalpha(mask)
    return img


def bong(glyph: Image.Image) -> Image.Image:
    """Bóng đổ mềm dưới hình trắng."""
    a = glyph.getchannel("A").filter(ImageFilter.GaussianBlur(S * 0.018))
    sh = Image.new("RGBA", (S, S), (40, 10, 60, 0))
    sh.putalpha(a.point(lambda v: int(v * 0.45)))
    out = Image.new("RGBA", (S, S))
    out.alpha_composite(sh, (0, int(S * 0.018)))
    out.alpha_composite(glyph)
    return out


def tam_giac(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float, fill) -> None:
    """Nút play bo tròn góc."""
    pts = [(cx - r * 0.62, cy - r), (cx - r * 0.62, cy + r), (cx + r * 1.0, cy)]
    w = int(r * 0.32)
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=fill, width=w, joint="curve")
    for px, py in pts:
        d.ellipse((px - w / 2, py - w / 2, px + w / 2, py + w / 2), fill=fill)


def ngoi_sao(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float, fill) -> None:
    """Lấp lánh 4 cánh (biểu tượng AI)."""
    import math

    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.3
        a = math.pi / 4 * i - math.pi / 2
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def icon_chinh() -> Image.Image:
    g = Image.new("RGBA", (S, S))
    d = ImageDraw.Draw(g)
    tam_giac(d, S * 0.47, S * 0.53, S * 0.25, (255, 255, 255, 255))
    ngoi_sao(d, S * 0.74, S * 0.27, S * 0.115, VANG + (255,))
    ngoi_sao(d, S * 0.84, S * 0.42, S * 0.05, (255, 255, 255, 235))
    img = nen()
    img.alpha_composite(bong(g))
    return img


def icon_dau_vao() -> Image.Image:
    """Khay + mũi tên đi xuống: chỗ bỏ file vào."""
    g = Image.new("RGBA", (S, S))
    d = ImageDraw.Draw(g)
    W = (255, 255, 255, 255)
    w = int(S * 0.07)
    # khay
    d.line([(S * 0.22, S * 0.56), (S * 0.22, S * 0.76), (S * 0.78, S * 0.76), (S * 0.78, S * 0.56)],
           fill=W, width=w, joint="curve")
    for p in [(S * 0.22, S * 0.56), (S * 0.78, S * 0.56), (S * 0.22, S * 0.76), (S * 0.78, S * 0.76)]:
        d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=W)
    # mũi tên
    d.line([(S * 0.5, S * 0.2), (S * 0.5, S * 0.58)], fill=VANG + (255,), width=w)
    d.line([(S * 0.36, S * 0.45), (S * 0.5, S * 0.6), (S * 0.64, S * 0.45)], fill=VANG + (255,), width=w,
           joint="curve")
    for p in [(S * 0.36, S * 0.45), (S * 0.64, S * 0.45), (S * 0.5, S * 0.2)]:
        d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=VANG + (255,))
    img = nen()
    img.alpha_composite(bong(g))
    return img


def icon_thanh_pham() -> Image.Image:
    """Khung phim + dấu tích: kết quả đã xong."""
    g = Image.new("RGBA", (S, S))
    d = ImageDraw.Draw(g)
    W = (255, 255, 255, 255)
    d.rounded_rectangle((S * 0.2, S * 0.24, S * 0.8, S * 0.72), radius=int(S * 0.07), fill=W)
    # lỗ phim
    for i in range(5):
        x = S * (0.27 + i * 0.115)
        for y in (S * 0.28, S * 0.645):
            d.rounded_rectangle((x, y, x + S * 0.06, y + S * 0.045), radius=int(S * 0.012), fill=MAU_1 + (255,))
    tam_giac(d, S * 0.49, S * 0.48, S * 0.085, MAU_2 + (255,))
    # huy hiệu tích
    cx, cy, r = S * 0.73, S * 0.73, S * 0.15
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(46, 196, 120, 255), outline=W, width=int(S * 0.025))
    w = int(S * 0.045)
    pts = [(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.35)]
    d.line(pts, fill=W, width=w, joint="curve")
    for p in pts:
        d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=W)
    img = nen()
    img.alpha_composite(bong(g))
    return img


def luu(img: Image.Image, ten: str) -> None:
    big = img.resize((1024, 1024), Image.LANCZOS)
    big.resize((256, 256), Image.LANCZOS).save(OUT / f"{ten}.png")
    sizes = [16, 20, 24, 32, 40, 48, 64, 128, 256]
    big.save(OUT / f"{ten}.ico", sizes=[(s, s) for s in sizes])
    if ten == "ai-studio":
        big.save(OUT / "ai-studio-1024.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    luu(icon_chinh(), "ai-studio")
    luu(icon_dau_vao(), "dau-vao")
    luu(icon_thanh_pham(), "thanh-pham")
    # ảnh xem trước: 3 icon ở nhiều cỡ trên nền sáng và tối
    prev = Image.new("RGB", (1180, 420), (251, 248, 244))
    ImageDraw.Draw(prev).rectangle((0, 210, 1180, 420), fill=(30, 27, 46))
    x = 20
    for ten in ("ai-studio", "dau-vao", "thanh-pham"):
        src = Image.open(OUT / f"{ten}.png")
        for y0 in (20, 230):
            xx = x
            for s in (160, 64, 32, 16):
                prev.paste(src.resize((s, s), Image.LANCZOS), (xx, y0 + (160 - s) // 2), src.resize((s, s), Image.LANCZOS))
                xx += s + 12
        x += 390
    prev.save(ROOT / ".cache" / "xem-icon.png")
    print("KET QUA:", OUT)
