import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, 10)
        self.knob_radius = 10
        self.knob_x = x + (initial_val - min_val) / (max_val - min_val) * width
        self.min_val = min_val
        self.max_val = max_val
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.circle(screen, (0, 0, 255), (int(self.knob_x), self.rect.y + self.rect.height // 2), self.knob_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                if (self.knob_x - self.knob_radius <= mouse_x <= self.knob_x + self.knob_radius and
                        self.rect.y - self.knob_radius <= mouse_y <= self.rect.y + self.knob_radius):
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, _ = event.pos
                self.knob_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width))

    def get_value(self):
        relative_x = (self.knob_x - self.rect.x) / self.rect.width
        return self.min_val + relative_x * (self.max_val - self.min_val)
