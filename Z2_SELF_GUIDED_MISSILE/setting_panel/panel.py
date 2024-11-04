import pygame
from Z2_SELF_GUIDED_MISSILE.setting_panel.slider import Slider

class Panel:
    def __init__(self, screen_width, screen_height,config):
        self.screen_size = (screen_width, screen_height)
        self.sliders = self.create_sliders(config)

    def create_sliders(self,config):
        # Tworzymy suwaki w określonych pozycjach na ekranie
        position_y = Slider(self.screen_size[0] + 50, self.screen_size[1] - 50, 250, 0, config["height"], 50)

        return [position_y]

    # Funkcja do rysowania i aktualizacji suwaków
    def draw_and_update_sliders(self, screen):
        for slider in self.sliders:
            slider.draw(screen)
            # Obsługa zdarzeń dla każdego suwaka indywidualnie
            for event in pygame.event.get():
                slider.handle_event(event)  # Przekazujemy pojedyncze zdarzenie
        return [slider.get_value() for slider in self.sliders]  # Zwracamy wartości suwaków
