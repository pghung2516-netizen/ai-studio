"""Ví dụ 9:16: 3 bước đặt hàng (sơ đồ luồng + danh sách bước)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from nen_tang import *

dung_khung("9:16")


class DatHang(Scene):
    def construct(self):
        tc = the_tieu_de("3 bước đặt hàng", "Nhanh gọn – chỉ 1 phút")
        self.play(FadeIn(tc, shift=UP * 0.4), run_time=1)
        self.wait(1)
        self.play(FadeOut(tc))
        so_do_luong(self, ["Chọn sản phẩm yêu thích", "Điền địa chỉ nhận hàng", "Thanh toán & nhận quà"],
                    tieu_de="Cách đặt hàng")
        self.wait(0.5)


if __name__ == "__main__":
    chay(DatHang, "9:16", "3-buoc-dat-hang")
