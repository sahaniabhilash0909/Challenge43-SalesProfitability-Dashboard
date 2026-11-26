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


# ---------------------------------------------------------------- Dark Sidebar + Workspace Header + Takeaway Bar (static labels baked into bg12.py)
def sidebar(p, pid, active):
    for k, ny in zip(('ch1', 'ch2', 'ch3'), NAV_Y):
        on = (active == k)
        tbutton(p, f'{pid}_nav_{k}', SB_X + 36, ny, SB_IW - 40, NAV_H, NAVL[k], lpage(PID[k]),
                WHITE if on else SLATE_100, WHITE, size=9.5, font=(FONT_SB if on else FONT),
                tip=f'Open {NAVL[k]}', align='left')

    sx, sy, sw, sh = SEASON_BOX
    sidebar_chips(p, f'{pid}_chip_season', sx, sy, sw, sh, 'DimDate.Season', 'sync_season', 1, rows=3, size=8.5, filt=SEASONS)

    cx, cy, cw, ch = CHANNEL_BOX
    sidebar_chips(p, f'{pid}_chip_channel', cx, cy, cw, ch, 'FactSales.Sales Channel', 'sync_channel', 1, rows=2, size=8.5)

    fx, fy, fw, fh = FILTERS_BTN
    tbutton(p, f'{pid}_btn_filters', fx + 34, fy, fw - 38, fh, 'More filters', lbm(f'bm_{pid}_filters'),
            WHITE, SLATE_100, size=9, tip='Segment, market, category, campaign type, discount band', align='left')
    rx_, ry_, rw, rh = RESET_BTN
    tbutton(p, f'{pid}_btn_reset', rx_ + 34, ry_, rw - 38, rh, 'Reset all', lbm(f'bm_{pid}_reset'),
            SLATE_100, WHITE, size=9, tip='Clear every filter: CY returns to latest season', align='left')

    tbutton(p, f'{pid}_btn_guide', SB_X + 38, INFO_Y[0], SB_IW - 40, 38, 'How to read', lbm(f'bm_{pid}_guide'),
            SLATE_200, WHITE, size=9, tip='How to read charts & Slate-Coral notation', align='left')
    tbutton(p, f'{pid}_btn_limits', SB_X + 38, INFO_Y[1], SB_IW - 40, 38, 'Data notes', lbm(f'bm_{pid}_limits'),
            SLATE_200, WHITE, size=9, tip='Definitions and limits of the dataset', align='left')


def header(p, pid, kicker, title, msg_m, nxt=None, back=False):
    hx, hy, hw, _ = HEADER
    px_, py_, pw, ph = PERIOD_PILL
    textcard(p, f'{pid}_period', px_ + 10, py_ + 3, pw - 20, ph - 6, 'Period Short', size=8, color=BODY, font=NUM, wrap=False, align='center')
    textcard(p, f'{pid}_filt', hx + hw - 18 - 736, hy + 41, 736, 18, 'Filters Line', size=7.5, color=MUTED, wrap=False, align='right')

    mx, my, mw, mh = MSG
    msg_w = mw - 134 if back else mw - 30
    textcard(p, f'{pid}_msg', mx + 16, my + 3, msg_w, mh - 6, msg_m, size=10.5, color=INK, font=FONT_SB, wrap=True)
    if back:
        bx, by, bw, bh = BACK_BTN
        tbutton(p, f'{pid}_btn_back', bx, by, bw, bh, '‹  Back', lback(), BODY, INK, size=9,
                tip='Back to the page you came from', align='center')

    if nxt:
        k, t = nxt
        lbl = 'Back to start  ·  What happened & why  ↺' if k == 'ch1' else f'Next chapter  ·  {t}  →'
        tbutton(p, f'{pid}_next', 1520, FOOT_Y - 3, 356, 26, lbl, lpage(PID[k]), SLATE, INK, size=9,
                tip=f'Open {t}', align='right')


def card_head(p, name, card, take_m, kicker, note=None):
    """Kickers & notes are baked into bg12.py; only emit dynamic headline textcards."""
    x, y, w, _ = card
    if take_m:
        mh = 24 if w >= 850 else 38
        textcard(p, f'{name}_m', x + 18, y + 31, w - 36, mh, take_m, size=9.5, color=INK, font=FONT_SB, wrap=True)
        return 31 + mh  # 55 on wide cards, 69 on narrow/medium cards
    return 33


def card_legend(p, name, card, items, y_off=58):
    """Legends are baked as crisp SVG swatches in bg12.py (zero runtime visuals)."""
    return None


# ---------------------------------------------------------------- Native 5-Tile KPI New Card Visual (callout + reference labels + built-in Oct-Jan trend)
def kpi_strip_v12(p, name, items):
    """Single all-in-one 5-tile cardVisual spanning the KPI strip with top accent bars, callouts, PY delta/baseline reference labels & built-in Oct-Jan trend sparklines."""
    q = query(
        {
            'Data': [(f'#{val_m}', lbl) for lbl, _, val_m, _, _, _ in items],
            'TrendVisualCategory': ['DimDate.Season Month'],
        },
        sort=[('DimDate.Season Month', 'Ascending')],
    )
    o = {
        'layout': [{
            'properties': {
                'orientation': L(2),
                'maxTiles': L(5),
                'cellPadding': D(16),
                'alignment': L('middle'),
                'contentOrder': L('callout_referenceLabel_image'),
                'collage': L('Default'),
                'calloutSize': D(54),
                'paddingUniform': L(0),
                'paddingIndividual': L(False),
                'backgroundShow': L(False),
            },
        }],
        'overFlow': [{
            'properties': {
                'overFlowStyle': L(1),
            },
        }],
        'shapeCustomRectangle': [{
            'properties': {
                'tileShape': L('rectangleRoundedByPixel'),
                'rectangleRoundedCurve': L(10),
                'rectangleRoundedCurveCustomStyle': L(False),
            },
            'selector': {'id': 'default'},
        }],
        'fillCustom': [
            {'properties': {'show': L(True)}},
            {'properties': {'fillColor': col(WHITE), 'transparency': D(0)}, 'selector': {'id': 'default'}},
        ],
        'outline': [
            {'properties': {'show': L(True)}},
            {'properties': {'show': L(True), 'lineColor': col(HAIR), 'weight': D(1), 'transparency': D(0)}, 'selector': {'id': 'default'}},
        ],
        'borderCustom': [
            {'properties': {'show': L(False)}},
            {'properties': {'show': L(False)}, 'selector': {'id': 'default'}},
        ],
        'shadowCustom': [
            {'properties': {'show': L(False)}},
            {'properties': {'show': L(False)}, 'selector': {'id': 'default'}},
        ],
        'glowCustom': [
            {'properties': {'show': L(False)}},
            {'properties': {'show': L(False)}, 'selector': {'id': 'default'}},
        ],
        'divider': [
            {'properties': {'show': L(False)}},
            {'properties': {'show': L(False)}, 'selector': {'id': 'default'}},
        ],
        'accentBar': [
            {'properties': {'show': L(True)}},
            {'properties': {'show': L(True), 'position': L('Top'), 'width': D(3), 'color': col(SLATE), 'transparency': D(0)}, 'selector': {'id': 'default'}},
        ] + [
            {'properties': {'color': col(CORAL)}, 'selector': {'metadata': f'_Measures.{val_m}'}}
            for _, _, val_m, _, _, is_risk in items if is_risk
        ],
        'padding': [{
            'properties': {
                'paddingUniform': L(10),
                'paddingIndividual': L(True),
                'topMargin': L(10),
                'bottomMargin': L(10),
                'leftMargin': L(14),
                'rightMargin': L(10),
            },
            'selector': {'id': 'default'},
        }],
        'spacing': [{
            'properties': {'verticalSpacing': D(2)},
            'selector': {'id': 'default'},
        }],
        'cardCalloutArea': [{
            'properties': {
                'show': L(False),
                'paddingUniform': L(0),
                'paddingIndividual': L(True),
                'topMargin': L(0),
                'bottomMargin': L(0),
                'leftMargin': L(0),
                'rightMargin': L(6),
            },
            'selector': {'id': 'default'},
        }],
        'label': [
            {'properties': {'show': L(True)}},
            {
                'properties': {
                    'show': L(True),
                    'position': L('aboveValue'),
                    'fontFamily': L(FONT_SB),
                    'fontSize': D(8.5),
                    'fontColor': col(MUTED),
                    'horizontalAlignment': L('left'),
                    'textWrap': L(False),
                },
                'selector': {'id': 'default'},
            },
        ],
        'value': [
            {'properties': {'show': L(True)}},
            {
                'properties': {
                    'fontColor': col(INK),
                    'fontSize': D(17),
                    'fontFamily': L(NUM),
                    'bold': L(True),
                    'horizontalAlignment': L('left'),
                    'verticalAlignment': L('middle'),
                    'showBlankAs': L('–'),
                    'textWrap': L(False),
                },
                'selector': {'id': 'default'},
            },
        ] + [
            {'properties': {'labelDisplayUnits': D(units), 'labelPrecision': L(prec)}, 'selector': {'metadata': f'_Measures.{val_m}'}}
            for _, _, val_m, units, prec, _ in items
        ],
        'referenceLabelLayout': [{
            'properties': {
                'position': L('below'),
                'arrangement': L('rows'),
                'style': L('tabular'),
                'horizontalAlignment': L('left'),
                'verticalAlignment': L('top'),
                'labelSpace': D(2),
                'outerPadding': D(0),
            },
            'selector': {'id': 'default'},
        }],
        'referenceLabel': [
            {'properties': {'backgroundShow': L(False), 'paddingUniform': L(0)}, 'selector': {'id': 'default'}},
        ],
        'referenceLabelTitle': [
            {'properties': {'show': L(False)}, 'selector': {'id': 'default'}},
        ],
        'referenceLabelValue': [
            {'properties': {'show': L(True)}, 'selector': {'id': 'default'}},
        ],
        'trendVisualLibrary': [
            {'properties': {'show': L(True)}},
            {
                'properties': {
                    'show': L(True),
                    'includePrimaryMeasure': L(True),
                    'chartType': L('line'),
                    'showTooltip': L(True),
                    'legendShow': L(False),
                    'paddingUniform': L(0),
                    'paddingIndividual': L(True),
                    'topMargin': L(12),
                    'rightMargin': L(4),
                    'bottomMargin': L(4),
                    'leftMargin': L(6),
                },
                'selector': {'id': 'default'},
            },
        ],
        'cartesianTrendVisual': [{
            'properties': {
                'seriesColor': col(SLATE),
                'showXAxis': L(True),
                'categoryAxisFontFamily': L(NUM),
                'categoryAxisFontSize': D(7),
                'categoryAxisColor': col(SUBTLE),
                'showYAxis': L(False),
                'showDataLabels': L(False),
            },
            'selector': {'id': 'default'},
        }],
        'lineTrendVisual': [{
            'properties': {
                'lineShow': L(True),
                'lineWidth': D(2),
                'lineTransparency': D(0),
                'lineStyle': L('solid'),
                'lineShape': L('smooth'),
                'fillArea': L(True),
                'fillAreaTransparency': D(86),
                'showMarkers': L(False),
            },
            'selector': {'id': 'default'},
        }],
    }
    for i, (_, k, val_m, _, _, _) in enumerate(items):
        md = f'_Measures.{val_m}'
        did, pid_ref = f'ref_d_{i}', f'ref_p_{i}'
        o['referenceLabel'].extend([
            {
                'properties': {'value': M(f'KPI {k} Tag')},
                'selector': {'data': [{'dataViewWildcard': {'matchingOption': 0}}], 'id': did, 'metadata': md, 'order': 0},
            },
            {
                'properties': {'value': M(f'KPI {k} PY')},
                'selector': {'data': [{'dataViewWildcard': {'matchingOption': 0}}], 'id': pid_ref, 'metadata': md, 'order': 1},
            },
        ])
        o['referenceLabelTitle'].extend([
            {'properties': {'show': L(False)}, 'selector': {'id': did, 'metadata': md}},
            {'properties': {'show': L(False)}, 'selector': {'id': pid_ref, 'metadata': md}},
        ])
        o['referenceLabelValue'].extend([
            {
                'properties': {'show': L(True), 'valueFontFamily': L(NUM), 'valueFontSize': D(8), 'valueBold': L(True)},
                'selector': {'id': did, 'metadata': md},
            },
            {
                'properties': {'valueFontColor': mcol(f'KPI {k} Col')},
                'selector': {'data': [{'dataViewWildcard': {'matchingOption': 0}}], 'id': did, 'metadata': md},
            },
            {
                'properties': {'show': L(True), 'valueFontFamily': L(NUM), 'valueFontSize': D(7), 'valueBold': L(False), 'valueFontColor': col(SUBTLE)},
                'selector': {'id': pid_ref, 'metadata': md},
            },
        ])
    p.add(name, 'cardVisual', X0, KPI_Y, MW, KPI_H, q=q, objects=o,
          vco_=vco(header=False, pad=(0, 0, 0, 0), tooltip=True), schema=SCH_V_210)


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


def heatmap(p, name, card, rows, colsf, val, col_m, font_m, take_m, kicker, note, nrows=4, ncols=5, rh_w=138, legend=None):
    leg_y = card_head(p, name, card, take_m, kicker, note)
    x, y, w, h = card
    if legend:
        card_legend(p, f'{name}_leg', card, legend, y_off=leg_y)
    top_y = y + (leg_y + 23 if legend else leg_y + 4)
    vw, vh = w - 32, h - ((leg_y + 33) if legend else (leg_y + 14))
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
    p.add(f'{name}_mx', 'pivotTable', x + 16, top_y, vw, vh,
          q=query({'Rows': [rows], 'Columns': [colsf], 'Values': [(f'#{val}', 'CY')]}), objects=o,
          vco_=vco(header=True, pad=(0, 0, 0, 0), tooltip_page=TT_PAGE))


def scorecard_matrix(p, name, card, rows, values, take_m, kicker, note, col_widths, alignments, cond_fmt, sort=None, legend=None):
    leg_y = card_head(p, name, card, take_m, kicker, note)
    x, y, w, h = card
    if legend:
        card_legend(p, f'{name}_leg', card, legend, y_off=leg_y)
    top_y = y + (leg_y + 23 if legend else leg_y + 4)
    vh = h - ((leg_y + 33) if legend else (leg_y + 14))
    vals_obj = [{'properties': {
        'fontSize': D(9.5), 'fontFamily': L(NUM), 'fontColorPrimary': col(INK), 'backColorPrimary': col(WHITE),
        'fontColorSecondary': col(INK), 'backColorSecondary': col(WHITE), 'outlineStyle': L(0),
    }}]
    for md, fmts in cond_fmt.items():
        vals_obj.append({
            'properties': fmts,
            'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}], 'metadata': md},
        })
    o = {
        'grid': props(gridVertical=L(False), gridHorizontal=L(True), gridHorizontalColor=col(HAIR), gridHorizontalWeight=D(1),
                      rowPadding=D(5.5 if legend else 7), outlineColor=col(HAIR), outlineWeight=D(1)),
        'columnHeaders': props(fontColor=col(MUTED), fontSize=D(8.5), fontFamily=L(FONT_SB), bold=L(True),
                               backColor=col(CALLOUT), outlineStyle=L(1), autoSizeColumnWidth=L(False)),
        'rowHeaders': props(fontColor=col(INK), fontSize=D(9.5), fontFamily=L(FONT_SB), backColor=col(WHITE),
                            outlineStyle=L(0), stepped=L(True), showExpandCollapseButtons=L(True)),
        'values': vals_obj,
        'columnWidth': [{'properties': {'value': D(cw)}, 'selector': {'metadata': md}} for md, cw in col_widths.items()],
        'columnFormatting': [{'properties': {'alignment': L(al)}, 'selector': {'metadata': md}} for md, al in alignments.items()],
        'subTotals': props(rowSubtotals=L(True), columnSubtotals=L(False), rowSubtotalsPosition=L('Bottom')),
        'total': props(fontColor=col(INK), backColor=col(SLATE_50), fontSize=D(9.5), fontFamily=L(NUM), bold=L(True), outlineStyle=L(2)),
    }
    p.add(f'{name}_mx', 'pivotTable', x + 16, top_y, w - 32, vh,
          q=query({'Rows': rows, 'Values': values}, sort), objects=o,
          vco_=vco(header=True, pad=(0, 0, 0, 0), tooltip_page=TT_PAGE))


def zc_chart(p, name, kind, card, roles, take_m, kicker, note, extra=None, sort=None, legend=None):
    leg_y = card_head(p, name, card, take_m, kicker, note)
    x, y, w, h = card
    if legend:
        card_legend(p, f'{name}_leg', card, legend, y_off=leg_y)
    top_y = y + (leg_y + 23 if legend else leg_y)
    vis_h = h - ((leg_y + 31) if legend else (leg_y + 8))
    vt, _ = ZC[kind]
    o = {'advanced': [{'properties': {'shouldApplyNewDefaults': L(True)}}], 'toolbar': props(show=L(False)), 'legend': props(show=L(False))}
    if extra:
        o.update(extra)
    return p.add(name, vt, x + 12, top_y, w - 24, vis_h, q=query(roles, sort), objects=o, vco_=vco(header=True, pad=(0, 0, 0, 0)))


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


def overlap_cy_py_cols(c_py=PY_BAR, c_cy=SLATE, py_w=84, cy_w=52):
    """Overlapping columns in ZoomCharts Combo PRO: wider light PY behind narrower Blue Slate CY, zero outline/marker."""
    o = series_colors({1: c_py, 2: c_cy})
    o['stacks'] = props(mode=L('based'), separateNegativeValues=L(True))
    o['seriesDefault'][0]['properties'].update({
        'seriesSettingSelector': L('s1'),
        'display': L('stacked'),
        'columnLineWidth': L(0),
        'lineColorOpacity': L(0),
        'lineMarker': L(''),
        'lineMarkerSize': L(0),
        'customize1': L(True),
        'display1': L('stacked'),
        'stack1': L('s1'),
        'type1': L('columns'),
        'fillColor1': col(c_py),
        'fillColorOpacity1': L(85),
        'widthScale1': L(py_w),
        'zIndex1': L(5),
        'columnLineWidth1': L(0),
        'lineColorOpacity1': L(0),
        'lineMarker1': L(''),
        'lineMarkerSize1': L(0),
        'customize2': L(True),
        'display2': L('stacked'),
        'stack2': L('s1'),
        'type2': L('columns'),
        'fillColor2': col(c_cy),
        'fillColorOpacity2': L(100),
        'widthScale2': L(cy_w),
        'zIndex2': L(20),
        'columnLineWidth2': L(0),
        'lineColorOpacity2': L(0),
        'lineMarker2': L(''),
        'lineMarkerSize2': L(0),
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
    o['columnBarSettings'] = props(leftPadding=L(14), rightPadding=L(14))
    return o


# ---------------------------------------------------------------- Slide-over Drawer
DR = DRAWER['panel']
DX, DW = DR['x'] + 24, DR['w'] - 48
NOTATION = ('How to read Slate-Coral IBCS',
            'Blue Slate (#4F5D75) = CY & favorable gains. Silver-Grey (#8B909E / #B5BECC) = PY (one season earlier). '
            'Coral Glow (#EF8354) = adverse bars, margin erosion & 15%+ return leaks; Burnt Coral (#BA4B1D) = small adverse text. '
            'KPI cards combine the CY headline metric, PY delta & baseline labels, and a built-in Oct–Jan CY trend sparkline.')
LIMITS = [
    ('Synthetic data.', ' Three October–January holiday windows (2023/24, 2024/25, 2025/26) across eight European city markets. 2023/24 has no PY.'),
    ('Descriptive, not causal.', ' There is no control group, randomisation or ad-exposure data, so nothing here proves a campaign caused extra sales, uplift or ROI.'),
    ('Contribution profit', ' = net sales − product cost − fulfilment − payment fees − return handling − allocated campaign spend. It excludes overhead, interest and tax.'),
    ('Unequal durations.', ' Black Friday and Cyber Monday run 3 days; Christmas 17 and New Year 15. Compare margins or per-day sales, not totals.'),
    ('Campaign spend', ' is each event budget allocated to sales lines by gross-sales share.'),
    ('Weighted discount %', ' = discount € ÷ gross sales €. Returns carry no return date; refunds count against the original sale.'),
]
GUIDES = {
    'ch1': [('KPI strip.', 'Top 5 native cards show CY hero metrics, PY delta/baseline labels, and built-in Oct–Jan CY trend sparklines.'),
            ('Profit bridge.', 'Left tall card reads top-down from PY contribution to CY: Blue Slate bars added margin, Coral Glow bars eroded it.'),
            ('Month, discount & campaign drills.', 'Monthly Contribution plots the solid CY line against a dotted light grey PY line with Max (Blue Slate) and Min (Coral) callouts; Discount Depth (Combo) drills into campaigns and the expandable Campaign Scorecard matrix compares Days, Net Sales, Sales/Day, Discount %, Contribution CY, ΔPY, and color-coded Margin % across Campaign Type › Event (right-click › Drill through).')],
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
kpi_strip_v12(p, f'{pid}_kpis', [
    ('Contribution profit', 'Contribution', 'Contribution AC', 1000, 1, False),
    ('Contribution margin', 'Margin', 'Margin AC', 1, 1, False),
    ('Net sales', 'Net Sales', 'Net Sales AC', 1000, 1, False),
    ('Weighted discount', 'Discount', 'Discount AC', 1, 1, True),
    ('Sales at 20%+ discount', 'Deep', 'Deep Share AC', 1, 1, True),
])

br_leg_y = card_head(p, f'{pid}_br', C['bridge'], 'Title Bridge Var', 'PROFIT BRIDGE', 'kEUR · PY to CY')
card_legend(p, f'{pid}_br_leg', C['bridge'], [
    ('■', CORAL, 'Took margin'),
    ('■', SLATE_400, 'Added margin'),
    ('■', SLATE, 'CY total'),
    ('■', PY_BAR, 'PY total'),
], y_off=br_leg_y)
table(p, f'{pid}_br', C['bridge'], 'Bridge Lines.Label', 126,
      [{'kind': 'stack', 'hdr': '', 'w': 392, 'end': 'Axis Bridge End 2',
        'series': [('Bridge Base k', WHITE, None), ('Bridge PY k', PY_BAR, None), ('Bridge AC k', SLATE, None),
                   ('Bridge Up k', SLATE_400, None), ('Bridge Down k', CORAL, None),
                   ('Bridge Tail k', WHITE, {'pos': 'InsideBase', 'value': 'Bridge Label k', 'color': INK})]}],
      [('Bridge Lines.Label', 'Ascending')], rows=10, anchor='Anchor Bridge', tt=False, y_off=br_leg_y + 24, hdr_y_off=br_leg_y)

mc_x, mc_y, mc_w, mc_h = C['month']
m_leg_y = card_head(p, f'{pid}_month', C['month'], 'Title Month AC', 'CONTRIBUTION BY MONTH', 'kEUR · Oct–Jan · CY solid vs PY dotted')
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
p.add(f'{pid}_month', 'areaChart', mc_x + 12, mc_y + m_leg_y + 24, mc_w - 24, mc_h - (m_leg_y + 32),
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
         'Title Discount Curve AC', 'DISCOUNT DEPTH', 'kEUR · click › campaigns',
         extra=overlap_cy_py_cols(PY_BAR, SLATE, py_w=84, cy_w=52),
         sort=[('FactSales.Discount Band', 'Ascending')],
         legend=[('■', SLATE, 'CY contribution'), ('■', PY_BAR, 'PY contribution')])

scorecard_matrix(
    p, f'{pid}_scorecard', C['type'],
    rows=['DimCampaign.Campaign Type', 'DimCampaign.Campaign'],
    values=[
        ('#Trading Days AC', 'Days'),
        ('#Net Sales AC', 'Net sales CY'),
        ('#Net Sales per Day AC', 'Sales / day'),
        ('#Discount AC', 'Discount %'),
        ('#Contribution AC', 'Contribution CY'),
        ('#Contribution ΔPY', 'ΔPY (€)'),
        ('#Margin AC', 'Margin %'),
    ],
    take_m='Title Scorecard Var',
    kicker='CAMPAIGN SCORECARD',
    note='expand + for events · right-click › Profile',
    col_widths={
        'DimCampaign.Campaign Type': 196,
        '_Measures.Trading Days AC': 72,
        '_Measures.Net Sales AC': 124,
        '_Measures.Net Sales per Day AC': 116,
        '_Measures.Discount AC': 106,
        '_Measures.Contribution AC': 136,
        '_Measures.Contribution ΔPY': 124,
        '_Measures.Margin AC': 116,
    },
    alignments={
        '_Measures.Trading Days AC': 'Right',
        '_Measures.Net Sales AC': 'Right',
        '_Measures.Net Sales per Day AC': 'Right',
        '_Measures.Discount AC': 'Right',
        '_Measures.Contribution AC': 'Right',
        '_Measures.Contribution ΔPY': 'Right',
        '_Measures.Margin AC': 'Center',
    },
    cond_fmt={
        '_Measures.Contribution ΔPY': {'fontColor': mcol('KPI Contribution Col')},
        '_Measures.Margin AC': {'backColor': mcol('Heat Margin Col'), 'fontColor': mcol('Heat Margin Font')},
    },
    sort=[('#Contribution AC', 'Descending')],
    legend=[
        ('■', SLATE, '30%+ margin'),
        ('■', SLATE_200, '10–30%'),
        ('■', CORAL_200, '<0% loss'),
        ('●', SLATE, 'ΔPY gain'),
        ('●', CORAL_TEXT, 'ΔPY drop'),
    ],
)

drawers['ch1'] = drawer(p, pid, GUIDES['ch1'])

# ================================================================== 2 · Where it leaks (4 ZoomCharts visuals)
pid = PID['ch2']; p = Page(pid, '2 · Where it leaks', BG['ch2']); pages['ch2'] = p; C = CARDS['ch2']
sidebar(p, pid, 'ch2')
header(p, pid, 'CHAPTER 2 OF 3  ·  PRODUCTS, CHANNELS, MARKETS & RETURNS', 'Where it leaks', 'Msg Ch3', nxt=CHAPTERS[2])
kpi_strip_v12(p, f'{pid}_kpis', [
    ('Online electronics margin', 'OE Margin', 'OE Margin AC', 1, 1, True),
    ('Net sales sold at a loss', 'Loss Share', 'Loss Share AC', 1, 1, True),
    ('Return rate · all units', 'Return', 'Return AC', 1, 1, True),
    ('Return rate · apparel', 'Apparel Return', 'Apparel Return Rate AC', 1, 1, True),
    ('Average order value', 'AOV', 'AOV AC', 1, 0, False),
])

zc_chart(p, f'{pid}_zc_cat', 'combobar', C['cat'],
         {'Category': ['DimProduct.Category', 'DimProduct.Subcategory', 'DimProduct.Product'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'CY')],
          'Tooltips': TIPS_C + [('#Return AC', 'Return rate CY')]},
         'Title Category AC', 'PRODUCTS', 'click › subcat › product',
         extra=overlap_cy_py_cols(PY_BAR, SLATE, py_w=84, cy_w=52), sort=[('#Contribution AC', 'Descending')],
         legend=[('■', SLATE, 'CY contribution'), ('■', PY_BAR, 'PY contribution')])

zc_chart(p, f'{pid}_zc_donut', 'donut', C['donut'],
         {'Category': ['FactSales.Customer Segment', 'FactSales.Sales Channel'],
          'Values': [('#Net Sales AC', 'Net sales CY')],
          'Tooltips': [('#Margin AC', 'Margin CY'), ('#Contribution AC', 'Contribution CY'), ('#Net Sales ΔPY%', 'Net sales ΔPY%'), ('#AOV AC', 'AOV CY')]},
         'Title Segment AC', 'SEGMENTS › CHANNELS', 'click segment › channel split',
         extra={'legend': props(show=L(True), displayMode=L('inline'), position=L('top'), alignHorizontal=L('left'),
                                markerShape=L('square'), markerSize=L(8), fontSize=D(8), fontFamily=L(FONT),
                                fontColor=col(MUTED), labelMode=L('name'))})

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
                'categoryColors1': props(propertyCache=L(city_cat_colors))},
         legend=[('●', CORAL, 'Berlin (lowest margin)'), ('●', SLATE, 'Other 7 cities')])

heatmap(p, f'{pid}_hm', C['heat'], 'DimProduct.Category', 'DimCampaign.Campaign Type', 'Return AC',
        'Heat Return Col', 'Heat Return Font', 'Title Returns AC', 'RETURNS  ·  CATEGORY × CAMPAIGN',
        'right-click › Profile', nrows=4, ncols=5, rh_w=138,
        legend=[('■', SLATE_50, '<6%'), ('■', SLATE_100, '6–10%'), ('■', SLATE_200, '10–15%'), ('■', CORAL_200, '15%+ high return')])

zc_chart(p, f'{pid}_zc_chan', 'combobar', C['chan'],
         {'Category': ['FactSales.Sales Channel', 'DimProduct.Category'],
          'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'CY')],
          'Tooltips': TIPS_C},
         'Title Channel AC', 'CHANNEL › CATEGORY', 'click Online › Electronics',
         extra=overlap_cy_py_cols(PY_BAR, SLATE, py_w=84, cy_w=52), sort=[('#Contribution AC', 'Descending')],
         legend=[('■', SLATE, 'CY contribution'), ('■', PY_BAR, 'PY contribution')])

drawers['ch2'] = drawer(p, pid, GUIDES['ch2'])

# ================================================================== 3 · What to do
pid = PID['ch3']; p = Page(pid, '3 · What to do', BG['ch3']); pages['ch3'] = p; C = CARDS['ch3']
sidebar(p, pid, 'ch3')
header(p, pid, 'CHAPTER 3 OF 3  ·  FOUR RECOMMENDED MOVES', 'What to do', 'Msg Ch4', nxt=CHAPTERS[0])

cx_, cy_, cw_, ch_ = C['callout']
textcard(p, f'{pid}_up_v', cx_ + 18, cy_ + 40, cw_ - 36, 54, 'Pot Total Text', size=26, color=SLATE, font=NUM, wrap=False, bold=True)

ux, uy, uw, uh = C['upside_bar']
card_head(p, f'{pid}_up', C['upside_bar'], None, 'UPSIDE BY MOVE', 'kEUR · CY simulation')
table(p, f'{pid}_up', (ux, uy, uw, uh), 'Moves.Label', 190,
      [{'kind': 'var', 'hdr': '', 'w': 308, 'm': 'Pot by Move k', 'label': 'Upside', 'fill': SLATE, 'end': 'Axis Moves End'}],
      [('#Pot by Move k', 'Descending')], rows=4, anchor='Anchor Moves', tt=False, y_off=58, hdr_y_off=44)

MOVES = [
    ('ACT-01', 'Evidence Discount', 'Pot Discount Text', 'ch1'),
    ('ACT-02', 'Evidence OE', 'Pot OE Text', 'ch2'),
    ('ACT-03', 'Evidence Returns', 'Pot Returns Text', 'ch2'),
    ('ACT-04', 'Evidence NY', 'Pot NY Text', 'ch1'),
]
for i, (code, ev, pot, src) in enumerate(MOVES):
    x, y, w, h = ACTION_ROWS[i]
    nm = f'{pid}_m{i}'
    textcard(p, f'{nm}_ev', x + 102, y + 50, 610, 96, ev, size=9, color=BODY, font=FONT, wrap=True)
    tbutton(p, f'{nm}_link', x + 92, y + h - 44, 300, 36, f'See evidence in Chapter {src[-1]}  →',
            lpage(PID[src]), SLATE, INK, size=9, tip=f'Open Chapter {src[-1]}', align='left')
    textcard(p, f'{nm}_pot', x + 756, y + 40, 280, 38, pot, size=19, color=SLATE, font=NUM, wrap=False, bold=True)

drawers['ch3'] = drawer(p, pid, GUIDES['ch3'])

# ================================================================== Campaign profile (drill-through, 2 ZoomCharts)
pid = PID['profile']
p = Page(pid, 'Campaign profile', BG['profile'], drill=[('DimCampaign', 'Campaign Type'), ('DimCampaign', 'Campaign')]); pages['profile'] = p; C = CARDS['profile']
sidebar(p, pid, 'ch1')
header(p, pid, 'DRILL-THROUGH  ·  CAMPAIGN PROFILE', 'Campaign profile', 'Title Drill AC', back=True)

fx_, fy_, fw_, fh_ = C['facts']
textcard(p, f'{pid}_facts_txt', fx_ + 18, fy_ + 34, fw_ - 36, 62, 'Drill Campaign Facts', size=9.5, color=BODY, font=FONT, wrap=True)

pl_leg_y = card_head(p, f'{pid}_pl', C['pnl'], 'Title Bridge AC', 'PROFIT AND LOSS', 'kEUR · costs in brackets')
card_legend(p, f'{pid}_pl_leg', C['pnl'], [
    ('■', PY_BAR, 'PY'),
    ('■', SLATE, 'CY / Favorable ΔPY'),
    ('■', CORAL, 'Adverse ΔPY'),
], y_off=pl_leg_y)
table(p, f'{pid}_pnl', C['pnl'], 'PnL Lines.Label', 134,
      [{'kind': 'single', 'hdr': 'PY', 'w': 158, 'm': 'PL PY k', 'label': 'PY', 'colour': PY_BAR, 'start': 'Axis PL Start', 'end': 'Axis PL End'},
       {'kind': 'single', 'hdr': 'CY', 'w': 158, 'm': 'PL AC k', 'label': 'CY', 'colour': SLATE, 'start': 'Axis PL Start', 'end': 'Axis PL End'},
       {'kind': 'var', 'hdr': 'ΔPY', 'w': 134, 'm': 'PL ΔPY k', 'label': 'ΔPY', 'fill_m': 'Colour PL Δ', 'start': 'Axis PL Δ Start', 'end': 'Axis PL Δ End'},
       {'kind': 'pin', 'hdr': 'ΔPY %', 'w': 126, 'm': 'PL ΔPY%', 'label': 'ΔPY %', 'fill_m': 'Colour PL Δ', 'start': 'Axis PL Δ% Start', 'end': 'Axis PL Δ% End'}],
      [('PnL Lines.Label', 'Ascending')], rows=10, anchor='Anchor PL', tt=False, y_off=pl_leg_y + 46, hdr_y_off=pl_leg_y + 24)

zc_chart(p, f'{pid}_zc_daily', 'combo', C['daily'],
         {'Category': ['DimDate.Date'], 'Values1': [('#Net Sales PY', 'PY')], 'Values2': [('#Net Sales AC', 'CY')],
          'Tooltips': [('#Contribution AC', 'Contribution CY'), ('#Margin AC', 'Margin CY')]},
         'Title Peak Day', 'NET SALES PER TRADING DAY', 'kEUR · daily trading',
         extra=overlap_cy_py_cols(PY_BAR, SLATE, py_w=90, cy_w=56),
         legend=[('■', SLATE, 'CY net sales'), ('■', PY_BAR, 'PY net sales')])

zc_chart(p, f'{pid}_zc_band', 'combo', C['band'],
         {'Category': ['FactSales.Discount Band'], 'Values1': [('#Contribution PY', 'PY')], 'Values2': [('#Contribution AC', 'CY')],
          'Tooltips': TIPS_C},
         'Title Discount Curve AC', 'DISCOUNT DEPTH', 'kEUR · by discount band',
         extra=overlap_cy_py_cols(PY_BAR, SLATE, py_w=84, cy_w=52),
         sort=[('FactSales.Discount Band', 'Ascending')],
         legend=[('■', SLATE, 'CY contribution'), ('■', PY_BAR, 'PY contribution')])

drawers['profile'] = drawer(p, pid, GUIDES['profile'])

# ================================================================== Tooltip page
p = Page(TT_PAGE, 'Snapshot tooltip', 'bg_tooltip_c43.png', tooltip=True, w=TT['w'], h=TT['h']); pages['tooltip'] = p
textcard(p, 'tt_header', 20, 6, 328, 50, 'TT Header', size=10.5, color=INK, font=FONT_SB, wrap=True, bold=True,
         sub_measure='Period Short', sub_size=7, sub_color=MUTED, sub_font=NUM)
for i, (k, x, y) in enumerate([
    ('Net Sales', 20, 70),
    ('Contribution', 198, 70),
    ('Margin', 20, 156),
    ('Discount', 198, 156),
]):
    textcard(p, f'tt_v{i}', x, y + 16, 160, 46, f'KPI {k} AC', size=15, color=INK, font=NUM, wrap=False, bold=True,
             sub_measure=f'KPI {k} Tag', sub_size=7.5, sub_color_measure=f'KPI {k} Col', sub_font=NUM, sub_bold=True)
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
