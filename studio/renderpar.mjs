// node studio/renderpar.mjs <film> <layout> [workers] [audio.wav]  ->  out/<film>_<layout>.silent.mp4 (+ _final.mp4 when audio is given)
// Same pixels as render.mjs, but the frame range is split across parallel Chromium workers, each piping to its own ffmpeg; segments are joined without re-encoding.
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { spawn, spawnSync } from 'node:child_process';
import { writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const [film = 'f369-engine', layout = '16x9', workersArg = '4', audio] = process.argv.slice(2);
const workers = +workersArg, out = resolve(here, '../out');
mkdirSync(out, { recursive: true });
const sizes = { '9x16': [1080, 1920], '4x5': [1080, 1350], '1x1': [1080, 1080], '16x9': [1920, 1080] }, [W, H] = sizes[layout];
const url = `file://${resolve(here, 'films', film, 'index.html')}?layout=${layout}`;
const seg = resolve(out, `.seg_${film}_${layout}`);
rmSync(seg, { recursive: true, force: true });
mkdirSync(seg, { recursive: true });

const probe = await chromium.launch({ args: ['--no-sandbox'] });
const pp = await (await probe.newContext({ viewport: { width: W, height: H } })).newPage();
await pp.goto(url);
await pp.evaluate(() => window.__ready || document.fonts.ready);
const tl = await pp.evaluate(() => window.TIMELINE);
await probe.close();
writeFileSync(resolve(out, `${film}.cues.json`), JSON.stringify(tl));
const srt = tl.captions.map(([a, b, l], i) => {
  const f = s => new Date(s * 1000).toISOString().slice(11, 23).replace('.', ',');
  return `${i + 1}\n${f(a)} --> ${f(b)}\n${l.join('\n')}\n`;
}).join('\n');
if (tl.captions.length) writeFileSync(resolve(out, `${film}.srt`), srt);

const n = Math.round(tl.duration * tl.fps), per = Math.ceil(n / workers);
async function work(k) {
  const a = k * per, b = Math.min(n, a + per), file = resolve(seg, `s${k}.mp4`);
  const br = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await (await br.newContext({ viewport: { width: W, height: H } })).newPage();
  await page.goto(url);
  await page.evaluate(() => window.__ready || document.fonts.ready);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(tl.fps), '-i', '-',
    '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int+bitexact,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'fast', '-profile:v', 'high', '-crf', '14', '-maxrate', '16M', '-bufsize', '32M',
    '-x264-params', 'keyint=60:scenecut=0', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-r', String(tl.fps), file], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = a; i < b; i++) {
    await page.evaluate(t => window.seek(t), i / tl.fps);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await br.close();
  return file;
}

const files = await Promise.all(Array.from({ length: workers }, (_, k) => work(k)));
writeFileSync(resolve(seg, 'list.txt'), files.map(f => `file '${f}'`).join('\n'));
const silent = resolve(out, `${film}_${layout}.silent.mp4`);
spawnSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', resolve(seg, 'list.txt'), '-c', 'copy', silent], { stdio: 'inherit' });
console.log('silent video ->', silent);
if (audio) {
  const fin = resolve(out, `${film}_${layout}_final.mp4`);
  spawnSync('ffmpeg', ['-v', 'error', '-y', '-i', silent, '-i', audio, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', '-movflags', '+faststart', fin], { stdio: 'inherit' });
  console.log('final ->', fin);
}
rmSync(seg, { recursive: true, force: true });
