// Trợ thủ dựng video động HTML (HyperFrames). Chạy bằng: node video-dong-html.mjs <lệnh> ...
//   tao  <tên-dự-án> [mẫu]       -> tạo thư mục làm việc trong .cache/hyperframes-work/<tên>
//   xuat <thư-mục-dự-án> <tên-file> [--nhanh] -> kiểm tra + render ra 02-THANH-PHAM/<hôm-nay>/<tên-file>.mp4 (không ghi đè)
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const skillDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(skillDir, "..", "..", "..");
const tool = path.join(root, "05-CONG-CU-THEM", "hyperframes");
const nm = path.join(tool, "node_modules");
const [lenh, ...args] = process.argv.slice(2);

function loi(msg) { console.error("LOI: " + msg); process.exit(2); }
if (!fs.existsSync(path.join(nm, "hyperframes"))) loi("Chưa cài HyperFrames. Làm theo mục 'Cài đặt' trong SKILL.md.");

const ext = process.platform === "win32" ? ".exe" : "";

function findOnPath(bin) {
  try {
    const cmd = process.platform === "win32" ? "where" : "which";
    const res = spawnSync(cmd, [bin], { encoding: "utf8" });
    if (res.status === 0 && res.stdout) {
      const first = res.stdout.trim().split(/\r?\n/)[0]?.trim();
      if (first && fs.existsSync(first)) return first;
    }
  } catch {}
  return null;
}

function findImageioFfmpeg() {
  const cacheFile = path.join(root, ".cache", "imageio-ffmpeg-path.txt");
  try {
    if (fs.existsSync(cacheFile)) {
      const p = fs.readFileSync(cacheFile, "utf8").trim();
      if (p && fs.existsSync(p)) return p;
    }
  } catch {}
  try {
    const res = spawnSync("uv", ["run", "python", "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"], {
      cwd: root,
      encoding: "utf8",
    });
    if (res.status === 0 && res.stdout) {
      const p = res.stdout.trim().split(/\r?\n/)[0]?.trim();
      if (p && fs.existsSync(p)) {
        try {
          fs.mkdirSync(path.join(root, ".cache"), { recursive: true });
          fs.writeFileSync(cacheFile, p, "utf8");
        } catch {}
        return p;
      }
    }
  } catch {}
  return null;
}

let ffmpegPath = process.env.HYPERFRAMES_FFMPEG_PATH && fs.existsSync(process.env.HYPERFRAMES_FFMPEG_PATH)
  ? process.env.HYPERFRAMES_FFMPEG_PATH
  : (process.env.HYPERFRAMES_FFMPEG_PATH || null);
if (!ffmpegPath) ffmpegPath = findOnPath("ffmpeg");
if (!ffmpegPath) ffmpegPath = findImageioFfmpeg();
if (!ffmpegPath) {
  const staticFfmpeg = path.join(nm, "ffmpeg-static", "ffmpeg" + ext);
  if (fs.existsSync(staticFfmpeg)) ffmpegPath = staticFfmpeg;
}

let ffprobePath = process.env.HYPERFRAMES_FFPROBE_PATH && fs.existsSync(process.env.HYPERFRAMES_FFPROBE_PATH)
  ? process.env.HYPERFRAMES_FFPROBE_PATH
  : (process.env.HYPERFRAMES_FFPROBE_PATH || null);
if (!ffprobePath) ffprobePath = findOnPath("ffprobe");
if (!ffprobePath) {
  const staticFfprobe = path.join(nm, "ffprobe-static", "bin", process.platform, process.arch, "ffprobe" + ext);
  if (fs.existsSync(staticFfprobe)) ffprobePath = staticFfprobe;
}

const pathDirs = [];
if (ffmpegPath) pathDirs.push(path.dirname(ffmpegPath));
if (ffprobePath) pathDirs.push(path.dirname(ffprobePath));
if (process.env.PATH) pathDirs.push(...process.env.PATH.split(path.delimiter));
pathDirs.push(path.join(nm, "ffmpeg-static"));
pathDirs.push(path.join(nm, "ffprobe-static", "bin", process.platform, process.arch));
const uniquePath = [...new Set(pathDirs.filter(Boolean))].join(path.delimiter);

const env = {
  ...process.env,
  HYPERFRAMES_NO_TELEMETRY: "1",
  DO_NOT_TRACK: "1",
  HYPERFRAMES_SKIP_SKILLS: "1",
  PATH: uniquePath,
  ...(ffmpegPath ? { HYPERFRAMES_FFMPEG_PATH: ffmpegPath } : {}),
  ...(ffprobePath ? { HYPERFRAMES_FFPROBE_PATH: ffprobePath } : {}),
};
const cli = path.join(nm, "hyperframes", "bin", "hyperframes.mjs");
const hf = (cwd, a) => spawnSync(process.execPath, [cli, ...a], { cwd, env, stdio: "inherit" }).status;

if (lenh === "tao") {
  const [ten, mau = "khuyen-mai-doc"] = args;
  if (!ten) loi("Thiếu tên dự án.");
  const src = path.join(skillDir, "templates", mau);
  if (!fs.existsSync(src)) loi("Không có mẫu: " + mau);
  const dst = path.join(root, ".cache", "hyperframes-work", ten);
  if (fs.existsSync(dst)) loi("Thư mục đã tồn tại, đặt tên khác: " + dst);
  fs.cpSync(src, dst, { recursive: true });
  fs.mkdirSync(path.join(dst, "vendor"), { recursive: true });
  fs.copyFileSync(path.join(nm, "gsap", "dist", "gsap.min.js"), path.join(dst, "vendor", "gsap.min.js"));
  fs.copyFileSync(path.join(nm, "three", "build", "three.min.js"), path.join(dst, "vendor", "three.min.js"));
  fs.cpSync(path.join(root, "assets", "fonts"), path.join(dst, "fonts"), { recursive: true });
  fs.mkdirSync(path.join(dst, "assets"), { recursive: true });
  fs.writeFileSync(path.join(dst, "meta.json"), JSON.stringify({ id: ten, name: ten }));
  fs.writeFileSync(path.join(dst, "hyperframes.json"), JSON.stringify({ paths: { blocks: "compositions", components: "compositions/components", assets: "assets" }, media: { autoProxy: false } }));
  console.log("KET QUA: " + dst);
} else if (lenh === "xuat") {
  const [dir, ten] = args;
  const nhanh = args.includes("--nhanh");
  if (!dir || !ten) loi("Cách dùng: xuat <thư-mục-dự-án> <tên-file>");
  if (hf(dir, ["check"]) !== 0) loi("Kiểm tra bố cục báo lỗi, sửa rồi chạy lại.");
  const d = new Date(); const p2 = (n) => String(n).padStart(2, "0");
  const ngay = `${d.getFullYear()}-${p2(d.getMonth() + 1)}-${p2(d.getDate())}`;
  const outDir = path.join(root, "02-THANH-PHAM", ngay);
  fs.mkdirSync(outDir, { recursive: true });
  let out = path.join(outDir, ten + ".mp4"), i = 2;
  while (fs.existsSync(out)) out = path.join(outDir, `${ten}_${i++}.mp4`);
  if (hf(dir, ["render", "-o", out, ...(nhanh ? ["-q", "draft"] : [])]) !== 0 || !fs.existsSync(out)) { console.error("LOI: render thất bại"); process.exit(1); }
  console.log("KET QUA: " + out);
} else loi("Lệnh: tao | xuat");
