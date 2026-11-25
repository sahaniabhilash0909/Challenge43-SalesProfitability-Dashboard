"""Patch _Measures.tmdl to the Slate-Coral Editorial Boardroom Analytics palette.
Run with Power BI Desktop closed."""
import re, sys, uuid

F = sys.argv[1]
s = open(F, encoding='utf-8', newline='').read()


def sub_measure(name, replacement_line):
    global s
    pat = re.compile(rf"(\tmeasure '{re.escape(name)}' = [^\r\n]+)")
    s_new, n = pat.subn(f"\tmeasure '{name}' = {replacement_line}", s)
    assert n == 1, f"Expected 1 match for {name}, got {n}"
    s = s_new


# Multi-line measure replacements
s_new, n = re.subn(
    r"(measure 'Colour Margin' =\r?\n\s*VAR m = \[Contribution Margin %\]\r?\n\s*RETURN )[^\r\n]+",
    r'\1SWITCH ( TRUE (), ISBLANK ( m ), BLANK (), m < 0, "#EF8354", m < 0.10, "#F4A37F", m < 0.25, "#7B89A0", "#4F5D75" )',
    s,
)
assert n == 1, f"Colour Margin match count={n}"
s = s_new

s_new, n = re.subn(
    r"(measure 'Colour TT Margin' =\r?\n\s*VAR m = \[Contribution Margin %\]\r?\n\s*RETURN )[^\r\n]+",
    r'\1SWITCH ( TRUE (), m < 0, "#EF8354", m < 0.10, "#F4A37F", "#4F5D75" )',
    s,
)
assert n == 1, f"Colour TT Margin match count={n}"
s = s_new

s_new, n = re.subn(
    r"(measure 'Colour Margin Font' =\r?\n\s*VAR m = \[Contribution Margin %\]\r?\n\s*RETURN )[^\r\n]+",
    r'\1IF ( NOT ISBLANK ( m ) && ( m < 0 || m >= 0.25 ), "#FFFFFF", "#2D3142" )',
    s,
)
assert n == 1, f"Colour Margin Font match count={n}"
s = s_new

s_new, n = re.subn(
    r"(measure 'Colour Scatter AC' =[\s\S]*?RETURN )[^\r\n]+",
    r'\1IF ( s = acS, "#4F5D75", "#BFC0C0" )',
    s,
)
assert n == 1, f"Colour Scatter AC match count={n}"
s = s_new

# Single-line graphic measures
sub_measure('Colour Contribution', 'IF ( [Contribution Profit] < 0, "#EF8354", "#2D3142" )')
sub_measure(
    'Colour Bridge Step',
    'SWITCH ( SELECTEDVALUE ( \'Profit Steps\'[Step Type] ), "Total", IF ( [Profit Step Value] < 0, "#EF8354", "#4F5D75" ), "Revenue leak", "#EF8354", "Product cost", "#7B89A0", "#B5BECC" )',
)
sub_measure('Colour Δ Net Sales', 'VAR d = [Net Sales ΔPY] RETURN IF ( ISBLANK ( d ), "#B5BECC", IF ( d >= 0, "#4F5D75", "#EF8354" ) )')
sub_measure('Colour Δ Contribution', 'VAR d = [Contribution ΔPY] RETURN IF ( ISBLANK ( d ), "#B5BECC", IF ( d >= 0, "#4F5D75", "#EF8354" ) )')
sub_measure('Colour Δ Margin', 'VAR d = [Margin ΔPY pp] RETURN IF ( ISBLANK ( d ), "#B5BECC", IF ( d >= 0, "#4F5D75", "#EF8354" ) )')
sub_measure('Colour Δ Return', 'VAR d = [Return ΔPY pp] RETURN IF ( ISBLANK ( d ), "#B5BECC", IF ( d <= 0, "#4F5D75", "#EF8354" ) )')
sub_measure('Colour Loss Value', 'IF ( [Contribution AC] < 0, "#EF8354", "#2D3142" )')
sub_measure('Colour Bar AC Neg', 'IF ( [Contribution AC] < 0, "#EF8354", "#4F5D75" )')
sub_measure('Colour Margin AC Bar', 'IF ( [Margin AC] < 0, "#EF8354", "#B5BECC" )')
sub_measure('Colour PL Δ', 'IF ( [PL ΔPY k] >= 0, "#4F5D75", "#EF8354" )')
sub_measure('Colour Spark', 'VAR s = SELECTEDVALUE ( \'Spark Season\'[Season] ) RETURN SWITCH ( TRUE (), s = [AC Season], "#4F5D75", s = [PY Season], "#8B909E", "#CFD5DF" )')
sub_measure('Colour Bridge Δ', 'IF ( [Bridge Impact k] >= 0, "#4F5D75", "#EF8354" )')

# Small adverse text measures (AA #BA4B1D, favorable #4F5D75, neutral #8B909E, primary #2D3142)
sub_measure('Colour Neg Font', 'IF ( [Contribution Margin %] < 0, "#BA4B1D", "#2D3142" )')
sub_measure('Colour Neg Font AC', 'IF ( [Margin AC] < 0, "#BA4B1D", "#2D3142" )')
sub_measure('Colour Δ Net Sales Font', 'VAR d = [Net Sales ΔPY%] RETURN IF ( ISBLANK ( d ), "#8B909E", IF ( d >= 0, "#4F5D75", "#BA4B1D" ) )')


def patch_kpi_col(m):
    txt = m.group(0)
    for old, new in [('"#908C99"', '"#8B909E"'), ('"#6E5FA6"', '"#4F5D75"'), ('"#B23A3A"', '"#BA4B1D"'), ('"#BE4444"', '"#BA4B1D"')]:
        txt = txt.replace(old, new)
    return txt


s, n_kcol = re.subn(r"\tmeasure 'KPI [^']+ Col' = [^\r\n]+", patch_kpi_col, s)
print(f"Patched KPI * Col measures: {n_kcol}")


def patch_kpi_bar(m):
    txt = m.group(0)
    for old, new in [('"#2E2938"', '"#7B89A0"'), ('"#6E5FA6"', '"#4F5D75"'), ('"#BE4444"', '"#EF8354"')]:
        txt = txt.replace(old, new)
    return txt


s, n_kbar = re.subn(r"\tmeasure 'KPI Bar [^']+' = [^\r\n]+", patch_kpi_bar, s)
print(f"Patched KPI Bar * measures: {n_kbar}")

# Heatmaps
sub_measure(
    'Heat Margin Col',
    'VAR m = [Margin AC] RETURN SWITCH ( TRUE (), ISBLANK ( m ), "#FFFFFF", m < 0, "#FAD3C1", m < 0.1, "#F3F5F8", m < 0.2, "#E2E6EC", m < 0.3, "#B5BECC", "#4F5D75" )',
)
sub_measure(
    'Heat Margin Font',
    'VAR m = [Margin AC] RETURN SWITCH ( TRUE (), ISBLANK ( m ), "#2D3142", m < 0, "#9E3E16", m >= 0.3, "#FFFFFF", "#2D3142" )',
)
sub_measure(
    'Heat Return Col',
    'VAR m = [Return AC] RETURN SWITCH ( TRUE (), ISBLANK ( m ), "#FFFFFF", m < 0.06, "#F3F5F8", m < 0.1, "#E2E6EC", m < 0.15, "#B5BECC", "#FAD3C1" )',
)
sub_measure('Heat Return Font', 'IF ( [Return AC] >= 0.15, "#9E3E16", "#2D3142" )')


# Add missing KPI Bar Discount and KPI Bar AOV
def make_meas(name, expr, folder):
    return "\r\n".join([f"\tmeasure '{name}' = {expr}", f"\t\tdisplayFolder: {folder}", f"\t\tlineageTag: {uuid.uuid4()}", ""]) + "\r\n"


add_blocks = []
if "measure 'KPI Bar Discount'" not in s:
    add_blocks.append(make_meas(
        'KPI Bar Discount',
        'VAR a = [Discount AC] VAR p = [Discount PY] RETURN IF ( ISBLANK ( a ) || ISBLANK ( p ) || a = p, "#7B89A0", IF ( a < p, "#4F5D75", "#EF8354" ) )',
        '15 Redesign\\Story\\KPI V6',
    ))
if "measure 'KPI Bar AOV'" not in s:
    add_blocks.append(make_meas(
        'KPI Bar AOV',
        'VAR a = [AOV AC] VAR p = [AOV PY] RETURN IF ( ISBLANK ( a ) || ISBLANK ( p ) || a = p, "#7B89A0", IF ( a > p, "#4F5D75", "#EF8354" ) )',
        '15 Redesign\\Story\\KPI V6',
    ))

if add_blocks:
    anchor = '\tcolumn x\r\n'
    idx = s.index(anchor)
    s = s[:idx] + ''.join(add_blocks) + s[idx:]

open(F, 'w', encoding='utf-8', newline='').write(s)

all_hex = sorted(set(re.findall(r"#[0-9A-Fa-f]{6}\b", s)))
print("Remaining distinct hex codes in _Measures.tmdl:", all_hex)
