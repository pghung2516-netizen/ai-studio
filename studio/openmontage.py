"""OpenMontage (AGPL-3.0) - công cụ thêm, tải về máy ở lần dùng đầu, KHÔNG nằm trong repo của workspace.

  studio openmontage cai          tải + cài (chỉ lần đầu, ~5-10 phút)
  studio openmontage trang-thai   xem đã cài chưa, công cụ nào sẵn sàng
  studio openmontage cong-cu <tên> '<json>'   chạy 1 công cụ offline (file vào lấy từ dự án, kết quả ra nháp)
  studio openmontage chay <...>   chạy python trong môi trường OpenMontage (thư mục làm việc = gốc OpenMontage)

Cài vào 05-CONG-CU-THEM/openmontage (đã nằm trong .gitignore). Bản được ghim theo commit
để lần cài nào cũng giống nhau; ffmpeg lấy từ bản đóng gói sẵn của workspace, ffprobe lấy từ
gói npm ffprobe-static (kiểm tra mã băm) - người dùng không phải cài gì thêm.
"""
from __future__ import annotations

import base64
import datetime as _dt
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from .common import CACHE, ROOT, LoiNguoiDung, bao, file_ra, ket_qua, thu_muc_hom_nay, tim_file

OM = ROOT / "05-CONG-CU-THEM" / "openmontage"
COMMIT = "fecb9a1e3cc23ef84de30b272059457a427f16f8"  # 2026-11-09
ZIP_URL = f"https://codeload.github.com/OpenMontageInc/OpenMontage/zip/{COMMIT}"
FFPROBE_TGZ = "https://registry.npmjs.org/ffprobe-static/-/ffprobe-static-3.1.0.tgz"
FFPROBE_SHA512 = "Dvpa9uhVMOYivhHKWLGDoa512J751qN1WZAIO+Xw4L/mrUSPxS4DApzSUDbCFE/LUq2+xYnznEahTd63AqBSpA=="
MARKER = OM / ".ttomorrow-cai-xong.json"
# Thư viện thêm ngoài requirements.txt của OpenMontage (đổi danh sách -> lần chạy sau tự cài bổ sung)
THU_VIEN_THEM = [
    "opencv-python-headless>=4.9",  # bám khuôn mặt khi cắt khung dọc (auto_reframe)
    "av<19",  # av 19 bỏ tham số metadata_errors mà faster-whisper dùng khi đọc thẳng file video
]
BIN = OM / "_bin"
LA_WIN = os.name == "nt"
EXE = ".exe" if LA_WIN else ""
# Công cụ OpenMontage mà skill openmontage dùng (đều chạy offline)
CONG_CU_CHINH = [
    "transcriber", "scene_detect", "frame_sampler", "silence_cutter", "video_trimmer",
    "auto_reframe", "face_tracker", "subtitle_gen", "audio_mixer", "audio_enhance",
    "video_compose", "video_stitch", "color_grade",
]
# Chỉ những công cụ này được gọi qua `cong-cu` - đều chạy trên máy, không gửi file đi đâu, không tốn tiền
CONG_CU_OFFLINE = set(CONG_CU_CHINH) | {
    "video_analyzer", "audio_energy", "audio_probe", "visual_qa", "face_enhance",
}
KHOA_FILE_VAO = ("input_path", "source", "audio_path", "subtitle_path", "face_tracking_json", "video_path")

_RUNNER = """
import json, sys
from tools.tool_registry import registry
registry.discover()
ten, f = sys.argv[1], sys.argv[2]
inputs = json.load(open(f, encoding="utf-8"))
r = registry.get(ten).execute(inputs)
print("JSON_KQ:" + json.dumps({"ok": r.success, "loi": r.error, "data": r.data,
      "artifacts": [str(x) for x in (r.artifacts or [])]}, ensure_ascii=False, default=str))
"""


def _python_om() -> Path:
    return OM / ".venv" / ("Scripts/python.exe" if LA_WIN else "bin/python")


def _uv() -> str:
    uv = os.environ.get("UV") or shutil.which("uv")
    if not uv:
        raise LoiNguoiDung("Không tìm thấy uv - chạy skill cai-dat trước.")
    return uv


def _moi_truong() -> dict[str, str]:
    env = dict(os.environ)
    env["PATH"] = str(BIN) + os.pathsep + env.get("PATH", "")
    env.setdefault("HF_HOME", str(CACHE / "huggingface"))  # dùng chung mô hình Whisper với studio
    env["HF_HUB_DISABLE_TELEMETRY"] = "1"
    env["PYTHONPATH"] = str(OM)  # để script đặt ở nơi khác vẫn import được tools/, lib/
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env.pop("VIRTUAL_ENV", None)  # đừng để môi trường của studio lẫn vào
    return env


def _tai(url: str, dich: Path, mo_ta: str) -> Path:
    dich.parent.mkdir(parents=True, exist_ok=True)
    tam = dich.with_suffix(dich.suffix + ".dang-tai")
    bao(f"⏳ Đang tải {mo_ta}…")
    req = urllib.request.Request(url, headers={"User-Agent": "ttomorrow-studio"})
    with urllib.request.urlopen(req, timeout=120) as r, open(tam, "wb") as f:
        shutil.copyfileobj(r, f, 1024 * 1024)
    tam.replace(dich)
    return dich


def _nen_tang_ffprobe() -> str:
    m = platform.machine().lower()
    if LA_WIN:
        return "win32/" + ("x64" if m in ("amd64", "x86_64", "arm64") else "ia32")
    if sys.platform == "darwin":
        return "darwin/" + ("arm64" if m == "arm64" else "x64")
    return "linux/" + ("x64" if m in ("x86_64", "amd64") else "ia32")


def _chuan_bi_bin() -> None:
    BIN.mkdir(parents=True, exist_ok=True)
    import imageio_ffmpeg

    ff = BIN / f"ffmpeg{EXE}"
    if not ff.exists():
        shutil.copy2(imageio_ffmpeg.get_ffmpeg_exe(), ff)
    fp = BIN / f"ffprobe{EXE}"
    if fp.exists():
        return
    tuong_doi = f"bin/{_nen_tang_ffprobe()}/ffprobe{EXE}"
    co_san = ROOT / "05-CONG-CU-THEM" / "hyperframes" / "node_modules" / "ffprobe-static" / tuong_doi
    if co_san.exists():
        shutil.copy2(co_san, fp)
    else:
        tgz = CACHE / "tai" / "ffprobe-static-3.1.0.tgz"
        if not tgz.exists():
            _tai(FFPROBE_TGZ, tgz, "ffprobe (~65MB)")
        bam = base64.b64encode(hashlib.sha512(tgz.read_bytes()).digest()).decode()
        if bam != FFPROBE_SHA512:
            tgz.unlink()
            raise LoiNguoiDung("File ffprobe tải về bị lỗi (mã băm không khớp) - thử chạy lại.")
        with tarfile.open(tgz, "r:gz") as t:
            m = t.getmember(f"package/{tuong_doi}")
            src = t.extractfile(m)
            assert src is not None
            with open(fp, "wb") as f:
                shutil.copyfileobj(src, f)
    if not LA_WIN:
        fp.chmod(0o755)


def _giai_nen_ma_nguon() -> None:
    zip_path = CACHE / "tai" / f"openmontage-{COMMIT[:12]}.zip"
    if not zip_path.exists():
        _tai(ZIP_URL, zip_path, "mã nguồn OpenMontage (~80MB)")
    with tempfile.TemporaryDirectory(dir=CACHE) as tmp:
        with zipfile.ZipFile(zip_path) as z:
            goc = Path(tmp).resolve()
            for ten in z.namelist():  # chặn file zip ghi ra ngoài thư mục
                if not (goc / ten).resolve().is_relative_to(goc):
                    raise LoiNguoiDung("File mã nguồn tải về không hợp lệ.")
            z.extractall(goc)
        trong = next(Path(tmp).iterdir())
        if OM.exists():  # bản cài dở / bản cũ do chính lệnh này tạo -> cất vào .cache, không xóa
            cat = CACHE / "openmontage-cu" / _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            cat.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(OM), str(cat))
        OM.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(trong), str(OM))
    # CLAUDE.md của OpenMontage bắt Claude đọc hướng dẫn tiếng Anh trước MỌI câu trả lời -> cất đi,
    # skill openmontage tự chỉ đúng file cần đọc, còn cách nói chuyện vẫn theo workspace.
    for ten in ("CLAUDE.md", "AGENTS.md"):
        if (OM / ten).exists():
            (OM / ten).rename(OM / f"{Path(ten).stem}.goc-openmontage.md")


def _cai_thu_vien() -> None:
    uv = _uv()
    py = _python_om()
    if not py.exists():
        subprocess.run([uv, "venv", "--python", sys.executable, str(OM / ".venv")], check=True)
    from importlib.metadata import version

    fw = version("faster-whisper")
    bao("⏳ Đang cài thư viện cho OpenMontage (lần đầu khoảng 3-5 phút)…")
    subprocess.run(
        [uv, "pip", "install", "--python", str(py), "-r", str(OM / "requirements.txt"), f"faster-whisper=={fw}",
         *THU_VIEN_THEM],
        check=True, env=_moi_truong(),
    )


def _da_cai() -> dict | None:
    try:
        info = json.loads(MARKER.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if info.get("commit") != COMMIT or info.get("thu_vien_them") != THU_VIEN_THEM or not _python_om().exists():
        return None
    return info


def _trang_thai_cong_cu() -> dict[str, str]:
    ma = (
        "import json\n"
        "from tools.tool_registry import registry\n"
        "registry.discover()\n"
        f"ten = {CONG_CU_CHINH!r}\n"
        "out = {}\n"
        "for n in ten:\n"
        "    t = registry.get(n)\n"
        "    out[n] = 'khong-co' if t is None else t.get_status().value\n"
        "print('JSON:' + json.dumps(out))\n"
    )
    r = subprocess.run([str(_python_om()), "-c", ma], cwd=OM, env=_moi_truong(),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    for dong in r.stdout.splitlines():
        if dong.startswith("JSON:"):
            return json.loads(dong[5:])
    raise LoiNguoiDung("OpenMontage chưa chạy được: " + (r.stderr.strip().splitlines() or ["không rõ lỗi"])[-1])


def lenh_cai(a) -> None:
    if _da_cai() and not getattr(a, "cai_lai", False):
        bao("✅ OpenMontage đã cài sẵn.")
        lenh_trang_thai(a)
        return
    bao("⏳ Lần đầu cần tải và cài OpenMontage (khoảng 5-10 phút, ~700MB).")
    try:
        commit_dang_co = (OM / ".ttomorrow-commit").read_text(encoding="utf-8").strip()
    except OSError:
        commit_dang_co = ""
    if getattr(a, "cai_lai", False) or commit_dang_co != COMMIT:
        _giai_nen_ma_nguon()
        (OM / ".ttomorrow-commit").write_text(COMMIT, encoding="utf-8")
    _chuan_bi_bin()
    _cai_thu_vien()
    tt = _trang_thai_cong_cu()
    MARKER.write_text(json.dumps({"commit": COMMIT, "thu_vien_them": THU_VIEN_THEM, "ngay": _dt.date.today().isoformat(), "cong_cu": tt},
                                 ensure_ascii=False, indent=2), encoding="utf-8")
    _in_trang_thai(tt)
    bao(f"KET QUA: {OM}")


def _in_trang_thai(tt: dict[str, str]) -> None:
    san = [n for n, s in tt.items() if s in ("available", "degraded")]  # degraded = chạy được, bản đơn giản hơn
    thieu = [n for n, s in tt.items() if n not in san]
    bao(f"✅ OpenMontage sẵn sàng: {len(san)}/{len(tt)} công cụ chính.")
    if thieu:
        bao("ℹ️  Chưa dùng được: " + ", ".join(thieu))
    bao("THONG TIN: " + json.dumps({"commit": COMMIT[:12], "cong_cu": tt}, ensure_ascii=False))


def lenh_trang_thai(a) -> None:
    if not _da_cai():
        bao("ℹ️  OpenMontage chưa cài. Chạy: studio openmontage cai")
        bao("THONG TIN: " + json.dumps({"da_cai": False}))
        return
    _in_trang_thai(_trang_thai_cong_cu())
    bao(f"KET QUA: {OM}")


def lenh_chay(a) -> None:
    if not _da_cai():
        raise LoiNguoiDung("OpenMontage chưa cài. Chạy trước: studio openmontage cai")
    tham_so = list(a.tham_so)
    if tham_so and tham_so[0] == "--":
        tham_so = tham_so[1:]
    if not tham_so:
        raise LoiNguoiDung("Thiếu lệnh. Ví dụ: studio openmontage chay -c \"print(1)\"")
    r = subprocess.run([str(_python_om()), *tham_so], cwd=OM, env=_moi_truong())
    if r.returncode:
        raise SystemExit(r.returncode)


def lenh_cong_cu(a) -> None:
    if not _da_cai():
        raise LoiNguoiDung("OpenMontage chưa cài. Chạy trước: studio openmontage cai")
    ten = a.ten
    if ten not in CONG_CU_OFFLINE:
        raise LoiNguoiDung(f"Công cụ '{ten}' không nằm trong danh sách chạy offline. Dùng được: "
                           + ", ".join(sorted(CONG_CU_OFFLINE)))
    try:
        inputs = json.loads(a.json or "{}")
    except ValueError as e:
        raise LoiNguoiDung(f"Tham số JSON sai: {e}")
    goc: Path | None = None
    for k in KHOA_FILE_VAO:
        v = inputs.get(k)
        if isinstance(v, str) and v:
            if "://" in v:
                raise LoiNguoiDung("Không tải video từ link. Hãy nhờ người dùng lưu video về máy rồi đưa file vào dự án.")
            inputs[k] = str(tim_file(v))
            goc = goc or Path(inputs[k])
    nhap = thu_muc_hom_nay()
    ra = inputs.get("output_path")
    if isinstance(ra, str) and ra and not Path(ra).is_absolute():
        inputs["output_path"] = str(nhap / ra)
    elif not ra and goc is not None and ten not in ("transcriber", "subtitle_gen", "video_analyzer", "frame_sampler",
                                                     "scene_detect", "face_tracker", "audio_energy", "audio_probe",
                                                     "visual_qa"):
        inputs["output_path"] = str(file_ra(goc, ten.replace("_", "-"), ".mp4" if goc.suffix.lower() != ".wav" else ".wav"))
    if not inputs.get("output_dir") and ten in ("transcriber", "video_analyzer", "frame_sampler", "scene_detect",
                                                "face_tracker", "visual_qa"):
        inputs["output_dir"] = str(nhap / f"{ten.replace('_', '-')}-{(goc.stem if goc else 'kq')}"[:80])
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8", dir=CACHE) as f:
        json.dump(inputs, f, ensure_ascii=False)
        tam = Path(f.name)
    try:
        r = subprocess.run([str(_python_om()), "-c", _RUNNER, ten, str(tam)], cwd=OM, env=_moi_truong(),
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    finally:
        tam.unlink(missing_ok=True)
    kq = None
    for dong in r.stdout.splitlines():
        if dong.startswith("JSON_KQ:"):
            kq = json.loads(dong[8:])
    if kq is None:
        loi = [d for d in (r.stderr or "").splitlines() if d.strip() and not d.startswith("objc[")]
        raise LoiNguoiDung(f"Công cụ {ten} lỗi: " + (loi[-1] if loi else "không rõ"))
    if not kq["ok"]:
        raise LoiNguoiDung(f"Công cụ {ten} báo lỗi: {kq['loi']}")
    data = kq.get("data") or {}
    # lưu đầy đủ kết quả (lời thoại, mốc cảnh...) ra file để Claude đọc khi cần, màn hình chỉ in tóm tắt
    nhat_ky = nhap / f"{ten.replace('_', '-')}-{(goc.stem if goc else 'kq')}"[:80]
    nhat_ky = nhat_ky.with_name(nhat_ky.name + ".json")
    nhat_ky.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    ra_file = [Path(p) for p in ([inputs.get("output_path")] if inputs.get("output_path") else []) if Path(p).exists()]
    tom_tat = {k: v for k, v in data.items() if not isinstance(v, (list, dict)) or len(json.dumps(v, default=str)) < 300}
    ket_qua(ra_file or [nhat_ky], du_lieu=str(nhat_ky), **{"tom_tat": tom_tat})
