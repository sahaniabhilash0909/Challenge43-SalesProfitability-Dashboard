"""Generate V12 Modern UX Dark-Rail + Slate-Coral SVG backgrounds and rasterize 2x retina PNGs via Playwright Chromium."""
import os
from playwright.sync_api import sync_playwright
from layout12 import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'design12')
os.makedirs(OUT, exist_ok=True)

# Exact Slate-Coral Design System Tokens (Zero Drop Shadows!)
OUTER = '#F2F3F5'
WS_BG = '#F5F6F8'
CALLOUT = '#F5F6F8'
WHITE = '#FFFFFF'
HAIR = '#E4E5E7'
SILVER = '#BFC0C0'
SURF_MUTED = '#EAEBED'

INK = '#2D3142'
BODY = '#454A5E'
MUTED = '#646B7D'
SUBTLE = '#8B909E'

SLATE_DARK = '#3B465A'
SLATE = '#4F5D75'
SLATE_200 = '#B5BECC'
SLATE_100 = '#E2E6EC'
SLATE_50 = '#F3F5F8'

CORAL = '#EF8354'
CORAL_TEXT = '#BA4B1D'
CORAL_50 = '#FEF5F0'


def rect(x, y, w, h, fill, rx=0, op=1, stroke=None, sw=1, dash=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{op}"{st}{da}/>'


def circle(cx, cy, r_, fill, stroke=None, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r_}" fill="{fill}"{st}/>'


def svg_icon(kind, tx, ty, color, sw=1.8):
    """Crisp 16x16 inline stroke icon translated to center (tx, ty) on a 24x24 viewBox scaled to ~15px."""
    paths = {
        'chart': '<path d="M4 19h16M7 16v-5M12 16V7M17 16V10"/>',
        'leak': '<path d="M12 4L3.5 19h17L12 4z"/><path d="M12 10v4"/><circle cx="12" cy="17" r="0.8" fill="currentColor" stroke="none"/>',
        'target': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1.3" fill="currentColor" stroke="none"/>',
        'filter': '<path d="M4 6h16l-6.2 7.2v5l-3.6 1.8v-6.8L4 6z"/>',
        'reset': '<path d="M4 12a8 8 0 1 0 2.4-5.7L4 8.5"/><path d="M4 4v4.5h4.5"/>',
        'help': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.6 2.6 0 0 1 5 0.8c0 1.8-2.5 2.2-2.5 3.7"/><circle cx="12" cy="17" r="0.8" fill="currentColor" stroke="none"/>',
        'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><circle cx="12" cy="8" r="0.8" fill="currentColor" stroke="none"/>',
        'euro': '<path d="M16.5 7.5A5.5 5.5 0 0 0 7 12a5.5 5.5 0 0 0 9.5 4.5M5.5 10.5h7M5.5 13.5h6"/>',
        'margin': '<path d="M18 6L6 18"/><circle cx="7.5" cy="7.5" r="2"/><circle cx="16.5" cy="16.5" r="2"/>',
        'trend': '<path d="M4 16l5-5 4 3 7-7"/><path d="M15 7h5v5"/>',
        'tag': '<path d="M4 12.5V5.5A1.5 1.5 0 0 1 5.5 4h7L20 11.5l-7 7L4 12.5z"/><circle cx="8.5" cy="8.5" r="1.2" fill="currentColor" stroke="none"/>',
        'alert': '<path d="M12 5v8"/><circle cx="12" cy="16.8" r="1" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="9"/>',
        'basket': '<path d="M6 10h12l-1.2 9H7.2L6 10z"/><path d="M9 10V7a3 3 0 0 1 6 0v3"/>',
    }
    body = paths[kind]
    # Center 24x24 viewport at (tx, ty) with scale 0.68 (~16.3px visual size)
    return (f'<g transform="translate({tx - 8.16:.2f},{ty - 8.16:.2f}) scale(0.68)" '
            f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
            f'style="color:{color}">{body}</g>')


KPI_META = {
    'ch1': [
        ('chart', False),
        ('margin', False),
        ('trend', False),
        ('tag', True),
        ('alert', True),
    ],
    'ch2': [
        ('margin', True),
        ('alert', True),
        ('reset', True),
        ('tag', True),
        ('basket', False),
    ],
}


def page(key, active, kpis=True):
    ax, ay, aw, ah = APP
    clip = f'<defs><clipPath id="appClip"><rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" rx="12"/></clipPath></defs>'
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', clip]

    # Outer mat
    s.append(rect(0, 0, W, H, OUTER))

    # Clipped App Frame: Dark #2D3142 Sidebar + #F5F6F8 Workspace + Pure #FFFFFF Top Header
    s.append('<g clip-path="url(#appClip)">')
    s.append(rect(ax, ay, SB_W, ah, INK))
    s.append(rect(WS_X, ay, WS_W, ah, WS_BG))
    s.append(rect(WS_X, ay, WS_W, TOP_H, WHITE))
    s.append(rect(WS_X, ay + TOP_H, WS_W, 1, HAIR))

    # Sidebar brand tile + subtle dividers
    s.append(rect(SB_X, 34, 34, 34, SLATE_DARK, rx=8))
    for i, (bh, bc) in enumerate([(8, SLATE_200), (13, SLATE_100), (18, CORAL)]):
        s.append(rect(SB_X + 7 + i * 7.5, 60 - bh, 5, bh, bc, rx=1))
    s.append(rect(SB_X, 86, SB_IW, 1, SLATE_DARK))

    # Sidebar chapter navigation pills (3 items with custom crisp icons)
    nav_icons = ['chart', 'leak', 'target']
    for k, ny, ic in zip(('ch1', 'ch2', 'ch3'), NAV_Y, nav_icons):
        on = (k == active)
        if on:
            s.append(rect(SB_X, ny, SB_IW, NAV_H, SLATE, rx=8))
            s.append(rect(SB_X, ny + 8, 3.5, NAV_H - 16, CORAL, rx=1.5))
            s.append(svg_icon(ic, SB_X + 20, ny + NAV_H / 2, WHITE))
        else:
            s.append(svg_icon(ic, SB_X + 20, ny + NAV_H / 2, SLATE_200))

    s.append(rect(SB_X, 282, SB_IW, 1, SLATE_DARK))
    s.append(rect(SB_X, 562, SB_IW, 1, SLATE_DARK))

    # Sidebar action buttons (More filters in Blue Slate, Reset all outlined dark slate)
    fx, fy, fw, fh = FILTERS_BTN
    s.append(rect(fx, fy, fw, fh, SLATE, rx=8))
    s.append(svg_icon('filter', fx + 20, fy + fh / 2, WHITE))

    rx_, ry_, rw, rh = RESET_BTN
    s.append(rect(rx_, ry_, rw, rh, SLATE_DARK, rx=8, stroke=SLATE, sw=1))
    s.append(svg_icon('reset', rx_ + 20, ry_ + rh / 2, SLATE_100))

    s.append(rect(SB_X, 686, SB_IW, 1, SLATE_DARK))
    for iy, ic in zip(INFO_Y, ('help', 'info')):
        s.append(rect(SB_X + 8, iy + 7, 24, 24, SLATE_DARK, rx=6))
        s.append(svg_icon(ic, SB_X + 20, iy + 19, SLATE_100))

    # Top-right Period badge pill
    px_, py_, pw, ph = PERIOD_PILL
    s.append(rect(px_, py_, pw, ph, SLATE_50, rx=13, stroke=SILVER, sw=1))

    # Takeaway Strip with 4px left semantic rail (Coral on leaks page, Blue Slate elsewhere)
    mx, my, mw, mh = MSG
    s.append(rect(mx, my, mw, mh, WHITE, rx=8, stroke=HAIR, sw=1))
    rail_col = CORAL if key == 'ch2' else SLATE
    s.append(rect(mx + 1, my + 7, 4, mh - 14, rail_col, rx=2))
    if key == 'profile':
        bx, by, bw, bh = BACK_BTN
        s.append(rect(bx, by, bw, bh, SURF_MUTED, rx=16, stroke=SILVER, sw=1))

    # 5 KPI Cards (Pages 1 & 2)
    if kpis and key in KPI_META:
        for (kx, ky, kw, kh), (ic, risk) in zip(KPIS, KPI_META[key]):
            s.append(rect(kx, ky, kw, kh, WHITE, rx=10, stroke=HAIR, sw=1))
            s.append(rect(kx + 14, ky + 1, kw - 28, 3, CORAL if risk else SLATE, rx=1.5))
            s.append(rect(kx + 14, ky + 13, 26, 26, CORAL_50 if risk else SLATE_100, rx=6))
            s.append(svg_icon(ic, kx + 27, ky + 26, CORAL_TEXT if risk else SLATE))

    # Main Cards per page
    if key in ('ch1', 'ch2'):
        for _, (cx, cy, cw, ch) in CARDS[key].items():
            s.append(rect(cx, cy, cw, ch, WHITE, rx=10, stroke=HAIR, sw=1))

    elif key == 'ch3':
        cx_, cy_, cw_, ch_ = CARDS['ch3']['callout']
        s.append(rect(cx_, cy_, cw_, ch_, CALLOUT, rx=10, stroke=SILVER, sw=1.5, dash='5 4'))
        ux, uy, uw, uh = CARDS['ch3']['upside_bar']
        s.append(rect(ux, uy, uw, uh, WHITE, rx=10, stroke=HAIR, sw=1))
        lx_, ly_, lw_, lh_ = CARDS['ch3']['limits']
        s.append(rect(lx_, ly_, lw_, lh_, WHITE, rx=10, stroke=HAIR, sw=1))
        for i in range(4):
            s.append(circle(lx_ + 28, ly_ + 68 + i * 62, 11, SLATE_100))
            s.append(svg_icon('info', lx_ + 28, ly_ + 68 + i * 62, SLATE, sw=2))
        for ax_, ay_, aw_, ah_ in ACTION_ROWS:
            s.append(rect(ax_, ay_, aw_, ah_, WHITE, rx=10, stroke=HAIR, sw=1))
            s.append(rect(ax_ + 1, ay_ + 16, 4, ah_ - 32, SLATE, rx=2))
            s.append(rect(ax_ + 20, ay_ + 18, 68, 24, SLATE_50, rx=4, stroke=SILVER, sw=1))
            s.append(rect(ax_ + 736, ay_ + 18, 1, ah_ - 36, HAIR))

    elif key == 'profile':
        fx_, fy_, fw_, fh_ = CARDS['profile']['facts']
        s.append(rect(fx_, fy_, fw_, fh_, CALLOUT, rx=10, stroke=SILVER, sw=1.5, dash='5 4'))
        for nm in ('pnl', 'daily', 'band'):
            cx, cy, cw, ch = CARDS['profile'][nm]
            s.append(rect(cx, cy, cw, ch, WHITE, rx=10, stroke=HAIR, sw=1))

    # Footer hairline
    s.append(rect(X0, 1024, MW, 1, HAIR))
    s.append('</g>')

    # Crisp outer 1px hairline border on the entire app frame
    s.append(rect(ax, ay, aw, ah, 'none', rx=12, stroke=HAIR, sw=1))
    s.append('</svg>')
    return ''.join(s)


def drawer():
    d = DRAWER['panel']
    cl = DRAWER['close']
    return ''.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        rect(0, 0, W, H, INK, 0, 0.28),
        rect(d['x'], d['y'], d['w'], d['h'], WHITE, rx=10, stroke=SILVER, sw=1),
        rect(cl['x'], cl['y'], cl['w'], cl['h'], SURF_MUTED, rx=15, stroke=SILVER, sw=1),
        rect(d['x'] + 24, DRAWER['divider'], d['w'] - 48, 2, SLATE),
        '</svg>',
    ])


def tooltip():
    w, h = TT['w'], TT['h']
    return ''.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        rect(0, 0, w, h, WHITE, rx=6, stroke=SILVER, sw=1),
        rect(0, 0, 4, h, SLATE, rx=2),
        rect(18, 60, w - 36, 1, HAIR),
        rect(18, 148, w - 36, 1, HAIR),
        rect(w // 2 + 4, 72, 1, 146, HAIR),
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

print('Generated V12 Slate-Coral Modern UX PNGs:', sorted(f for f in os.listdir(OUT) if f.endswith('.png')))
