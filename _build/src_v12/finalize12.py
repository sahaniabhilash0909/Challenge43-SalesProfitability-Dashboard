"""Registers V12 backgrounds + sanitized Slate-Coral theme in report.json, removes stale pages.
Note: deliberately omits paid/license keys so the public repo stays secret-free;
run _build/merge_zc_license.py locally before opening in Power BI Desktop."""
import json, os, sys, shutil, glob

ROOT, ASSETS = sys.argv[1], sys.argv[2]
rr = os.path.join(ROOT, 'StaticResources', 'RegisteredResources')
os.makedirs(rr, exist_ok=True)

imgs = []
for src, dst in [('bg_ch1', 'bg_ch1_c43'), ('bg_ch2', 'bg_ch2_c43'), ('bg_ch3', 'bg_ch3_c43'),
                 ('bg_profile', 'bg_profile_c43'), ('bg_tooltip', 'bg_tooltip_c43'), ('overlay_drawer', 'overlay_drawer_c43')]:
    shutil.copy(os.path.join(ASSETS, src + '.png'), os.path.join(rr, dst + '.png'))
    imgs.append(dst + '.png')

theme = {
    "name": "Holiday PnL C43 Slate-Coral",
    "dataColors": [
        "#4F5D75",
        "#8B909E",
        "#7B89A0",
        "#B5BECC",
        "#2D3142",
        "#BFC0C0",
        "#3B465A",
        "#CFD5DF",
        "#EF8354",
        "#F4A37F"
    ],
    "foreground": "#2D3142",
    "foregroundNeutralSecondary": "#646B7D",
    "foregroundNeutralTertiary": "#8B909E",
    "background": "#FFFFFF",
    "backgroundLight": "#F5F6F8",
    "backgroundNeutral": "#F2F3F5",
    "tableAccent": "#4F5D75",
    "good": "#4F5D75",
    "neutral": "#8B909E",
    "bad": "#EF8354",
    "maximum": "#4F5D75",
    "center": "#B5BECC",
    "minimum": "#F3F5F8",
    "textClasses": {
        "callout": {"fontFace": "Consolas", "color": "#2D3142"},
        "title": {"fontFace": "Segoe UI Semibold", "fontSize": 12, "color": "#2D3142"},
        "header": {"fontFace": "Segoe UI Semibold", "fontSize": 10, "color": "#2D3142"},
        "label": {"fontFace": "Segoe UI", "fontSize": 9, "color": "#646B7D"}
    },
    "visualStyles": {
        "*": {
            "*": {
                "background": [{"show": False}],
                "border": [{"show": False}],
                "dropShadow": [{"show": False}],
                "visualTooltip": [{
                    "titleFontColor": "#B5BECC",
                    "valueFontColor": "#FFFFFF",
                    "background": "#2D3142",
                    "fontSize": 9,
                    "transparency": 0,
                    "fontFamily": "Segoe UI"
                }],
                "visualHeader": [{
                    "background": "#FFFFFF",
                    "border": "#FFFFFF",
                    "foreground": "#646B7D",
                    "transparency": 0
                }]
            }
        },
        "page": {
            "*": {
                "background": [{"transparency": 0}],
                "outspace": [{"color": {"solid": {"color": "#F2F3F5"}}}]
            }
        }
    }
}
json.dump(theme, open(os.path.join(rr, 'HolidayPnL_C43_Theme.json'), 'w', encoding='utf-8'), indent=2)

rp = os.path.join(ROOT, 'definition', 'report.json')
r = json.load(open(rp, encoding='utf-8'))
pk = [x for x in r.get('resourcePackages', []) if x['name'] != 'RegisteredResources']
pk.append({
    "name": "RegisteredResources",
    "type": "RegisteredResources",
    "items": [{"name": n, "path": n, "type": "Image"} for n in imgs] + [
        {"name": "HolidayPnL_C43_Theme.json", "path": "HolidayPnL_C43_Theme.json", "type": "CustomTheme"}
    ]
})
r['resourcePackages'] = pk
r['themeCollection']['customTheme'] = {
    "name": "HolidayPnL_C43_Theme.json",
    "reportVersionAtImport": r['themeCollection']['baseTheme']['reportVersionAtImport'],
    "type": "RegisteredResources"
}
r.setdefault('objects', {})['outspacePane'] = [{"properties": {"expanded": {"expr": {"Literal": {"Value": "false"}}}}}]
r['publicCustomVisuals'] = sorted({
    "ZoomChartsDrillDownComboBarProE77E4ED357DC402ABA005987437CF800",
    "ZoomChartsFacetChartPaidE77E4ED357DC402ABA005987437CF500",
    "ZoomChartsPieChartPaidE77E4ED357DC402ABA005987437CF500",
    "ZoomChartsScatterChartPaidA2C55E4B59078FDD51C4CD1C4D4E6623V9N8"
})
json.dump(r, open(rp, 'w', encoding='utf-8'), indent=2)

keep = set(json.load(open(os.path.join(ROOT, 'definition', 'pages', 'pages.json'), encoding='utf-8'))['pageOrder'])
for d in glob.glob(os.path.join(ROOT, 'definition', 'pages', '*')):
    if os.path.isdir(d) and os.path.basename(d) not in keep:
        shutil.rmtree(d)
        print('removed stale page', os.path.basename(d))
print('finalized V12:', imgs)
