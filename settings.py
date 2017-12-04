# game options/settings
TITLE = "Jumping coney"
WIDTH =  900# 480
HEIGHT = 700 #600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "hightscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
BG_IMAGE = "bg_layer1.png"
# ICON = "icon_lifes.png"
ICON = "icon.png"

# define colors
# find more color code : http://www.0to255.com/
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# Player properties
PLAYER_ACC = 0.85
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 22

# starting platforms
# PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
# 				 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
# 				 (125, HEIGHT - 350, 100, 20),
# 				 (350, 200, 100, 20),
# 				 (175, 100, 50, 20)]

# starting platforms
# PLATFORM_LIST = [(0, HEIGHT - 60),
# 				 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
# 				 (125, HEIGHT - 350),
# 				 (350, 200),
# 				 (175, 100)]

PLATFORM_LIST = [(0, HEIGHT - 45),
				 (WIDTH / 3, 550),
				 (WIDTH - 300, 450), 
				 (110, HEIGHT - 270),
				 (220, 250),
				 (610, 125),
				 (750, 75),
				 (50, 50), 
				 (WIDTH - 450, 20)]


# game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7 + 10 # PCT = pacentage
SPIKE_SPAWN_PCT = 50
GRASS_SPAWN_PCT = 50
CACTUS_SPAWN_PCT = 50
MOB_RREQ = 5000

# layer properties
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0
ENIMES_LAYER = 2
GRASS_LAYER = 2



# score properties
GOLD_POINTS = 100
SILVER_POINTS = 50
BRONZE_POINTS = 25

LOST_POINTS_BY_HIT_CACTUS = 1
LOST_POINTS_BY_HIT_GRASS = 1
LOST_POINTS_BY_HIT_SPIKEMAN = 2
LOST_POINTS_BY_HIT_WINGMAN = 20