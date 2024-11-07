import pygame


class Button:
    """
    Represents a clickable button in a Pygame interface.

    Attributes:
        rect (pygame.Rect): The rectangle defining the button's position and size.
        color (tuple): RGB color of the button background.
        text_color (tuple): RGB color of the button's text.
        text (str): Text displayed on the button.
        font (pygame.font.Font): Font used to render the button text.
        action (callable): Optional function to execute when the button is clicked.
    """

    def __init__(self, x, y, width, height, text, color, text_color, action=None):
        """
        Initializes a Button instance with specified properties.

        :param x: The X-coordinate of the button's top-left corner.
        :param y: The Y-coordinate of the button's top-left corner.
        :param width: The width of the button.
        :param height: The height of the button.
        :param text: Text displayed on the button.
        :param color: RGB color tuple for the button background.
        :param text_color: RGB color tuple for the button text.
        :param action: Optional function to execute when the button is clicked.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.action = action

    def render(self, screen):
        """
        Draws the button on the given Pygame screen.

        :param screen: The Pygame screen where the button will be displayed.
        """
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """
        Checks if the button was clicked based on the given mouse position.

        :param pos: Tuple of (x, y) coordinates for the mouse position.
        :return: True if the button was clicked, otherwise False.
        """
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        """
        Handles a Pygame event for button interaction.

        If the button is clicked with the left mouse button, and an action
        is assigned, the action is executed.

        :param event: Pygame event object to be handled.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_clicked(event.pos) and self.action:
                    self.action()
