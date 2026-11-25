"""Geometry for the V12 Modern UX Dark-Rail App Shell + Slate-Coral Editorial layout (1920x1080)."""
W, H = 1920, 1080
APP = (16, 14, 1888, 1052)      # App shell bounds (x=16..1904, y=14..1066)
SB_W = 216                        # Dark #2D3142 navigation sidebar width (x=16..232)
WS_X = 232                        # Workspace start x
WS_W = 1904 - WS_X                # 1672px main workspace

X0, X1 = 264, 1876                # Content horizontal bounds
MW = X1 - X0                      # 1612px main width

# Dark Sidebar layout (x=30..218)
SB_X, SB_IW = 30, 188
NAV_H, NAV_STEP = 42, 50
NAV_Y = [124, 174, 224]
SEASON_BOX = (26, 316, 196, 114)
CHANNEL_BOX = (26, 466, 196, 78)
FILTERS_BTN = (30, 580, 188, 38)
RESET_BTN = (30, 628, 188, 38)
INFO_Y = [724, 770]

# Workspace Header + Takeaway Banner
TOP_H = 74                        # y=14..88
MSG = (X0, 102, MW, 42)
BACK_BTN = (1768, 107, 96, 32)
PERIOD_PILL = (1556, 24, 320, 26)

# Horizontal 5-KPI Executive Strip (y=158..294)
KPI_Y, KPI_H, KPI_GAP = 158, 136, 16
KPI_W = (MW - 4 * KPI_GAP) / 5    # 309.6
KPIS = [(round(X0 + i * (KPI_W + KPI_GAP), 2), KPI_Y, round(KPI_W, 2), KPI_H) for i in range(5)]

# Main Analytical Card Grids (y=310..1016 on Ch1/Ch2, y=158..1016 on Ch3/Profile)
CARDS = {
    'ch1': {
        'bridge': (264, 310, 560, 706),
        'month': (840, 310, 508, 344),
        'band': (1364, 310, 512, 344),
        'type': (840, 670, 1036, 346),
    },
    'ch2': {
        'cat': (264, 310, 526, 344),
        'donut': (806, 310, 526, 344),
        'scatter': (1348, 310, 528, 344),
        'heat': (264, 670, 996, 346),
        'chan': (1276, 670, 600, 346),
    },
    'ch3': {
        'callout': (264, 158, 540, 166),
        'upside_bar': (264, 340, 540, 336),
        'limits': (264, 692, 540, 324),
    },
    'profile': {
        'facts': (264, 158, 796, 106),
        'pnl': (264, 280, 796, 736),
        'daily': (1076, 158, 800, 420),
        'band': (1076, 594, 800, 422),
    },
}

ACTION_ROWS = [(820, 158 + i * 218, 1056, 202) for i in range(4)]

FOOT_Y = 1030
DRAWER = dict(panel=dict(x=1408, y=56, w=472, h=984), close=dict(x=1784, y=76, w=76, h=30), divider=130)
TT = dict(w=368, h=236)
