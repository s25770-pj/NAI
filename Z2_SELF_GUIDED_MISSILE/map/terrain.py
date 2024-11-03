# import noise
import pygame
from Z2_SELF_GUIDED_MISSILE.config import Settings


# TODO: Napisać nowe generowanie terenu
#  zmienne przeniesione do configu
# Generate mountain terrain points
# def generate_terrain(screen_width):
#     terrain_points = []
#     for x in range(screen_width):
#         # Generate a y value using Perlin noise
#         y = int(terrain_height / 2 + noise.pnoise1(x * scale, octaves=octaves) * mountain_height)
#         terrain_points.append((x, y))
#     return terrain_points

# Draw the terrain on screen
def draw_terrain(screen, screen_width, screen_height):
    # Draw the sky and ground colors
    screen.fill((Settings().map_settings.colors['sky']))  # Light blue sky
    pygame.draw.rect(screen, Settings().map_settings.colors['grass'], (0, screen_height // 2, screen_width, screen_height // 2))  # Ground

    # Draw mountains
    # pygame.draw.polygon(screen, BROWN, [(0, screen_height)] + points + [(screen_width, screen_height)])