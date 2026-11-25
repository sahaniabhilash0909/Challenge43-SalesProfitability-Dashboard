"""Geometry for the V11 Slate-Coral Editorial Boardroom Analytics layout (1920x1080)."""
W, H = 1920, 1080
SHEET = (16, 14, 1888, 1052)    # white editorial sheet x=16..1904, y=14..1066
TOP_Y = 80                        # bottom hairline of 66px topbar (y=14..80)
FOOT_Y = 1034                     # footer text y (hairline at 1026)

# Topbar navigation & utility bar (right-aligned)
TABS = {
    'ch1': (946, 192),
    'ch2': (1154, 146),
    'ch3': (1316, 120),
}
TOP_DIV_X = 1456
UTIL = {
    'guide': (1474, 78),
    'limits': (1558, 74),
    'reset': (1642, 104),
    'filters': (1758, 118),
}

# Asymmetric Split Grid (standard pages: 34.5% left rail / 65.5% right canvas)
LX, LW = 44, 624
DIV_X = 696
RX, RW = 724, 1152

# Drill-through profile split (wider left rail for 4-col P&L bar table)
PROF_LW = 788
PROF_DIV_X = 860
PROF_RX, PROF_RW = 888, 988

# Left-rail inline segmented filters (Season + Channel)
SEG_SEASON = (96, 214, 294, 32)
SEG_CHANNEL = (464, 214, 204, 32)

# Left-rail 5 hairline-stacked KPI rows (y=286..1016)
KPI_ROWS = [(LX, 286 + i * 146, LW, 146) for i in range(5)]

# Right-canvas (and Ch3 / Profile) zones
BLK = {
    'ch1': {
        'bridge': (724, 92, 580, 448),
        'month': (1336, 92, 540, 448),
        'band': (724, 568, 520, 448),
        'type': (1276, 568, 600, 448),
    },
    'ch2': {
        'cat': (724, 92, 364, 448),
        'donut': (1112, 92, 364, 448),
        'scatter': (1500, 92, 376, 448),
        'heat': (724, 568, 674, 448),
        'chan': (1430, 568, 446, 448),
    },
    'ch3': {
        'callout': (44, 286, 624, 150),
        'upside_bar': (44, 454, 624, 274),
        'limits': (44, 746, 624, 270),
    },
    'profile': {
        'facts': (44, 198, 788, 92),
        'pnl': (44, 310, 788, 706),
        'daily': (888, 92, 988, 448),
        'band': (888, 568, 988, 448),
    },
}

ACTION_ROWS = [(724, 168 + i * 212, 1152, 204) for i in range(4)]

DRAWER = dict(panel=dict(x=1408, y=56, w=472, h=984), close=dict(x=1784, y=76, w=76, h=30), divider=130)
TT = dict(w=368, h=236)
