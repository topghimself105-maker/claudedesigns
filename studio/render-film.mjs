// node studio/render-film.mjs <film> <layout> [--reduced] [--fps N] [--name file.mp4] [--audio-only]
// Headless Chrome steps t = n/fps, pipes PNG frames to ffmpeg (libx264, crf 16, yuv420p, BT.709 tagged).
// If the film exposes window.renderAudio() (Web Audio, rendered offline) the PCM is written to out/<film>/audio.wav.
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const a = process.argv.slice(2), film = a[0], layout = a[1];
const flag = n => a.includes(n), opt = n => { const i = a.indexOf(n); return i > -1 ? a[i + 1] : undefined; };
const reduced = flag('--reduced'), audioOnly = flag('--audio-only');
const out = resolve(here, '../out', film); mkdirSync(out, { recursive: true });
const sizes = { '16x9': [1920, 1080], '1x1': [1080, 1080], '9x16': [1080, 1920], '4x5': [1080, 1350] }, [W, H] = sizes[layout];
const url = `file://${resolve(here, 'films', film, 'index.html')}?layout=${layout}${reduced ? '&reduced=1' : ''}`;
const browser = await chromium.launch({ args: ['--no-sandbox'] });
const page = await (await browser.newContext({ viewport: { width: W, height: H } })).newPage();
page.on('pageerror', e => { console.error('PAGE ERROR', e.message); process.exit(1); });
await page.goto(url); await page.evaluate(() => window.READY || document.fonts.ready);
const tl = await page.evaluate(() => window.TIMELINE);
const fps = +(opt('--fps') || tl.fps);
if (tl.captions && tl.captions.length) {
  const f = s => new Date(Math.round(s * 1000)).toISOString().slice(11, 23).replace('.', ',');
  writeFileSync(resolve(out, 'captions.srt'), tl.captions.map(([s, e, l], i) => `${i + 1}\n${f(s)} --> ${f(e)}\n${l.join('\n')}\n`).join('\n'));
}
writeFileSync(resolve(out, 'timeline.json'), JSON.stringify(tl, null, 1));
if (audioOnly || (await page.evaluate(() => typeof window.renderAudio)) === 'function' && flag('--with-audio')) {
  const r = await page.evaluate(() => window.renderAudio());
  const pcm = Buffer.from(r.b64, 'base64'), hdr = Buffer.alloc(44);
  hdr.write('RIFF', 0); hdr.writeUInt32LE(36 + pcm.length, 4); hdr.write('WAVEfmt ', 8); hdr.writeUInt32LE(16, 16); hdr.writeUInt16LE(1, 20); hdr.writeUInt16LE(1, 22);
  hdr.writeUInt32LE(r.sampleRate, 24); hdr.writeUInt32LE(r.sampleRate * 2, 28); hdr.writeUInt16LE(2, 32); hdr.writeUInt16LE(16, 34); hdr.write('data', 36); hdr.writeUInt32LE(pcm.length, 40);
  writeFileSync(resolve(out, 'audio_raw.wav'), Buffer.concat([hdr, pcm])); console.log('audio ->', resolve(out, 'audio_raw.wav'));
}
if (!audioOnly) {
  const name = opt('--name') || `${layout}${reduced ? '_reduced' : ''}.mp4`, file = resolve(out, name.replace(/\.mp4$/, '.silent.mp4'));
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-vf', 'scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int+bitexact,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-r', String(fps), '-movflags', '+faststart', file], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round(tl.duration * fps);
  for (let i = 0; i < n; i++) { await page.evaluate(t => window.seek(t), i / fps); const buf = await page.screenshot({ type: 'png' }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log('video ->', file, n, 'frames @', fps);
}
await browser.close();
