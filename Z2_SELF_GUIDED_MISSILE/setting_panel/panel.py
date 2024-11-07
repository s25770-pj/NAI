import pygame
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO
from Z2_SELF_GUIDED_MISSILE.setting_panel.slider import Slider
from Z2_SELF_GUIDED_MISSILE.setting_panel.button import Button


class Panel:
    def __init__(self, screen_width, screen_height, config):
        self.screen_size = (screen_width, screen_height)
        self.max_height = 10_000
        self.grass_height = int(config)
        self.sliders = self.create_sliders()
        self.buttons = self.create_buttons()

    def create_UFO(self):
        # Pobieranie wysokości z suwaka
        altitude = self.sliders["altitude"]["model"].get_value()
        y_position = self.altitude_to_y(altitude)

        UFO(
            speed=self.sliders["speed"]["model"].get_value(),
            max_speed=600,
            altitude=altitude,
            temperature=self.sliders["temperature"]["model"].get_value(),
            x=self.screen_size[0] + 25,
            y=y_position-20,
            screen_width=self.screen_size[0],
            width = 80, height = 40
        )
        print("Fly with altitude:", altitude, "and y-position:", y_position)

    def altitude_to_y(self, altitude):
        altitude = max(0, min(altitude, self.max_height))
        normalized_altitude = altitude / self.max_height
        y_position = max((self.grass_height) * (1 - normalized_altitude), 1)
        return round(y_position)

    def create_sliders(self):
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
            "temperature": {
                "model": Slider(self.screen_size[0] + 50, self.screen_size[1] - 150, 200, -50, 50, -10),
                "text": {
                    "content": ["Temperature: ", "C"],
                    "position": (self.screen_size[0] + 300, self.screen_size[1] - 150)
                }
            }
        }

    def create_buttons(self):
        return {
            "send_UFO": Button(self.screen_size[0] + 200, 25, 200, 50, "Send me", [200, 200, 200], [0, 0, 0],
                               self.create_UFO)
        }
    def draw_scale(self,screen,scale_interval):
        pygame.draw.line(screen, (0, 0, 0), (self.screen_size[0], 0), (self.screen_size[0],self.screen_size[1]), 2)

        for i in range(scale_interval, self.max_height-1, scale_interval):
            pygame.draw.line(screen, (0, 0, 0), (self.screen_size[0]-10,self.altitude_to_y(i)), (self.screen_size[0]+10, self.altitude_to_y(i)), 1)
            font = pygame.font.Font(None, 16)
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (self.screen_size[0]+10, self.altitude_to_y(i)-25))

    def render(self, screen):

        for slider in self.sliders.values():
            model = slider["model"]
            model.render(screen)
            text = slider["text"]
            font = pygame.font.Font(None, 24)
            screen.blit(font.render(
                f'{text["content"][0]} {round(model.get_value())} {text["content"][1] if len(text["content"]) > 1 else ""}',
                True, (0, 0, 0)), text["position"])
        for button in self.buttons.values():
            button.render(screen)
        self.draw_scale(screen,1000)
        return {key: slider["model"].get_value() for key, slider in self.sliders.items()}
