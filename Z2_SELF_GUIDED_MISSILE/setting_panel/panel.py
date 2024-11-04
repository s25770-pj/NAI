from tkinter import font

import pygame

from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO
from Z2_SELF_GUIDED_MISSILE.setting_panel.slider import Slider
from Z2_SELF_GUIDED_MISSILE.setting_panel.button import Button

class Panel:
    def __init__(self, screen_width, screen_height,config):
        self.screen_size = (screen_width, screen_height)
        self.sliders = self.create_sliders(config)
        self.buttons = self.create_buttons(config)

    def create_UFO(self):
        UFO(speed=self.sliders["speed"]["model"].get_value(), max_speed=600, altitude=self.sliders["position_y"]["model"].get_value(),
            temperature=self.sliders["temperature"]["model"].get_value(),
            x=self.screen_size[0] + 50, y=self.sliders["position_y"]["model"].get_value(),
            screen_width=self.screen_size[0])

    def create_sliders(self,config):
        return {
            "position_y":{
                "model":Slider(self.screen_size[0] + 50, self.screen_size[1] - 100, 250, 15, config["height"], 15),
                "text": {
                    "content":["position Y: "],
                    "position":(self.screen_size[0] + 350, self.screen_size[1] - 100)

                }
            },
            "speed": {
                "model": Slider(self.screen_size[0] + 50, self.screen_size[1] - 50, 250, 1, 2000, 1),
                "text": {
                    "content": ["Speed: ", " km/h"],
                    "position": (self.screen_size[0] + 350, self.screen_size[1] - 50)

                }
            },
            "temperature": {
                "model": Slider(self.screen_size[0] + 50, self.screen_size[1] - 150, 250, 30, 300, 30),
                "text": {
                    "content": ["temperature: ", "C"],
                    "position": (self.screen_size[0] + 350, self.screen_size[1] - 150)

                }
            }
        }

    def create_buttons(self,config):
        return {"send_UFO":Button(self.screen_size[0] +  200, 150, 250, 100,"Send me",[200,200,200], [0,0,0],self.create_UFO)}

    def redner(self, screen):
        for slider in self.sliders.values():
            model = slider["model"]
            model.render(screen)
            text = slider["text"]
            font = pygame.font.Font(None, 24)
            screen.blit(font.render(f'{text["content"][0]} {round(model.get_value())}', True, (0, 0, 0)), text["position"])
        for button in self.buttons.values():
            button.render(screen)
        return {key: slider["model"].get_value() for key, slider in self.sliders.items()}
