"""Generate V12 Modern UX Dark-Rail + Slate-Coral backgrounds with baked static typography, kickers, and vector legends via Playwright Chromium."""
import html as html_lib
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
SLATE_400 = '#7B89A0'
SLATE_200 = '#B5BECC'
SLATE_100 = '#E2E6EC'
SLATE_50 = '#F3F5F8'

CORAL = '#EF8354'
CORAL_TEXT = '#BA4B1D'
CORAL_200 = '#FAD3C1'
CORAL_50 = '#FEF5F0'

PY_BAR = SLATE_200

FOOT = ('Source: FP20 Analytics Challenge 43 (synthetic data)  ·  CY = selected season  ·  PY = same dates one season earlier  ·  '
        'Blue Slate = CY/favorable, Coral = adverse/leak  ·  contribution excludes overhead, interest & tax')


def rect(x, y, w, h, fill, rx=0, op=1, stroke=None, sw=1, dash=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{op}"{st}{da}/>'


def circle(cx, cy, r_, fill, stroke=None, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r_}" fill="{fill}"{st}/>'


def svg_icon(kind, tx, ty, color, sw=1.8):
    """Crisp 16x16 inline stroke icon centered at (tx, ty)."""
    paths = {
        'chart': '<path d="M4 19h16M7 16v-5M12 16V7M17 16V10"/>',
        'leak': '<path d="M12 4L3.5 19h17L12 4z"/><path d="M12 10v4"/><circle cx="12" cy="17" r="0.8" fill="currentColor" stroke="none"/>',
        'target': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1.3" fill="currentColor" stroke="none"/>',
        'filter': '<path d="M4 6h16l-6.2 7.2v5l-3.6 1.8v-6.8L4 6z"/>',
        'reset': '<path d="M4 12a8 8 0 1 0 2.4-5.7L4 8.5"/><path d="M4 4v4.5h4.5"/>',
        'help': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.6 2.6 0 0 1 5 0.8c0 1.8-2.5 2.2-2.5 3.7"/><circle cx="12" cy="17" r="0.8" fill="currentColor" stroke="none"/>',
        'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><circle cx="12" cy="8" r="0.8" fill="currentColor" stroke="none"/>',
        'margin': '<path d="M18 6L6 18"/><circle cx="7.5" cy="7.5" r="2"/><circle cx="16.5" cy="16.5" r="2"/>',
        'trend': '<path d="M4 16l5-5 4 3 7-7"/><path d="M15 7h5v5"/>',
        'tag': '<path d="M4 12.5V5.5A1.5 1.5 0 0 1 5.5 4h7L20 11.5l-7 7L4 12.5z"/><circle cx="8.5" cy="8.5" r="1.2" fill="currentColor" stroke="none"/>',
        'alert': '<path d="M12 5v8"/><circle cx="12" cy="16.8" r="1" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="9"/>',
        'basket': '<path d="M6 10h12l-1.2 9H7.2L6 10z"/><path d="M9 10V7a3 3 0 0 1 6 0v3"/>',
    }
    body = paths[kind]
    return (f'<g transform="translate({tx - 8.16:.2f},{ty - 8.16:.2f}) scale(0.68)" '
            f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
            f'style="color:{color}">{body}</g>')


def htxt(x, y, w, h, runs, align='left', lh=1.22):
    """Positioned HTML text layer rendered at exact browser font metrics (matching Power BI pt)."""
    spans = []
    for text, size, color, font, bold in runs:
        fw = '700' if bold else '400'
        spans.append(f'<span style="font-size:{size}pt;color:{color};font-family:\'{font}\',\'Segoe UI\',sans-serif;font-weight:{fw};">{html_lib.escape(text)}</span>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'line-height:{lh};text-align:{align};white-space:pre-wrap;overflow:hidden;">{"".join(spans)}</div>')


def hlegend(x, y, w, items):
    """Crisp flexbox legend row with vector SVG swatches and exact browser spacing."""
    parts = []
    for sym, sc, lbl in items:
        if sym == '■':
            sw = f'<svg width="9" height="9" viewBox="0 0 9 9" style="flex:none;"><rect x="0.5" y="0.5" width="8" height="8" rx="1.8" fill="{sc}"/></svg>'
        elif sym == '●':
            sw = f'<svg width="9" height="9" viewBox="0 0 9 9" style="flex:none;"><circle cx="4.5" cy="4.5" r="4" fill="{sc}"/></svg>'
        elif sym == '━━':
            sw = f'<svg width="16" height="9" viewBox="0 0 16 9" style="flex:none;"><line x1="1" y1="4.5" x2="15" y2="4.5" stroke="{sc}" stroke-width="2.4" stroke-linecap="round"/></svg>'
        elif sym == '···':
            sw = f'<svg width="16" height="9" viewBox="0 0 16 9" style="flex:none;"><line x1="1.5" y1="4.5" x2="14.5" y2="4.5" stroke="{sc}" stroke-width="2.2" stroke-dasharray="1.5 3" stroke-linecap="round"/></svg>'
        else:
            sw = f'<svg width="9" height="9" viewBox="0 0 9 9" style="flex:none;"><rect x="0.5" y="0.5" width="8" height="8" rx="1.8" fill="{sc}"/></svg>'
        parts.append(f'<span style="display:inline-flex;align-items:center;gap:5px;margin-right:12px;">{sw}'
                     f'<span style="font-size:7.5pt;color:{MUTED};font-family:\'Segoe UI\',sans-serif;">{html_lib.escape(lbl)}</span></span>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:18px;'
            f'display:flex;align-items:center;white-space:nowrap;">{"".join(parts)}</div>')


def card_kicker_html(card, kicker, note=None, legend=None, leg_y=69):
    cx, cy, cw, _ = card
    runs = [(kicker.upper(), 7.5, MUTED, 'Segoe UI Semibold', True)]
    if note:
        runs.append(('   ·   ' + note, 7.5, SUBTLE, 'Segoe UI', False))
    out = [htxt(cx + 18, cy + 11, cw - 36, 18, runs)]
    if legend:
        out.append(hlegend(cx + 18, cy + leg_y, cw - 36, legend))
    return out


KPI_META = {
    'ch1': [
        ('chart', False, 'Contribution profit'),
        ('margin', False, 'Contribution margin'),
        ('trend', False, 'Net sales'),
        ('tag', True, 'Weighted discount'),
        ('alert', True, 'Sales at 20%+ discount'),
    ],
    'ch2': [
        ('margin', True, 'Online electronics margin'),
        ('alert', True, 'Net sales sold at a loss'),
        ('reset', True, 'Return rate · all units'),
        ('tag', True, 'Return rate · apparel'),
        ('basket', False, 'Average order value'),
    ],
}

PAGE_META = {
    'ch1': ('CHAPTER 1 OF 3  ·  HOLIDAY TRADING AUDIT · 8 EUROPEAN CITY MARKETS', 'What happened & why'),
    'ch2': ('CHAPTER 2 OF 3  ·  PRODUCTS, CHANNELS, MARKETS & RETURNS', 'Where it leaks'),
    'ch3': ('CHAPTER 3 OF 3  ·  FOUR RECOMMENDED MOVES', 'What to do'),
    'profile': ('DRILL-THROUGH  ·  CAMPAIGN PROFILE', 'Campaign profile'),
}

LIM_SHORT = [
    ('Not causal.', ' Synthetic data with no control group: nothing proves a campaign caused uplift or ROI.'),
    ('Before overhead.', ' Contribution excludes corporate overhead, interest and tax.'),
    ('Unequal lengths.', ' Campaigns run 3 to 17 days; compare margins and sales/day, not raw totals.'),
    ('Allocated spend.', ' Campaign budgets are spread across sales lines by gross-sales share.'),
]

MOVES_STATIC = [
    ('ACT-01', 'Keep every event discount below 20%', 'Cap Black Friday and New Year offers at 19% in 2 test markets; compare against 6 control markets.'),
    ('ACT-02', 'Sell online electronics on value, not price', 'Bundle laptops with accessories online; restrict price cuts to aged clearance SKUs only.'),
    ('ACT-03', 'Bring apparel returns down to store average', 'Add fit notes and sizing guides to the 10 most-returned apparel items before peak traffic.'),
    ('ACT-04', 'Run New Year as clearance, not a second Christmas', 'Limit New Year promotions to aged inventory and exclude high-return apparel lines.'),
]


def page(key, active, kpis=True):
    ax, ay, aw, ah = APP
    clip = f'<defs><clipPath id="appClip"><rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" rx="12"/></clipPath></defs>'
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="display:block;">', clip]
    layers = []

    # Outer mat
    s.append(rect(0, 0, W, H, OUTER))

    # Clipped App Frame: Dark #2D3142 Sidebar + #F5F6F8 Workspace + Floating #FFFFFF Header Card
    s.append('<g clip-path="url(#appClip)">')
    s.append(rect(ax, ay, SB_W, ah, INK))
    s.append(rect(WS_X, ay, WS_W, ah, WS_BG))
    hx, hy, hw, hh = HEADER
    s.append(rect(hx, hy, hw, hh, WHITE, rx=10, stroke=HAIR, sw=1))

    # Sidebar brand tile + static sidebar labels
    s.append(rect(SB_X, 34, 34, 34, SLATE_DARK, rx=8))
    for i, (bh, bc) in enumerate([(8, SLATE_200), (13, SLATE_100), (18, CORAL)]):
        s.append(rect(SB_X + 7 + i * 7.5, 60 - bh, 5, bh, bc, rx=1))
    s.append(rect(SB_X, 86, SB_IW, 1, SLATE_DARK))
    layers.append(htxt(72, 31, 146, 20, [('HOLIDAY P&L', 10.5, WHITE, 'Segoe UI Semibold', True)]))
    layers.append(htxt(72, 50, 146, 16, [('CHALLENGE 43', 7, SLATE_200, 'Consolas', False)]))
    layers.append(htxt(SB_X, 99, SB_IW, 18, [('NAVIGATION', 7, SUBTLE, 'Segoe UI Semibold', True)]))

    # Sidebar chapter navigation pills
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
    layers.append(htxt(SB_X, 295, SB_IW, 18, [
        ('SEASON', 7, SUBTLE, 'Segoe UI Semibold', True),
        ('  none = latest', 6.8, SLATE_200, 'Segoe UI', False),
    ]))
    layers.append(htxt(SB_X, 445, SB_IW, 18, [('CHANNEL', 7, SUBTLE, 'Segoe UI Semibold', True)]))
    s.append(rect(SB_X, 562, SB_IW, 1, SLATE_DARK))

    fx, fy, fw, fh = FILTERS_BTN
    s.append(rect(fx, fy, fw, fh, SLATE, rx=8))
    s.append(svg_icon('filter', fx + 20, fy + fh / 2, WHITE))

    rx_, ry_, rw, rh = RESET_BTN
    s.append(rect(rx_, ry_, rw, rh, SLATE_DARK, rx=8, stroke=SLATE, sw=1))
    s.append(svg_icon('reset', rx_ + 20, ry_ + rh / 2, SLATE_100))

    s.append(rect(SB_X, 686, SB_IW, 1, SLATE_DARK))
    layers.append(htxt(SB_X, 699, SB_IW, 18, [('GUIDE & NOTES', 7, SUBTLE, 'Segoe UI Semibold', True)]))
    for iy, ic in zip(INFO_Y, ('help', 'info')):
        s.append(rect(SB_X + 8, iy + 7, 24, 24, SLATE_DARK, rx=6))
        s.append(svg_icon(ic, SB_X + 20, iy + 19, SLATE_100))

    layers.append(htxt(SB_X, 997, SB_IW, 16, [('CREATED BY', 6.5, SUBTLE, 'Segoe UI Semibold', True)]))
    layers.append(htxt(SB_X, 1013, SB_IW, 18, [('Abhilash Sahani · 2026', 8, SLATE_100, 'Segoe UI Semibold', False)]))

    # Floating Header static kicker & page title + bottom footer
    kicker_txt, title_txt = PAGE_META[key]
    layers.append(htxt(hx + 18, hy + 8, 860, 18, [(kicker_txt, 7.5, SLATE, 'Segoe UI Semibold', True)]))
    layers.append(htxt(hx + 18, hy + 25, 860, 38, [(title_txt, 18, INK, 'Segoe UI Semibold', True)]))
    layers.append(htxt(X0, FOOT_Y + 2, 1260, 18, [(FOOT, 7, MUTED, 'Segoe UI', False)]))

    # Top-right Period badge pill
    px_, py_, pw, ph = PERIOD_PILL
    s.append(rect(px_, py_, pw, ph, SLATE_50, rx=13, stroke=SILVER, sw=1))

    # Takeaway Strip
    mx, my, mw, mh = MSG
    s.append(rect(mx, my, mw, mh, WHITE, rx=8, stroke=HAIR, sw=1))
    rail_col = CORAL if key == 'ch2' else SLATE
    s.append(rect(mx + 1, my + 7, 4, mh - 14, rail_col, rx=2))
    if key == 'profile':
        bx, by, bw, bh = BACK_BTN
        s.append(rect(bx, by, bw, bh, SURF_MUTED, rx=16, stroke=SILVER, sw=1))

    # 5 KPI Cards (Pages 1 & 2) with baked labels
    if kpis and key in KPI_META:
        for (kx, ky, kw, kh), (ic, risk, lbl) in zip(KPIS, KPI_META[key]):
            s.append(rect(kx, ky, kw, kh, WHITE, rx=10, stroke=HAIR, sw=1))
            s.append(rect(kx + 14, ky + 1, kw - 28, 3, CORAL if risk else SLATE, rx=1.5))
            s.append(rect(kx + 14, ky + 13, 26, 26, CORAL_50 if risk else SLATE_100, rx=6))
            s.append(svg_icon(ic, kx + 27, ky + 26, CORAL_TEXT if risk else SLATE))
            layers.append(htxt(kx + 46, ky + 16, kw - 58, 20, [(lbl, 8, MUTED, 'Segoe UI Semibold', False)]))

    # Main Cards + Baked Kickers & Vector Legends
    if key == 'ch1':
        for _, (cx, cy, cw, ch) in CARDS['ch1'].items():
            s.append(rect(cx, cy, cw, ch, WHITE, rx=10, stroke=HAIR, sw=1))
        layers += card_kicker_html(CARDS['ch1']['bridge'], 'PROFIT BRIDGE', 'kEUR · PY to CY',
                                   [('■', CORAL, 'Took margin'), ('■', SLATE_400, 'Added margin'), ('■', SLATE, 'CY total'), ('■', PY_BAR, 'PY total')], leg_y=69)
        layers += card_kicker_html(CARDS['ch1']['month'], 'CONTRIBUTION BY MONTH', 'kEUR · Oct–Jan · CY solid vs PY dotted',
                                   [('━━', SLATE, 'CY'), ('···', SUBTLE, 'PY'), ('●', SLATE, 'Max'), ('●', CORAL, 'Min')], leg_y=69)
        layers += card_kicker_html(CARDS['ch1']['band'], 'DISCOUNT DEPTH', 'kEUR · click › campaigns',
                                   [('■', SLATE, 'CY contribution'), ('■', PY_BAR, 'PY contribution')], leg_y=69)
        layers += card_kicker_html(CARDS['ch1']['scorecard'] if 'scorecard' in CARDS['ch1'] else CARDS['ch1']['type'],
                                   'CAMPAIGN SCORECARD', 'expand + for events · right-click › Profile',
                                   [('■', SLATE, '30%+ margin'), ('■', SLATE_200, '10–30%'), ('■', CORAL_200, '<0% loss'), ('●', SLATE, 'ΔPY gain'), ('●', CORAL_TEXT, 'ΔPY drop')], leg_y=55)

    elif key == 'ch2':
        for _, (cx, cy, cw, ch) in CARDS['ch2'].items():
            s.append(rect(cx, cy, cw, ch, WHITE, rx=10, stroke=HAIR, sw=1))
        layers += card_kicker_html(CARDS['ch2']['cat'], 'PRODUCTS', 'click › subcat › product',
                                   [('■', SLATE, 'CY contribution'), ('■', PY_BAR, 'PY contribution')], leg_y=69)
        layers += card_kicker_html(CARDS['ch2']['donut'], 'SEGMENTS › CHANNELS', 'click segment › channel split')
        layers += card_kicker_html(CARDS['ch2']['scatter'], 'MARKETS', 'x = discount %, y = margin %',
                                   [('●', CORAL, 'Berlin (lowest margin)'), ('●', SLATE, 'Other 7 cities')], leg_y=69)
        layers += card_kicker_html(CARDS['ch2']['heat'], 'RETURNS  ·  CATEGORY × CAMPAIGN', 'right-click › Profile',
                                   [('■', SLATE_50, '<6%'), ('■', SLATE_100, '6–10%'), ('■', SLATE_200, '10–15%'), ('■', CORAL_200, '15%+ high return')], leg_y=55)
        layers += card_kicker_html(CARDS['ch2']['chan'], 'CHANNEL › CATEGORY', 'click Online › Electronics',
                                   [('■', SLATE, 'CY contribution'), ('■', PY_BAR, 'PY contribution')], leg_y=69)

    elif key == 'ch3':
        cx_, cy_, cw_, ch_ = CARDS['ch3']['callout']
        s.append(rect(cx_, cy_, cw_, ch_, CALLOUT, rx=10, stroke=SILVER, sw=1.5, dash='5 4'))
        layers.append(htxt(cx_ + 20, cy_ + 16, cw_ - 40, 18, [
            ('COMBINED INDICATIVE UPSIDE', 7.5, MUTED, 'Segoe UI Semibold', True),
            ('   ·   per season', 7.5, SUBTLE, 'Segoe UI', False),
        ]))
        layers.append(htxt(cx_ + 20, cy_ + 102, cw_ - 40, 48, [
            ('Projected from CY volumes & margins assuming volumes hold; order of magnitude, not a forecast.', 8.5, BODY, 'Segoe UI', False),
        ]))

        ux, uy, uw, uh = CARDS['ch3']['upside_bar']
        s.append(rect(ux, uy, uw, uh, WHITE, rx=10, stroke=HAIR, sw=1))
        layers += card_kicker_html(CARDS['ch3']['upside_bar'], 'UPSIDE BY MOVE', 'kEUR · CY simulation',
                                   [('■', SLATE, 'Indicative CY contribution upside (€k)')], leg_y=33)

        lx_, ly_, lw_, lh_ = CARDS['ch3']['limits']
        s.append(rect(lx_, ly_, lw_, lh_, WHITE, rx=10, stroke=HAIR, sw=1))
        layers += card_kicker_html(CARDS['ch3']['limits'], 'ANALYTICAL GUARDRAILS', 'what this dataset cannot tell you')
        for i, (t_, d_) in enumerate(LIM_SHORT):
            s.append(circle(lx_ + 28, ly_ + 68 + i * 62, 11, SLATE_100))
            s.append(svg_icon('info', lx_ + 28, ly_ + 68 + i * 62, SLATE, sw=2))
            layers.append(htxt(lx_ + 48, ly_ + 49 + i * 62, lw_ - 66, 48, [
                (t_, 9, INK, 'Segoe UI Semibold', True),
                (d_, 9, BODY, 'Segoe UI', False),
            ]))

        for (ax_, ay_, aw_, ah_), (code, title, test) in zip(ACTION_ROWS, MOVES_STATIC):
            s.append(rect(ax_, ay_, aw_, ah_, WHITE, rx=10, stroke=HAIR, sw=1))
            s.append(rect(ax_ + 1, ay_ + 16, 4, ah_ - 32, SLATE, rx=2))
            s.append(rect(ax_ + 20, ay_ + 18, 68, 24, SLATE_50, rx=4, stroke=SILVER, sw=1))
            s.append(rect(ax_ + 736, ay_ + 18, 1, ah_ - 36, HAIR))
            layers.append(htxt(ax_ + 20, ay_ + 22, 68, 20, [(code, 8.5, BODY, 'Consolas', True)], align='center'))
            layers.append(htxt(ax_ + 102, ay_ + 17, 610, 28, [(title, 12, INK, 'Segoe UI Semibold', True)]))
            layers.append(htxt(ax_ + 758, ay_ + 21, 280, 18, [('INDICATIVE UPSIDE', 7, MUTED, 'Segoe UI Semibold', True)]))
            layers.append(htxt(ax_ + 758, ay_ + 89, 280, 18, [('PILOT TEST', 7, MUTED, 'Segoe UI Semibold', True)]))
            layers.append(htxt(ax_ + 758, ay_ + 109, 280, 78, [(test, 9, BODY, 'Segoe UI', False)]))

    elif key == 'profile':
        fx_, fy_, fw_, fh_ = CARDS['profile']['facts']
        s.append(rect(fx_, fy_, fw_, fh_, CALLOUT, rx=10, stroke=SILVER, sw=1.5, dash='5 4'))
        layers.append(htxt(fx_ + 18, fy_ + 13, fw_ - 36, 18, [
            ('EVENT FACTS', 7.5, MUTED, 'Segoe UI Semibold', True),
            ('   ·   for the campaign or type you drilled into', 7.5, SUBTLE, 'Segoe UI', False),
        ]))
        for nm in ('pnl', 'daily', 'band'):
            cx, cy, cw, ch = CARDS['profile'][nm]
            s.append(rect(cx, cy, cw, ch, WHITE, rx=10, stroke=HAIR, sw=1))
        layers += card_kicker_html(CARDS['profile']['pnl'], 'PROFIT AND LOSS', 'kEUR · costs in brackets',
                                   [('■', PY_BAR, 'PY'), ('■', SLATE, 'CY / Favorable ΔPY'), ('■', CORAL, 'Adverse ΔPY')], leg_y=69)
        px0, py0, _, _ = CARDS['profile']['pnl']
        hx_ = px0 + 16 + 134 + 8
        for lbl, wcol in [('PY', 158), ('CY', 158), ('ΔPY', 134), ('ΔPY %', 126)]:
            layers.append(htxt(hx_, py0 + 94, wcol, 18, [(lbl, 7.5, MUTED, 'Segoe UI Semibold', True)]))
            hx_ += wcol + 10
        layers += card_kicker_html(CARDS['profile']['daily'], 'NET SALES PER TRADING DAY', 'kEUR · daily trading',
                                   [('■', SLATE, 'CY net sales'), ('■', PY_BAR, 'PY net sales')], leg_y=69)
        layers += card_kicker_html(CARDS['profile']['band'], 'DISCOUNT DEPTH', 'kEUR · by discount band',
                                   [('■', SLATE, 'CY contribution'), ('■', PY_BAR, 'PY contribution')], leg_y=69)

    s.append(rect(X0, 1024, MW, 1, HAIR))
    s.append('</g>')
    s.append(rect(ax, ay, aw, ah, 'none', rx=12, stroke=HAIR, sw=1))
    s.append('</svg>')
    return f'<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;">{"".join(s)}{"".join(layers)}</div>', ''.join(s)


def drawer():
    d = DRAWER['panel']
    cl = DRAWER['close']
    svg = ''.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="display:block;">',
        rect(0, 0, W, H, INK, 0, 0.28),
        rect(d['x'], d['y'], d['w'], d['h'], WHITE, rx=10, stroke=SILVER, sw=1),
        rect(cl['x'], cl['y'], cl['w'], cl['h'], SURF_MUTED, rx=15, stroke=SILVER, sw=1),
        rect(d['x'] + 24, DRAWER['divider'], d['w'] - 48, 2, SLATE),
        '</svg>',
    ])
    return svg, svg


def tooltip():
    w, h = TT['w'], TT['h']
    svg = ''.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block;">',
        rect(0, 0, w, h, WHITE, rx=6, stroke=SILVER, sw=1),
        rect(0, 0, 4, h, SLATE, rx=2),
        rect(18, 60, w - 36, 1, HAIR),
        rect(18, 148, w - 36, 1, HAIR),
        rect(w // 2 + 4, 72, 1, 146, HAIR),
        '</svg>',
    ])
    layers = [
        htxt(20, 71, 154, 16, [('NET SALES · CY', 6.5, MUTED, 'Segoe UI Semibold', True)]),
        htxt(198, 71, 154, 16, [('CONTRIBUTION · CY', 6.5, MUTED, 'Segoe UI Semibold', True)]),
        htxt(20, 157, 154, 16, [('MARGIN · CY', 6.5, MUTED, 'Segoe UI Semibold', True)]),
        htxt(198, 157, 154, 16, [('WEIGHTED DISCOUNT · CY', 6.5, MUTED, 'Segoe UI Semibold', True)]),
    ]
    return f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;">{svg}{"".join(layers)}</div>', svg


files = {
    'bg_ch1': (*page('ch1', 'ch1', kpis=False), W, H, False),
    'bg_ch2': (*page('ch2', 'ch2', kpis=False), W, H, False),
    'bg_ch3': (*page('ch3', 'ch3', kpis=False), W, H, False),
    'bg_profile': (*page('profile', 'ch1', kpis=False), W, H, False),
    'overlay_drawer': (*drawer(), W, H, True),
    'bg_tooltip': (*tooltip(), TT['w'], TT['h'], True),
}

for n, (_, svg_only, _, _, _) in files.items():
    open(os.path.join(OUT, n + '.svg'), 'w', encoding='utf-8').write(svg_only)

with sync_playwright() as p:
    browser = p.chromium.launch()
    for n, (body_html, _, vw, vh, transparent) in files.items():
        pw_page = browser.new_page(viewport={'width': vw, 'height': vh}, device_scale_factor=2)
        html = f'<!DOCTYPE html><html><body style="margin:0;padding:0;background:transparent;overflow:hidden;">{body_html}</body></html>'
        pw_page.set_content(html, wait_until='load')
        pw_page.screenshot(path=os.path.join(OUT, n + '.png'), omit_background=transparent)
        pw_page.close()
    browser.close()

print('Generated V12 Baked-Typography 2x Retina PNGs:', sorted(f for f in os.listdir(OUT) if f.endswith('.png')))
