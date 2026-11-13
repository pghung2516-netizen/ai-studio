"""Bộ lệnh 'studio'. Cách chạy:  uv run python -m studio <lệnh> [tùy chọn]
Xem tất cả lệnh:  uv run python -m studio --help
Xem chi tiết 1 lệnh:  uv run python -m studio <lệnh> --help
"""
from __future__ import annotations

import argparse
import sys
import traceback

from .common import LoiNguoiDung, bat_utf8

VI_TRI = ["tren", "giua", "duoi", "trai", "phai", "tren-trai", "tren-phai", "duoi-trai", "duoi-phai"]


def _chu_opts(p: argparse.ArgumentParser, vi_tri_mac_dinh: str) -> None:
    p.add_argument("--vi-tri", default=vi_tri_mac_dinh, choices=VI_TRI)
    p.add_argument("--co", default="vua", choices=["nho", "vua", "lon"], help="cỡ chữ")
    p.add_argument("--co-chu", type=int, help="cỡ chữ chính xác theo pixel (ghi đè --co)")
    p.add_argument("--mau", default="#FFFFFF", help="màu chữ: mã #RRGGBB hoặc trang/den/vang/do/xanh...")
    p.add_argument("--mau-vien", default="#000000", help="màu viền chữ")
    p.add_argument("--mau-nen", help="màu hộp nền sau chữ (bỏ trống = không có hộp)")
    p.add_argument("--do-mo-nen", type=float, default=0.75, help="độ đậm hộp nền 0-1")


def tao_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="studio", description="Bộ công cụ sửa video/ảnh. Thêm --du-an \"<dự án>\" để làm trong một dự án (nháp ở .cache/nhap, bản cuối chốt bằng du-an chot)")
    ap.add_argument("--du-an", metavar="<dự án>", help="dùng Gốc và thư mục bản nháp của dự án (có thể đặt sau lệnh)")
    sub = ap.add_subparsers(dest="lenh", metavar="<lệnh>")

    def L(ten, ham, help_):
        p = sub.add_parser(ten, help=help_, description=help_)
        p.set_defaults(ham=ham)
        return p

    from . import doctor, du_an, image, subtitle, tim_file_moi, video

    # --- dự án
    p_da = sub.add_parser("du-an", help="Tạo và quản lý dự án", description="Tạo và quản lý dự án")
    da_sub = p_da.add_subparsers(dest="lenh_du_an", metavar="<lệnh dự án>")
    p = da_sub.add_parser("moi", help="Tạo dự án mới")
    p.add_argument("ten", help="tên dự án")
    p.add_argument("file", nargs="*", help="file đầu vào")
    p.add_argument("--lay-hop-thu", action="store_true", help="lấy mọi file đang nằm trực tiếp trong 01-DAU-VAO")
    p.set_defaults(ham=du_an.lenh_moi)
    p = da_sub.add_parser("them", help="Thêm file gốc vào dự án")
    p.add_argument("du_an", help="tên hoặc một phần tên dự án")
    p.add_argument("file", nargs="*", help="file đầu vào")
    p.add_argument("--lay-hop-thu", action="store_true", help="lấy mọi file đang nằm trực tiếp trong 01-DAU-VAO")
    p.set_defaults(ham=du_an.lenh_them)
    p = da_sub.add_parser("ds", help="Liệt kê dự án mới nhất")
    p.add_argument("--so", type=int, default=20)
    p.set_defaults(ham=du_an.lenh_ds)
    p = da_sub.add_parser("xem", help="Xem file và nhật ký dự án")
    p.add_argument("du_an")
    p.set_defaults(ham=du_an.lenh_xem)
    p = da_sub.add_parser("ghi", help="Ghi thêm vào nhật ký")
    p.add_argument("du_an")
    p.add_argument("noi_dung")
    p.set_defaults(ham=du_an.lenh_ghi)
    p = da_sub.add_parser("chot", help="Chốt một bản nháp thành thành phẩm")
    p.add_argument("du_an")
    p.add_argument("file")
    p.add_argument("--ten", required=True, help="nhãn phiên bản, ví dụ quang-cao")
    p.add_argument("--ghi-chu")
    p.add_argument("--kem-phu-de", action="store_true", help="chép kèm .srt/.txt cùng tên nếu có")
    p.set_defaults(ham=du_an.lenh_chot)

    p = L("tim-file-moi", tim_file_moi.lenh_tim_file_moi, "Tìm media mới nhất trong các thư mục thường dùng")
    p.add_argument("--loai", default="tat-ca", choices=["video", "anh", "am-thanh", "tat-ca"])
    p.add_argument("--so", type=int, default=10)
    p.add_argument("--gio", type=int, default=168)
    p = L("don-dep", du_an.lenh_don_dep, "Xem trước hoặc chuyển dự án cũ vào Thùng rác")
    p.add_argument("--cu-hon", type=int, default=30, help="số ngày không hoạt động")
    p.add_argument("--du-an", dest="_du_an_hien_thi", metavar="<dự án>", help="chọn duy nhất một dự án")
    p.add_argument("--xac-nhan", action="store_true", help="chuyển vào Thùng rác")

    # --- hệ thống
    L("kiem-tra", doctor.lenh_kiem_tra, "Kiểm tra máy đã cài đủ công cụ chưa")
    p = L("tai-mo-hinh", doctor.lenh_tai_mo_hinh, "Tải trước mô hình AI (phụ đề, xóa nền)")
    p.add_argument("--loai", default="tat-ca", choices=["tat-ca", "phu-de", "xoa-nen"])
    p.add_argument("--whisper", default="small", help="base | small | medium | large-v3")
    p = L("danh-sach", doctor.lenh_danh_sach, "Liệt kê file trong 01-DAU-VAO (mới nhất trước)")
    p.add_argument("--thu-muc", help="thư mục khác, ví dụ 02-DU-AN")
    p = L("thong-tin", video.lenh_thong_tin, "Xem thông tin video/ảnh/âm thanh (độ dài, kích thước...)")
    p.add_argument("file", help="file hoặc thư mục")

    # --- video
    p = L("cat", video.lenh_cat, "Cắt lấy 1 đoạn video")
    p.add_argument("video")
    p.add_argument("--tu", help="mốc bắt đầu, ví dụ 0:15")
    p.add_argument("--den", help="mốc kết thúc, ví dụ 1:30")
    p.add_argument("--dai", help="hoặc độ dài đoạn cần lấy, ví dụ 30 (giây)")
    p = L("ghep", video.lenh_ghep, "Ghép nhiều video nối tiếp nhau")
    p.add_argument("video", nargs="+", help="các file theo thứ tự, hoặc 1 thư mục (sắp theo tên)")
    p.add_argument("--ti-le", help="9:16 | 16:9 | 1:1 | 4:5 (mặc định theo video đầu)")
    p.add_argument("--kieu", default="nen-mo", choices=["cat", "vua", "nen-mo"])
    p = L("khung", video.lenh_khung, "Đổi khung hình: dọc 9:16, ngang 16:9, vuông 1:1, 4:5")
    p.add_argument("video")
    p.add_argument("--ti-le", required=True, help="9:16 | 16:9 | 1:1 | 4:5 | doc | ngang | vuong")
    p.add_argument("--kieu", default="nen-mo", choices=["cat", "vua", "nen-mo"],
                   help="cat = lấp đầy (mất mép) | vua = giữ trọn, viền đen | nen-mo = giữ trọn, nền mờ")
    p = L("nen", video.lenh_nen, "Nén video cho nhẹ để đăng/gửi")
    p.add_argument("video")
    p.add_argument("--muc", default="vua", choices=["nhe", "vua", "manh"], help="mức nén")
    p.add_argument("--toi-da", type=int, help="giảm độ phân giải: cạnh ngắn tối đa (vd 720, 1080)")
    p.add_argument("--toi-da-mb", type=float, help="giới hạn dung lượng (MB), vd 25 cho Zalo/email")
    p = L("toc-do", video.lenh_toc_do, "Tua nhanh / làm chậm video")
    p.add_argument("video")
    p.add_argument("--he-so", type=float, required=True, help="1.5 = nhanh 1.5 lần; 0.5 = chậm một nửa")
    p = L("nhac", video.lenh_nhac, "Chèn nhạc nền (tự lặp/cắt cho vừa, tự giảm nhạc khi có người nói)")
    p.add_argument("video")
    p.add_argument("nhac", help="file nhạc mp3/wav/m4a")
    p.add_argument("--am-luong", type=float, default=0.25, help="âm lượng nhạc 0-1 (mặc định 0.25)")
    p.add_argument("--bo-tieng-goc", action="store_true", help="bỏ hẳn tiếng gốc, chỉ giữ nhạc")
    p.add_argument("--khong-giam-nhac", action="store_true", help="không tự giảm nhạc khi có người nói")
    p = L("chuan-am", video.lenh_chuan_am, "Cân bằng âm lượng chuẩn TikTok/YouTube (-14 LUFS)")
    p.add_argument("video")
    p = L("tat-tieng", video.lenh_tat_tieng, "Bỏ toàn bộ âm thanh của video")
    p.add_argument("video")
    p = L("tach-am", video.lenh_tach_am, "Tách âm thanh từ video ra file nhạc")
    p.add_argument("video")
    p.add_argument("--dinh-dang", default="mp3", choices=["mp3", "wav", "m4a"])
    p = L("xoay", video.lenh_xoay, "Xoay / lật video")
    p.add_argument("video")
    p.add_argument("--huong", required=True, choices=["phai", "trai", "180", "lat-ngang", "lat-doc"])
    p = L("logo", video.lenh_logo, "Chèn logo/watermark vào video, ảnh, hoặc cả thư mục ảnh")
    p.add_argument("file")
    p.add_argument("logo", help="file logo (nên là PNG nền trong suốt)")
    p.add_argument("--vi-tri", default="tren-phai", choices=VI_TRI)
    p.add_argument("--ti-le", type=float, default=0.15, help="logo rộng bằng bao nhiêu phần khung (0.15 = 15%%)")
    p.add_argument("--do-mo", type=float, default=0.9, help="độ rõ của logo 0-1")
    p = L("chu", video.lenh_chu, "Chèn dòng chữ tiếng Việt vào video (có thể chỉ hiện trong 1 khoảng thời gian)")
    p.add_argument("video")
    p.add_argument("--noi-dung", required=True)
    p.add_argument("--tu", help="hiện từ giây thứ...")
    p.add_argument("--den", help="ẩn ở giây thứ...")
    _chu_opts(p, "tren")
    p = L("khung-hinh", video.lenh_khung_hinh, "Trích khung hình + ảnh tổng hợp có mốc giờ (để xem nhanh nội dung)")
    p.add_argument("video")
    p.add_argument("--so", type=int, default=12, help="số khung hình (mặc định 12)")
    p.add_argument("--kiem-tra", action="store_true", help="để Claude tự kiểm tra: lưu vào .cache, không vào thư mục kết quả")
    p = L("gif", video.lenh_gif, "Cắt 1 đoạn video thành ảnh GIF")
    p.add_argument("video")
    p.add_argument("--tu")
    p.add_argument("--den")
    p.add_argument("--rong", type=int, default=480)
    p.add_argument("--fps", type=int, default=12)
    p = L("anh-thanh-video", video.lenh_anh_thanh_video, "Dựng video từ nhiều ảnh (zoom chậm, chuyển cảnh, chữ, nhạc)")
    p.add_argument("anh", nargs="+", help="các ảnh theo thứ tự, hoặc 1 thư mục (sắp theo tên)")
    p.add_argument("--ti-le", default="9:16")
    p.add_argument("--giay-moi-anh", type=float, default=3.0)
    p.add_argument("--kieu", default="nen-mo", choices=["cat", "vua", "nen-mo"])
    p.add_argument("--hieu-ung", default="zoom", choices=["zoom", "khong"])
    p.add_argument("--chuyen-canh", default="fade", help="fade | slideleft | slideup | circleopen | dissolve | ngau-nhien ...")
    p.add_argument("--chu", help="chữ cho từng ảnh, ngăn bằng dấu |  ví dụ: 'Câu 1|Câu 2||Câu 4'")
    p.add_argument("--nhac", help="file nhạc nền")
    p.add_argument("--am-luong", type=float, default=0.8)
    _chu_opts(p, "duoi")

    # --- phụ đề
    def _pd_style(p):
        p.add_argument("--kieu", default="tiktok", choices=["tiktok", "don-gian", "hop-den", "trang-den"])
        p.add_argument("--vi-tri", default="duoi", choices=["duoi", "giua", "tren"])
        p.add_argument("--co", default="vua", choices=["nho", "vua", "lon"])
        p.add_argument("--in-hoa", action="store_true", help="viết HOA toàn bộ phụ đề")

    p = L("phu-de", subtitle.lenh_phu_de, "Nghe giọng nói → file phụ đề .srt (+ lời thoại .txt), có thể đốt luôn vào video")
    p.add_argument("video")
    p.add_argument("--ngon-ngu", default="vi", help="vi | en | tu-dong ...")
    p.add_argument("--mo-hinh", default="vua", help="nhanh | vua | chuan | tot-nhat (càng tốt càng chậm)")
    p.add_argument("--toi-da-ky-tu", type=int, help="số ký tự tối đa mỗi câu phụ đề")
    p.add_argument("--dot-vao", action="store_true", help="đốt phụ đề vào video luôn")
    _pd_style(p)
    p = L("dot-phu-de", subtitle.lenh_dot_phu_de, "Đốt file phụ đề .srt (đã sửa) vào video")
    p.add_argument("video")
    p.add_argument("srt")
    _pd_style(p)

    # --- ảnh
    p = L("doi-co", image.lenh_doi_co, "Đổi cỡ ảnh theo kênh (shopee, tiktok, youtube-thumbnail...) - nhận cả thư mục")
    p.add_argument("anh", help="ảnh hoặc thư mục ảnh")
    p.add_argument("--kenh", help="facebook-post | story | youtube-thumbnail | shopee | banner-web | ...")
    p.add_argument("--kich-thuoc", help="hoặc kích thước tự chọn, vd 1200x628")
    p.add_argument("--kieu", default="vua", choices=["cat", "vua", "nen-mo"])
    p.add_argument("--mau-nen", default="#FFFFFF", help="màu nền khi kieu=vua")
    p.add_argument("--dinh-dang", choices=["jpg", "png", "webp"])
    p = L("xoa-nen", image.lenh_xoa_nen, "Xóa nền ảnh (sản phẩm, chân dung) - nhận cả thư mục")
    p.add_argument("anh")
    p.add_argument("--nen", help="thay nền mới: trang | den | #RRGGBB | mo (bỏ trống = trong suốt)")
    p.add_argument("--cat-sat", action="store_true", help="cắt sát quanh chủ thể")
    p.add_argument("--mo-hinh", default="isnet-general-use", help="isnet-general-use | u2net | u2net_human_seg")
    p = L("chu-anh", image.lenh_chu_anh, "Chèn chữ tiếng Việt lên ảnh - nhận cả thư mục")
    p.add_argument("anh")
    p.add_argument("--noi-dung", required=True)
    p.add_argument("--dinh-dang", choices=["jpg", "png", "webp"])
    _chu_opts(p, "duoi")
    p = L("nen-anh", image.lenh_nen_anh, "Nén/thu nhỏ ảnh cho nhẹ - nhận cả thư mục")
    p.add_argument("anh")
    p.add_argument("--dinh-dang", default="jpg", choices=["jpg", "webp", "png"])
    p.add_argument("--chat-luong", type=int, default=82)
    p.add_argument("--rong-toi-da", type=int, default=2048, help="cạnh dài tối đa (px)")
    p = L("ghep-anh", image.lenh_ghep_anh, "Ghép nhiều ảnh: lưới (collage) hoặc trước-sau")
    p.add_argument("anh", nargs="+")
    p.add_argument("--kieu", default="luoi", choices=["luoi", "truoc-sau"])
    p.add_argument("--so-cot", type=int)
    p.add_argument("--co-o", type=int, default=600, help="cỡ mỗi ô (px) khi ghép lưới")
    p.add_argument("--khoang-cach", type=int, default=12)
    p.add_argument("--mau-nen", default="#FFFFFF")
    p.add_argument("--nhan", help="nhãn kiểu trước-sau, vd 'TRƯỚC|SAU'")
    p = L("doi-dinh-dang", image.lenh_doi_dinh_dang, "Đổi định dạng ảnh (HEIC → JPG, PNG → WEBP...)")
    p.add_argument("anh")
    p.add_argument("--sang", default="jpg", choices=["jpg", "png", "webp"])

    # --- OpenMontage (công cụ thêm, tải khi cần)
    from . import openmontage

    p_om = sub.add_parser("openmontage", help="Công cụ thêm OpenMontage: cắt video dài thành clip ngắn, video người nói, video theo mẫu",
                          description="Công cụ thêm OpenMontage (tải ở lần dùng đầu)")
    om_sub = p_om.add_subparsers(dest="lenh_om", metavar="<cai | trang-thai | cong-cu | chay>")
    p = om_sub.add_parser("cai", help="Tải và cài OpenMontage (lần đầu ~5-10 phút)")
    p.add_argument("--cai-lai", action="store_true", help="tải lại từ đầu")
    p.set_defaults(ham=openmontage.lenh_cai)
    p = om_sub.add_parser("trang-thai", help="Xem đã cài chưa, công cụ nào dùng được")
    p.set_defaults(ham=openmontage.lenh_trang_thai)
    p = om_sub.add_parser("cong-cu", help="Chạy 1 công cụ offline của OpenMontage với tham số JSON")
    p.add_argument("ten", help="tên công cụ, ví dụ silence_cutter")
    p.add_argument("json", nargs="?", default="{}", help="tham số dạng JSON, file vào tìm trong Gốc của dự án")
    p.set_defaults(ham=openmontage.lenh_cong_cu)
    p = om_sub.add_parser("chay", help="Chạy python trong môi trường OpenMontage", prefix_chars="\0")
    p.add_argument("tham_so", nargs=argparse.REMAINDER)
    p.set_defaults(ham=openmontage.lenh_chay)

    # --- CapCut
    p = L("capcut-sao-luu", doctor.lenh_capcut_sao_luu, "Sao lưu 1 dự án CapCut trước khi cho Claude sửa")
    p.add_argument("du_an", help="tên (hoặc 1 phần tên) dự án CapCut")
    return ap


def main(argv: list[str] | None = None) -> int:
    bat_utf8()
    ap = tao_parser()
    raw = list(sys.argv[1:] if argv is None else argv)
    clean: list[str] = []
    du_an_name: str | None = None
    i = 0
    while i < len(raw):
        token = raw[i]
        if token == "--du-an":
            if i + 1 >= len(raw):
                ap.error("--du-an cần tên dự án")
            du_an_name = raw[i + 1]
            i += 2
            continue
        if token.startswith("--du-an="):
            du_an_name = token.split("=", 1)[1]
            i += 1
            continue
        clean.append(token)
        i += 1
    a = ap.parse_args(clean)
    a.du_an_studio = du_an_name
    if not getattr(a, "ham", None):
        ap.print_help()
        return 0
    try:
        if du_an_name and a.lenh not in ("du-an", "don-dep", "tim-file-moi"):
            from .common import dat_du_an_hien_tai
            from .du_an import tim_du_an

            dat_du_an_hien_tai(tim_du_an(du_an_name))
        a.ham(a)
        return 0
    except LoiNguoiDung as e:
        print(f"❌ {e}", flush=True)
        return 2
    except KeyboardInterrupt:
        print("⏹️  Đã dừng.", flush=True)
        return 130
    except Exception as e:  # noqa: BLE001
        print(f"❌ Có lỗi kỹ thuật: {e}", flush=True)
        traceback.print_exc(limit=3)
        return 1


if __name__ == "__main__":
    sys.exit(main())
