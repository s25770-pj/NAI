# import noise
import pygame


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
def draw_terrain(screen, screen_width, screen_height, config):
    # Draw the sky and ground colors
    # background_image = pygame.image.load('texture/sky.jpg')
    # background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    screen.fill((config["COLORS"]['SKY']))
    # screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, config["COLORS"]['GRASS'],
                     (0, config["GRASS"]["height"], screen_width, config["GRASS"]["y"]))  # Ground

    # Draw mountains
    # pygame.draw.polygon(screen, BROWN, [(0, screen_height)] + points + [(screen_width, screen_height)])
