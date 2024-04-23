import math

# Käyttöliittymä
DISPLAY_SIZE = (960, 540)
FONT_SIZE = 48
SIDEBAR_MARGIN = 50

# Hiiren painikkeet
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3
MOUSE_WHEEL_SCROLL_UP = 4
MOUSE_WHEEL_SCROLL_DOWN = 5

# Laitumet
PASTURE_RADIUS = 50
HALF_RADIUS = PASTURE_RADIUS / 2
MINIMAL_RADIUS = PASTURE_RADIUS * math.cos(math.radians(30))
PASTURE_BORDER_WIDTH = 4
HIGHLIGHT_OFFSET = 60

# Värit
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PASTURE_COLOR = (163, 178, 3)  # vaalea ruoho
PASTURE_BORDER_COLOR = (90, 110, 2)  # tummempi ruoho
RED_SHEEP_COLOR = (206, 51, 27)
BLUE_SHEEP_COLOR = (7, 83, 141)

# Pelilogiikka
INITIAL_SHEEP = 16
MAX_SHEEP_TO_MOVE = 15
MIN_SHEEP_TO_MOVE = 1

# Algoritmi
ALPHA = float('-Inf')
BETA = float('Inf')
DEPTH = 2