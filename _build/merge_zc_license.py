"""Merge the ZoomCharts licence (paid + license) from _build/private/zc_license_theme.json into the report theme.
Run with Power BI Desktop closed:  python3 _build/merge_zc_license.py"""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
lic = json.load(open(os.path.join(here, 'private', 'zc_license_theme.json')))
src = lic['visualStyles']['*']['*']
tp = os.path.join(here, '..', 'Challenge43_SalesProfitability.Report', 'StaticResources', 'RegisteredResources', 'HolidayPnL_C43_Theme.json')
t = json.load(open(tp, encoding='utf-8'))
star = t.setdefault('visualStyles', {}).setdefault('*', {}).setdefault('*', {})
for k in ('paid', 'license'):
    star[k] = src[k]
json.dump(t, open(tp, 'w', encoding='utf-8'), indent=2)
print('ZoomCharts licence merged into', os.path.basename(tp), '| keys under *.*:', sorted(star))
