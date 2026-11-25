"""Challenge 43 - Holiday P&L, V11 Slate-Coral Editorial Boardroom Analytics Edition.
3 main pages + 1 hidden drill-through + 1 hidden tooltip; >= 2 ZoomCharts on every data page (9 total);
10 editorial KPI rows with monthly area/bar+PY-tick spark charts; zero-shadow #FFFFFF canvas;
Blue Slate (#4F5D75) vs Coral Glow (#EF8354) / Accessible Text Coral (#BA4B1D) semantic encoding."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pb import *
from layout11 import *

ROOT = sys.argv[1]
TT_PAGE = 'tt_snapshot'
PID = {'ch1': 'p1_what_why', 'ch2': 'p2_leaks', 'ch3': 'p3_actions', 'profile': 'p4_campaign_profile'}
BG = {k: f'bg_{k}_c43.png' for k in PID}
CHAPTERS = [
    ('ch1', '1 · What happened & why'),
    ('ch2', '2 · Where it leaks'),
    ('ch3', '3 · What to do'),
]
SEASONS = ['2023/24', '2024/25', '2025/26']
FOOT = ('Source: FP20 Analytics Challenge 43 (synthetic data)  ·  AC = selected season  ·  PY = same dates one season earlier  ·  '
        'Blue Slate = favorable/AC, Coral = adverse/leak  ·  contribution excludes overhead, interest & tax  ·  Abhilash Sahani · 2026')


def slabel(txt, size=7.5, color=MUTED):
    return run(txt.upper(), size, color, FONT_SB, True)


# ---------------------------------------------------------------- Topbar + Left Executive Rail + Footer
def topbar(p, pid, active):
    textbox(p, f'{pid}_brand', LX + 42, 27, 360, 40, [
        [run('HOLIDAY P&L', 10, INK, 'Segoe UI Semibold', True)],
        [run('The Holiday Audit  ·  Challenge 43', 7.5, MUTED)],
    ])
    for k, t in CHAPTERS:
        on = active == k
        tx, tw = TABS[k]
        tbutton(p, f'{pid}_nav_{k}', tx, 22, tw, 50, t, lpage(PID[k]),
                INK if on else MUTED, INK, size=9.5, font=(FONT_SB if on else FONT),
                tip=f'Open {t}', align='center')

    gx, gw = UTIL['guide']
    lx, lw = UTIL['limits']
    rx_, rw = UTIL['reset']
    fx, fw = UTIL['filters']
    tbutton(p, f'{pid}_btn_guide', gx, 31, gw, 32, '?  Guide', lbm(f'bm_{pid}_guide'), MUTED, INK, size=8.5,
            tip='How to read this page', align='center')
    tbutton(p, f'{pid}_btn_limits', lx, 31, lw, 32, 'i  Notes', lbm(f'bm_{pid}_limits'), MUTED, INK, size=8.5,
            tip='Data notes and limits', align='center')
    tbutton(p, f'{pid}_btn_reset', rx_, 31, rw, 32, '↺  Reset', lbm(f'bm_{pid}_reset'), BODY, INK, size=8.5,
            tip='Reset all filters: AC returns to latest season', align='center')
    tbutton(p, f'{pid}_btn_filters', fx, 30, fw, 34, '☰  Filters', lbm(f'bm_{pid}_filters'), WHITE, SLATE_100, size=9,
            tip='Segment, market, category, campaign type, discount band', align='center')


def left_header(p, pid, kicker, msg_m, nxt=None, back=False, lw=LW):
    textbox(p, f'{pid}_kicker', LX, 94, 340, 18, [[slabel(kicker, 7.5, MUTED)]])
    if back:
        tbutton(p, f'{pid}_btn_back', LX + PROF_LW - 96, 94, 96, 32, '‹  Back', lback(), BODY, INK, size=9,
                tip='Back to the page you came from', align='center')
        textcard(p, f'{pid}_period', LX, 114, 420, 18, 'Period Short', size=7.5, color=MUTED, font=NUM, wrap=False)
        textcard(p, f'{pid}_msg', LX, 134, PROF_LW, 56, msg_m, size=13.5, color=INK, font=FONT_SB, wrap=True)
    else:
        textcard(p, f'{pid}_period', LX + 340, 94, lw - 340, 18, 'Period Short', size=7.5, color=MUTED, font=NUM, wrap=False, align='right')
        textcard(p, f'{pid}_msg', LX, 118, lw, 86, msg_m, size=14.5, color=INK, font=FONT_SB, wrap=True)
        textbox(p, f'{pid}_lbl_season', LX, 220, 48, 20, [[slabel('Season', 7.5, MUTED)]])
        sx, sy, sw, sh = SEG_SEASON
        segmented_chips(p, f'{pid}_chip_season', sx + 1, sy + 1, sw - 2, sh - 2, 'DimDate.Season', 'sync_season', 3, rows=1, size=8, filt=SEASONS)
        textbox(p, f'{pid}_lbl_channel', LX + 362, 220, 56, 20, [[slabel('Channel', 7.5, MUTED)]])
        cx, cy, cw, ch = SEG_CHANNEL
        segmented_chips(p, f'{pid}_chip_channel', cx + 1, cy + 1, cw - 2, ch - 2, 'FactSales.Sales Channel', 'sync_channel', 2, rows=1, size=8)
        textcard(p, f'{pid}_filt', LX, 253, lw, 18, 'Filters Line', size=7.5, color=SUBTLE, wrap=False)

    textbox(p, f'{pid}_foot', LX, FOOT_Y, 1440, 20, [[run(FOOT, 7, MUTED)]])
    if nxt:
        k, t = nxt
        lbl = 'Back to start  ·  1 · What happened & why  ↺' if k == 'ch1' else f'Next  ·  {t}  →'
        tbutton(p, f'{pid}_next', 1520, FOOT_Y - 3, 356, 26, lbl, lpage(PID[k]), SLATE, INK, size=9,
                tip=f'Go to {t}', align='right')


def head(p, name, blk, take_m, kicker, note=None):
    x, y, w, _ = blk
    parts = [slabel(kicker, 7.5, MUTED)]
    if note:
        parts.append(run('   ·   ' + note, 7.5, SUBTLE))
    textbox(p, f'{name}_t', x, y, w, 18, [parts])
    textcard(p, f'{name}_m', x, y + 20, w, 26, take_m, size=11, color=INK, font=FONT_SB, wrap=False)


# ---------------------------------------------------------------- V11 Editorial KPI Row (Jet Black mono + Oct-Jan micro-chart)
def kpi_row_v11(p, name, box, label, k, ac_m, py_m, style='bars', bar_col_m=None):
    x, y, w, h = box
    textbox(p, f'{name}_lbl', x, y + 10, 286, 18, [[run(label, 8.5, MUTED, FONT_SB)]])
    textcard(p, f'{name}_val', x - 1, y + 30, 288, 38, f'KPI {k} AC', size=20.5, color=INK, font=NUM, wrap=False, bold=True)
    textcard(p, f'{name}_d', x, y + 72, 288, 18, f'KPI {k} Tag', size=8.5, font=NUM, wrap=False, color_measure=f'KPI {k} Col', bold=True)
    textcard(p, f'{name}_py', x, y + 94, 288, 18, f'KPI {k} PY', size=7.5, color=SUBTLE, font=NUM, wrap=False)

    cx, cy, cw, ch = x + 298, y + 14, w - 302, h - 22
    if style == 'area':
        o = {
            'legend': props(show=L(False)),
            'valueAxis': props(show=L(False), gridlineShow=L(False), showAxisTitle=L(False)),
            'categoryAxis': props(show=L(True), fontSize=D(7.5), labelColor=col(SUBTLE), fontFamily=L(NUM), showAxisTitle=L(False)),
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
        q = query({'Category': ['DimDate.Season Month'], 'Y': [(f'#{py_m}', 'PY'), (f'#{ac_m}', 'AC')]}, [('DimDate.Season Month', 'Ascending')])
        p.add(f'{name}_spark', 'areaChart', cx, cy, cw, ch, q=q, objects=o, vco_=vco(header=False, pad=(0, 0, 0, 0), tooltip=True))
    else:
        o = {
            'layout': props(clusteredGapOverlaps=L(True), clusteredGapSize=D(100)),
            'legend': props(show=L(False)),
            'valueAxis': props(show=L(False), gridlineShow=L(False), showAxisTitle=L(False)),
            'categoryAxis': props(show=L(True), fontSize=D(7.5), labelColor=col(SUBTLE), fontFamily=L(NUM), showAxisTitle=L(False), innerPadding=D(38)),
            'labels': props(show=L(False)),
            'dataPoint': [measure_fill(bar_col_m)],
            'error': error_target_tick(ac_m, py_m, color=INK),
        }
        q = query({'Category': ['DimDate.Season Month'], 'Y': [(f'#{ac_m}', 'AC')], 'Tooltips': [(f'#{py_m}', 'PY')]}, [('DimDate.Season Month', 'Ascending')])
        p.add(f'{name}_spark', 'clusteredColumnChart', cx, cy, cw, ch, q=q, objects=o, vco_=vco(header=False, pad=(0, 0, 0, 0), tooltip=True))


# ---------------------------------------------------------------- Native Bar Table + Heatmap + ZoomCharts Helpers
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


def table(p, name, blk, cat, label_w, cols, sort, rows, anchor, tt=True, y_off=66, hdr_y_off=44):
    """Editorial bar table on pure white #FFFFFF canvas."""
    x, y, w, h = blk
    cy, ch = y + y_off, h - y_off - 4
    rowh = ch / rows
    pad_bar = pad_pin = max(30, min(88, round(100 * (1 - 18 / rowh))))
    sort_tips = [(s_[0], 'sort') for s_ in sort if s_[0].startswith('#')]
    base_tips = [(f'#{anchor}', 'row')] + [t for t in sort_tips if t[0] != f'#{anchor}']

    def tips_for(ms):
        used = {m if isinstance(m, str) else m[0] for m in ms}
        return [t for t in base_tips if t[0] not in used]

    cx = x
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

        if k == 'pair':
            o = axis_fix(bar_obj(True, pad_bar, c.get('start'), c.get('end'), fill=PY_BAR, units=c.get('units'), prec=c.get('prec')), first)
            o['labels'][0]['properties']['color'] = col(WHITE)
            o['categoryAxis'][0]['properties']['labelColor'] = col(WHITE)
            ms = [(f"#{c['py']}", 'PY')]
            bar(p, f'{name}_{i}py', cx, cy - 5, cw, ch, cat, ms, o, sort, tt, tips=tips_for(ms))
            o = axis_fix(bar_obj(True, pad_bar, c.get('start'), c.get('end'), fill=AC, units=c.get('units'), prec=c.get('prec')), first)
            ms = [(f"#{c['ac']}", 'AC')]
            bar(p, f'{name}_{i}ac', cx, cy, cw, ch, cat, ms, o, sort, tt, tips=[(f"#{c['py']}", 'PY')] + tips_for(ms))
        elif k == 'stack':
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
            ms = [(f'#{mm}', mm.replace(' k', '').replace('Bridge ', '')) for mm, _, _ in c['series']]
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


def heatmap(p, name, blk, rows, colsf, val, col_m, font_m, take_m, kicker, note, nrows=4, ncols=5, rh_w=130):
    head(p, name, blk, take_m, kicker, note)
    x, y, w, h = blk
    vw, vh = w, h - 72
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
    p.add(f'{name}_mx', 'pivotTable', x, y + 66, vw, vh,
          q=query({'Rows': [rows], 'Columns': [colsf], 'Values': [(f'#{val}', 'AC')]}), objects=o,
          vco_=vco(header=True, pad=(0, 0, 0, 0), tooltip_page=TT_PAGE))


def zc_chart(p, name, kind, blk, roles, take_m, kicker, note, extra=None, sort=None, y_off=50):
    head(p, name, blk, take_m, kicker, note)
    x, y, w, h = blk
    vt, _ = ZC[kind]
    o = {'advanced': [{'properties': {'shouldApplyNewDefaults': L(True)}}], 'toolbar': props(show=L(False)), 'legend': props(show=L(False))}
    if extra:
        o.update(extra)
    return p.add(name, vt, x, y + y_off, w, h - y_off - 4, q=query(roles, sort), objects=o, vco_=vco(header=True, pad=(0, 0, 0, 0)))


def refline_acpy(c_py=PY, c_ac=SLATE, pad_lr=False):
    """PY rendered as subtle reference line + AC in Blue Slate #4F5D75 with clean value labels."""
    o = series_colors({1: c_py, 2: c_ac})
    o['seriesDefault'][0]['properties'].update({
        'seriesSettingSelector': L('s1'),
        'type1': L('referenceLine'),
        'customize1': L(True),
        'lineWidth1': L(3),
        'lineColor1': col(c_py),
        'zIndex1': L(25),
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
    if pad_lr:
        o['columnBarSettings'] = props(leftPadding=L(15), rightPadding=L(15))
    return o


# ---------------------------------------------------------------- Side Drawer (Filters / Guide / Notes)
DR = DRAWER['panel']
DX, DW = DR['x'] + 24, DR['w'] - 48
NOTATION = ('How to read Slate-Coral IBCS',
            'Blue Slate (#4F5D75) = AC & favorable gains. Silver-Grey (#8B909E / #B5BECC) = PY (one season earlier). '
            'Coral Glow (#EF8354) = adverse bars, margin erosion & 15%+ return leaks; Burnt Coral (#BA4B1D) = small adverse text. '
            'In KPI rows, Oct–Jan columns show AC colored vs PY with horizontal target ticks.')
LIMITS = [
    ('Synthetic data.', ' Three October–January holiday windows (2023/24, 2024/25, 2025/26) across eight European city markets. 2023/24 has no PY.'),
    ('Descriptive, not causal.', ' There is no control group, randomisation or ad-exposure data, so nothing here proves a campaign caused extra sales, uplift or ROI.'),
    ('Contribution profit', ' = net sales − product cost − fulfilment − payment fees − return handling − allocated campaign spend. It excludes overhead, interest and tax.'),
    ('Unequal durations.', ' Black Friday and Cyber Monday run 3 days; Christmas 17 and New Year 15. Compare margins or per-day sales, not totals.'),
    ('Campaign spend', ' is each event budget allocated to sales lines by gross-sales share.'),
    ('Weighted discount %', ' = discount € ÷ gross sales €. Returns carry no return date; refunds count against the original sale.'),
]
GUIDES = {
    'ch1': [('Executive KPI stack.', 'Left rail pairs the thesis headline with five KPIs and Oct–Jan trends (area/line on top, variance bars with PY target ticks below).'),
            ('Profit bridge.', 'Reads top-down from PY contribution to AC: Blue Slate bars added margin, Coral Glow bars eroded it.'),
            ('Month, discount & campaign drills.', 'Right ZoomCharts visuals compare AC bars against the Silver PY reference line; click any bar/month to drill down or right-click a campaign › Drill through › Campaign profile.')],
    'ch2': [('Product hierarchy.', 'Top-left ZoomCharts Combo Bar drills Category › Subcategory › Product (PY ref line vs AC Blue Slate bars).'),
            ('Segments & cities.', 'Top-mid ZoomCharts Donut drills Customer Segment › Channel; top-right ZoomCharts Scatter plots city discount % vs contribution margin %.'),
            ('Returns & channels.', 'Bottom-left heatmap flags 15%+ return cells in Coral; bottom-right Combo Bar drills Sales Channel › Category.')],
    'ch3': [('Projected callout & bar summary.', 'Top-left dashed Slate-50 box shows combined indicative seasonal upside; below it, upside ranked by move and data limits.'),
            ('Action rails (ACT-01 to ACT-04).', 'Each move pairs live evidence, a deep-link back to Chapter 1 or 2, indicative €k upside, and the pilot test to run first.')],
    'profile': [('Drill-through profile.', 'Filtered to the campaign or campaign type you right-clicked from Chapter 1 or Chapter 2.'),
                ('P&L & daily/discount drills.', 'Left P&L bar table breaks down PY, AC, ΔPY and ΔPY%; right ZoomCharts visuals track daily net sales and discount bands.')],
}


def drawer(p, pid, guide_lines):
    g = {'common': [], 'filters': [], 'guide': [], 'limits': []}
    g['common'].append(resimg(p, f'{pid}_dw_img', 0, 0, W, H, 'overlay_drawer_c43.png', hidden=True)['name'])
    c = DRAWER['close']
    g['common'].append(tbutton(p, f'{pid}_dw_close', c['x'], c['y'], c['w'], c['h'], 'Close  ✕', lbm(f'bm_{pid}_close'), BODY, INK, size=8.5, hidden=True, tip='Close panel')['name'])

    def hdr(kind, title, sub):
        g[kind].append(textbox(p, f'{pid}_dw_{kind}_hdr', DX, DR['y'] + 14, 340, 50,
                               [[run(title, 13, INK, FONT_SB, True)], [run(sub, 8, MUTED)]], hidden=True)['name'])

    hdr('filters', 'More filters', 'Apply across all chapters  ·  Season & Channel are on-page')
    y = 148
    for key, label, field, cols, rows in [('seg', 'CUSTOMER SEGMENT', 'FactSales.Customer Segment', 2, 2),
                                          ('city', 'MARKET', 'DimLocation.City', 4, 2),
                                          ('cat', 'PRODUCT CATEGORY', 'DimProduct.Category', 2, 2),
                                          ('ctype', 'CAMPAIGN TYPE', 'DimCampaign.Campaign Type', 3, 2),
                                          ('band', 'DISCOUNT BAND', 'FactSales.Discount Band', 3, 2)]:
        g['filters'].append(textbox(p, f'{pid}_dw_l_{key}', DX, y, DW, 18, [[slabel(label)]], hidden=True)['name'])
        g['filters'].append(drawer_chips(p, f'{pid}_dw_s_{key}', DX - 4, y + 20, DW + 8, 38 * rows, field, f'sync_{key}', cols, rows=rows, size=8.5, hidden=True)['name'])
        y += 24 + 38 * rows + 18

    hdr('guide', 'How to read this page', 'Blue Slate = AC/favorable  ·  Silver = PY  ·  Coral = adverse')
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
TIPS_C = ['#Margin AC', '#Net Sales AC', '#Contribution ΔPY']

# ================================================================== 1 · What happened & why (3 ZoomCharts visuals)
pid = PID['ch1']; p = Page(pid, '1 · What happened & why', BG['ch1']); pages['ch1'] = p; B = BLK['ch1']
topbar(p, pid, 'ch1')
left_header(p, pid, 'CHAPTER 1 OF 3  ·  2023/24 TO 2025/26', 'Msg Ch1', nxt=CHAPTERS[1])
for i, (lbl, k, ac_m, py_m, sty, bar_m) in enumerate([
    ('Contribution profit, AC', 'Contribution', 'Contribution AC k', 'Contribution PY k', 'area', None),
    ('Contribution margin, AC', 'Margin', 'Margin AC', 'Margin PY', 'bars', 'KPI Bar Margin'),
    ('Net sales, AC', 'Net Sales', 'Net Sales AC k', 'Net Sales PY k', 'bars', 'KPI Bar Net Sales'),
    ('Weighted discount, AC', 'Discount', 'Discount AC', 'Discount PY', 'bars', 'KPI Bar Discount'),
    ('Sales at 20%+ discount', 'Deep', 'Deep Share AC', 'Deep Share PY', 'bars', 'KPI Bar Deep'),
]):
    kpi_row_v11(p, f'{pid}_k{i}', KPI_ROWS[i], lbl, k, ac_m, py_m, style=sty, bar_col_m=bar_m)

head(p, f'{pid}_br', B['bridge'], 'Title Bridge Var', 'PROFIT BRIDGE', 'kEUR · PY to AC')
textbox(p, f'{pid}_br_leg', B['bridge'][0], B['bridge'][1] + 46, 580, 18, [[
    run('●  ', 8, CORAL), run('Took margin   ', 7.5, MUTED),
    run('●  ', 8, SLATE), run('Added / AC   ', 7.5, MUTED),
    run('●  ', 8, PY_BAR), run('PY', 7.5, MUTED),
]])
table(p, f'{pid}_br', B['bridge'], 'Bridge Lines.Label', 132,
      [{'kind': 'stack', 'hdr': '', 'w': 438, 'end': 'Axis Bridge End 2',
        'series': [('Bridge Base k', WHITE, None), ('Bridge PY k', PY_BAR, None), ('Bridge AC k', SLATE, None),
                   ('Bridge Up k', SLATE_400, None), ('Bridge Down k', CORAL, None),
                   ('Bridge Tail k', WHITE, {'pos': 'InsideBase', 'value': 'Bridge Label k', 'color': INK})]}],
      [('Bridge Lines.Label', 'Ascending')], rows=10, anchor='Anchor Bridge', tt=False, y_off=72)

zc_chart(p, f'{pid}_zc_month', 'combo', B['month'],
         {'Category': ['DimDate.Season Month', 'DimDate.Date'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'AC')],
          'Tooltips': TIPS_C + ['#Net Sales per Day AC']},
         'Title Month AC', 'CONTRIBUTION BY MONTH', 'PY line vs AC bars · click month › day',
         extra=refline_acpy(PY, SLATE, pad_lr=True))

zc_chart(p, f'{pid}_zc_band', 'combo', B['band'],
         {'Category': ['FactSales.Discount Band', 'DimCampaign.Campaign Type'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'AC')],
          'Tooltips': TIPS_C + ['#Deep Share AC']},
         'Title Discount Curve AC', 'DISCOUNT DEPTH', 'PY line vs AC bars · click band › campaigns',
         extra=refline_acpy(PY, SLATE, pad_lr=True), sort=[('FactSales.Discount Band', 'Ascending')])

zc_chart(p, f'{pid}_zc_type', 'combobar', B['type'],
         {'Category': ['DimCampaign.Campaign Type', 'DimCampaign.Campaign'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'AC')],
          'Tooltips': TIPS_C + ['#Net Sales per Day AC', '#Sales per Day vs Regular AC', '#Trading Days AC']},
         'Title Scorecard Var', 'CAMPAIGN SCORECARD', 'PY line vs AC bars · click › events · right-click › Profile',
         extra=refline_acpy(PY, SLATE), sort=[('#Contribution AC', 'Descending')])

drawers['ch1'] = drawer(p, pid, GUIDES['ch1'])

# ================================================================== 2 · Where it leaks (4 ZoomCharts visuals)
pid = PID['ch2']; p = Page(pid, '2 · Where it leaks', BG['ch2']); pages['ch2'] = p; B = BLK['ch2']
topbar(p, pid, 'ch2')
left_header(p, pid, 'CHAPTER 2 OF 3  ·  PRODUCTS, CHANNELS & RETURNS', 'Msg Ch3', nxt=CHAPTERS[2])
for i, (lbl, k, ac_m, py_m, sty, bar_m) in enumerate([
    ('Online electronics margin', 'OE Margin', 'OE Margin AC', 'OE Margin PY', 'area', None),
    ('Net sales sold at a loss', 'Loss Share', 'Loss Share AC', 'Loss Share PY', 'bars', 'KPI Bar Loss Share'),
    ('Return rate · all units', 'Return', 'Return AC', 'Return PY', 'bars', 'KPI Bar Return'),
    ('Return rate · apparel', 'Apparel Return', 'Apparel Return Rate AC', 'Apparel Return Rate PY', 'bars', 'KPI Bar Apparel Return'),
    ('Average order value', 'AOV', 'AOV AC', 'AOV PY', 'bars', 'KPI Bar AOV'),
]):
    kpi_row_v11(p, f'{pid}_k{i}', KPI_ROWS[i], lbl, k, ac_m, py_m, style=sty, bar_col_m=bar_m)

zc_chart(p, f'{pid}_zc_cat', 'combobar', B['cat'],
         {'Category': ['DimProduct.Category', 'DimProduct.Subcategory', 'DimProduct.Product'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'AC')],
          'Tooltips': TIPS_C + ['#Return AC']},
         'Title Category AC', 'PRODUCTS', 'click › subcat › product',
         extra=refline_acpy(PY, SLATE), sort=[('#Contribution AC', 'Descending')])

zc_chart(p, f'{pid}_zc_donut', 'donut', B['donut'],
         {'Category': ['FactSales.Customer Segment', 'FactSales.Sales Channel'],
          'Values': [('#Net Sales AC', 'Net sales AC')],
          'Tooltips': ['#Margin AC', '#Contribution AC', '#Net Sales ΔPY%', '#AOV AC']},
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

zc_chart(p, f'{pid}_zc_scatter', 'scatter', B['scatter'],
         {'category': ['DimLocation.City'],
          'sourceNodes': [('#Discount AC', 'Weighted discount')],
          'targetNodes': [('#Margin AC', 'Contribution margin')],
          'Tooltips': ['#Net Sales AC', '#Contribution AC', '#Return AC']},
         'Title Map AC', 'MARKETS', 'x = discount %, y = margin %',
         extra={'colors1': props(propertyCache=L('{"source":"","props":{}}')),
                'shapes1': props(propertyCache=L('{"source":"","props":{}}')),
                'categoryColors1': props(propertyCache=L(city_cat_colors))})

heatmap(p, f'{pid}_hm', B['heat'], 'DimProduct.Category', 'DimCampaign.Campaign Type', 'Return AC',
        'Heat Return Col', 'Heat Return Font', 'Title Returns AC', 'RETURNS  ·  CATEGORY × CAMPAIGN',
        'Coral = 15%+ units returned · right-click › Profile', nrows=4, ncols=5, rh_w=130)

zc_chart(p, f'{pid}_zc_chan', 'combobar', B['chan'],
         {'Category': ['FactSales.Sales Channel', 'DimProduct.Category'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'AC')],
          'Tooltips': TIPS_C},
         'Title Channel AC', 'CHANNEL › CATEGORY', 'click Online › Electronics',
         extra=refline_acpy(PY, SLATE), sort=[('#Contribution AC', 'Descending')])

drawers['ch2'] = drawer(p, pid, GUIDES['ch2'])

# ================================================================== 3 · What to do
pid = PID['ch3']; p = Page(pid, '3 · What to do', BG['ch3']); pages['ch3'] = p; B = BLK['ch3']
topbar(p, pid, 'ch3')
left_header(p, pid, 'CHAPTER 3 OF 3  ·  RECOMMENDED PLAN', 'Msg Ch4', nxt=CHAPTERS[0])

cx_, cy_, cw_, ch_ = B['callout']
textbox(p, f'{pid}_up_t', cx_ + 18, cy_ + 14, cw_ - 36, 18, [[slabel('COMBINED INDICATIVE UPSIDE', 7.5, MUTED), run('   ·   per season', 7.5, SUBTLE)]])
textcard(p, f'{pid}_up_v', cx_ + 17, cy_ + 36, cw_ - 34, 52, 'Pot Total Text', size=26, color=SLATE, font=NUM, wrap=False, bold=True)
textbox(p, f'{pid}_up_n', cx_ + 18, cy_ + 94, cw_ - 36, 44, [[run('Projected from AC volumes & margins assuming volumes hold; order of magnitude, not a forecast.', 8.5, BODY)]])

ux, uy, uw, uh = B['upside_bar']
textbox(p, f'{pid}_up_t2', ux, uy, uw, 18, [[slabel('UPSIDE BY MOVE', 7.5, MUTED), run('   ·   kEUR', 7.5, SUBTLE)]])
table(p, f'{pid}_up', (ux, uy, uw, uh), 'Moves.Label', 204,
      [{'kind': 'var', 'hdr': '', 'w': 402, 'm': 'Pot by Move k', 'label': 'Upside', 'fill': SLATE, 'end': 'Axis Moves End'}],
      [('#Pot by Move k', 'Descending')], rows=4, anchor='Anchor Moves', tt=False, y_off=26)

lx_, ly_, lw_, lh_ = B['limits']
textbox(p, f'{pid}_lim_t', lx_, ly_, lw_, 18, [[slabel('WHAT THIS DATA CANNOT TELL YOU', 7.5, MUTED)]])
LIM_SHORT = [
    ('Not causal.', ' Synthetic data with no control group: nothing proves a campaign caused uplift or ROI.'),
    ('Before overhead.', ' Contribution excludes corporate overhead, interest and tax.'),
    ('Unequal lengths.', ' Campaigns run 3 to 17 days, so compare margins and sales/day, not totals.'),
    ('Allocated spend.', ' Campaign budgets are spread across sales lines by gross-sales share.'),
]
for i, (t_, d_) in enumerate(LIM_SHORT):
    iy = ly_ + 26 + i * 54
    textbox(p, f'{pid}_lim_i{i}', lx_, iy + 7, 20, 20, [[run('i', 8.5, SLATE, NUM, True)]], align='center')
    textbox(p, f'{pid}_lim_b{i}', lx_ + 28, iy, lw_ - 28, 46, [[run(t_, 9, INK, FONT_SB, True), run(d_, 9, BODY)]])

textbox(p, f'{pid}_plan_hdr', RX, 92, RW, 62, [
    [slabel('THE PLAN', 7.5, MUTED)],
    [run('Four moves, each answering a finding from Chapters 1–2', 14.5, INK, 'Segoe UI Semibold', True)],
    [run('Change Season or Channel on the left and every indicative figure recalculates live.', 8.5, MUTED)],
])

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
    textbox(p, f'{nm}_code', x + 16, y + 22, 68, 24, [[run(code, 8.5, BODY, NUM, True)]], align='center')
    textbox(p, f'{nm}_title', x + 100, y + 18, 696, 28, [[run(title, 12, INK, FONT_SB, True)]])
    textcard(p, f'{nm}_ev', x + 100, y + 52, 696, 98, ev, size=9, color=BODY, font=FONT, wrap=True)
    tbutton(p, f'{nm}_link', x + 90, y + h - 44, 320, 38, f'See evidence in Chapter {src[-1]}  →',
            lpage(PID[src]), SLATE, INK, size=9, tip=f'Open Chapter {src[-1]}', align='left')
    textbox(p, f'{nm}_plbl', x + 842, y + 20, 310, 18, [[slabel('INDICATIVE UPSIDE', 7, MUTED)]])
    textcard(p, f'{nm}_pot', x + 840, y + 40, 310, 38, pot, size=19, color=SLATE, font=NUM, wrap=False, bold=True)
    textbox(p, f'{nm}_tlbl', x + 842, y + 88, 310, 18, [[slabel('PILOT TEST', 7, MUTED)]])
    textbox(p, f'{nm}_test', x + 842, y + 108, 310, 82, [[run(test, 9, BODY)]])

drawers['ch3'] = drawer(p, pid, GUIDES['ch3'])

# ================================================================== Campaign profile (drill-through, 2 ZoomCharts)
pid = PID['profile']
p = Page(pid, 'Campaign profile', BG['profile'], drill=[('DimCampaign', 'Campaign Type'), ('DimCampaign', 'Campaign')]); pages['profile'] = p; B = BLK['profile']
topbar(p, pid, 'ch1')
left_header(p, pid, 'DRILL-THROUGH  ·  CAMPAIGN PROFILE', 'Title Drill AC', back=True)

fx_, fy_, fw_, fh_ = B['facts']
textbox(p, f'{pid}_facts_hdr', fx_ + 16, fy_ + 10, fw_ - 32, 18, [[slabel('EVENT FACTS', 7.5, MUTED), run('   ·   for the campaign or type you picked', 7.5, SUBTLE)]])
textcard(p, f'{pid}_facts_txt', fx_ + 16, fy_ + 30, fw_ - 32, 54, 'Drill Campaign Facts', size=9.5, color=BODY, font=FONT, wrap=True)

head(p, f'{pid}_pl', B['pnl'], 'Title Bridge AC', 'PROFIT AND LOSS', 'kEUR · costs in brackets')
table(p, f'{pid}_pnl', B['pnl'], 'PnL Lines.Label', 136,
      [{'kind': 'single', 'hdr': 'PY', 'w': 160, 'm': 'PL PY k', 'label': 'PY', 'colour': PY_BAR, 'start': 'Axis PL Start', 'end': 'Axis PL End'},
       {'kind': 'single', 'hdr': 'AC', 'w': 160, 'm': 'PL AC k', 'label': 'AC', 'colour': SLATE, 'start': 'Axis PL Start', 'end': 'Axis PL End'},
       {'kind': 'var', 'hdr': 'ΔPY', 'w': 136, 'm': 'PL ΔPY k', 'label': 'ΔPY', 'fill_m': 'Colour PL Δ', 'start': 'Axis PL Δ Start', 'end': 'Axis PL Δ End'},
       {'kind': 'pin', 'hdr': 'ΔPY %', 'w': 126, 'm': 'PL ΔPY%', 'label': 'ΔPY %', 'fill_m': 'Colour PL Δ', 'start': 'Axis PL Δ% Start', 'end': 'Axis PL Δ% End'}],
      [('PnL Lines.Label', 'Ascending')], rows=10, anchor='Anchor PL', tt=False, y_off=72, hdr_y_off=48)

zc_chart(p, f'{pid}_zc_daily', 'combo', B['daily'],
         {'Category': ['DimDate.Date'], 'Values1': [('#Net Sales PY', 'PY')], 'Values2': [('#Net Sales AC', 'AC')],
          'Tooltips': ['#Contribution AC', '#Margin AC']},
         'Title Peak Day', 'NET SALES PER TRADING DAY', 'PY Silver line vs AC Blue Slate bars',
         extra=refline_acpy(PY, SLATE))

zc_chart(p, f'{pid}_zc_band', 'combo', B['band'],
         {'Category': ['FactSales.Discount Band'], 'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'AC')],
          'Tooltips': TIPS_C},
         'Title Discount Curve AC', 'DISCOUNT DEPTH', 'PY Silver line vs AC Blue Slate bars',
         extra=refline_acpy(PY, SLATE, pad_lr=True), sort=[('FactSales.Discount Band', 'Ascending')])

drawers['profile'] = drawer(p, pid, GUIDES['profile'])

# ================================================================== Tooltip page (Slate-Coral crisp card)
p = Page(TT_PAGE, 'Snapshot tooltip', 'bg_tooltip_c43.png', tooltip=True, w=TT['w'], h=TT['h']); pages['tooltip'] = p
textcard(p, 'tt_header', 20, 10, 328, 24, 'TT Header', size=11.5, color=INK, font=FONT_SB, wrap=False, bold=True)
textcard(p, 'tt_sel', 20, 36, 328, 18, 'Period Short', size=7, color=MUTED, font=NUM, wrap=False)
for i, (lbl, k, x, y) in enumerate([
    ('NET SALES · AC', 'Net Sales', 20, 70),
    ('CONTRIBUTION · AC', 'Contribution', 198, 70),
    ('MARGIN · AC', 'Margin', 20, 156),
    ('WEIGHTED DISCOUNT · AC', 'Discount', 198, 156),
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
print('V11 Slate-Coral built | visible visuals per page:', vis, '| bookmarks:', len(bms))
