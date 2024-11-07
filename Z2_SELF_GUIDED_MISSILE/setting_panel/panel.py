import pygame
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO
from Z2_SELF_GUIDED_MISSILE.setting_panel.slider import Slider
from Z2_SELF_GUIDED_MISSILE.setting_panel.button import Button


class Panel:
    """
    Represents the control panel for configuring and launching UFOs, with sliders and buttons for input.

    This panel allows the user to adjust UFO properties (altitude, speed, weapon) and launch the UFO.
    It also displays a visual scale for altitude and details of the selected UFO when hovered over.

    Attributes:
        screen_size (tuple): The width and height of the screen.
        max_height (int): The maximum altitude value for the UFO.
        grass_height (int): The height of the ground or grass level.
        sliders (dict): A dictionary of sliders for altitude, speed, and weapon settings.
        buttons (dict): A dictionary of buttons for triggering actions.
        selected_ufo (UFO or None): The UFO currently under the cursor for detail display.
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
        self.selected_ufo = None  # Tracks the UFO currently under the cursor

    def create_UFO(self):
        """
        Creates a UFO instance using the current values of the sliders.

        The UFO is instantiated with the speed, altitude, and other properties
        selected by the user via the control panel sliders.
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
            weapon=self.sliders["weapon"]["model"].get_value()
        )

    def altitude_to_y(self, altitude):
        """
        Converts altitude to a y-coordinate on the screen.

        :param altitude: The altitude value to convert (0 to 10,000 meters).
        :return: The corresponding y-coordinate, scaled between 1 and the grass height.
        """
        altitude = max(0, min(altitude, self.max_height))
        normalized_altitude = altitude / self.max_height
        y_position = max(self.grass_height * (1 - normalized_altitude), 1)
        return round(y_position)

    def create_sliders(self):
        """
        Creates and initializes sliders for altitude, speed, and weapon.

        :return: A dictionary of sliders with their respective models and labels.
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

        :return: A dictionary of buttons with their respective action functions.
        """
        return {
            "send_UFO": Button(self.screen_size[0] + 300, self.screen_size[1] - 150, 150, 25, "GO!", [34, 139, 34],
                               [0, 0, 0],
                               self.create_UFO)
        }

    def draw_scale(self, screen, scale_interval):
        """
        Draws a vertical scale on the screen to represent altitude.

        The scale visually indicates altitude values by drawing horizontal lines at intervals along
        the y-axis and labeling them with the corresponding altitude values.

        :param screen: The Pygame surface to draw the scale on.
        :param scale_interval: The interval at which altitude lines are drawn (in meters).
        """
        pygame.draw.line(screen, (0, 0, 0), (self.screen_size[0], 0), (self.screen_size[0], self.screen_size[1]), 2)

        for i in range(scale_interval, self.max_height - 1, scale_interval):
            pygame.draw.line(screen, (0, 0, 0), (self.screen_size[0] - 10, self.altitude_to_y(i)),
                             (self.screen_size[0] + 10, self.altitude_to_y(i)), 1)
            font = pygame.font.Font(None, 16)
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (self.screen_size[0] + 10, self.altitude_to_y(i) - 25))

    def render(self, screen, ufo_list):
        """
        Renders the control panel, sliders, buttons, scale, and details of the selected UFO.

        It also checks if the mouse is hovering over a UFO and displays its details (altitude, speed, weapon)
        in the panel.

        :param screen: The Pygame surface to render the panel on.
        :param ufo_list: A list of UFO instances to check for hover interaction.
        :return: A dictionary of the current values of the sliders.
        """
        pygame.draw.rect(screen, (150, 150, 150),
                         (self.screen_size[0], 0, self.screen_size[0] * 2, self.screen_size[1]))
        pygame.draw.rect(screen, (70, 70, 70),
                         (self.screen_size[0],self.grass_height+30, self.screen_size[0] * 2, self.screen_size[1]))
        for slider in self.sliders.values():
            model = slider["model"]
            model.render(screen)
            text = slider["text"]
            font = pygame.font.Font(None, 24)

            screen.blit(font.render(
                f'{text["content"][0]} {round(model.get_value())} {text["content"][1] if len(text["content"]) > 1 else ""}',
                True, (250, 250, 250)), text["position"])

        for button in self.buttons.values():
            button.render(screen)

        # Draw the scale
        self.draw_scale(screen, 1000)

        # Check if mouse is over any UFO and update selected UFO details
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for ufo in ufo_list:
            if ufo.x <= mouse_x <= ufo.x + ufo.width and ufo.y <= mouse_y <= ufo.y + ufo.height:
                self.selected_ufo = ufo
                break
        else:
            self.selected_ufo = None

        # Display details of the selected UFO
        if self.selected_ufo:
            font = pygame.font.Font(None, 24)
            details = [
                f"Altitude: {round(self.selected_ufo.altitude)} m",
                f"Speed: {round(self.selected_ufo.speed)} km/h",
                f"Weapon: {"yes" if self.selected_ufo.weapon == 1 else "no"}"
            ]
            image_plane = pygame.image.load('texture/plane.png')
            image_plane = pygame.transform.scale(image_plane, (160, 80))
            screen.blit(image_plane, (self.screen_size[0] + (250 - 160), 225))
            for i, detail in enumerate(details):
                screen.blit(font.render(detail, True, (0, 0, 0)),
                            (self.screen_size[0] + 250, 225 + i * 30))

        return {key: slider["model"].get_value() for key, slider in self.sliders.items()}
