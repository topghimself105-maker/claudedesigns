#!/usr/bin/env python3
"""Dutch transcript of an audio/video file or one fragment of it -> .txt, .srt, .docx, .pdf in out/transcripts/.
Usage: python3 studio/transcribe.py <file> [--start 0:00] [--end 30:00] [--model small] [--lang nl]
Long files are processed in 5-minute chunks; the .txt/.srt are rewritten after every chunk so partial results survive."""
import argparse, os, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

def secs(s):
    p = [float(x) for x in s.split(':')]
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
def ts(t, comma=False):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',' if comma else '.') if comma else f"{h:d}:{m:02d}:{int(s):02d}" if h else f"{m:d}:{int(s):02d}"

ap = argparse.ArgumentParser()
ap.add_argument('file'); ap.add_argument('--start', default='0'); ap.add_argument('--end')
ap.add_argument('--model', default='small'); ap.add_argument('--lang', default='nl')
ap.add_argument('--title'); ap.add_argument('--outdir', default='out/transcripts')
a = ap.parse_args()
name = os.path.splitext(os.path.basename(a.file))[0]
title = a.title or name
os.makedirs(a.outdir, exist_ok=True)
base = os.path.join(a.outdir, name)
start = secs(a.start)
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.file]))
end = secs(a.end) if a.end else dur
end = min(end, dur)
CH = 300.0
model = WhisperModel(a.model, device='cpu', compute_type='int8', cpu_threads=os.cpu_count())
segs = []

def save():
    with open(base + '.txt', 'w', encoding='utf-8') as f:
        f.write(f"{title}\nFragment {ts(start)} - {ts(end)}\n\n")
        for s in segs: f.write(f"[{ts(s[0])}] {s[2]}\n")
    with open(base + '.srt', 'w', encoding='utf-8') as f:
        for i, s in enumerate(segs, 1):
            f.write(f"{i}\n{ts(s[0], True)} --> {ts(s[1], True)}\n{s[2]}\n\n")

pos = start
while pos < end:
    d = min(CH, end - pos)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(pos), '-t', str(d), '-i', a.file, '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], check=True, stdout=subprocess.PIPE).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    it, _ = model.transcribe(audio, language=a.lang, vad_filter=True, beam_size=5, condition_on_previous_text=False)
    for s in it:
        t = s.text.strip()
        if t: segs.append((pos + s.start, pos + s.end, t))
    pos += d
    save()
    print(f"{ts(pos)} / {ts(end)}  ({len(segs)} segments)", flush=True)
save()

# DOCX: one paragraph per ~60 s block with a timestamp heading, then PDF via LibreOffice
from docx import Document
from docx.shared import Pt
doc = Document()
doc.styles['Normal'].font.name = 'Calibri'; doc.styles['Normal'].font.size = Pt(11)
doc.add_heading(title, 1)
doc.add_paragraph(f"Transcript (Nederlands), fragment {ts(start)} - {ts(end)}. Automatisch gegenereerd met Whisper ({a.model}); controleer namen en vakwoorden.")
blk, buf = None, []
def flush():
    if buf: doc.add_paragraph(' '.join(buf))
for s in segs:
    b = int((s[0] - start) // 60)
    if b != blk:
        flush(); buf = []; blk = b
        doc.add_heading(ts(s[0]), 3)
    buf.append(s[2])
flush()
doc.save(base + '.docx')
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', a.outdir, base + '.docx'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('klaar:', ', '.join(base + e for e in ('.txt', '.srt', '.docx', '.pdf')))
