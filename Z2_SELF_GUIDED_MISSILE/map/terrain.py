import json
# import noise
import pygame

with open('./config.json', 'r') as file:
    config = json.load(file)

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
    screen.fill((config['MAP']['COLORS']['SKY']))  # Light blue sky
    pygame.draw.rect(screen, config['MAP']['COLORS']['GRASS'], (0, screen_height // 2, screen_width, screen_height // 2))  # Ground

    # Draw mountains
    # pygame.draw.polygon(screen, BROWN, [(0, screen_height)] + points + [(screen_width, screen_height)])