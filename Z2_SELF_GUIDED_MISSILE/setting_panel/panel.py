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
        UFO(speed=100, max_speed=600, altitude=500, temperature=70, x=self.screen_size[0] + 50, y=self.sliders["position_y"].get_value(),
            screen_width=self.screen_size[0])

    def create_sliders(self,config):
        return {"position_y":Slider(self.screen_size[0] + 50, self.screen_size[1] - 50, 250, 0, config["height"], 50)}

    def create_buttons(self,config):
        return {"send_UFO":Button(self.screen_size[0] +  200, 150, 250, 100,"Send me",[200,200,200], [0,0,0],self.create_UFO)}

    def redner(self, screen):
        for slider in self.sliders.values():
            slider.render(screen)
        for button in self.buttons.values():
            button.render(screen)
        return {key: slider.get_value() for key, slider in self.sliders.items()}
