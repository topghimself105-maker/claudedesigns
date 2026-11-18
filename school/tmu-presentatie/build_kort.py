# The Matrix Unlocked – Mijn stage (korte versie, ±10 minuten, 8 dia's, 16:9, Nederlands)
# Bouwt TMU_Bedrijfsprofiel_Stagegids.pptx met python-pptx. Alle tekst, vormen en diagrammen zijn bewerkbaar.
# Huisstijl afgeleid van thematrixunlocked.com: zwarte achtergrond, groen #16E36F, lettertype Outfit.
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = lambda p: os.path.join(HERE, 'assets', p)
OUT = os.path.join(HERE, 'TMU_Mijn_Stage_10min.pptx')

GREEN = RGBColor(0x16, 0xE3, 0x6F)
WHITE = RGBColor(0xF4, 0xF6, 0xF5)
GREY = RGBColor(0xA6, 0xAE, 0xAA)
DIM = RGBColor(0x6B, 0x74, 0x70)
CARD = RGBColor(0x0D, 0x0E, 0x10)
CARD2 = RGBColor(0x0B, 0x1A, 0x11)
LINE = RGBColor(0x1E, 0x2A, 0x24)
BLACK = RGBColor(0x00, 0x00, 0x00)
F_LIGHT, F_REG, F_SEMI, F_XB = 'Outfit Light', 'Outfit', 'Outfit SemiBold', 'Outfit ExtraBold'
SRC_SITE = 'Bron: thematrixunlocked.com (geraadpleegd november 2026)'

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
TOTAL = 8


def txt(s, x, y, w, h, parts, size=14, font=F_LIGHT, color=WHITE, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        spacing=1.1, space_after=0, bold=False):
    """parts: str, or list of paragraphs; a paragraph is str or list of (text, dict) runs."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = parts if isinstance(parts, list) else [parts]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        runs = para if isinstance(para, list) else [(para, {})]
        for t, o in runs:
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = o.get('font', font)
            f.size = Pt(o.get('size', size))
            f.color.rgb = o.get('color', color)
            f.bold = o.get('bold', bold)
    return tb


def box(s, x, y, w, h, fill=CARD, line=LINE, radius=0.08, lw=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = radius
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    sh.text_frame.margin_left = sh.text_frame.margin_right = 0
    return sh


def pill(s, x, y, text, color=GREEN, size=9, w=None, filled=False):
    w = w or (0.16 + len(text) * size * 0.0072)
    b = box(s, x, y, w, 0.28, fill=(color if filled else CARD2), line=color, radius=0.5, lw=0.75)
    tf = b.text_frame
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name, r.font.size, r.font.color.rgb = F_SEMI, Pt(size), (BLACK if filled else color)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return b


def img(s, path, x, y, w=None, h=None):
    kw = {}
    if w: kw['width'] = Inches(w)
    if h: kw['height'] = Inches(h)
    return s.shapes.add_picture(A(path), Inches(x), Inches(y), **kw)


def eyebrow(s, x, y, text):
    txt(s, x, y, 8, 0.3, text.upper(), size=10.5, font=F_SEMI, color=GREEN)


def title(s, text, sub=None, x=0.7, y=0.62, w=11.9):
    txt(s, x, y, w, 0.75, text, size=32, font=F_XB, color=WHITE, spacing=1.0)
    if sub:
        txt(s, x, y + 0.72, w, 0.45, sub, size=14, font=F_LIGHT, color=GREY)


def slide(bg='bg.png', n=None):
    s = prs.slides.add_slide(BLANK)
    s.shapes.add_picture(A('img/' + bg), 0, 0, prs.slide_width, prs.slide_height)
    if n:
        img(s, 'img/logo_mark.png', 0.7, 7.02, h=0.24)
        txt(s, 1.02, 7.05, 6, 0.25, 'The Matrix Unlocked  ·  Mijn stage', size=9, color=DIM)
        txt(s, 11.9, 7.05, 0.73, 0.25, f'{n:02d} / {TOTAL}', size=9, color=DIM, align=PP_ALIGN.RIGHT)
    return s


def source(s, text, x=0.7, y=6.72, w=8):
    txt(s, x, y, w, 0.22, text, size=8.5, color=DIM)


def bullets(s, x, y, w, h, items, size=11, color=GREY, bullet_color=GREEN, spacing=1.05, gap=3):
    paras = [[('▪  ', {'color': bullet_color, 'font': F_SEMI, 'size': size - 1}), (it, {})] for it in items]
    return txt(s, x, y, w, h, paras, size=size, color=color, spacing=spacing, space_after=gap)



def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def card(s, x, y, w, h, head, body, accent=False, head_size=15, body_size=11.5):
    box(s, x, y, w, h, fill=(CARD2 if accent else CARD), line=(GREEN if accent else LINE), lw=(1 if accent else 0.75))
    box(s, x, y + 0.22, 0.05, 0.5, fill=GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
    txt(s, x + 0.28, y + 0.2, w - 0.5, 0.4, head, size=head_size, font=F_SEMI, color=WHITE)
    if body:
        if isinstance(body, list):
            bullets(s, x + 0.28, y + 0.68, w - 0.5, h - 0.8, body, size=body_size, gap=3)
        else:
            txt(s, x + 0.28, y + 0.66, w - 0.5, h - 0.8, body, size=body_size, color=GREY, spacing=1.15)


# ---------------------------------------------------------------- 1 COVER  (±0:30)
s = slide('bg_cover.png')
img(s, 'img/logo_wordmark.png', 0.7, 0.62, h=0.62)
txt(s, 0.7, 2.4, 7.4, 0.35, 'STAGEPRESENTATIE  ·  INTERNATIONAL BUSINESS', size=11, font=F_SEMI, color=GREEN)
txt(s, 0.7, 2.85, 7.6, 2.0, ['MIJN STAGE BIJ', 'THE MATRIX', 'UNLOCKED'], size=48, font=F_XB, color=WHITE, spacing=0.92)
box(s, 0.7, 5.25, 0.9, 0.04, fill=GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
txt(s, 0.7, 5.5, 7.4, 0.9, [
    [('NHL Stenden', {'font': F_SEMI, 'color': WHITE})],
    [('International Business', {})],
    [('[Naam student]  ·  [Studentnummer]', {'color': DIM})]], size=12, color=GREY, spacing=1.15)
notes(s, 'Kort voorstellen: naam, opleiding, waar ik stage loop. (±30 sec)')

# ---------------------------------------------------------------- 2 TMU IN HET KORT  (±1:00)
s = slide('bg.png', 2)
eyebrow(s, 0.7, 0.42, 'Het bedrijf in één minuut')
title(s, 'The Matrix Unlocked')
txt(s, 0.7, 1.75, 6.6, 1.3,
    'Een trading-educatiebedrijf en community. Traders leren er het Time & Price-framework, '
    'via een 12-weeks programma met persoonlijke 1-op-1 coaching.',
    size=17, color=WHITE, spacing=1.2)
facts = [('12 weken', '1-op-1 coaching'), ('400+', 'studenten gecoacht'), ('4,92/5', 'gemiddelde beoordeling')]
for i, (big, small) in enumerate(facts):
    fx = 0.7 + i * 2.25
    txt(s, fx, 3.55, 2.1, 0.6, big, size=30, font=F_XB, color=GREEN)
    txt(s, fx, 4.2, 2.1, 0.35, small, size=11.5, color=GREY)
txt(s, 0.7, 5.0, 6.6, 0.9,
    [[('Volledig online bedrijf ', {'font': F_SEMI, 'color': WHITE}),
      ('met een community, eigen tools en in-person events.', {})]], size=13, color=GREY, spacing=1.2)
pic = img(s, 'img/frank.jpg', 8.05, 1.62, w=4.6)
pic.crop_left, pic.crop_right, pic.crop_top, pic.crop_bottom = 0.2, 0.2, 0.06, 0.152
pic.width, pic.height = Inches(4.6), Inches(3.4)
box(s, 8.05, 5.0, 4.6, 1.05, fill=CARD, line=LINE, radius=0.04)
txt(s, 8.3, 5.15, 4.2, 0.35, 'Frank Warrink (Frank369)', size=15, font=F_SEMI, color=WHITE)
txt(s, 8.3, 5.5, 4.2, 0.3, 'Founder & Head Coach', size=11, color=GREEN)
source(s, 'Bron: thematrixunlocked.com. Cijfers zoals vermeld door het bedrijf zelf.')
notes(s, 'Alleen de context: wat TMU doet en wie Frank is. Niet te lang bij stilstaan. (±1 min)')

# ---------------------------------------------------------------- 3 WAT IK DOE  (±2:00)
s = slide('bg_alt.png', 3)
eyebrow(s, 0.7, 0.42, 'Mijn stage')
title(s, 'Wat ik doe', 'Mijn rol groeide uit tot een mix van sales, marketing, creatief werk en business development.')
R = [('Sales & Client Success', ['Contact met bestaande en nieuwe klanten', 'Leads opvolgen en kwalificeren',
                                  'Calls inplannen met sales of de leiding', 'Klantrelaties onderhouden']),
     ('Marketing & leadgeneratie', ['Webinarcampagnes en lead nurturing', 'Opvolging van webinardeelnemers',
                                     'Een extra kanaal op X (Twitter) opbouwen', 'Nieuwe marketingkansen verkennen']),
     ('Creatief & funnels', ['Funnels mee ontwikkelen en verbeteren', 'De klantreis begrijpen en verbeteren',
                             'Creatieve marketingprojecten']),
     ('Business development', ['Nieuw communicatie- en belsysteem mee invoeren', 'Kennismaking met AI-ontwikkeling',
                               'Werken naast de leiding'])]
cw, ch = 5.9, 2.05
for i, (h, its) in enumerate(R):
    card(s, 0.7 + (i % 2) * 6.03, 2.0 + (i // 2) * 2.2, cw, ch, h, its, accent=(i == 0), head_size=16, body_size=12.5)
notes(s, 'Per blok één concreet voorbeeld uit mijn eigen werk noemen. Begin bij sales: dat is de kern van mijn rol. (±2 min)')

# ---------------------------------------------------------------- 4 MIJN ROL IN DE KLANTREIS  (±1:30)
s = slide('bg.png', 4)
eyebrow(s, 0.7, 0.42, 'Hoe mijn werk samenhangt')
title(s, 'Mijn rol in de klantreis')
stages = [('Aantrekken', 'Social media (o.a. X), webinars'), ('Opvolgen', 'Webinar- en marketingleads opvolgen'),
          ('Kwalificeren', 'De situatie van de lead begrijpen'), ('Gesprek', 'Calls inplannen met sales of de leiding'),
          ('Conversie', 'High-ticket verkoop van het programma'), ('Klant', 'Relatie onderhouden na de aankoop')]
sw = 1.92
for i, (h, t) in enumerate(stages):
    sx = 0.7 + i * (sw + 0.08)
    hl = i == 4
    box(s, sx, 2.2, sw, 0.75, fill=(GREEN if hl else CARD2), line=GREEN, radius=0.5)
    txt(s, sx, 2.2, sw, 0.75, h, size=14, font=F_SEMI, color=(BLACK if hl else WHITE), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, sx + 0.1, 3.15, sw - 0.2, 0.9, t, size=11, color=GREY, align=PP_ALIGN.CENTER, spacing=1.12)
box(s, 0.7, 4.55, 11.93, 1.55, fill=CARD, line=LINE)
txt(s, 1.0, 4.78, 11.4, 1.2,
    [[('Wat dit me leert: ', {'font': F_SEMI, 'color': GREEN}),
      ('ik zie het hele commerciële proces van dichtbij, van de eerste interesse tot een tevreden klant. '
       'Daardoor begrijp ik hoe marketing, sales en klantcontact op elkaar aansluiten.', {})]],
    size=15, color=WHITE, spacing=1.25)
notes(s, 'Laten zien dat ik in elke fase meewerk. Benadruk high-ticket sales (groen). (±1,5 min)')

# ---------------------------------------------------------------- 5 DE WERKOMGEVING  (±1:30)
s = slide('bg_center.png', 5)
eyebrow(s, 0.7, 0.42, 'De werkomgeving')
txt(s, 0.7, 0.9, 12, 1.4, ['Snel. Kort.', 'Altijd in beweging.'], size=46, font=F_XB, color=WHITE, spacing=0.95)
E = [('Meetings op korte termijn', 'Een overleg kan dezelfde dag worden ingepland. Je moet dan direct klaarstaan.'),
     ('Prioriteiten veranderen snel', 'Wat vandaag belangrijk is, kan morgen anders zijn. Plannen staan nooit helemaal vast.'),
     ('Snel schakelen', 'Je werkt aan meerdere dingen tegelijk en moet snel van taak kunnen wisselen.'),
     ('Korte lijnen', 'Direct contact met de leiding: beslissingen worden snel genomen.')]
for i, (h, b) in enumerate(E):
    card(s, 0.7 + (i % 2) * 6.03, 2.85 + (i // 2) * 1.75, 5.9, 1.6, h, b, accent=(i == 0), head_size=16, body_size=12)
source(s, 'Gebaseerd op mijn eigen ervaring tijdens de stage.')
notes(s, 'Een eigen voorbeeld geven van een meeting die kort van tevoren werd gepland of een prioriteit die ineens veranderde. (±1,5 min)')

# ---------------------------------------------------------------- 6 DE CULTUUR  (±2:00)
s = slide('bg_alt.png', 6)
eyebrow(s, 0.7, 0.42, 'De cultuur')
title(s, 'Wat deze omgeving van je vraagt')
C2 = [('Aanpassingsvermogen', 'Meebewegen als plannen veranderen, zonder dat je werk eronder lijdt.'),
      ('De wil om te leren', 'Nieuwe systemen, nieuwe taken: je leert vooral door het gewoon te doen.'),
      ('Snel kunnen bewegen', 'Niet afwachten, maar direct oppakken wat er ligt.'),
      ('Initiatief & verantwoordelijkheid', 'Zelf zien wat er moet gebeuren en het eigenaarschap nemen.')]
for i, (h, b) in enumerate(C2):
    card(s, 0.7, 1.75 + i * 1.12, 6.9, 1.0, h, None, accent=(i < 2), head_size=16)
    txt(s, 0.98, 1.75 + i * 1.12 + 0.58, 6.4, 0.4, b, size=12.5, color=GREY)
box(s, 8.0, 1.75, 4.63, 4.36, fill=CARD2, line=GREEN, lw=1)
txt(s, 8.3, 2.0, 4.1, 0.35, 'MIJN ERVARING', size=10.5, font=F_SEMI, color=GREEN)
txt(s, 8.3, 2.45, 4.1, 3.5,
    ['Het tempo was in het begin wennen.',
     '',
     'Door me snel aan te passen en vragen te durven stellen, kreeg ik steeds meer verantwoordelijkheid: '
     'van leads opvolgen tot high-ticket sales en het invoeren van nieuwe systemen.'],
    size=14, color=WHITE, spacing=1.25)
notes(s, 'Het belangrijkste deel: de cultuur. Vertel eerlijk hoe het voor mij was en wat ik heb moeten leren. '
         'Pas de tekst in het groene vak aan als die niet precies klopt met mijn ervaring. (±2 min)')

# ---------------------------------------------------------------- 7 WAT IK MEENEEM  (±1:30)
s = slide('bg.png', 7)
eyebrow(s, 0.7, 0.42, 'Terugblik')
title(s, 'Wat ik meeneem', 'De koppeling met International Business.')
K = [('Sales', 'gesprekken voeren, high-ticket verkoop'), ('Marketing', 'funnels, campagnes en social media'),
     ('Klantrelaties', 'leads opvolgen en klanten begeleiden'), ('Digital business', 'een volledig online businessmodel'),
     ('Ondernemerschap', 'initiatief nemen in een snelle omgeving'), ('Aanpassingsvermogen', 'snel schakelen als alles verandert')]
for i, (h, b) in enumerate(K):
    x, y = 0.7 + (i % 3) * 4.02, 2.05 + (i // 3) * 2.05
    img(s, 'icons/check.png', x, y + 0.08, h=0.36)
    txt(s, x + 0.55, y, 3.3, 0.45, h, size=18, font=F_SEMI, color=WHITE)
    txt(s, x + 0.55, y + 0.5, 3.3, 0.8, b, size=12.5, color=GREY, spacing=1.15)
box(s, 0.7, 6.15, 11.93, 0.04, fill=GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
notes(s, 'Kort koppelen aan mijn studie: wat heb ik geleerd dat ik later meeneem. (±1,5 min)')

# ---------------------------------------------------------------- 8 AFSLUITING  (±0:30 + vragen)
s = slide('bg_cover.png', 8)
txt(s, 0.7, 2.2, 7.6, 2.0, ['BEDANKT', 'VOOR JULLIE', 'AANDACHT'], size=48, font=F_XB, color=WHITE, spacing=0.92)
box(s, 0.7, 4.55, 0.9, 0.04, fill=GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
txt(s, 0.7, 4.8, 7.4, 0.5, 'Vragen?', size=26, font=F_LIGHT, color=WHITE)
txt(s, 0.7, 5.5, 6, 0.3, 'thematrixunlocked.com', size=12, font=F_SEMI, color=GREEN)
s.shapes[-1].click_action.hyperlink.address = 'https://thematrixunlocked.com/'
notes(s, 'Afsluiten en ruimte voor vragen.')

prs.save(OUT)
print('saved', OUT, len(prs.slides), 'slides')
