# import noise
import pygame

class Terrain:
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
    def __init__(self,screen_width,config):
        self.screen_width = screen_width
        self.color_sky = config["COLORS"]['SKY']
        self.color_grass = config["COLORS"]['GRASS']
        self.grass_height = config["GRASS"]["height"]
        self.grass_pos_y = config["GRASS"]["y"]

    def render(self,screen):
        # Draw the sky and ground colors
        screen.fill(self.color_sky)
        pygame.draw.rect(screen, self.color_grass, (0, self.grass_height, self.screen_width, self.grass_pos_y))  # Ground

        # Draw mountains
        # pygame.draw.polygon(screen, BROWN, [(0, screen_height)] + points + [(screen_width, screen_height)])