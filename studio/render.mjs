// node studio/render.mjs <film> <layout> [reduced]   ->  out/<film>_<layout>[_reduced].mp4 (+ audio, + captions.srt)
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { spawn, spawnSync } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const [film = 'signal-to-fill', layout = '1x1', reduced] = process.argv.slice(2);
const tag = `${layout}${reduced ? '_reduced' : ''}`;
const out = resolve(here, '../out'); mkdirSync(out, { recursive: true });
const url = `file://${resolve(here, 'films', film, 'index.html')}?layout=${layout}${reduced ? '&reduced=1' : ''}`;
const sizes = { '4x5': [1080, 1350], '1x1': [1080, 1080], '9x16': [1080, 1920], '16x9': [1920, 1080] }, [W, H] = sizes[layout];

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] }).catch(() => chromium.launch({ args: ['--no-sandbox'] }));
const page = await (await browser.newContext({ viewport: { width: W, height: H } })).newPage();
await page.goto(url); await page.evaluate(() => document.fonts.ready);
const tl = await page.evaluate(() => window.TIMELINE);
writeFileSync(resolve(out, `${film}.cues.json`), JSON.stringify(tl));
const srt = tl.captions.map(([a, b, l], i) => { const f = s => new Date(s * 1000).toISOString().slice(11, 23).replace('.', ','); return `${i + 1}\n${f(a)} --> ${f(b)}\n${l.join('\n')}\n`; }).join('\n');
writeFileSync(resolve(out, `${film}.srt`), srt);

const silent = resolve(out, `${film}_${tag}.silent.mp4`);
const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(tl.fps), '-i', '-', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', String(tl.fps), silent], { stdio: ['pipe', 'inherit', 'inherit'] });
const n = Math.round(tl.duration * tl.fps);
for (let i = 0; i < n; i++) {
  await page.evaluate(t => window.seek(t), i / tl.fps);
  const buf = await page.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await browser.close();
console.log('silent video ->', silent);
