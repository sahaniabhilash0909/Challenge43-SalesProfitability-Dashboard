"""PBIR helpers for the Challenge 43 V11 Slate-Coral Editorial Boardroom Analytics edition."""
import json, os

SCH_V = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json'
SCH_P = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json'

FONT = "'Segoe UI'"
FONT_SB = "'Segoe UI Semibold'"
NUM = "'Consolas'"

# Slate-Coral Design System Tokens (exact from Slate_coral/tokens/tokens.json)
INK = '#2D3142'         # ~Jet Black (primary ink)
BODY = '#454A5E'        # secondary narrative ink
MUTED = '#646B7D'       # kickers, subtitles, headers
SUBTLE = '#8B909E'      # chart axis ticks, quiet metadata, PY reference line

SILVER = '#BFC0C0'      # structural borders, segmented frame, dashed callout
HAIR = '#E4E5E7'        # 1px editorial hairline dividers
SURF_MUTED = '#EAEBED'  # active segmented button fill, secondary reset pill
CALLOUT = '#F5F6F8'     # projected callout wash
CANVAS = '#F2F3F5'      # outer viewport mat
WHITE = '#FFFFFF'       # pure-white editorial sheet surface

SLATE_DARK = '#3B465A'  # hover/pressed primary CTA
SLATE = '#4F5D75'       # ~Blue Slate (primary CTA, active rail, gains, AC)
SLATE_400 = '#7B89A0'   # mid slate (neutral/historical peak)
SLATE_200 = '#B5BECC'   # soft slate (PY bars & bridge base)
SLATE_100 = '#E2E6EC'   # pale slate (brand tile, PY area wash, pass bg)
SLATE_50 = '#F3F5F8'    # faint slate tint (code pills, hover tint)

CORAL_DARK = '#9E3E16'  # high-emphasis adverse text / heatmap alert text
CORAL_TEXT = '#BA4B1D'  # WCAG AA small adverse text on white
CORAL = '#EF8354'       # ~Coral Glow (adverse graphic fills/strokes)
CORAL_400 = '#F4A37F'   # soft coral
CORAL_200 = '#FAD3C1'   # pale coral (heatmap alert fill)
CORAL_50 = '#FEF5F0'    # faint coral wash

AC = SLATE
PY = SUBTLE
PY_BAR = SLATE_200
PY_AREA = SLATE_100
GOOD = SLATE
BAD = CORAL
BAD_T = CORAL_TEXT
NAVY = INK


def L(v):
    if isinstance(v, bool):
        s = 'true' if v else 'false'
    elif isinstance(v, int):
        s = f'{v}L'
    elif isinstance(v, float):
        s = f'{v}D'
    else:
        s = "'" + str(v).replace("'", "''") + "'"
    return {'expr': {'Literal': {'Value': s}}}


def D(v):
    return {'expr': {'Literal': {'Value': f'{v}D'}}}


def col(c):
    return {'solid': {'color': L(c)}}


def fcol(e, p):
    return {'Column': {'Expression': {'SourceRef': {'Entity': e}}, 'Property': p}}


def fmea(p, e='_Measures'):
    return {'Measure': {'Expression': {'SourceRef': {'Entity': e}}, 'Property': p}}


def M(name):
    return {'expr': fmea(name)}


def mcol(name):
    return {'solid': {'color': M(name)}}


def F(spec):
    """'Table.Column' or '#Measure'"""
    if spec.startswith('#'):
        return fmea(spec[1:])
    e, p = spec.split('.', 1)
    return fcol(e, p)


def qref(f):
    k = 'Column' if 'Column' in f else 'Measure'
    return f"{f[k]['Expression']['SourceRef']['Entity']}.{f[k]['Property']}", f[k]['Property']


def query(roles, sort=None):
    qs = {}
    for r, fields in roles.items():
        ps = []
        for f in fields:
            disp = None
            if isinstance(f, tuple):
                f, disp = f
            fld = F(f)
            qr, nq = qref(fld)
            d = {'field': fld, 'queryRef': qr, 'nativeQueryRef': nq}
            if disp:
                d['displayName'] = disp
            ps.append(d)
        qs[r] = {'projections': ps}
    q = {'queryState': qs}
    if sort:
        q['sortDefinition'] = {'sort': [{'field': F(s[0]), 'direction': s[1]} for s in sort], 'isDefaultSort': False}
    return q


def props(**kw):
    return [{'properties': kw}]


def vco(title=None, tmeasure=None, sub=None, header=True, pad=(12, 8, 16, 16), wrap=False, tsize=12, tcolor=INK,
        link=None, alt=None, tooltip=True, tooltip_page=None, align='left'):
    o = {}
    if title or tmeasure:
        o['title'] = props(show=L(True), text=(M(tmeasure) if tmeasure else L(title)), fontColor=col(tcolor), fontSize=D(tsize),
                           fontFamily=L(FONT_SB), bold=L(False), titleWrap=L(wrap), alignment=L(align))
    else:
        o['title'] = props(show=L(False))
    if sub:
        o['subTitle'] = props(show=L(True), text=L(sub), fontColor=col(MUTED), fontSize=D(9), fontFamily=L(FONT), alignment=L(align))
    else:
        o['subTitle'] = props(show=L(False))
    o['background'] = props(show=L(False))
    o['border'] = props(show=L(False))
    o['dropShadow'] = props(show=L(False))
    o['divider'] = props(show=L(False))
    o['visualHeader'] = props(show=L(header))
    o['padding'] = props(top=D(pad[0]), bottom=D(pad[1]), left=D(pad[2]), right=D(pad[3]))
    if not tooltip:
        o['visualTooltip'] = props(show=L(False))
    elif tooltip_page:
        o['visualTooltip'] = props(show=L(True), type=L('Canvas'), section=L(tooltip_page))
    if link:
        o['visualLink'] = link
    if alt or title:
        o['general'] = props(altText=L(alt or title))
    return o


class Page:
    def __init__(s, name, display, bg=None, drill=None, tooltip=False, w=1920, h=1080):
        s.name, s.display, s.bg, s.drill, s.tooltip, s.w, s.h = name, display, bg, drill, tooltip, w, h
        s.visuals = []
        s.z = 0

    def add(s, name, vtype, x, y, w, h, q=None, objects=None, vco_=None, hidden=False, extra=None):
        assert len(name) <= 50, name
        s.z += 1
        v = {'$schema': SCH_V, 'name': name,
             'position': {'x': round(x, 2), 'y': round(y, 2), 'z': s.z * 100, 'height': round(h, 2), 'width': round(w, 2), 'tabOrder': s.z * 100}}
        vis = {'visualType': vtype}
        if q:
            vis['query'] = q
        if objects:
            vis['objects'] = objects
        vis['visualContainerObjects'] = vco_ if vco_ is not None else vco(header=False)
        vis['drillFilterOtherVisuals'] = True
        if extra:
            vis.update(extra)
        v['visual'] = vis
        if hidden:
            v['isHidden'] = True
        s.visuals.append(v)
        return v

    def write(s, root):
        pd = os.path.join(root, 'definition', 'pages', s.name)
        os.makedirs(pd, exist_ok=True)
        page = {'$schema': SCH_P, 'name': s.name, 'displayName': s.display,
                'displayOption': 'ActualSize' if s.tooltip else 'FitToPage', 'height': s.h, 'width': s.w}
        objs = {}
        if s.bg:
            objs['background'] = [{'properties': {'image': {'image': {'name': L(s.bg), 'url': {'expr': {'ResourcePackageItem': {
                'PackageName': 'RegisteredResources', 'PackageType': 1, 'ItemName': s.bg}}}, 'scaling': L('Fit')}}, 'transparency': D(0)}}]
            objs['outspace'] = [{'properties': {'color': col(CANVAS), 'transparency': D(0)}}]
        page['objects'] = objs
        if s.drill:
            fl = [{'name': f'dt_{p.lower().replace(" ", "_")}', 'field': fcol(e, p), 'type': 'Categorical', 'howCreated': 'Drillthrough'} for e, p in s.drill]
            page['filterConfig'] = {'filters': fl}
            page['type'] = 'Drillthrough'
            page['pageBinding'] = {'name': 'dt_binding', 'type': 'Drillthrough', 'referenceScope': 'Default',
                                   'parameters': [{'name': f'dt_param_{f["name"]}', 'boundFilter': f['name'], 'fieldExpr': f['field']} for f in fl]}
            page['visibility'] = 'HiddenInViewMode'
        if s.tooltip:
            page['type'] = 'Tooltip'
            page['pageBinding'] = {'name': 'tt_binding', 'type': 'Tooltip', 'referenceScope': 'Default'}
            page['visibility'] = 'HiddenInViewMode'
        json.dump(page, open(os.path.join(pd, 'page.json'), 'w', encoding='utf-8'), indent=2)
        for v in s.visuals:
            vd = os.path.join(pd, 'visuals', v['name'])
            os.makedirs(vd, exist_ok=True)
            json.dump(v, open(os.path.join(vd, 'visual.json'), 'w', encoding='utf-8'), indent=2)


def run(v, size, color=INK, font='Segoe UI', bold=False):
    st = {'fontFamily': font, 'fontSize': f'{size}pt', 'color': color}
    if bold:
        st['fontWeight'] = 'bold'
    return {'value': v, 'textStyle': st}


def textbox(p, name, x, y, w, h, paras, hidden=False, align='left'):
    if len(paras) == 1:
        mx = max(float(r['textStyle']['fontSize'][:-2]) for r in paras[0])
        h = max(h, round(mx * 1.85 + 7))
    ps = [{'textRuns': r, 'horizontalTextAlignment': align} for r in paras]
    v = p.add(name, 'textbox', x, y, w, h, objects={'general': [{'properties': {'paragraphs': ps}}]},
              vco_=vco(header=False, pad=(0, 0, 0, 0), tooltip=False), hidden=hidden)
    v['visual']['drillFilterOtherVisuals'] = False
    return v


def textcard(p, name, x, y, w, h, measure, size=10.5, color=INK, font=FONT, hidden=False, wrap=True, color_measure=None, align='left', bold=False):
    objs = {'shape': props(tileShape=L('rectangle')), 'fill': [{'properties': {'show': L(False)}}], 'outline': props(show=L(False))}
    c = vco(tmeasure=measure, header=False, pad=(0, 0, 0, 0), wrap=wrap, tsize=size, tcolor=color, tooltip=False, align=align)
    c['title'][0]['properties']['fontFamily'] = L(font)
    c['title'][0]['properties']['bold'] = L(bool(bold))
    if color_measure:
        c['title'][0]['properties']['fontColor'] = mcol(color_measure)
    return p.add(name, 'shape', x, y, w, h, objects=objs, vco_=c, hidden=hidden)


def resimg(p, name, x, y, w, h, item, hidden=False):
    objs = {'general': props(imageUrl={'expr': {'ResourcePackageItem': {'PackageName': 'RegisteredResources', 'PackageType': 1, 'ItemName': item}}}),
            'imageScaling': props(imageScalingType=L('Fit'))}
    return p.add(name, 'image', x, y, w, h, objects=objs, vco_=vco(header=False, pad=(0, 0, 0, 0), tooltip=False), hidden=hidden)


def lpage(pg): return props(show=L(True), type=L('PageNavigation'), navigationSection=L(pg))
def lbm(b): return props(show=L(True), type=L('Bookmark'), bookmark=L(b))
def lback(): return props(show=L(True), type=L('Back'))


def tbutton(p, name, x, y, w, h, text, link, fc, hfc=None, size=10, font=FONT_SB, hidden=False, tip=None, align='center'):
    objs = {'icon': [{'properties': {'shapeType': L('blank')}, 'selector': {'id': 'default'}}, {'properties': {'show': L(False)}}],
            'text': [{'properties': {'show': L(True)}},
                     {'properties': {'text': L(text), 'fontColor': col(fc), 'fontSize': D(size), 'fontFamily': L(font),
                                     'horizontalAlignment': L(align), 'verticalAlignment': L('middle')}, 'selector': {'id': 'default'}},
                     {'properties': {'fontColor': col(hfc or fc)}, 'selector': {'id': 'hover'}}],
            'fill': [{'properties': {'show': L(False)}}],
            'outline': [{'properties': {'show': L(False)}}],
            'glow': [{'properties': {'show': L(False)}}],
            'shadow': [{'properties': {'show': L(False)}}]}
    c = vco(header=False, pad=(0, 0, 0, 0), link=link, tooltip=False)
    if tip:
        c['visualLink'][0]['properties']['tooltip'] = L(tip)
    return p.add(name, 'actionButton', x, y, w, h, objects=objs, vco_=c, hidden=hidden)


def _slicer_base(p, name, x, y, w, h, field, group, cols, rows, size, hidden, filt, pad_cell, rx,
                 fill_def, fill_hov, fill_sel, txt_def, txt_sel, font_fam):
    S = lambda i: {'id': i}
    objs = {'layout': props(rowCount=L(rows), columnCount=L(cols), cellPadding=D(pad_cell)),
            'shapeCustomRectangle': [{'properties': {'tileShape': L('rectangleRoundedByPixel'), 'rectangleRoundedCurve': L(rx)}, 'selector': S('default')}],
            'fillCustom': [{'properties': {'show': L(True)}},
                           {'properties': {'fillColor': col(fill_def), 'transparency': D(0)}, 'selector': S('default')},
                           {'properties': {'fillColor': col(fill_hov), 'transparency': D(0)}, 'selector': S('interaction:hover')},
                           {'properties': {'fillColor': col(fill_sel), 'transparency': D(0)}, 'selector': S('selection:selected')}],
            'value': [{'properties': {'show': L(True)}},
                      {'properties': {'fontColor': col(txt_def), 'fontSize': D(size), 'fontFamily': L(font_fam), 'horizontalAlignment': L('center')}, 'selector': S('default')},
                      {'properties': {'fontColor': col(txt_sel), 'fontFamily': L(FONT_SB)}, 'selector': S('selection:selected')}],
            'label': [{'properties': {'show': L(False)}}],
            'outline': [{'properties': {'show': L(False)}}],
            'accentBar': [{'properties': {'show': L(False)}}],
            'shadow': [{'properties': {'show': L(False)}}],
            'glow': [{'properties': {'show': L(False)}}],
            'padding': [{'properties': {'leftMargin': L(3), 'rightMargin': L(3)}, 'selector': S('default')}]}
    v = p.add(name, 'advancedSlicerVisual', x, y, w, h, q=query({'Values': [field]}), objects=objs,
              vco_=vco(header=False, pad=(0, 0, 0, 0)), hidden=hidden)
    v['visual']['syncGroup'] = {'groupName': group, 'fieldChanges': True, 'filterChanges': True}
    if filt:
        e, prop = field.split('.', 1)
        v['filterConfig'] = {'filters': [{'name': f'f_{name[-20:]}', 'field': fcol(e, prop), 'type': 'Categorical',
                                          'filter': {'Version': 2, 'From': [{'Name': 'd', 'Entity': e, 'Type': 0}],
                                                     'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 'd'}}, 'Property': prop}}],
                                                                                      'Values': [[{'Literal': {'Value': "'" + x_ + "'"}}] for x_ in filt]}}}]},
                                          'howCreated': 'User'}]}
    return v


def segmented_chips(p, name, x, y, w, h, field, group, cols, rows=1, size=8.5, hidden=False, filt=None):
    """Inline segmented control inside Silver #BFC0C0 frame: #EAEBED selected fill + #2D3142 bold ink."""
    return _slicer_base(p, name, x, y, w, h, field, group, cols, rows, size, hidden, filt,
                        pad_cell=2, rx=4, fill_def=WHITE, fill_hov=SLATE_50, fill_sel=SURF_MUTED,
                        txt_def=MUTED, txt_sel=INK, font_fam=FONT)


def drawer_chips(p, name, x, y, w, h, field, group, cols, rows=1, size=8.5, hidden=False, filt=None):
    """Multi-select filter pills inside side drawer: Slate-50 default, Blue Slate #4F5D75 selected."""
    return _slicer_base(p, name, x, y, w, h, field, group, cols, rows, size, hidden, filt,
                        pad_cell=4, rx=6, fill_def=SLATE_50, fill_hov=SLATE_100, fill_sel=SLATE,
                        txt_def=BODY, txt_sel=WHITE, font_fam=FONT)


def error_target_tick(ac_measure, py_measure, color=INK):
    """Native Power BI error bar configured as a horizontal PY target tick."""
    return [
        {'properties': {
            'enabled': L(True),
            'barColor': col(color),
            'barWidth': D(10),
            'barBorderSize': L(2),
            'barBorderColor': col(color),
            'markerSize': D(10),
        }, 'selector': {'metadata': f'_Measures.{ac_measure}'}},
        {'properties': {
            'errorRange': {
                'kind': 'ErrorRange',
                'explicit': {
                    'isRelative': L(False),
                    'lowerBound': M(py_measure),
                    'upperBound': M(py_measure),
                }
            }
        }, 'selector': {'data': [{'dataViewWildcard': {'matchingOption': 0}}], 'metadata': f'_Measures.{ac_measure}', 'highlightMatching': 1}},
    ]


ZC = {'combo': ('ZoomChartsFacetChartPaidE77E4ED357DC402ABA005987437CF500', 'v1.12.157.0'),
      'donut': ('ZoomChartsPieChartPaidE77E4ED357DC402ABA005987437CF500', 'v1.12.103.0'),
      'combobar': ('ZoomChartsDrillDownComboBarProE77E4ED357DC402ABA005987437CF800', 'v1.12.156.0'),
      'scatter': ('ZoomChartsScatterChartPaidA2C55E4B59078FDD51C4CD1C4D4E6623V9N8', 'v1.8.312.0')}


def series_colors(cmap, stacked=False):
    pr = {}
    if stacked:
        pr['display'] = L('stacked')
    for i, c in cmap.items():
        pr[f'useDefaults{i}'] = L(False)
        pr[f'fillColor{i}'] = col(c)
    return {'seriesDefault': [{'properties': pr}]}


def measure_fill(measure):
    return {'properties': {'fill': mcol(measure)}, 'selector': {'data': [{'dataViewWildcard': {'matchingOption': 1}}]}}
