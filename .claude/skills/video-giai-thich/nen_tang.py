"""Nền tảng video giải thích (Manim) cho TTomorrow Studio.

Cung cấp: đăng ký font Be Vietnam Pro, khung 9:16 / 16:9, bảng màu thương hiệu,
và các khối dựng sẵn (thẻ tiêu đề, danh sách bước, biểu đồ cột, sơ đồ luồng).

Cách dùng trong file cảnh:
    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from nen_tang import *
    khung = dung_khung("9:16")        # PHẢI gọi trước khi tạo Scene
    class Canh(Scene):
        def construct(self): ...
    if __name__ == "__main__":
        chay(Canh, "9:16", "ten-video")
Cỡ chữ dùng thang "16:9" (chữ chính ~44, tiêu đề ~64); khung dọc tự phóng to 1.3 lần.
"""
from __future__ import annotations

import re
import shutil
import sys
import textwrap
from datetime import date
from pathlib import Path

import manimpango
from manim import *  # noqa: F401,F403
from manim import config

GOC = Path(__file__).resolve().parents[3]          # thư mục gốc workspace
FONT_DIR = GOC / "assets" / "fonts"
TEN_FONT = "Be Vietnam Pro"
CACHE = GOC / ".cache" / "manim-test"

_font_da_dang_ky = False


def dang_ky_font() -> str:
    """Đăng ký font Be Vietnam Pro với Pango. Trả về tên font để dùng trong Text(font=...)."""
    global _font_da_dang_ky
    if not _font_da_dang_ky:
        for f in sorted(FONT_DIR.glob("BeVietnamPro-*.ttf")):
            try:
                manimpango.register_font(str(f))
            except Exception as e:  # không chết nếu 1 font lỗi
                print(f"[nen_tang] không đăng ký được {f.name}: {e}")
        _font_da_dang_ky = True
    return TEN_FONT


def _mau_thuong_hieu() -> dict:
    mac_dinh = {"chinh": "#E8505B", "phu": "#14274E", "nhan": "#F9B233",
                "nen": "#FFF8F0", "chu": "#1F2937"}
    f = GOC / "03-THUONG-HIEU" / "thuong-hieu.md"
    try:
        txt = f.read_text(encoding="utf-8")
    except OSError:
        return mac_dinh
    for khoa, nhan in (("chinh", "Màu chính"), ("phu", "Màu phụ"), ("nhan", "Màu nhấn")):
        m = re.search(nhan + r"\s*:\s*\[?\s*(#[0-9A-Fa-f]{6})", txt)
        if m:
            mac_dinh[khoa] = m.group(1).upper()
    return mac_dinh


MAU = _mau_thuong_hieu()   # dict: chinh, phu, nhan, nen, chu
K = 1.0                    # hệ số nhân khoảng cách/nét (2.0 với khung dọc)
KF = 1.0                   # hệ số nhân cỡ chữ (1.3 với khung dọc)
DOC = False                # True nếu khung dọc


def dung_khung(ti_le: str = "16:9", xem_truoc: bool = False, nen: str | None = None) -> dict:
    """Đặt khung hình. 9:16 = 1080x1920, 16:9 = 1920x1080, 30fps. xem_truoc = nửa độ phân giải, 15fps."""
    global K, KF, DOC
    dang_ky_font()
    dai, cao = (1080, 1920) if ti_le == "9:16" else (1920, 1080)
    DOC = ti_le == "9:16"
    K = 2.0 if DOC else 1.0
    KF = 1.3 if DOC else 1.0
    config.pixel_width, config.pixel_height = (dai // 2, cao // 2) if xem_truoc else (dai, cao)
    config.frame_rate = 15 if xem_truoc else 30
    config.frame_height = 16.0 if DOC else 8.0
    config.frame_width = config.frame_height * dai / cao
    config.background_color = nen or MAU["nen"]
    config.verbosity = "WARNING"
    config.progress_bar = "none"
    config.disable_caching = True
    return {"rong": config.frame_width, "cao": config.frame_height, "k": K}


def chu(noi_dung: str, co: float = 44, mau: str | None = None, dam: bool = False,
        rong_toi_da: int | None = None) -> Text:
    """Chữ tiếng Việt. co theo thang 16:9. rong_toi_da = số ký tự mỗi dòng (tự xuống dòng)."""
    if rong_toi_da:
        noi_dung = "\n".join(textwrap.wrap(noi_dung, rong_toi_da))
    return Text(noi_dung, font=TEN_FONT, font_size=co * KF, color=mau or MAU["chu"],
                weight=BOLD if dam else NORMAL)


def the_tieu_de(tieu_de: str, phu_de: str | None = None) -> VGroup:
    """Thẻ tiêu đề: chữ lớn, phụ đề nhỏ, vạch màu nhấn bên dưới. Dùng FadeIn / Write."""
    cot = [chu(tieu_de, 64, MAU["phu"], True, 11 if DOC else 30)]
    vach = Line(LEFT, RIGHT, color=MAU["nhan"], stroke_width=8 * K).set_width(2.5 * K)
    cot.append(vach)
    if phu_de:
        cot.append(chu(phu_de, 34, MAU["chu"], False, 26 if DOC else 50))
    return VGroup(*cot).arrange(DOWN, buff=0.35 * K)


def danh_sach_buoc(scene: Scene, buoc: list[str], tieu_de: str | None = None,
                   giay_moi_buoc: float = 1.6, cho_cuoi: float = 1.5) -> VGroup:
    """Hiện lần lượt từng bước (vòng tròn số + chữ), bước trước mờ đi. Trả về nhóm."""
    dong = []
    for i, nd in enumerate(buoc, 1):
        so = VGroup(Circle(radius=0.45 * K, color=MAU["chinh"], fill_opacity=1, stroke_width=0),
                    chu(str(i), 40, WHITE, True))
        so[1].move_to(so[0])
        van = chu(nd, 42, MAU["chu"], False, 13 if DOC else 40)
        dong.append(VGroup(so, van.next_to(so, RIGHT, buff=0.4 * K)))
    nhom = VGroup(*dong).arrange(DOWN, aligned_edge=LEFT, buff=0.9 * K)
    if tieu_de:
        td = the_tieu_de(tieu_de)
        td.to_edge(UP, buff=1.0 * K)
        nhom.next_to(td, DOWN, buff=1.2 * K)
        scene.play(FadeIn(td, shift=DOWN * 0.3), run_time=0.8)
    nhom.set_x(0)
    for i, d in enumerate(dong):
        if i:
            scene.play(*[x.animate.set_opacity(0.45) for x in dong[:i]], run_time=0.3)
        scene.play(FadeIn(d, shift=RIGHT * 0.5 * K), run_time=0.7)
        scene.wait(max(giay_moi_buoc - 1.0, 0.2))
    scene.play(*[x.animate.set_opacity(1) for x in dong], run_time=0.4)
    scene.wait(cho_cuoi)
    return nhom


def bieu_do_cot(scene: Scene, nhan: list[str], gia_tri: list[float], tieu_de: str | None = None,
                don_vi: str = "", mau_cot: list[str] | None = None, cao_toi_da: float | None = None,
                giay_moi_cot: float = 0.9, cho_cuoi: float = 2.0) -> VGroup:
    """Biểu đồ cột mọc dần từ đáy, kèm số liệu. Chiều cao tự co theo khung."""
    W, H = config.frame_width, config.frame_height
    vung_rong = W * 0.82
    cao_max = cao_toi_da or (H * (0.34 if DOC else 0.36))
    n = len(gia_tri)
    rong_cot = vung_rong / (n * 1.6)
    max_v = max(gia_tri)
    y_day = -H * (0.15 if DOC else 0.2)
    if tieu_de:
        td = chu(tieu_de, 56, MAU["phu"], True, 13 if DOC else 40).to_edge(UP, buff=0.9 * K)
        scene.play(FadeIn(td, shift=DOWN * 0.3), run_time=0.8)
    mau_cot = mau_cot or [MAU["chinh"], MAU["phu"], MAU["nhan"]]
    truc = Line(LEFT * vung_rong / 2, RIGHT * vung_rong / 2, color=MAU["chu"], stroke_width=3 * K)
    truc.move_to([0, y_day, 0])
    scene.play(Create(truc), run_time=0.5)
    cac_cot = VGroup()
    for i, (nh, v) in enumerate(zip(nhan, gia_tri)):
        x = -vung_rong / 2 + vung_rong * (i + 0.5) / n
        h = max(cao_max * v / max_v, 0.05)
        cot = Rectangle(width=rong_cot, height=h, color=mau_cot[i % len(mau_cot)],
                        fill_opacity=1, stroke_width=0)
        cot.move_to([x, y_day, 0], aligned_edge=DOWN)
        nh_t = chu(nh, 34, MAU["chu"]).next_to(truc, DOWN, buff=0.3 * K).set_x(x)
        so = chu(f"{v:g}{don_vi}", 38, MAU["phu"], True).next_to(cot, UP, buff=0.2 * K)
        cac_cot.add(VGroup(cot, nh_t, so))
        scene.play(FadeIn(nh_t), run_time=0.2)
        scene.play(GrowFromEdge(cot, DOWN), run_time=giay_moi_cot)
        scene.play(FadeIn(so, shift=UP * 0.2), run_time=0.3)
    scene.wait(cho_cuoi)
    return cac_cot


def so_do_luong(scene: Scene, buoc: list[str], tieu_de: str | None = None,
                giay_moi_buoc: float = 1.2, cho_cuoi: float = 1.5) -> VGroup:
    """Sơ đồ ô -> ô -> ô có mũi tên. Khung dọc xếp từ trên xuống, khung ngang xếp từ trái sang phải."""
    W, H = config.frame_width, config.frame_height
    mau = [MAU["chinh"], MAU["phu"], MAU["nhan"]]
    o = []
    for i, nd in enumerate(buoc):
        t = chu(nd, 36, WHITE if i % 3 != 2 else MAU["chu"], True, 14 if DOC else 14)
        if DOC:
            rong, cao = W * 0.78, max(t.height + 0.7 * K, 1.2 * K)
        else:
            rong, cao = (W * 0.88 - 0.9 * (len(buoc) - 1)) / len(buoc), max(t.height + 1.0, 1.8)
            t.scale_to_fit_width(min(t.width, rong * 0.88))
        hop = RoundedRectangle(corner_radius=0.25 * K, width=rong, height=cao,
                               color=mau[i % 3], fill_opacity=1, stroke_width=0)
        o.append(VGroup(hop, t.move_to(hop)))
    nhom = VGroup(*o).arrange(DOWN if DOC else RIGHT, buff=0.8 * K if DOC else 0.9)
    nhom.move_to(ORIGIN)
    if tieu_de:
        td = chu(tieu_de, 56, MAU["phu"], True, 12 if DOC else 40).to_edge(UP, buff=0.9 * K)
        # đặt sơ đồ ở giữa phần còn lại bên dưới tiêu đề
        nhom.set_y((td.get_bottom()[1] - H / 2) / 2)
        scene.play(FadeIn(td, shift=DOWN * 0.3), run_time=0.8)
    mui = []
    for i, h in enumerate(o):
        if i:
            a = Arrow(o[i - 1].get_bottom() if DOC else o[i - 1].get_right(),
                      h.get_top() if DOC else h.get_left(), buff=0.12 * K,
                      color=MAU["chu"], stroke_width=8 * K, max_tip_length_to_length_ratio=0.5)
            mui.append(a)
            scene.play(GrowArrow(a), run_time=0.4)
        scene.play(FadeIn(h, scale=0.85), run_time=0.6)
        scene.wait(max(giay_moi_buoc - 1.0, 0.1))
    scene.wait(cho_cuoi)
    return VGroup(*o, *mui)


def chay(lop_canh, ti_le: str, ten_file: str, argv: list[str] | None = None) -> Path:
    """Render một cảnh. Tùy chọn dòng lệnh: --xem-truoc (nhanh, nhẹ), --ra <thư mục> (copy MP4 vào đó,
    không ghi đè: nếu trùng tên thì thêm _2, _3...). Mặc định để trong .cache/manim-test."""
    argv = list(sys.argv[1:] if argv is None else argv)
    xem_truoc = "--xem-truoc" in argv
    ra = Path(argv[argv.index("--ra") + 1]) if "--ra" in argv else None
    dung_khung(ti_le, xem_truoc)
    config.media_dir = str(CACHE)
    config.output_file = ten_file + ("_xemtruoc" if xem_truoc else "")
    canh = lop_canh()
    canh.render()
    nguon = Path(canh.renderer.file_writer.movie_file_path)
    if ra is None:
        print("KET QUA:", nguon)
        return nguon
    ra.mkdir(parents=True, exist_ok=True)
    dich = ra / f"{ten_file}.mp4"
    n = 2
    while dich.exists():
        dich = ra / f"{ten_file}_{n}.mp4"
        n += 1
    shutil.copy2(nguon, dich)
    print("KET QUA:", dich)
    return dich
