import math

BOARD_HEIGHT = 4
BOARD_WIDTH = 8
DEPTH = 2
SIMULATED_PLAYER_DEPTH = 2

# Käyttöliittymä
DISPLAY_SIZE = (960, 540)
BOARD_FONT_SIZE = 48
SIDEBAR_MARGIN = 30
SIDEBAR_DIVIDER = 50
SIDEBAR_FONT_SIZE = 36

# Hiiren painikkeet
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3
MOUSE_WHEEL_SCROLL_UP = 4
MOUSE_WHEEL_SCROLL_DOWN = 5

# Laitumet
INITIAL_POSITION = (50, 50)
PASTURE_RADIUS = 50
HALF_RADIUS = PASTURE_RADIUS / 2
MINIMAL_RADIUS = PASTURE_RADIUS * math.cos(math.radians(30))
PASTURE_BORDER_WIDTH = 4
HIGHLIGHT_OFFSET = 60

# Kuusikulmioruudukon suuntavektorit
DIRECTION_VECTORS = [
    (0, -2 * MINIMAL_RADIUS),  # "Pohjoinen"
    (0, 2 * MINIMAL_RADIUS),  # "Etelä"
    (math.sqrt(3) * MINIMAL_RADIUS, - MINIMAL_RADIUS),  # "Koillinen"
    (-(math.sqrt(3) * MINIMAL_RADIUS), - MINIMAL_RADIUS),  # "Luode"
    (math.sqrt(3) * MINIMAL_RADIUS, MINIMAL_RADIUS),  # "Kaakko"
    (-(math.sqrt(3) * MINIMAL_RADIUS), MINIMAL_RADIUS),  # "Lounas"
]

# Värit
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FREE_PASTURE_COLOR = (163, 178, 3)  # vaalea ruoho
PLAYERS_PASTURE_COLOR = (7, 83, 141)  # sininen
COMPUTERS_PASTURE_COLOR = (206, 51, 27)  # punainen
PASTURE_BORDER_COLOR = (90, 110, 2)  # tummempi ruoho

# Pelilogiikka
PLAYER = 0
COMPUTER = 1

# Algoritmi
ALPHA = float('-Inf')
BETA = float('Inf')
