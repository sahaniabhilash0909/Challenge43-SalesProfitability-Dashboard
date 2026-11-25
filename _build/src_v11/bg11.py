"""Generate V11 Slate-Coral SVG backgrounds and rasterize 2x retina PNGs via Playwright Chromium."""
import os
from playwright.sync_api import sync_playwright
from layout11 import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'design11')
os.makedirs(OUT, exist_ok=True)

# Slate-Coral Design System Color Anchors (Zero Drop Shadows!)
OUTER = '#F2F3F5'
WHITE = '#FFFFFF'
HAIR = '#E4E5E7'
SILVER = '#BFC0C0'
SURF_MUTED = '#EAEBED'
CALLOUT = '#F5F6F8'
INK = '#2D3142'
SLATE = '#4F5D75'
SLATE_400 = '#7B89A0'
SLATE_200 = '#B5BECC'
SLATE_100 = '#E2E6EC'
SLATE_50 = '#F3F5F8'


def r(x, y, w, h, fill, rx=0, op=1, stroke=None, sw=1, dash=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{op}"{s}{d}/>'


def c(cx, cy, rr, fill):
    return f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{fill}"/>'


def page(key, active, kpis=True):
    sx, sy, sw, sh = SHEET
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    # Outer mat + pure white zero-shadow sheet bordered by 1px #E4E5E7 hairline
    s.append(r(0, 0, W, H, OUTER))
    s.append(r(sx, sy, sw, sh, WHITE, rx=3, stroke=HAIR, sw=1))

    # Topbar bottom hairline & Brand Icon Tile (30x30 #E2E6EC rx=6, 3 Slate bars)
    s.append(r(sx, TOP_Y, sw, 1, HAIR))
    s.append(r(LX, 32, 30, 30, SLATE_100, rx=6))
    for i, (bh, bc) in enumerate([(8, SLATE_200), (13, SLATE_400), (18, SLATE)]):
        s.append(r(LX + 6 + i * 6.5, 56 - bh, 4.5, bh, bc, rx=1))

    # Active tab crisp 2.5px Blue Slate bottom underline
    if active and active in TABS:
        tx, tw = TABS[active]
        s.append(r(tx + 8, TOP_Y - 2.5, tw - 16, 2.5, SLATE, rx=1))

    # Topbar separator & secondary Reset / primary Filters pills
    s.append(r(TOP_DIV_X, 35, 1, 24, HAIR))
    rx_, rw = UTIL['reset']
    s.append(r(rx_, 31, rw, 32, SURF_MUTED, rx=16, stroke=SILVER, sw=1))
    fx, fw = UTIL['filters']
    s.append(r(fx, 30, fw, 34, SLATE, rx=17))

    # Vertical split rail & footer hairline
    divx = PROF_DIV_X if key == 'profile' else DIV_X
    s.append(r(divx, TOP_Y, 1, 1026 - TOP_Y, HAIR))
    s.append(r(LX, 1026, 1876 - LX, 1, HAIR))

    # Inline Segmented Controls (1px solid Silver #BFC0C0 frame)
    if key != 'profile':
        for bx, by, bw, bh in (SEG_SEASON, SEG_CHANNEL):
            s.append(r(bx, by, bw, bh, WHITE, rx=6, stroke=SILVER, sw=1))

    # Left rail 5 hairline-stacked KPI rows (no grey card boxes)
    if kpis:
        for (kx, ky, kw, kh) in KPI_ROWS:
            s.append(r(kx, ky, kw, 1, HAIR))

    # Page-specific right canvas hairlines & callouts
    if key == 'ch1':
        s.append(r(1320, 92, 1, 448, HAIR))
        s.append(r(RX, 554, RW, 1, HAIR))
        s.append(r(1260, 568, 1, 448, HAIR))

    elif key == 'ch2':
        s.append(r(1100, 92, 1, 448, HAIR))
        s.append(r(1488, 92, 1, 448, HAIR))
        s.append(r(RX, 554, RW, 1, HAIR))
        s.append(r(1414, 568, 1, 448, HAIR))

    elif key == 'ch3':
        cx_, cy_, cw_, ch_ = BLK['ch3']['callout']
        s.append(r(cx_, cy_, cw_, ch_, CALLOUT, rx=8, stroke=SILVER, sw=1, dash='4 3'))
        s.append(r(LX, 446, LW, 1, HAIR))
        s.append(r(LX, 738, LW, 1, HAIR))
        for i in range(4):
            s.append(c(LX + 10, 788 + i * 54, 9, SLATE_100))
        for ax, ay, aw, ah in ACTION_ROWS:
            s.append(r(ax, ay, aw, 1, HAIR))
            s.append(r(ax, ay + 18, 3, ah - 32, SLATE, rx=1.5))
            s.append(r(ax + 16, ay + 22, 68, 24, SLATE_50, rx=4, stroke=SILVER, sw=1))
            s.append(r(ax + 820, ay + 20, 1, ah - 36, HAIR))

    elif key == 'profile':
        s.append(r(LX + PROF_LW - 96, 94, 96, 32, SURF_MUTED, rx=16, stroke=SILVER, sw=1))
        fx_, fy_, fw_, fh_ = BLK['profile']['facts']
        s.append(r(fx_, fy_, fw_, fh_, CALLOUT, rx=8, stroke=SILVER, sw=1, dash='4 3'))
        s.append(r(LX, 302, PROF_LW, 1, HAIR))
        s.append(r(PROF_RX, 554, PROF_RW, 1, HAIR))

    s.append('</svg>')
    return ''.join(s)


def drawer():
    d = DRAWER['panel']
    cl = DRAWER['close']
    return ''.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        r(0, 0, W, H, INK, 0, 0.24),
        r(d['x'], d['y'], d['w'], d['h'], WHITE, rx=6, stroke=SILVER, sw=1),
        r(cl['x'], cl['y'], cl['w'], cl['h'], SURF_MUTED, rx=15, stroke=SILVER, sw=1),
        r(d['x'] + 24, DRAWER['divider'], d['w'] - 48, 2, SLATE),
        '</svg>',
    ])


def tooltip():
    w, h = TT['w'], TT['h']
    return ''.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        r(0, 0, w, h, WHITE, rx=4, stroke=SILVER, sw=1),
        r(0, 0, 4, h, SLATE, rx=2),
        r(18, 60, w - 36, 1, HAIR),
        r(18, 148, w - 36, 1, HAIR),
        r(w // 2 + 4, 72, 1, 146, HAIR),
        '</svg>',
    ])


files = {
    'bg_ch1': (page('ch1', 'ch1'), W, H, False),
    'bg_ch2': (page('ch2', 'ch2'), W, H, False),
    'bg_ch3': (page('ch3', 'ch3', kpis=False), W, H, False),
    'bg_profile': (page('profile', 'ch1', kpis=False), W, H, False),
    'overlay_drawer': (drawer(), W, H, True),
    'bg_tooltip': (tooltip(), TT['w'], TT['h'], True),
}

for n, (svg, _, _, _) in files.items():
    open(os.path.join(OUT, n + '.svg'), 'w', encoding='utf-8').write(svg)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for n, (svg, vw, vh, transparent) in files.items():
        pw_page = browser.new_page(viewport={'width': vw, 'height': vh}, device_scale_factor=2)
        html = f'<!DOCTYPE html><html><body style="margin:0;padding:0;background:transparent;overflow:hidden;">{svg}</body></html>'
        pw_page.set_content(html, wait_until='load')
        pw_page.screenshot(path=os.path.join(OUT, n + '.png'), omit_background=transparent)
        pw_page.close()
    browser.close()

print('Generated V11 Slate-Coral PNGs:', sorted(f for f in os.listdir(OUT) if f.endswith('.png')))
