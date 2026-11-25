"""Challenge 43 - Holiday P&L, V12 Modern UX Dark-Rail + Slate-Coral Editorial Edition.
Dark Jet Black (#2D3142) vertical navigation rail + #F5F6F8 cool workspace + pure #FFFFFF zero-shadow cards;
3 main pages + 1 hidden drill-through + 1 hidden tooltip; 9 ZoomCharts visuals; 10 KPI micro-charts; 20 bookmarks."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pb import *
from layout12 import *

ROOT = sys.argv[1]
TT_PAGE = 'tt_snapshot'
PID = {'ch1': 'p1_what_why', 'ch2': 'p2_leaks', 'ch3': 'p3_actions', 'profile': 'p4_campaign_profile'}
BG = {k: f'bg_{k}_c43.png' for k in PID}
CHAPTERS = [
    ('ch1', 'What happened & why'),
    ('ch2', 'Where it leaks'),
    ('ch3', 'What to do'),
]
NAVL = {'ch1': 'What & why', 'ch2': 'Where it leaks', 'ch3': 'What to do'}
SEASONS = ['2023/24', '2024/25', '2025/26']
FOOT = ('Source: FP20 Analytics Challenge 43 (synthetic data)  ·  CY = selected season  ·  PY = same dates one season earlier  ·  '
        'Blue Slate = CY/favorable, Coral = adverse/leak  ·  contribution excludes overhead, interest & tax')


def slabel(txt, size=7.5, color=MUTED):
    return run(txt.upper(), size, color, FONT_SB, True)


# ---------------------------------------------------------------- Dark Sidebar + Workspace Header + Takeaway Bar
def sidebar(p, pid, active):
    textbox(p, f'{pid}_brand', 72, 30, 146, 42, [
        [run('HOLIDAY P&L', 10.5, WHITE, FONT_SB, True)],
        [run('CHALLENGE 43', 7, SLATE_200, NUM)],
    ])
    textbox(p, f'{pid}_lbl_nav', SB_X, 98, SB_IW, 18, [[slabel('Navigation', 7, SUBTLE)]])
    for k, ny in zip(('ch1', 'ch2', 'ch3'), NAV_Y):
        on = (active == k)
        tbutton(p, f'{pid}_nav_{k}', SB_X + 36, ny, SB_IW - 40, NAV_H, NAVL[k], lpage(PID[k]),
                WHITE if on else SLATE_100, WHITE, size=9.5, font=(FONT_SB if on else FONT),
                tip=f'Open {NAVL[k]}', align='left')

    textbox(p, f'{pid}_lbl_season', SB_X, 294, SB_IW, 18, [[slabel('Season', 7, SUBTLE), run('  none = latest', 6.8, SLATE_200)]])
    sx, sy, sw, sh = SEASON_BOX
    sidebar_chips(p, f'{pid}_chip_season', sx, sy, sw, sh, 'DimDate.Season', 'sync_season', 1, rows=3, size=8.5, filt=SEASONS)

    textbox(p, f'{pid}_lbl_channel', SB_X, 444, SB_IW, 18, [[slabel('Channel', 7, SUBTLE)]])
    cx, cy, cw, ch = CHANNEL_BOX
    sidebar_chips(p, f'{pid}_chip_channel', cx, cy, cw, ch, 'FactSales.Sales Channel', 'sync_channel', 1, rows=2, size=8.5)

    fx, fy, fw, fh = FILTERS_BTN
    tbutton(p, f'{pid}_btn_filters', fx + 34, fy, fw - 38, fh, 'More filters', lbm(f'bm_{pid}_filters'),
            WHITE, SLATE_100, size=9, tip='Segment, market, category, campaign type, discount band', align='left')
    rx_, ry_, rw, rh = RESET_BTN
    tbutton(p, f'{pid}_btn_reset', rx_ + 34, ry_, rw - 38, rh, 'Reset all', lbm(f'bm_{pid}_reset'),
            SLATE_100, WHITE, size=9, tip='Clear every filter: CY returns to latest season', align='left')

    textbox(p, f'{pid}_lbl_info', SB_X, 698, SB_IW, 18, [[slabel('Guide & notes', 7, SUBTLE)]])
    tbutton(p, f'{pid}_btn_guide', SB_X + 38, INFO_Y[0], SB_IW - 40, 38, 'How to read', lbm(f'bm_{pid}_guide'),
            SLATE_200, WHITE, size=9, tip='How to read charts & Slate-Coral notation', align='left')
    tbutton(p, f'{pid}_btn_limits', SB_X + 38, INFO_Y[1], SB_IW - 40, 38, 'Data notes', lbm(f'bm_{pid}_limits'),
            SLATE_200, WHITE, size=9, tip='Definitions and limits of the dataset', align='left')

    textbox(p, f'{pid}_credit', SB_X, 996, SB_IW, 44, [
        [run('CREATED BY', 6.5, SUBTLE, FONT_SB, True)],
        [run('Abhilash Sahani · 2026', 8, SLATE_100, FONT_SB)],
    ])


def header(p, pid, kicker, title, msg_m, nxt=None, back=False):
    textbox(p, f'{pid}_kicker', X0, 23, 860, 18, [[slabel(kicker, 7.5, SLATE)]])
    textbox(p, f'{pid}_title', X0, 41, 860, 40, [[run(title, 18, INK, FONT_SB, True)]])
    px_, py_, pw, ph = PERIOD_PILL
    textcard(p, f'{pid}_period', px_ + 10, py_ + 3, pw - 20, ph - 6, 'Period Short', size=8, color=BODY, font=NUM, wrap=False, align='center')
    textcard(p, f'{pid}_filt', 1140, 56, 736, 18, 'Filters Line', size=7.5, color=MUTED, wrap=False, align='right')

    mx, my, mw, mh = MSG
    msg_w = mw - 134 if back else mw - 30
    textcard(p, f'{pid}_msg', mx + 16, my + 7, msg_w, mh - 14, msg_m, size=11.5, color=INK, font=FONT_SB, wrap=False)
    if back:
        bx, by, bw, bh = BACK_BTN
        tbutton(p, f'{pid}_btn_back', bx, by, bw, bh, '‹  Back', lback(), BODY, INK, size=9,
                tip='Back to the page you came from', align='center')

    textbox(p, f'{pid}_foot', X0, FOOT_Y, 1260, 20, [[run(FOOT, 7, MUTED)]])
    if nxt:
        k, t = nxt
        lbl = 'Back to start  ·  What happened & why  ↺' if k == 'ch1' else f'Next chapter  ·  {t}  →'
        tbutton(p, f'{pid}_next', 1520, FOOT_Y - 3, 356, 26, lbl, lpage(PID[k]), SLATE, INK, size=9,
                tip=f'Open {t}', align='right')


def card_head(p, name, card, take_m, kicker, note=None):
    x, y, w, _ = card
    parts = [slabel(kicker, 7.5, MUTED)]
    if note:
        parts.append(run('   ·   ' + note, 7.5, SUBTLE))
    textbox(p, f'{name}_t', x + 18, y + 12, w - 36, 18, [parts])
    if take_m:
        textcard(p, f'{name}_m', x + 18, y + 32, w - 36, 24, take_m, size=10.5, color=INK, font=FONT_SB, wrap=False)


# ---------------------------------------------------------------- KPI Cards (Icon Badge + Monospace Hero + Oct-Jan Micro-Chart)
def kpi_card_v12(p, name, box, label, k, ac_m, py_m, style='bars', bar_col_m=None):
    x, y, w, h = box
    textbox(p, f'{name}_lbl', x + 46, y + 15, w - 58, 20, [[run(label, 8, MUTED, FONT_SB)]])
    textcard(p, f'{name}_val', x + 13, y + 44, 134, 34, f'KPI {k} AC', size=17.5, color=INK, font=NUM, wrap=False, bold=True)
    textcard(p, f'{name}_d', x + 14, y + 82, 138, 18, f'KPI {k} Tag', size=8, font=NUM, wrap=False, color_measure=f'KPI {k} Col', bold=True)
    textcard(p, f'{name}_py', x + 14, y + 104, 138, 18, f'KPI {k} PY', size=7, color=SUBTLE, font=NUM, wrap=False)

    cx, cy, cw, ch = x + 150, y + 38, w - 160, h - 46
    if style == 'area':
        o = {
            'legend': props(show=L(False)),
            'valueAxis': props(show=L(False), gridlineShow=L(False), showAxisTitle=L(False)),
            'categoryAxis': props(show=L(True), fontSize=D(7), labelColor=col(SUBTLE), fontFamily=L(NUM), showAxisTitle=L(False)),
            'labels': props(show=L(False)),
            'lineStyles': [
                {'properties': {'strokeWidth': D(2), 'areaShow': L(False), 'strokeTransparency': D(0)}, 'selector': {'metadata': f'_Measures.{ac_m}'}},
                {'properties': {'strokeWidth': D(1), 'strokeTransparency': D(100), 'areaMatchStrokeColor': L(True)}, 'selector': {'metadata': f'_Measures.{py_m}'}},
            ],
            'dataPoint': [
                {'properties': {'fill': col(SLATE)}, 'selector': {'metadata': f'_Measures.{ac_m}'}},
                {'properties': {'fill': col(PY_AREA)}, 'selector': {'metadata': f'_Measures.{py_m}'}},
            ],
        }
        q = query({'Category': ['DimDate.Season Month'], 'Y': [(f'#{py_m}', 'PY'), (f'#{ac_m}', 'CY')]}, [('DimDate.Season Month', 'Ascending')])
        p.add(f'{name}_spark', 'areaChart', cx, cy, cw, ch, q=q, objects=o, vco_=vco(header=False, pad=(0, 0, 0, 0), tooltip=True))
    else:
        o = {
            'layout': props(clusteredGapOverlaps=L(True), clusteredGapSize=D(100)),
            'legend': props(show=L(False)),
            'valueAxis': props(show=L(False), gridlineShow=L(False), showAxisTitle=L(False)),
            'categoryAxis': props(show=L(True), fontSize=D(7), labelColor=col(SUBTLE), fontFamily=L(NUM), showAxisTitle=L(False), innerPadding=D(38)),
            'labels': props(show=L(False)),
            'dataPoint': [measure_fill(bar_col_m)],
            'error': error_target_tick(ac_m, py_m, color=INK),
        }
        q = query({'Category': ['DimDate.Season Month'], 'Y': [(f'#{ac_m}', 'CY')], 'Tooltips': [(f'#{py_m}', 'PY')]}, [('DimDate.Season Month', 'Ascending')])
        p.add(f'{name}_spark', 'clusteredColumnChart', cx, cy, cw, ch, q=q, objects=o, vco_=vco(header=False, pad=(0, 0, 0, 0), tooltip=True))


# ---------------------------------------------------------------- Native Bar Table + Heatmap + ZoomCharts
def bar_obj(cat_axis, pad, start=None, end=None, fill=None, fill_m=None, labels=True, units=None, prec=None, cat_col=INK, lsize=8.5):
    va = {'show': L(False), 'gridlineShow': L(False)}
    if start:
        va['start'] = M(start)
    if end:
        va['end'] = M(end)
    o = {'legend': props(show=L(False)),
         'valueAxis': [{'properties': va}],
         'categoryAxis': props(show=L(cat_axis), fontSize=D(lsize), labelColor=col(cat_col), fontFamily=L(FONT), showAxisTitle=L(False),
                               innerPadding=D(pad), maxMarginFactor=D(45), preferredCategoryWidth=D(10)),
         'labels': props(show=L(labels), fontSize=D(8), color=col(INK), fontFamily=L(NUM))}
    if units is not None:
        o['labels'][0]['properties']['labelDisplayUnits'] = D(units)
    if prec is not None:
        o['labels'][0]['properties']['labelPrecision'] = L(prec)
    if fill:
        o['dataPoint'] = [{'properties': {'fill': col(fill)}}]
    if fill_m:
        o['dataPoint'] = [measure_fill(fill_m)]
    return o


def bar(p, name, x, y, w, h, cat, ms, objects, sort, tt=True, tips=None, vtype='clusteredBarChart'):
    roles = {'Category': [cat], 'Y': ms}
    if tips:
        roles['Tooltips'] = tips
    c = vco(header=True, pad=(0, 0, 0, 0), tooltip_page=(TT_PAGE if tt else None))
    return p.add(name, vtype, x, y, w, h, q=query(roles, sort), objects=objects, vco_=c)


def table(p, name, blk, cat, label_w, cols, sort, rows, anchor, tt=True, y_off=82, hdr_y_off=60):
    """Editorial bar table inside a pure-white card."""
    x, y, w, h = blk
    cy, ch = y + y_off, h - y_off - 12
    rowh = ch / rows
    pad_bar = pad_pin = max(30, min(88, round(100 * (1 - 22 / rowh))))
    sort_tips = [(s_[0], 'sort') for s_ in sort if s_[0].startswith('#')]
    base_tips = [(f'#{anchor}', 'row')] + [t for t in sort_tips if t[0] != f'#{anchor}']

    def tips_for(ms):
        used = {m if isinstance(m, str) else m[0] for m in ms}
        return [t for t in base_tips if t[0] not in used]

    cx = x + 16
    for i, c in enumerate(cols):
        first = i == 0
        cw = c['w'] + (label_w + 8 if first else 0)
        hx = cx + (label_w + 8 if first else 0)
        if c.get('hdr'):
            textbox(p, f'{name}_h{i}', hx, y + hdr_y_off, c['w'], 20, [[run(c['hdr'], 7.5, MUTED, FONT_SB, True)]])
        k = c['kind']

        def axis_fix(o, show_labels):
            ca = o['categoryAxis'][0]['properties']
            ca['show'] = L(True)
            if show_labels:
                ca['maxMarginFactor'] = D(round(100 * (label_w + 4) / cw))
            else:
                ca['labelColor'] = col(WHITE)
                ca['maxMarginFactor'] = D(5)
            return o

        if k == 'stack':
            o = bar_obj(True, pad_bar, c.get('start'), c.get('end'))
            o['dataPoint'] = [{'properties': {'fill': col(cc)}, 'selector': {'metadata': f'_Measures.{mm}'}} for mm, cc, _ in c['series']]
            lab = [{'properties': {'show': L(True), 'fontSize': D(8.5), 'color': col(INK), 'fontFamily': L(NUM), 'labelOverflow': L(True)}}]
            for mm, _, lc in c['series']:
                if not lc:
                    lab.append({'properties': {'show': L(False)}, 'selector': {'metadata': f'_Measures.{mm}'}})
                    continue
                lab.append({'properties': {'show': L(True), 'color': col(lc.get('color', INK)), 'labelPosition': L(lc.get('pos', 'Auto'))},
                            'selector': {'metadata': f'_Measures.{mm}'}})
                if lc.get('value'):
                    lab.append({'properties': {'dynamicLabelValue': {'expr': fmea(lc['value'])}},
                                'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}], 'metadata': f'_Measures.{mm}', 'highlightMatching': 1}})
            o['labels'] = lab
            o = axis_fix(o, first)
            ms = [(f'#{mm}', mm.replace(' k', '').replace('Bridge ', '').replace('AC', 'CY')) for mm, _, _ in c['series']]
            bar(p, f'{name}_{i}', cx, cy, cw, ch, cat, ms, o, sort, tt, tips=tips_for(ms), vtype='barChart')
        else:
            if k == 'single':
                o = bar_obj(True, pad_bar, c.get('start'), c.get('end'), fill=c['colour'], units=c.get('units'), prec=c.get('prec'))
            else:
                o = bar_obj(True, pad_pin if k == 'pin' else pad_bar, c.get('start'), c.get('end'), fill_m=c.get('fill_m'),
                            fill=c.get('fill'), units=c.get('units'), prec=c.get('prec'))
            o = axis_fix(o, first)
            ms = [(f"#{c['m']}", c.get('label', c['m']))]
            bar(p, f'{name}_{i}', cx, cy, cw, ch, cat, ms, o, sort, tt, tips=tips_for(ms))
        cx += cw + 10


def heatmap(p, name, card, rows, colsf, val, col_m, font_m, take_m, kicker, note, nrows=4, ncols=5, rh_w=138):
    card_head(p, name, card, take_m, kicker, note)
    x, y, w, h = card
    vw, vh = w - 32, h - 76
    rp = max(4, min(14, round(((vh - 14) / (nrows + 1) - 27) / 2)))
    cw = max(60, min(170, round((vw - rh_w - 12) / ncols) - 6))
    o = {'grid': props(gridVertical=L(True), gridVerticalColor=col(WHITE), gridVerticalWeight=D(4),
                       gridHorizontal=L(True), gridHorizontalColor=col(WHITE), gridHorizontalWeight=D(4),
                       rowPadding=D(rp), outlineColor=col(WHITE), outlineWeight=D(0)),
         'columnHeaders': props(fontColor=col(MUTED), fontSize=D(9), fontFamily=L(NUM), alignment=L('Center'), backColor=col(WHITE), outlineStyle=L(0),
                                autoSizeColumnWidth=L(False)),
         'rowHeaders': props(fontColor=col(INK), fontSize=D(10), fontFamily=L(FONT), backColor=col(WHITE), outlineStyle=L(0)),
         'values': [{'properties': {'fontSize': D(10.5), 'fontFamily': L(NUM), 'outlineStyle': L(0)}},
                    {'properties': {'backColor': mcol(col_m), 'fontColor': mcol(font_m)},
                     'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}], 'metadata': f'_Measures.{val}'}}],
         'columnWidth': [{'properties': {'value': D(cw)}, 'selector': {'metadata': f'_Measures.{val}'}}],
         'columnFormatting': [{'properties': {'alignment': L('Center')}, 'selector': {'metadata': f'_Measures.{val}'}}],
         'subTotals': props(rowSubtotals=L(False), columnSubtotals=L(False))}
    p.add(f'{name}_mx', 'pivotTable', x + 16, y + 64, vw, vh,
          q=query({'Rows': [rows], 'Columns': [colsf], 'Values': [(f'#{val}', 'CY')]}), objects=o,
          vco_=vco(header=True, pad=(0, 0, 0, 0), tooltip_page=TT_PAGE))


def zc_chart(p, name, kind, card, roles, take_m, kicker, note, extra=None, sort=None):
    card_head(p, name, card, take_m, kicker, note)
    x, y, w, h = card
    vt, _ = ZC[kind]
    o = {'advanced': [{'properties': {'shouldApplyNewDefaults': L(True)}}], 'toolbar': props(show=L(False)), 'legend': props(show=L(False))}
    if extra:
        o.update(extra)
    return p.add(name, vt, x + 12, y + 58, w - 24, h - 66, q=query(roles, sort), objects=o, vco_=vco(header=True, pad=(0, 0, 0, 0)))


def refline_acpy(c_py=INK, c_ac=SLATE_400, pad_lr=False, bar_w_pct=46, marker_w_pct=84, pad_tb=False):
    o = series_colors({1: c_py, 2: c_ac})
    o['seriesDefault'][0]['properties'].update({
        'seriesSettingSelector': L('s1'),
        'type1': L('referenceLine'),
        'customize1': L(True),
        'lineWidth1': L(3),
        'lineColor1': col(c_py),
        'widthPercent1': L(marker_w_pct),
        'zIndex1': L(25),
        'customize2': L(True),
        'widthPercent2': L(bar_w_pct),
    })
    o['valueAxis1'] = props(show=L(False))
    o['seriesValueLabelsDefault'] = [{
        'properties': {
            'seriesValueLabelSettingSelector': L('s2'),
            'show1': L(False),
            'useDefaults1': L(False),
            'valueLabelPosition1': L('outside'),
            'fontSize1': D(9),
            'backgroundColorOpacity1': L(0),
            'show2': L(True),
            'useDefaults2': L(False),
            'valueLabelPosition2': L('outside'),
            'fontSize2': D(9),
            'backgroundColorOpacity2': L(0),
        }
    }]
    cb = {}
    if pad_lr:
        cb.update(leftPadding=L(15), rightPadding=L(15))
    if pad_tb:
        cb.update(topPadding=L(10), bottomPadding=L(10))
    if cb:
        o['columnBarSettings'] = props(**cb)
    return o


# ---------------------------------------------------------------- Slide-over Drawer
DR = DRAWER['panel']
DX, DW = DR['x'] + 24, DR['w'] - 48
NOTATION = ('How to read Slate-Coral IBCS',
            'Blue Slate (#4F5D75) = CY & favorable gains. Silver-Grey (#8B909E / #B5BECC) = PY (one season earlier). '
            'Coral Glow (#EF8354) = adverse bars, margin erosion & 15%+ return leaks; Burnt Coral (#BA4B1D) = small adverse text. '
            'In KPI cards, Oct–Jan micro-charts plot the solid Blue Slate CY line over the shaded PY area.')
LIMITS = [
    ('Synthetic data.', ' Three October–January holiday windows (2023/24, 2024/25, 2025/26) across eight European city markets. 2023/24 has no PY.'),
    ('Descriptive, not causal.', ' There is no control group, randomisation or ad-exposure data, so nothing here proves a campaign caused extra sales, uplift or ROI.'),
    ('Contribution profit', ' = net sales − product cost − fulfilment − payment fees − return handling − allocated campaign spend. It excludes overhead, interest and tax.'),
    ('Unequal durations.', ' Black Friday and Cyber Monday run 3 days; Christmas 17 and New Year 15. Compare margins or per-day sales, not totals.'),
    ('Campaign spend', ' is each event budget allocated to sales lines by gross-sales share.'),
    ('Weighted discount %', ' = discount € ÷ gross sales €. Returns carry no return date; refunds count against the original sale.'),
]
GUIDES = {
    'ch1': [('KPI strip.', 'Top 5 cards show CY hero metrics, PY delta tags, and Oct–Jan CY lines over shaded PY baselines.'),
            ('Profit bridge.', 'Left tall card reads top-down from PY contribution to CY: Blue Slate bars added margin, Coral Glow bars eroded it.'),
            ('Month, discount & campaign drills.', 'Monthly Contribution plots the solid CY line against a dotted light grey PY line with Max (Blue Slate) and Min (Coral) callouts; Discount Depth & Campaign Scorecard ZoomCharts cards drill down or right-click › Drill through.')],
    'ch2': [('Product hierarchy.', 'Top-left ZoomCharts Combo Bar drills Category › Subcategory › Product.'),
            ('Segments & cities.', 'Top-mid ZoomCharts Donut drills Customer Segment › Channel; top-right Scatter plots city discount % vs contribution margin %.'),
            ('Returns & channels.', 'Bottom-left heatmap flags 15%+ return cells in Coral; bottom-right Combo Bar drills Sales Channel › Category.')],
    'ch3': [('Projected callout & upside bar.', 'Top-left dashed Slate-50 card shows combined indicative upside; below it, upside ranked by move and analytical guardrails.'),
            ('Action rails (ACT-01 to ACT-04).', 'Each move pairs live DAX evidence, a deep-link back to Chapter 1 or 2, indicative €k upside, and a pilot test protocol.')],
    'profile': [('Drill-through profile.', 'Filtered to the campaign or campaign type you right-clicked from Chapter 1 or Chapter 2.'),
                ('P&L & daily/discount drills.', 'Left P&L card compares PY, CY, ΔPY and ΔPY%; right ZoomCharts cards track daily net sales and discount bands.')],
}


def drawer(p, pid, guide_lines):
    g = {'common': [], 'filters': [], 'guide': [], 'limits': []}
    g['common'].append(resimg(p, f'{pid}_dw_img', 0, 0, W, H, 'overlay_drawer_c43.png', hidden=True)['name'])
    c = DRAWER['close']
    g['common'].append(tbutton(p, f'{pid}_dw_close', c['x'], c['y'], c['w'], c['h'], 'Close  ✕', lbm(f'bm_{pid}_close'), BODY, INK, size=8.5, hidden=True, tip='Close panel')['name'])

    def hdr(kind, title, sub):
        g[kind].append(textbox(p, f'{pid}_dw_{kind}_hdr', DX, DR['y'] + 14, 340, 50,
                               [[run(title, 13, INK, FONT_SB, True)], [run(sub, 8, MUTED)]], hidden=True)['name'])

    hdr('filters', 'More filters', 'Apply across all chapters  ·  Season & Channel are in the left rail')
    y = 148
    for key, label, field, cols, rows in [('seg', 'CUSTOMER SEGMENT', 'FactSales.Customer Segment', 2, 2),
                                          ('city', 'MARKET', 'DimLocation.City', 4, 2),
                                          ('cat', 'PRODUCT CATEGORY', 'DimProduct.Category', 2, 2),
                                          ('ctype', 'CAMPAIGN TYPE', 'DimCampaign.Campaign Type', 3, 2),
                                          ('band', 'DISCOUNT BAND', 'FactSales.Discount Band', 3, 2)]:
        g['filters'].append(textbox(p, f'{pid}_dw_l_{key}', DX, y, DW, 18, [[slabel(label)]], hidden=True)['name'])
        g['filters'].append(drawer_chips(p, f'{pid}_dw_s_{key}', DX - 4, y + 20, DW + 8, 38 * rows, field, f'sync_{key}', cols, rows=rows, size=8.5, hidden=True)['name'])
        y += 24 + 38 * rows + 18

    hdr('guide', 'How to read this page', 'Blue Slate = CY/favorable  ·  Silver = PY  ·  Coral = adverse')
    paras = [[run(NOTATION[0], 10, INK, FONT_SB, True)], [run(NOTATION[1], 9, BODY)], [run(' ', 5)]]
    for i, (t, d) in enumerate(guide_lines):
        paras += [[run(f'{i + 1}  {t}', 10, INK, FONT_SB, True)], [run(d, 9, BODY)], [run(' ', 4)]]
    g['guide'].append(textbox(p, f'{pid}_dw_g_txt', DX, 148, DW, 860, paras, hidden=True)['name'])

    hdr('limits', 'Data notes and limits', 'Read these before drawing conclusions')
    paras = []
    for t, d in LIMITS:
        paras += [[run(t, 9.5, INK, FONT_SB, True), run(d, 9.5, BODY)], [run(' ', 5)]]
    g['limits'].append(textbox(p, f'{pid}_dw_lim_txt', DX, 148, DW, 860, paras, hidden=True)['name'])

    return g


pages, drawers = {}, {}
TIPS_C = [('#Margin AC', 'Margin CY'), ('#Net Sales AC', 'Net sales CY'), ('#Contribution ΔPY', 'Contribution ΔPY')]

# ================================================================== 1 · What happened & why (3 ZoomCharts visuals)
pid = PID['ch1']; p = Page(pid, '1 · What happened & why', BG['ch1']); pages['ch1'] = p; C = CARDS['ch1']
sidebar(p, pid, 'ch1')
header(p, pid, 'CHAPTER 1 OF 3  ·  HOLIDAY TRADING AUDIT · 8 EUROPEAN CITY MARKETS', 'What happened & why', 'Msg Ch1', nxt=CHAPTERS[1])
for i, (lbl, k, ac_m, py_m, sty, bar_m) in enumerate([
    ('Contribution profit', 'Contribution', 'Contribution AC k', 'Contribution PY k', 'area', None),
    ('Contribution margin', 'Margin', 'Margin AC', 'Margin PY', 'area', None),
    ('Net sales', 'Net Sales', 'Net Sales AC k', 'Net Sales PY k', 'area', None),
    ('Weighted discount', 'Discount', 'Discount AC', 'Discount PY', 'area', None),
    ('Sales at 20%+ discount', 'Deep', 'Deep Share AC', 'Deep Share PY', 'area', None),
]):
    kpi_card_v12(p, f'{pid}_k{i}', KPIS[i], lbl, k, ac_m, py_m, style=sty, bar_col_m=bar_m)

card_head(p, f'{pid}_br', C['bridge'], 'Title Bridge Var', 'PROFIT BRIDGE', 'kEUR · PY to CY')
textbox(p, f'{pid}_br_leg', C['bridge'][0] + 18, C['bridge'][1] + 58, 520, 18, [[
    run('●  ', 8, CORAL), run('Took margin   ', 7.5, MUTED),
    run('●  ', 8, SLATE), run('Added / CY   ', 7.5, MUTED),
    run('●  ', 8, PY_BAR), run('PY', 7.5, MUTED),
]])
table(p, f'{pid}_br', C['bridge'], 'Bridge Lines.Label', 126,
      [{'kind': 'stack', 'hdr': '', 'w': 392, 'end': 'Axis Bridge End 2',
        'series': [('Bridge Base k', WHITE, None), ('Bridge PY k', PY_BAR, None), ('Bridge AC k', SLATE, None),
                   ('Bridge Up k', SLATE_400, None), ('Bridge Down k', CORAL, None),
                   ('Bridge Tail k', WHITE, {'pos': 'InsideBase', 'value': 'Bridge Label k', 'color': INK})]}],
      [('Bridge Lines.Label', 'Ascending')], rows=10, anchor='Anchor Bridge', tt=False, y_off=82, hdr_y_off=60)

mc_x, mc_y, mc_w, mc_h = C['month']
card_head(p, f'{pid}_month', C['month'], 'Title Month AC', 'CONTRIBUTION BY MONTH', 'CY solid vs PY dotted · click › daily')
textbox(p, f'{pid}_month_leg', mc_x + 18, mc_y + 58, mc_w - 36, 18, [[
    run('━━ ', 7.5, SLATE, FONT_SB, True), run('CY   ', 7.5, MUTED),
    run('··· ', 9, SUBTLE, FONT_SB, True), run('PY   ', 7.5, MUTED),
    run('● ', 8.5, SLATE), run('Max   ', 7.5, SLATE, FONT_SB, True),
    run('● ', 8.5, CORAL), run('Min', 7.5, CORAL_TEXT, FONT_SB, True),
]])
month_objs = {
    'legend': props(show=L(False)),
    'valueAxis': props(show=L(False), gridlineShow=L(False), showAxisTitle=L(False)),
    'categoryAxis': props(show=L(True), fontSize=D(8.5), labelColor=col(MUTED), fontFamily=L(NUM), showAxisTitle=L(False)),
    'lineStyles': [
        {'properties': {'showMarker': L(True)}},
        {'properties': {'strokeWidth': D(2), 'lineStyle': L('dotted'), 'areaShow': L(False), 'strokeTransparency': D(0), 'showMarker': L(False)},
         'selector': {'metadata': '_Measures.Contribution PY k'}},
        {'properties': {'strokeWidth': D(2.5), 'areaShow': L(False), 'strokeTransparency': D(0), 'showMarker': L(False)},
         'selector': {'metadata': '_Measures.Contribution AC k'}},
        {'properties': {'strokeWidth': D(4), 'areaShow': L(False), 'strokeTransparency': D(0), 'showMarker': L(True), 'markerShape': L('circle'), 'markerSize': D(8)},
         'selector': {'metadata': '_Measures.Month Contrib Max AC k'}},
        {'properties': {'strokeWidth': D(4), 'areaShow': L(False), 'strokeTransparency': D(0), 'showMarker': L(True), 'markerShape': L('circle'), 'markerSize': D(8)},
         'selector': {'metadata': '_Measures.Month Contrib Min AC k'}},
    ],
    'dataPoint': [
        {'properties': {'fill': col(SUBTLE)}, 'selector': {'metadata': '_Measures.Contribution PY k'}},
        {'properties': {'fill': col(SLATE)}, 'selector': {'metadata': '_Measures.Contribution AC k'}},
        {'properties': {'fill': col(SLATE)}, 'selector': {'metadata': '_Measures.Month Contrib Max AC k'}},
        {'properties': {'fill': col(CORAL)}, 'selector': {'metadata': '_Measures.Month Contrib Min AC k'}},
    ],
    'labels': [
        {'properties': {'show': L(True), 'fontFamily': L(NUM), 'fontSize': D(9.5), 'bold': L(True), 'labelDisplayUnits': D(1), 'enableBackground': L(False)}},
        {'properties': {'showSeries': L(False)}, 'selector': {'metadata': '_Measures.Contribution PY k'}},
        {'properties': {'showSeries': L(False)}, 'selector': {'metadata': '_Measures.Contribution AC k'}},
        {'properties': {'showSeries': L(True), 'color': col(SLATE), 'labelPosition': L('Above')},
         'selector': {'metadata': '_Measures.Month Contrib Max AC k'}},
        {'properties': {'showSeries': L(True), 'color': col(CORAL_TEXT), 'labelPosition': L('Above')},
         'selector': {'metadata': '_Measures.Month Contrib Min AC k'}},
    ],
}
p.add(f'{pid}_month', 'areaChart', mc_x + 12, mc_y + 78, mc_w - 24, mc_h - 88,
      q=query({'Category': ['DimDate.Season Month', 'DimDate.Date'],
               'Y': [('#Contribution PY k', 'PY'), ('#Contribution AC k', 'CY'),
                     ('#Month Contrib Max AC k', 'Max'), ('#Month Contrib Min AC k', 'Min')],
               'Tooltips': TIPS_C + [('#Net Sales per Day AC', 'Net sales / day CY')]},
              sort=[('DimDate.Season Month', 'Ascending')]),
      objects=month_objs, vco_=vco(header=True, pad=(6, 0, 6, 6), tooltip_page=TT_PAGE))

zc_chart(p, f'{pid}_zc_band', 'combo', C['band'],
         {'Category': ['FactSales.Discount Band', 'DimCampaign.Campaign Type'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'CY')],
          'Tooltips': TIPS_C + [('#Deep Share AC', 'Sales at 20%+ discount CY')]},
         'Title Discount Curve AC', 'DISCOUNT DEPTH', 'Slate column = CY · Jet Black tick = PY · click › campaigns',
         extra=refline_acpy(INK, SLATE_400, pad_lr=True, bar_w_pct=46, marker_w_pct=84),
         sort=[('FactSales.Discount Band', 'Ascending')])

zc_chart(p, f'{pid}_zc_type', 'combobar', C['type'],
         {'Category': ['DimCampaign.Campaign Type', 'DimCampaign.Campaign'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'CY')],
          'Tooltips': TIPS_C + [('#Net Sales per Day AC', 'Net sales / day CY'),
                                ('#Sales per Day vs Regular AC', 'Sales / day vs Regular CY'),
                                ('#Trading Days AC', 'Trading days CY')]},
         'Title Scorecard Var', 'CAMPAIGN SCORECARD', 'Slate bar = CY · Jet Black tick = PY · click › events · right-click › Profile',
         extra=refline_acpy(INK, SLATE_400, bar_w_pct=46, marker_w_pct=84, pad_tb=True),
         sort=[('#Contribution AC', 'Descending')])

drawers['ch1'] = drawer(p, pid, GUIDES['ch1'])

# ================================================================== 2 · Where it leaks (4 ZoomCharts visuals)
pid = PID['ch2']; p = Page(pid, '2 · Where it leaks', BG['ch2']); pages['ch2'] = p; C = CARDS['ch2']
sidebar(p, pid, 'ch2')
header(p, pid, 'CHAPTER 2 OF 3  ·  PRODUCTS, CHANNELS, MARKETS & RETURNS', 'Where it leaks', 'Msg Ch3', nxt=CHAPTERS[2])
for i, (lbl, k, ac_m, py_m, sty, bar_m) in enumerate([
    ('Online electronics margin', 'OE Margin', 'OE Margin AC', 'OE Margin PY', 'area', None),
    ('Net sales sold at a loss', 'Loss Share', 'Loss Share AC', 'Loss Share PY', 'area', None),
    ('Return rate · all units', 'Return', 'Return AC', 'Return PY', 'area', None),
    ('Return rate · apparel', 'Apparel Return', 'Apparel Return Rate AC', 'Apparel Return Rate PY', 'area', None),
    ('Average order value', 'AOV', 'AOV AC', 'AOV PY', 'area', None),
]):
    kpi_card_v12(p, f'{pid}_k{i}', KPIS[i], lbl, k, ac_m, py_m, style=sty, bar_col_m=bar_m)

zc_chart(p, f'{pid}_zc_cat', 'combobar', C['cat'],
         {'Category': ['DimProduct.Category', 'DimProduct.Subcategory', 'DimProduct.Product'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'CY')],
          'Tooltips': TIPS_C + [('#Return AC', 'Return rate CY')]},
         'Title Category AC', 'PRODUCTS', 'click › subcat › product',
         extra=refline_acpy(PY, SLATE), sort=[('#Contribution AC', 'Descending')])

zc_chart(p, f'{pid}_zc_donut', 'donut', C['donut'],
         {'Category': ['FactSales.Customer Segment', 'FactSales.Sales Channel'],
          'Values': [('#Net Sales AC', 'Net sales CY')],
          'Tooltips': [('#Margin AC', 'Margin CY'), ('#Contribution AC', 'Contribution CY'), ('#Net Sales ΔPY%', 'Net sales ΔPY%'), ('#AOV AC', 'AOV CY')]},
         'Title Segment AC', 'SEGMENTS › CHANNELS', 'click segment › channel split')

city_cat_colors = json.dumps({
    'source': 'DimLocation.City',
    'props': {
        'Amsterdam': {'color': SLATE},
        'Berlin': {'color': CORAL},
        'Lisbon': {'color': SLATE_400},
        'Madrid': {'color': SLATE_DARK},
        'Paris': {'color': INK},
        'Riga': {'color': SLATE_200},
        'Stockholm': {'color': MUTED},
        'Warsaw': {'color': SUBTLE},
    }
}, separators=(',', ':'))

zc_chart(p, f'{pid}_zc_scatter', 'scatter', C['scatter'],
         {'category': ['DimLocation.City'],
          'sourceNodes': [('#Discount AC', 'Weighted discount')],
          'targetNodes': [('#Margin AC', 'Contribution margin')],
          'Tooltips': [('#Net Sales AC', 'Net sales CY'), ('#Contribution AC', 'Contribution CY'), ('#Return AC', 'Return rate CY')]},
         'Title Map AC', 'MARKETS', 'x = discount %, y = margin %',
         extra={'colors1': props(propertyCache=L('{"source":"","props":{}}')),
                'shapes1': props(propertyCache=L('{"source":"","props":{}}')),
                'categoryColors1': props(propertyCache=L(city_cat_colors))})

heatmap(p, f'{pid}_hm', C['heat'], 'DimProduct.Category', 'DimCampaign.Campaign Type', 'Return AC',
        'Heat Return Col', 'Heat Return Font', 'Title Returns AC', 'RETURNS  ·  CATEGORY × CAMPAIGN',
        'Coral = 15%+ units returned · right-click › Profile', nrows=4, ncols=5, rh_w=138)

zc_chart(p, f'{pid}_zc_chan', 'combobar', C['chan'],
         {'Category': ['FactSales.Sales Channel', 'DimProduct.Category'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'CY')],
          'Tooltips': TIPS_C},
         'Title Channel AC', 'CHANNEL › CATEGORY', 'click Online › Electronics',
         extra=refline_acpy(PY, SLATE), sort=[('#Contribution AC', 'Descending')])

drawers['ch2'] = drawer(p, pid, GUIDES['ch2'])

# ================================================================== 3 · What to do
pid = PID['ch3']; p = Page(pid, '3 · What to do', BG['ch3']); pages['ch3'] = p; C = CARDS['ch3']
sidebar(p, pid, 'ch3')
header(p, pid, 'CHAPTER 3 OF 3  ·  FOUR RECOMMENDED MOVES', 'What to do', 'Msg Ch4', nxt=CHAPTERS[0])

cx_, cy_, cw_, ch_ = C['callout']
textbox(p, f'{pid}_up_t', cx_ + 20, cy_ + 16, cw_ - 40, 18, [[slabel('COMBINED INDICATIVE UPSIDE', 7.5, MUTED), run('   ·   per season', 7.5, SUBTLE)]])
textcard(p, f'{pid}_up_v', cx_ + 18, cy_ + 40, cw_ - 36, 54, 'Pot Total Text', size=26, color=SLATE, font=NUM, wrap=False, bold=True)
textbox(p, f'{pid}_up_n', cx_ + 20, cy_ + 102, cw_ - 40, 48, [[run('Projected from CY volumes & margins assuming volumes hold; order of magnitude, not a forecast.', 8.5, BODY)]])

ux, uy, uw, uh = C['upside_bar']
card_head(p, f'{pid}_up', C['upside_bar'], None, 'UPSIDE BY MOVE', 'kEUR · CY simulation')
table(p, f'{pid}_up', (ux, uy, uw, uh), 'Moves.Label', 190,
      [{'kind': 'var', 'hdr': '', 'w': 308, 'm': 'Pot by Move k', 'label': 'Upside', 'fill': SLATE, 'end': 'Axis Moves End'}],
      [('#Pot by Move k', 'Descending')], rows=4, anchor='Anchor Moves', tt=False, y_off=44, hdr_y_off=34)

lx_, ly_, lw_, lh_ = C['limits']
card_head(p, f'{pid}_lim', C['limits'], None, 'ANALYTICAL GUARDRAILS', 'what this dataset cannot tell you')
LIM_SHORT = [
    ('Not causal.', ' Synthetic data with no control group: nothing proves a campaign caused uplift or ROI.'),
    ('Before overhead.', ' Contribution excludes corporate overhead, interest and tax.'),
    ('Unequal lengths.', ' Campaigns run 3 to 17 days; compare margins and sales/day, not raw totals.'),
    ('Allocated spend.', ' Campaign budgets are spread across sales lines by gross-sales share.'),
]
for i, (t_, d_) in enumerate(LIM_SHORT):
    iy = ly_ + 48 + i * 62
    textbox(p, f'{pid}_lim_b{i}', lx_ + 48, iy, lw_ - 66, 48, [[run(t_, 9, INK, FONT_SB, True), run(d_, 9, BODY)]])

MOVES = [
    ('ACT-01', 'Keep every event discount below 20%', 'Evidence Discount', 'Pot Discount Text', 'ch1',
     'Cap Black Friday and New Year offers at 19% in 2 test markets; compare against 6 control markets.'),
    ('ACT-02', 'Sell online electronics on value, not price', 'Evidence OE', 'Pot OE Text', 'ch2',
     'Bundle laptops with accessories online; restrict price cuts to aged clearance SKUs only.'),
    ('ACT-03', 'Bring apparel returns down to store average', 'Evidence Returns', 'Pot Returns Text', 'ch2',
     'Add fit notes and sizing guides to the 10 most-returned apparel items before peak traffic.'),
    ('ACT-04', 'Run New Year as clearance, not a second Christmas', 'Evidence NY', 'Pot NY Text', 'ch1',
     'Limit New Year promotions to aged inventory and exclude high-return apparel lines.'),
]
for i, (code, title, ev, pot, src, test) in enumerate(MOVES):
    x, y, w, h = ACTION_ROWS[i]
    nm = f'{pid}_m{i}'
    textbox(p, f'{nm}_code', x + 20, y + 18, 68, 24, [[run(code, 8.5, BODY, NUM, True)]], align='center')
    textbox(p, f'{nm}_title', x + 102, y + 16, 610, 28, [[run(title, 12, INK, FONT_SB, True)]])
    textcard(p, f'{nm}_ev', x + 102, y + 50, 610, 96, ev, size=9, color=BODY, font=FONT, wrap=True)
    tbutton(p, f'{nm}_link', x + 92, y + h - 44, 300, 36, f'See evidence in Chapter {src[-1]}  →',
            lpage(PID[src]), SLATE, INK, size=9, tip=f'Open Chapter {src[-1]}', align='left')
    textbox(p, f'{nm}_plbl', x + 758, y + 20, 280, 18, [[slabel('INDICATIVE UPSIDE', 7, MUTED)]])
    textcard(p, f'{nm}_pot', x + 756, y + 40, 280, 38, pot, size=19, color=SLATE, font=NUM, wrap=False, bold=True)
    textbox(p, f'{nm}_tlbl', x + 758, y + 88, 280, 18, [[slabel('PILOT TEST', 7, MUTED)]])
    textbox(p, f'{nm}_test', x + 758, y + 108, 280, 78, [[run(test, 9, BODY)]])

drawers['ch3'] = drawer(p, pid, GUIDES['ch3'])

# ================================================================== Campaign profile (drill-through, 2 ZoomCharts)
pid = PID['profile']
p = Page(pid, 'Campaign profile', BG['profile'], drill=[('DimCampaign', 'Campaign Type'), ('DimCampaign', 'Campaign')]); pages['profile'] = p; C = CARDS['profile']
sidebar(p, pid, 'ch1')
header(p, pid, 'DRILL-THROUGH  ·  CAMPAIGN PROFILE', 'Campaign profile', 'Title Drill AC', back=True)

fx_, fy_, fw_, fh_ = C['facts']
textbox(p, f'{pid}_facts_hdr', fx_ + 18, fy_ + 12, fw_ - 36, 18, [[slabel('EVENT FACTS', 7.5, MUTED), run('   ·   for the campaign or type you drilled into', 7.5, SUBTLE)]])
textcard(p, f'{pid}_facts_txt', fx_ + 18, fy_ + 34, fw_ - 36, 62, 'Drill Campaign Facts', size=9.5, color=BODY, font=FONT, wrap=True)

card_head(p, f'{pid}_pl', C['pnl'], 'Title Bridge AC', 'PROFIT AND LOSS', 'kEUR · costs in brackets')
table(p, f'{pid}_pnl', C['pnl'], 'PnL Lines.Label', 134,
      [{'kind': 'single', 'hdr': 'PY', 'w': 158, 'm': 'PL PY k', 'label': 'PY', 'colour': PY_BAR, 'start': 'Axis PL Start', 'end': 'Axis PL End'},
       {'kind': 'single', 'hdr': 'CY', 'w': 158, 'm': 'PL AC k', 'label': 'CY', 'colour': SLATE, 'start': 'Axis PL Start', 'end': 'Axis PL End'},
       {'kind': 'var', 'hdr': 'ΔPY', 'w': 134, 'm': 'PL ΔPY k', 'label': 'ΔPY', 'fill_m': 'Colour PL Δ', 'start': 'Axis PL Δ Start', 'end': 'Axis PL Δ End'},
       {'kind': 'pin', 'hdr': 'ΔPY %', 'w': 126, 'm': 'PL ΔPY%', 'label': 'ΔPY %', 'fill_m': 'Colour PL Δ', 'start': 'Axis PL Δ% Start', 'end': 'Axis PL Δ% End'}],
      [('PnL Lines.Label', 'Ascending')], rows=10, anchor='Anchor PL', tt=False, y_off=88, hdr_y_off=64)

zc_chart(p, f'{pid}_zc_daily', 'combo', C['daily'],
         {'Category': ['DimDate.Date'], 'Values1': [('#Net Sales PY', 'PY')], 'Values2': [('#Net Sales AC', 'CY')],
          'Tooltips': [('#Contribution AC', 'Contribution CY'), ('#Margin AC', 'Margin CY')]},
         'Title Peak Day', 'NET SALES PER TRADING DAY', 'Slate column = CY · Jet Black tick = PY',
         extra=refline_acpy(INK, SLATE_400, bar_w_pct=75, marker_w_pct=100))

zc_chart(p, f'{pid}_zc_band', 'combo', C['band'],
         {'Category': ['FactSales.Discount Band'], 'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'CY')],
          'Tooltips': TIPS_C},
         'Title Discount Curve AC', 'DISCOUNT DEPTH', 'Slate column = CY · Jet Black tick = PY',
         extra=refline_acpy(INK, SLATE_400, pad_lr=True, bar_w_pct=46, marker_w_pct=84),
         sort=[('FactSales.Discount Band', 'Ascending')])

drawers['profile'] = drawer(p, pid, GUIDES['profile'])

# ================================================================== Tooltip page
p = Page(TT_PAGE, 'Snapshot tooltip', 'bg_tooltip_c43.png', tooltip=True, w=TT['w'], h=TT['h']); pages['tooltip'] = p
textcard(p, 'tt_header', 20, 10, 328, 24, 'TT Header', size=11.5, color=INK, font=FONT_SB, wrap=False, bold=True)
textcard(p, 'tt_sel', 20, 36, 328, 18, 'Period Short', size=7, color=MUTED, font=NUM, wrap=False)
for i, (lbl, k, x, y) in enumerate([
    ('NET SALES · CY', 'Net Sales', 20, 70),
    ('CONTRIBUTION · CY', 'Contribution', 198, 70),
    ('MARGIN · CY', 'Margin', 20, 156),
    ('WEIGHTED DISCOUNT · CY', 'Discount', 198, 156),
]):
    textbox(p, f'tt_l{i}', x, y, 154, 16, [[slabel(lbl, 6.5, MUTED)]])
    textcard(p, f'tt_v{i}', x, y + 16, 154, 28, f'KPI {k} AC', size=15, color=INK, font=NUM, wrap=False, bold=True)
    textcard(p, f'tt_d{i}', x, y + 46, 160, 18, f'KPI {k} Tag', size=7.5, font=NUM, wrap=False, color_measure=f'KPI {k} Col', bold=True)
for v in p.visuals:
    v['visual']['visualContainerObjects']['visualTooltip'] = props(show=L(False))

# ================================================================== Write pages + bookmarks
for pg in pages.values():
    pg.write(ROOT)
order = [PID[k] for k in ['ch1', 'ch2', 'ch3', 'profile']] + [TT_PAGE]
json.dump({'$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json',
           'pageOrder': order, 'activePageName': PID['ch1']}, open(os.path.join(ROOT, 'definition', 'pages', 'pages.json'), 'w', encoding='utf-8'), indent=2)


def vtype(pg, n):
    for v in pg.visuals:
        if v['name'] == n:
            return v['visual']['visualType']
    raise KeyError(n)


def bm(bid, disp, key, show, hide):
    pg = pages[key]; px = PID[key]; vc = {}
    for n in show:
        vc[n] = {'singleVisual': {'visualType': vtype(pg, n), 'objects': {}}}
    for n in hide:
        vc[n] = {'singleVisual': {'visualType': vtype(pg, n), 'objects': {}, 'display': {'mode': 'hidden'}}}
    return {'$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/1.4.0/schema.json',
            'displayName': disp, 'name': bid,
            'options': {'targetVisualNames': show + hide, 'applyOnlyToTargetVisuals': True, 'suppressData': True},
            'explorationState': {'version': '1.3', 'activeSection': px, 'sections': {px: {'visualContainers': vc}}}}


bms = []
for k, g in drawers.items():
    px = PID[k]
    kinds = [x_ for x_ in ['filters', 'guide', 'limits'] if g[x_]]
    allv = g['common'] + sum((g[x_] for x_ in kinds), [])
    for kind in kinds:
        show = g['common'] + g[kind]
        bms.append(bm(f'bm_{px}_{kind}', f'{k} · {kind}', k, show, [n for n in allv if n not in show]))
    bms.append(bm(f'bm_{px}_close', f'{k} · close panel', k, [], allv))


def reset_bm(key):
    pg = pages[key]; px = PID[key]; vc = {}
    for v in pg.visuals:
        vis = v['visual']; sv = {'visualType': vis['visualType'], 'objects': {}}
        if v.get('isHidden'):
            sv['display'] = {'mode': 'hidden'}
        e = {'singleVisual': sv}
        if vis['visualType'] == 'advancedSlicerVisual':
            fld = vis['query']['queryState']['Values']['projections'][0]['field']
            flt = {'name': f"r{abs(hash(v['name'])) % 10**12}", 'type': 'Categorical', 'expression': fld, 'howCreated': 0}
            byexpr = [flt]
            for f in v.get('filterConfig', {}).get('filters', []):
                byexpr = [{'name': f['name'], 'type': 'Categorical', 'filter': f['filter'], 'expression': f['field'], 'howCreated': 1}]
            e['filters'] = {'byExpr': byexpr}
        vc[v['name']] = e
    return {'$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json',
            'displayName': f'{key} · reset all filters', 'name': f'bm_{px}_reset',
            'options': {'targetVisualNames': []},
            'explorationState': {'version': '1.3', 'activeSection': px, 'sections': {px: {'visualContainers': vc}}}}


for k in drawers:
    bms.append(reset_bm(k))
bd = os.path.join(ROOT, 'definition', 'bookmarks'); os.makedirs(bd, exist_ok=True)
for b_ in bms:
    json.dump(b_, open(os.path.join(bd, b_['name'] + '.bookmark.json'), 'w', encoding='utf-8'), indent=2)
json.dump({'$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmarksMetadata/1.0.0/schema.json',
           'items': [{'name': b_['name']} for b_ in bms]}, open(os.path.join(bd, 'bookmarks.json'), 'w', encoding='utf-8'), indent=2)
vis = {k: sum(1 for v in pg.visuals if not v.get('isHidden')) for k, pg in pages.items()}
print('V12 Modern UX built | visible visuals per page:', vis, '| bookmarks:', len(bms))
