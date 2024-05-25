import pygame

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
MID_GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (211, 211, 211)
RANGE_COLOR = (90, 211, 90)
SAND = (194, 178, 128)

#--- misc
HEALTH_SPAWN = 20
HEALTH_MAX = 200

pygame.font.init()
font = pygame.font.SysFont('Arial', 16)