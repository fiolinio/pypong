from enum import Enum

PIXEL_SIZE = 25
BARS_GAP = 2
DIMS = (30, 50)
LBL_FONT = ("Small Fonts", 100)
BALL_DELAY = 200
NEW_BALL_DELAY = 500
REFRESH_RATE = 30


class Direction(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3
