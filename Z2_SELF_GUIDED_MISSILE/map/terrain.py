# import noise
import pygame


class Terrain:
    """
    Represents the terrain in a game environment, including the sky, grass, and other potential elements like mountains.

    Attributes:
        screen_width (int): The width of the game screen in pixels.
        color_sky (tuple): The RGB color value for the sky.
        color_grass (tuple): The RGB color value for the grass.
        grass_height (int): The height of the grass area in pixels.
        grass_pos_y (int): The Y-coordinate of the grass area on the screen.
    """

    def __init__(self, screen_width, config):
        """
        Initializes the Terrain object with screen dimensions and configuration settings.

        :param screen_width: The width of the screen in pixels.
        :param config: A dictionary containing configuration for colors and grass properties.
        """
        self.screen_width = screen_width
        self.color_sky = config["COLORS"]['SKY']
        self.color_grass = config["COLORS"]['GRASS']
        self.grass_height = config["GRASS"]["height"]
        self.grass_pos_y = config["GRASS"]["y"]

    def render(self, screen):
        """
        Renders the terrain on the screen, including the sky and grass.

        :param screen: The pygame screen object where the terrain will be drawn.
        """
        # Draw the sky and grass
        screen.fill(self.color_sky)
        pygame.draw.rect(
            screen,
            self.color_grass,
            (0, self.grass_height, self.screen_width, self.grass_pos_y)
        )
