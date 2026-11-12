// Render mỗi dòng trong file JSON/CSV thành 1 video MP4.
// Dùng:  node scripts/render-batch.mjs <du-lieu.json|csv> <thu-muc-dau-ra> [--chung="{...json props chung...}"]
// Cột đặc biệt: "ten-file" (tên file kết quả), "image" (đường dẫn ảnh sản phẩm - tự chép vào public/imgs).
// Không bao giờ ghi đè: nếu trùng tên sẽ thêm _2, _3...
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const args = process.argv.slice(2);
const chungArg = (args.find((a) => a.startsWith('--chung=')) || '--chung={}').slice(8);
// --chung=@duong-dan.json (khuyên dùng trên Windows) hoặc --chung={...json...}
const common = JSON.parse(chungArg.startsWith('@') ? fs.readFileSync(chungArg.slice(1), 'utf8').replace(/^\uFEFF/, '') : chungArg);
const [dataFile, outDir] = args.filter((a) => !a.startsWith('--'));
if (!dataFile || !outDir) {
  console.error('Thiếu tham số: node scripts/render-batch.mjs <du-lieu.json|csv> <thu-muc-dau-ra>');
  process.exit(2);
}

function parseCsv(text) {
  const rows = [];
  let cur = [''], q = false;
  text = text.replace(/^﻿/, '');
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"' && text[i + 1] === '"') { cur[cur.length - 1] += '"'; i++; }
      else if (c === '"') q = false;
      else cur[cur.length - 1] += c;
    } else if (c === '"') q = true;
    else if (c === ',' || c === ';') cur.push('');
    else if (c === '\n') { rows.push(cur); cur = ['']; }
    else if (c !== '\r') cur[cur.length - 1] += c;
  }
  if (cur.length > 1 || cur[0] !== '') rows.push(cur);
  const head = rows.shift().map((h) => h.trim());
  return rows.filter((r) => r.some((x) => x.trim())).map((r) => Object.fromEntries(head.map((h, i) => [h, (r[i] ?? '').trim()])));
}

const raw = fs.readFileSync(dataFile, 'utf8');
const items = dataFile.toLowerCase().endsWith('.csv') ? parseCsv(raw) : JSON.parse(raw.replace(/^﻿/, ''));

fs.mkdirSync(outDir, {recursive: true});
fs.mkdirSync(path.join(root, 'public', 'imgs'), {recursive: true});

const slug = (s) =>
  String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D')
    .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'video';
const freeName = (base) => {
  let n = base, i = 2;
  while (fs.existsSync(path.join(outDir, n + '.mp4'))) n = `${base}_${i++}`;
  return n;
};

console.log(`Đang chuẩn bị (${items.length} video)...`);
const serveUrl = await bundle({entryPoint: path.join(root, 'src', 'index.ts'), webpackOverride: (c) => c});
const results = [];
for (let i = 0; i < items.length; i++) {
  const {['ten-file']: tenFile, image, ...rest} = items[i];
  const props = {...common, ...rest};
  if (image) {
    const ext = path.extname(image);
    const imgName = `${slug(tenFile || rest.name || i)}-${i}${ext}`;
    fs.copyFileSync(path.resolve(image), path.join(root, 'public', 'imgs', imgName));
    props.image = imgName;
  }
  const composition = await selectComposition({serveUrl, id: 'ProductCard', inputProps: props});
  const out = path.join(outDir, freeName(slug(tenFile || rest.name || `video-${i + 1}`)) + '.mp4');
  await renderMedia({
    composition, serveUrl, codec: 'h264', outputLocation: out, inputProps: props,
    ...(process.env.REMOTION_LICENSE_KEY ? {licenseKey: process.env.REMOTION_LICENSE_KEY} : {}),
    isProduction: process.env.REMOTION_TEST !== '1',
    onProgress: ({progress}) => process.stdout.write(`\r  [${i + 1}/${items.length}] ${Math.round(progress * 100)}%   `),
  });
  console.log(`\n  Xong: ${out}`);
  results.push(out);
}
console.log('KET QUA: ' + results.join(' | '));
