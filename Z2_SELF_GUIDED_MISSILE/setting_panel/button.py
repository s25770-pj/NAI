import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.action = action

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Lewy przycisk myszy
                if self.is_clicked(event.pos) and self.action:
                    self.action()
                else:
                    print(f"{self.text} was clicked!")
