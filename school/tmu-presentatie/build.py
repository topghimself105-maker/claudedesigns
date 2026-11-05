# The Matrix Unlocked – Bedrijfsprofiel & Stagegids (10 dia's, 16:9, Nederlands)
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
OUT = os.path.join(HERE, 'TMU_Bedrijfsprofiel_Stagegids.pptx')

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
        txt(s, 1.02, 7.05, 6, 0.25, 'The Matrix Unlocked  ·  Bedrijfsprofiel & Stagegids', size=9, color=DIM)
        txt(s, 11.9, 7.05, 0.73, 0.25, f'{n:02d} / 10', size=9, color=DIM, align=PP_ALIGN.RIGHT)
    return s


def source(s, text, x=0.7, y=6.72, w=8):
    txt(s, x, y, w, 0.22, text, size=8.5, color=DIM)


def bullets(s, x, y, w, h, items, size=11, color=GREY, bullet_color=GREEN, spacing=1.05, gap=3):
    paras = [[('▪  ', {'color': bullet_color, 'font': F_SEMI, 'size': size - 1}), (it, {})] for it in items]
    return txt(s, x, y, w, h, paras, size=size, color=color, spacing=spacing, space_after=gap)


# ---------------------------------------------------------------- 1 COVER
s = slide('bg_cover.png')
img(s, 'img/logo_wordmark.png', 0.7, 0.62, h=0.62)
txt(s, 0.7, 2.25, 7.4, 0.35, 'STAGEPRESENTATIE  ·  INTERNATIONAL BUSINESS', size=11, font=F_SEMI, color=GREEN)
txt(s, 0.7, 2.7, 7.6, 2.0, ['THE MATRIX', 'UNLOCKED'], size=60, font=F_XB, color=WHITE, spacing=0.92)
txt(s, 0.7, 4.65, 7.4, 0.5, 'Bedrijfsprofiel & Stagegids', size=24, font=F_LIGHT, color=WHITE)
box(s, 0.7, 5.35, 0.9, 0.04, fill=GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
txt(s, 0.7, 5.6, 7.4, 0.9, [
    [('NHL Stenden', {'font': F_SEMI, 'color': WHITE})],
    [('International Business  ·  Stageperiode 2026', {})],
    [('[Naam student]  ·  [Studentnummer]', {'color': DIM})]], size=12, color=GREY, spacing=1.15)
txt(s, 9.0, 6.95, 3.65, 0.3, 'Foto: TMU-community tijdens een privé-evenement (thematrixunlocked.com)',
    size=8, color=DIM, align=PP_ALIGN.RIGHT)

# ---------------------------------------------------------------- 2 OVER TMU
s = slide('bg.png', 2)
eyebrow(s, 0.7, 0.42, 'Het bedrijf')
title(s, 'Over The Matrix Unlocked')
txt(s, 0.7, 1.7, 6.9, 1.2,
    'The Matrix Unlocked (TMU, ook bekend als Team369) is een trading-educatiecommunity en coachingprogramma. '
    'Traders leren er het Time & Price-framework: hoe tijd en prijs samen de markt bewegen.',
    size=14.5, color=WHITE, spacing=1.2)
cards = [
    ('Branche', 'Online trading-educatie en coaching: een digitaal kennis- en begeleidingsbedrijf.'),
    ('Aanbod', '12 weken 1-op-1 coaching, een gestructureerd lesprogramma, eigen tools en een privécommunity.'),
    ('Positionering', 'Voor traders die de markt als een business willen benaderen; uitdrukkelijk geen signaaldienst of snel-rijk-schema.'),
    ('Framework', 'Time Cycles, Price Cycles, Liquidity, Market Maker Models en Imbalances als één objectief proces.'),
]
for i, (h, t) in enumerate(cards):
    cx, cy = 0.7 + (i % 2) * 3.5, 3.0 + (i // 2) * 1.55
    box(s, cx, cy, 3.35, 1.4)
    txt(s, cx + 0.22, cy + 0.18, 2.95, 0.3, h.upper(), size=9.5, font=F_SEMI, color=GREEN)
    txt(s, cx + 0.22, cy + 0.48, 2.95, 0.85, t, size=11, color=GREY, spacing=1.12)
# founder
pic = img(s, 'img/frank.jpg', 8.05, 1.62, w=4.6)
pic.crop_left, pic.crop_right, pic.crop_top, pic.crop_bottom = 0.2, 0.2, 0.06, 0.152
pic.width, pic.height = Inches(4.6), Inches(3.4)
fy = 1.62 + 3.4
box(s, 8.05, fy - 0.02, 4.6, 1.38, fill=CARD, line=LINE, radius=0.04)
txt(s, 8.3, fy + 0.15, 4.2, 0.35, 'Frank Warrink (Frank369)', size=15, font=F_SEMI, color=WHITE)
txt(s, 8.3, fy + 0.5, 4.2, 0.3, 'Founder & Head Coach', size=11, color=GREEN)
txt(s, 8.3, fy + 0.8, 4.2, 0.5, '400+ studenten gecoacht  ·  gemiddelde beoordeling 4,92/5', size=10, color=GREY)
source(s, SRC_SITE + '. Cijfers zoals vermeld door het bedrijf zelf.')

# ---------------------------------------------------------------- 3 BUSINESSMODEL
s = slide('bg_alt.png', 3)
eyebrow(s, 0.7, 0.42, 'Hoe TMU waarde creëert')
title(s, 'Businessmodel & diensten', 'Een high-ticket coachingprogramma, verkocht via een aanvraag en een persoonlijk strategiegesprek.')
groups = [
    ('Coaching', ['12 weken persoonlijke 1-op-1 coaching', 'Persoonlijke accountability partner']),
    ('Educatie', ['12-weeks programma: lessen + huiswerk', 'Mechanisch TMU Protocol', 'Reversal Sequence-training in Time & Price']),
    ('Tools', ['Exclusieve algoritmische trading-tools', 'TMU Trading Journal']),
    ('Community', ['Privécommunity (levenslang)', 'Educatieve bibliotheek', 'Privé in-person evenementen']),
    ('Funding', ['$90K funding-traject: kapitaal na het halen van de evaluatie']),
]
gw = 2.32
for i, (h, its) in enumerate(groups):
    gx = 0.7 + i * (gw + 0.13)
    box(s, gx, 1.95, gw, 2.05)
    txt(s, gx + 0.2, 2.1, gw - 0.3, 0.3, h.upper(), size=10, font=F_SEMI, color=GREEN)
    bullets(s, gx + 0.2, 2.45, gw - 0.35, 1.5, its, size=10.5, gap=4)
# customer journey
txt(s, 0.7, 4.25, 8, 0.3, 'KLANTREIS EN DE BIJDRAGE VAN ELKE BEDRIJFSFUNCTIE', size=10, font=F_SEMI, color=WHITE)
steps = [('Awareness', 'Creative & Content\nMarketing'), ('Interest', 'Marketing\n(gratis training)'),
         ('Leadgeneratie', 'Marketing\nCRM & Automation'), ('Kwalificatie', 'Sales\n(aanvraag)'),
         ('Consultatie', 'Sales\n(strategiegesprek)'), ('Conversie', 'Sales &\nBusiness Dev.'),
         ('Onboarding', 'Client Success\nBackend & CRM'), ('Klantervaring', 'Coaching, Client Success\nSoftware & AI')]
sw = 1.43
for i, (st, fn) in enumerate(steps):
    sx = 0.7 + i * (sw + 0.07)
    sh = box(s, sx, 4.65, sw, 0.62, fill=(GREEN if i in (3, 4) else CARD2), line=GREEN, radius=0.5)
    txt(s, sx, 4.65, sw, 0.62, st, size=11, font=F_SEMI, color=(BLACK if i in (3, 4) else WHITE),
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, sx, 5.38, sw, 0.7, fn.split('\n'), size=9, color=GREY, align=PP_ALIGN.CENTER, spacing=1.05)
txt(s, 0.7, 6.15, 11.9, 0.45,
    [[('Geverifieerd op de website: ', {'font': F_SEMI, 'color': WHITE}),
      ('gratis training → aanvraag (5 vragen) → strategiegesprek van 30 minuten → start 12-weeks programma. ', {}),
      ('Koppeling met functies: ', {'font': F_SEMI, 'color': WHITE}), ('eigen analyse op basis van de stage.', {})]],
    size=10, color=GREY)
source(s, SRC_SITE)

# ---------------------------------------------------------------- 4 FUNCTIES & STAGEMOGELIJKHEDEN
s = slide('bg_center.png', 4)
eyebrow(s, 0.7, 0.42, 'Stagemogelijkheden')
title(s, 'Zeven bedrijfsfuncties, veel richtingen')
txt(s, 0.7, 1.33, 11.9, 0.35,
    'Functies, geen vaste afdelingen: verantwoordelijkheden overlappen en stagiairs werken over functies heen. '
    'Indicatieve stagemogelijkheden, geen bevestigde vacatures.', size=11.5, color=GREY)
F = [
    ('sales', 'Sales & Business Development', ['Leadkwalificatie & follow-ups', 'High-ticket salesgesprekken', 'Conversie-optimalisatie'],
     'International Business, Sales, Commercieel Management', False),
    ('marketing', 'Marketing & Lead Generation', ['Marketingstrategie & social media', 'Webinarcampagnes', 'Leadgeneratie & publieksgroei'],
     'Marketing, Communicatie, Digital Marketing, IB', False),
    ('creative', 'Creative & Content', ['Content & video-editing', 'Creatieve campagnes', 'Branding & marketingmateriaal'],
     'Creative Business, Media, Multimedia Design', False),
    ('client', 'Client Success & Operations', ['Onboarding van klanten', 'Klantcommunicatie & tevredenheid', 'Interne processen'],
     'IB, Bedrijfskunde, Customer Experience', False),
    ('software', 'Software Development & Engineering', ['Platform- en softwareontwikkeling', 'Nieuwe functionaliteiten', 'Technische probleemoplossing'],
     'Software Development, Informatica, ICT', True),
    ('crm', 'Backend, CRM & Automation', ['CRM-beheer & datamanagement', 'Workflow-optimalisatie', 'Sales- en marketingautomatisering'],
     'ICT, Business IT, Data Management', True),
    ('ai', 'AI & Innovation', ['AI-modelontwikkeling', 'AI-implementatie', 'Procesautomatisering', 'Nieuwe technologie testen'],
     'AI, Data Science, Software Engineering', True),
]
cw, ch = 2.88, 2.3
for i, (ic, h, its, prof, tech) in enumerate(F):
    row = i // 4
    col = i % 4
    cx = 0.7 + col * (cw + 0.13) + (row * (cw + 0.13) / 2)
    cy = 1.8 + row * (ch + 0.13)
    box(s, cx, cy, cw, ch, fill=(CARD2 if tech else CARD), line=(GREEN if tech else LINE), lw=(1 if tech else 0.75))
    img(s, 'icons/' + ic + '.png', cx + 0.2, cy + 0.2, h=0.42)
    if tech:
        pill(s, cx + cw - 1.05, cy + 0.27, 'TECHNISCH', size=8, w=0.85)
    txt(s, cx + 0.2, cy + 0.72, cw - 0.4, 0.5, h, size=12.5, font=F_SEMI, color=WHITE, spacing=1.0)
    bullets(s, cx + 0.2, cy + 1.15, cw - 0.35, 0.8, its, size=9.5, gap=0)
    txt(s, cx + 0.2, cy + ch - 0.42, cw - 0.35, 0.36, [[('Voor: ', {'font': F_SEMI, 'color': GREEN}), (prof, {})]],
        size=8.5, color=GREY, spacing=1.0)
txt(s, 0.7, 6.72, 11.9, 0.22,
    'Indeling en profielen: eigen analyse op basis van de activiteiten van TMU en de stage-ervaring. Groen omlijnd = technische richting.',
    size=8.5, color=DIM)

# ---------------------------------------------------------------- 5 CULTUUR
s = slide('bg.png', 5)
eyebrow(s, 0.7, 0.42, 'Werkomgeving')
title(s, 'Cultuur & werkomgeving')
txt(s, 0.7, 1.55, 4.4, 2.2,
    [[('Een ondernemende online organisatie waar je ', {}), ('leert door te doen', {'font': F_SEMI, 'color': GREEN}), ('.', {})]],
    size=22, color=WHITE, spacing=1.15)
txt(s, 0.7, 3.25, 4.3, 2.4,
    'De structuur is flexibel: taken lopen over functies heen. Daardoor kun je als stagiair ervaring opdoen in sales, marketing, '
    'creatie én systemen, afhankelijk van je initiatief en de prioriteiten van het moment.',
    size=11.5, color=GREY, spacing=1.25)
pill(s, 0.7, 5.3, 'GEBASEERD OP MIJN STAGE-ERVARING', size=8.5, w=2.75)
T = [('Ondernemend', 'Denken als eigenaar: resultaat en groei staan centraal.'),
     ('Flexibele structuur', 'Rollen zijn niet vastgezet; je schakelt mee waar nodig.'),
     ('Dynamisch & online', 'Een digitaal bedrijf waarin dingen snel veranderen.'),
     ('Samenwerken', 'Sales, marketing en techniek werken nauw samen.'),
     ('Initiatief', 'Ruimte voor eigen ideeën en verantwoordelijkheid.'),
     ('Praktijkleren', 'Je leert vooral door echte opdrachten uit te voeren.'),
     ('Dicht bij de leiding', 'Inzicht in beslissingen en strategie van dichtbij.'),
     ('Aanpassingsvermogen', 'Problemen oplossen en meebewegen met prioriteiten.')]
for i, (h, t) in enumerate(T):
    cx, cy = 5.55 + (i % 2) * 3.58, 1.55 + (i // 2) * 1.22
    box(s, cx, cy, 3.45, 1.08)
    box(s, cx, cy + 0.2, 0.05, 0.68, fill=GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
    txt(s, cx + 0.25, cy + 0.15, 3.05, 0.3, h, size=12.5, font=F_SEMI, color=WHITE)
    txt(s, cx + 0.25, cy + 0.48, 3.05, 0.55, t, size=10, color=GREY, spacing=1.1)
source(s, 'Beschrijving gebaseerd op eigen ervaring tijdens de stage; geen formeel bedrijfsbeleid.')

# ---------------------------------------------------------------- 6 SALES, MARKETING & FUNNEL
s = slide('bg_alt.png', 6)
eyebrow(s, 0.7, 0.42, 'Commercieel')
title(s, 'Sales, marketing & de klantreis')
stages = [('Aantrekken', 'Content, social media (o.a. X), webinars en gratis training', True),
          ('Opvolgen', 'Lead nurturing en follow-up van webinar- en marketingleads', True),
          ('Kwalificeren', 'Aanvraag beoordelen, situatie en doelen van de lead begrijpen', True),
          ('Gesprek', 'Strategiegesprek met een salesmedewerker of de leiding', True),
          ('Conversie', 'High-ticket verkoop van het 12-weeks programma', True),
          ('Client success', 'Onboarding en relatiebeheer na de aankoop', True)]
top_w, bot_w, x_c = 6.6, 3.0, 4.1
for i, (h, t, mine) in enumerate(stages):
    wdt = top_w - (top_w - bot_w) * i / (len(stages) - 1)
    y = 1.55 + i * 0.78
    b = box(s, x_c - wdt / 2, y, wdt, 0.64, fill=(CARD2 if i % 2 else CARD), line=GREEN, radius=0.5, lw=(1.25 if i == 4 else 0.75))
    txt(s, x_c - wdt / 2, y, wdt, 0.64, h, size=13, font=F_SEMI, color=(GREEN if i == 4 else WHITE),
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 7.65, y + 0.06, 4.0, 0.6, t, size=10.5, color=GREY, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
    img(s, 'icons/check.png', 12.15, y + 0.17, h=0.32)
    s.shapes.add_connector(1, Inches(x_c + wdt / 2 + 0.08), Inches(y + 0.32), Inches(7.5), Inches(y + 0.32)).line.color.rgb = LINE
txt(s, 11.65, 1.25, 1.2, 0.3, 'MIJN ROL', size=9, font=F_SEMI, color=GREEN, align=PP_ALIGN.CENTER)
txt(s, 7.65, 1.25, 4, 0.3, 'WAT ER GEBEURT', size=9, font=F_SEMI, color=GREEN)
txt(s, 0.7, 6.32, 11.9, 0.35,
    'Marketing vult de funnel, sales zet interesse om in klanten en client success houdt ze tevreden. '
    'Als stagiair werkte ik in elke fase mee (✓).', size=10.5, color=WHITE)
source(s, 'Stappen gebaseerd op de website (aanvraag, strategiegesprek, programma) en op eigen stage-ervaring.')

# ---------------------------------------------------------------- 7 TECHNOLOGIE
s = slide('bg_center.png', 7)
eyebrow(s, 0.7, 0.42, 'Techniek')
title(s, 'Technologie, ontwikkeling & innovatie', 'Technologie ondersteunt zowel de commerciële kant als de operatie en het product.')
cxh, cyh = 3.75, 4.3
hub = box(s, cxh - 1.15, cyh - 0.62, 2.3, 1.24, fill=CARD2, line=GREEN, radius=0.5, lw=1.5)
txt(s, cxh - 1.15, cyh - 0.62, 2.3, 1.24, ['Technologie', 'als motor'], size=15, font=F_SEMI, color=WHITE,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.0)
nodes = [('Software & platform', -2.2, -1.55), ('Backend & CRM', 0, -1.95), ('Automatisering', 2.2, -1.55),
         ('Systeemintegraties', 2.2, 1.55), ('Datamanagement', 0, 1.95), ('AI-ontwikkeling', -2.2, 1.55)]
for (h, dx, dy) in nodes:
    nx, ny = cxh + dx, cyh + dy
    s.shapes.add_connector(1, Inches(cxh), Inches(cyh), Inches(nx), Inches(ny)).line.color.rgb = RGBColor(0x1F, 0x5C, 0x3B)
for (h, dx, dy) in nodes:
    nx, ny = cxh + dx, cyh + dy
    box(s, nx - 1.0, ny - 0.3, 2.0, 0.6, fill=CARD, line=LINE, radius=0.5)
    txt(s, nx - 1.0, ny - 0.3, 2.0, 0.6, h, size=10.5, font=F_SEMI, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
box(s, cxh - 1.15, cyh - 0.62, 2.3, 1.24, fill=CARD2, line=GREEN, radius=0.5, lw=1.5)
txt(s, cxh - 1.15, cyh - 0.62, 2.3, 1.24, ['Technologie', 'als motor'], size=15, font=F_SEMI, color=WHITE,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.0)
cols = [('Commercieel', ['Leads vastleggen en opvolgen in een CRM', 'Automatische follow-ups en workflows', 'Data voor betere salesbeslissingen']),
        ('Operatie & product', ['Onboarding en klantcommunicatie', "Eigen tools voor studenten (algoritmische tools, Trading Journal)", 'Efficiëntere interne processen']),
        ('Mogelijke projecten voor technische stagiairs', ['Een workflow automatiseren', 'CRM-data structureren en rapporteren', 'Een AI-toepassing testen voor een intern proces', 'Een platformfunctie verbeteren'])]
for i, (h, its) in enumerate(cols):
    cy = 1.95 + i * 1.42
    hh = 1.3 if i < 2 else 1.6
    box(s, 7.1, cy, 5.55, hh, fill=(CARD2 if i == 2 else CARD), line=(GREEN if i == 2 else LINE))
    txt(s, 7.32, cy + 0.15, 5.1, 0.3, h.upper(), size=9.5, font=F_SEMI, color=GREEN)
    bullets(s, 7.32, cy + 0.45, 5.1, hh - 0.5, its, size=10.5, gap=1)
source(s, 'Eigen ervaring: betrokken bij de implementatie van een nieuw communicatie- en belsysteem en kennismaking met AI-modelontwikkeling. '
          'Projecten zijn voorbeelden, geen vacatures.', w=11.9)

# ---------------------------------------------------------------- 8 MIJN STAGE
s = slide('bg.png', 8)
eyebrow(s, 0.7, 0.42, 'Persoonlijke ervaring')
title(s, 'Mijn stage & verantwoordelijkheden')
pill(s, 0.7, 1.35, 'MIJN EIGEN ROL, NIET HETZELFDE VOOR ELKE STAGIAIR', size=8.5, w=3.75)
R = [('Sales & Client Success', ['Contact met bestaande en potentiële klanten', 'Leads opvolgen en kwalificeren', 'Gesprekken inplannen met sales of leiding', 'Diensten uitleggen, relaties onderhouden']),
     ('Marketing & leadgeneratie', ['Leadgeneratie en webinarcampagnes', 'Opvolging van webinardeelnemers', 'Extra aanwezigheid op X (Twitter) opbouwen', 'Nieuwe marketingkansen verkennen']),
     ('Creatief & funnel', ['Funnels mee ontwikkelen en optimaliseren', 'Inzicht in de klantreis', 'Creatieve marketingprojecten', 'Communicatie en conversie verbeteren']),
     ('Business development & innovatie', ['Implementatie nieuw communicatie- en belsysteem', 'Kennismaking met AI-modelontwikkeling', 'Werken naast de leiding', 'Inzicht in strategische beslissingen'])]
for i, (h, its) in enumerate(R):
    cx, cy = 0.7 + (i % 2) * 3.95, 1.9 + (i // 2) * 2.35
    box(s, cx, cy, 3.8, 2.2)
    txt(s, cx + 0.22, cy + 0.18, 3.4, 0.3, h, size=13, font=F_SEMI, color=WHITE)
    bullets(s, cx + 0.22, cy + 0.6, 3.4, 1.55, its, size=10.5, gap=3)
box(s, 8.75, 1.9, 3.9, 4.55, fill=CARD2, line=GREEN, lw=1)
txt(s, 8.98, 2.08, 3.5, 0.3, 'KOPPELING MET INTERNATIONAL BUSINESS', size=9.5, font=F_SEMI, color=GREEN)
K = [('Sales', 'gesprekstechniek, high-ticket verkoop'), ('Marketing', 'funnels, campagnes, social media'),
     ('CRM', 'klantrelaties en leadbeheer'), ('Digital business', 'een volledig online businessmodel'),
     ('Communicatie', 'internationale klanten en leads'), ('Ondernemerschap', 'initiatief en eigenaarschap'),
     ('Business development', 'systemen, AI en groei')]
for i, (h, t) in enumerate(K):
    y = 2.5 + i * 0.55
    txt(s, 8.98, y, 3.5, 0.5, [[(h, {'font': F_SEMI, 'color': WHITE, 'size': 11.5})], [(t, {})]], size=9.5, color=GREY, spacing=1.0)
source(s, 'Gebaseerd op mijn eigen stage-ervaring bij TMU.')

# ---------------------------------------------------------------- 9 DAGELIJKSE PRAKTIJK
s = slide('bg_alt.png', 9)
eyebrow(s, 0.7, 0.42, 'Voor toekomstige stagiairs')
title(s, 'Dagelijkse praktijk & leerkansen')
txt(s, 0.7, 1.4, 3.6, 0.3, 'WAT KUN JE VERWACHTEN?', size=9.5, font=F_SEMI, color=GREEN)
bullets(s, 0.7, 1.75, 3.6, 4.6, ['Werken aan echte businessprojecten', 'Samenwerken met verschillende functies', 'Contact met collega’s en de leiding',
                                 'Eigenaarschap over je taken', 'Zelfstandig werken', 'Nieuwe systemen en processen leren',
                                 'Meebewegen met veranderende prioriteiten', 'Feedback krijgen en verbeteren'], size=11, gap=5)
txt(s, 4.55, 1.4, 4.5, 0.3, 'VOORBEELDEN VAN ACTIVITEITEN (INDICATIEF)', size=9.5, font=F_SEMI, color=GREEN)
E = [('sales', 'Sales', 'Leads kwalificeren en gesprekken voorbereiden'), ('marketing', 'Marketing', 'Een webinarcampagne mee opzetten'),
     ('creative', 'Creative', 'Korte video’s en social content maken'), ('client', 'Client Success', 'Onboarding van nieuwe klanten ondersteunen'),
     ('software', 'Software', 'Een platformfunctie bouwen of verbeteren'), ('crm', 'CRM & Automation', 'Een follow-up-workflow automatiseren'),
     ('ai', 'AI & Innovation', 'Een AI-toepassing testen voor een intern proces')]
for i, (ic, h, t) in enumerate(E):
    y = 1.78 + i * 0.66
    box(s, 4.55, y, 4.45, 0.56)
    img(s, 'icons/' + ic + '.png', 4.7, y + 0.12, h=0.32)
    txt(s, 5.15, y + 0.04, 3.75, 0.5, [[(h + '  ', {'font': F_SEMI, 'color': WHITE})], [(t, {})]], size=9.5, color=GREY, spacing=0.98,
        anchor=MSO_ANCHOR.MIDDLE)
box(s, 9.3, 1.4, 3.35, 5.05, fill=CARD2, line=GREEN, lw=1)
txt(s, 9.52, 1.6, 2.95, 0.7, 'Wat maakt een succesvolle stagiair bij TMU?', size=14, font=F_SEMI, color=WHITE, spacing=1.05)
Q = ['Proactief', 'Nieuwsgierig', 'Flexibel', 'Verantwoordelijk', 'Communicatief', 'Leergierig', 'Neemt graag initiatief']
for i, q in enumerate(Q):
    pill(s, 9.52, 2.5 + i * 0.52, q.upper(), size=9.5, w=2.9)
source(s, 'Gebaseerd op eigen stage-ervaring; activiteiten zijn voorbeelden en verschillen per stagiair en periode.')

# ---------------------------------------------------------------- 10 CONCLUSIE
s = slide('bg_cover.png', 10)
eyebrow(s, 0.7, 0.42, 'Conclusie')
title(s, 'Samengevat')
C = [('Wat TMU doet', 'Trading-educatie en 12 weken 1-op-1 coaching rond het Time & Price-framework.'),
     ('Zeven functies', 'Van sales, marketing en creatie tot software, CRM, AI en client success.'),
     ('Ondernemende omgeving', 'Flexibel, online en dicht bij de leiding: leren door te doen.'),
     ('Brede stagekansen', 'Ook voor technische studenten: software, data, automatisering en AI.'),
     ('Aansluiting op studies', 'International Business en daarnaast marketing-, creatieve en ICT-opleidingen.')]
for i, (h, t) in enumerate(C):
    y = 1.6 + i * 0.78
    img(s, 'icons/check.png', 0.7, y + 0.06, h=0.32)
    txt(s, 1.2, y, 6.2, 0.75, [[(h, {'font': F_SEMI, 'color': WHITE, 'size': 13})], [(t, {})]], size=10.5, color=GREY, spacing=1.05)
box(s, 0.7, 5.65, 7.0, 0.04, fill=GREEN, line=None, shape=MSO_SHAPE.RECTANGLE)
txt(s, 0.7, 5.8, 7.4, 0.7, ['THE MATRIX UNLOCKED – A DYNAMIC ENVIRONMENT', 'TO LEARN, CONTRIBUTE AND GROW.'],
    size=15, font=F_XB, color=WHITE, spacing=1.05)
txt(s, 0.7, 6.55, 6, 0.3, 'thematrixunlocked.com', size=12, font=F_SEMI, color=GREEN)
s.shapes[-1].click_action.hyperlink.address = 'https://thematrixunlocked.com/'

prs.save(OUT)
print('saved', OUT, len(prs.slides), 'slides')
