import pygame

from Z2_SELF_GUIDED_MISSILE.fuzzy_logic.threat_level import weapon
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO
from Z2_SELF_GUIDED_MISSILE.setting_panel.slider import Slider
from Z2_SELF_GUIDED_MISSILE.setting_panel.button import Button


class Panel:
    """
    Represents the control panel for configuring and launching UFOs, with sliders and buttons for input.

    Attributes:
        screen_size (tuple): The width and height of the screen.
        max_height (int): The maximum altitude value for the UFO.
        grass_height (int): The height of the ground or grass level.
        sliders (dict): A dictionary of sliders for adjusting altitude, speed, and temperature.
        buttons (dict): A dictionary of buttons for performing actions.
    """
    def __init__(self, screen_width, screen_height, config):
        """
        Initializes the panel with screen dimensions and configuration.

        :param screen_width: The width of the screen.
        :param screen_height: The height of the screen.
        :param config: Configuration dictionary containing settings like grass height.
        """
        self.screen_size = (screen_width, screen_height)
        self.max_height = 10_000
        self.grass_height = int(config)
        self.sliders = self.create_sliders()
        self.buttons = self.create_buttons()

    def create_UFO(self):
        """
        Creates a UFO instance using the current values of the sliders.
        """
        altitude = self.sliders["altitude"]["model"].get_value()
        y_position = self.altitude_to_y(altitude)

        UFO(
            speed=self.sliders["speed"]["model"].get_value(),
            max_speed=600,
            altitude=altitude,
            temperature=100,
            x=self.screen_size[0] + 25,
            y=y_position - 20,
            screen_width=self.screen_size[0],
            width=80,
            height=40,
            weapon = self.sliders["weapon"]["model"].get_value()
        )
        print("Fly with altitude:", altitude, "and y-position:", y_position)

    def altitude_to_y(self, altitude):
        """
        Converts altitude to a y-coordinate on the screen.

        :param altitude: The altitude value to convert.
        :return: The corresponding y-coordinate.
        """
        altitude = max(0, min(altitude, self.max_height))
        normalized_altitude = altitude / self.max_height
        y_position = max((self.grass_height) * (1 - normalized_altitude), 1)
        return round(y_position)

    def create_sliders(self):
        """
        Creates and initializes sliders for altitude, speed, and temperature.

        :return: A dictionary of slider configurations.
        """
        return {
            "altitude": {
                "model": Slider(self.screen_size[0] + 50, self.screen_size[1] - 100, 200, 50.0, self.max_height, 100),
                "text": {
                    "content": ["Altitude: "],
                    "position": (self.screen_size[0] + 300, self.screen_size[1] - 100)
                }
            },
            "speed": {
                "model": Slider(self.screen_size[0] + 50, self.screen_size[1] - 50, 200, 10, 1500, 10),
                "text": {
                    "content": ["Speed: ", " km/h"],
                    "position": (self.screen_size[0] + 300, self.screen_size[1] - 50)
                }
            },
            "weapon": {
                "model": Slider(self.screen_size[0] + 50, self.screen_size[1] - 150, 20, 0, 1, 1),
                "text": {
                    "content": ["Weapon: "],
                    "position": (self.screen_size[0] + 100, self.screen_size[1] - 150)
                }
            }
        }

    def create_buttons(self):
        """
        Creates and initializes buttons for performing actions.

        :return: A dictionary of button configurations.
        """
        return {
            "send_UFO": Button(self.screen_size[0] + 200, 25, 200, 50, "GO!", [200, 200, 200], [0, 0, 0],
                               self.create_UFO)
        }

    def draw_scale(self, screen, scale_interval):
        """
        Draws a vertical scale on the screen to represent altitude.

        :param screen: The Pygame surface where the scale will be drawn.
        :param scale_interval: The interval between scale markers.
        """
        pygame.draw.line(screen, (0, 0, 0), (self.screen_size[0], 0), (self.screen_size[0], self.screen_size[1]), 2)

        for i in range(scale_interval, self.max_height - 1, scale_interval):
            pygame.draw.line(screen, (0, 0, 0), (self.screen_size[0] - 10, self.altitude_to_y(i)),
                             (self.screen_size[0] + 10, self.altitude_to_y(i)), 1)
            font = pygame.font.Font(None, 16)
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (self.screen_size[0] + 10, self.altitude_to_y(i) - 25))

    def render(self, screen):
        """
        Renders sliders, buttons, and the scale on the screen.

        :param screen: The Pygame surface where elements will be rendered.
        :return: A dictionary of current slider values.
        """
        pygame.draw.rect(screen,(150,150,150), (self.screen_size[0],0,self.screen_size[0]*2,self.screen_size[1]))
        for slider in self.sliders.values():
            model = slider["model"]
            model.render(screen)
            text = slider["text"]
            font = pygame.font.Font(None, 24)
            if slider["model"] == self.sliders["weapon"]["model"]:
                weapon_status = "Yes" if round(model.get_value()) == 1 else "No"
                screen.blit(font.render(
                    f'{text["content"][0]} {weapon_status}',
                    True, (0, 0, 0)), text["position"])
            else:
                screen.blit(font.render(
                    f'{text["content"][0]} {round(model.get_value())} {text["content"][1] if len(text["content"]) > 1 else ""}',
                    True, (0, 0, 0)), text["position"])

        for button in self.buttons.values():
            button.render(screen)
        self.draw_scale(screen, 1000)
        return {key: slider["model"].get_value() for key, slider in self.sliders.items()}
