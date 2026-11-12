"""Ví dụ 16:9: biểu đồ cột Doanh thu 4 tháng (triệu đồng)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from nen_tang import *

dung_khung("16:9")


class DoanhThu(Scene):
    def construct(self):
        bieu_do_cot(self, ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4"], [45, 62, 80, 118],
                    tieu_de="Doanh thu 4 tháng (triệu đồng)", don_vi="tr")
        ghi = chu("Tăng trưởng gần gấp 3 lần – ơ kìa, đẹp quá!", 36, MAU["chinh"], True).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(ghi, shift=UP * 0.3))
        self.wait(1.5)


if __name__ == "__main__":
    chay(DoanhThu, "16:9", "doanh-thu-4-thang")
