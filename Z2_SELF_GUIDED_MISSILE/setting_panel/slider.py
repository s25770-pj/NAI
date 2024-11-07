import pygame


class Slider:
    """
    A class representing a slider widget for selecting a value in a specified range.

    Attributes:
        rect (pygame.Rect): The rectangle defining the slider's position and size.
        knob_radius (int): The radius of the knob (the draggable part of the slider).
        knob_x (float): The current x-coordinate of the knob.
        min_val (float): The minimum value of the slider.
        max_val (float): The maximum value of the slider.
        dragging (bool): Whether the user is currently dragging the knob.

    Methods:
        render(screen): Renders the slider and its knob onto the given screen.
        handle_event(event): Handles mouse events such as click and drag to adjust the knob's position.
        get_value(): Returns the value corresponding to the current knob position.
    """

    def __init__(self, x, y, width, min_val, max_val, initial_val):
        """
        Initializes a new Slider object.

        Args:
            x (int): The x-coordinate of the slider's starting position.
            y (int): The y-coordinate of the slider's starting position.
            width (int): The width of the slider.
            min_val (float): The minimum value the slider can represent.
            max_val (float): The maximum value the slider can represent.
            initial_val (float): The initial value of the slider (where the knob starts).
        """
        self.rect = pygame.Rect(x, y, width, 10)  # Creates the slider's rectangle area
        self.knob_radius = 10  # Knob radius
        self.knob_x = x + (initial_val - min_val) / (max_val - min_val) * width  # Knob initial x position
        self.min_val = min_val  # Minimum value of the slider
        self.max_val = max_val  # Maximum value of the slider
        self.dragging = False  # State of the dragging action

    def render(self, screen):
        """
        Renders the slider and the knob onto the given screen.

        Args:
            screen (pygame.Surface): The screen surface to render the slider on.
        """
        # Draw the slider's background (rectangular part)
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        # Draw the knob (circular part)
        pygame.draw.circle(screen, (100, 100, 100), (int(self.knob_x), self.rect.y + self.rect.height // 2),
                           self.knob_radius)

    def handle_event(self, event):
        """
        Handles mouse events to enable dragging of the knob on the slider.

        Args:
            event (pygame.event.Event): The pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                # Check if the click was on the knob
                if (self.knob_x - self.knob_radius <= mouse_x <= self.knob_x + self.knob_radius and
                        self.rect.y - self.knob_radius <= mouse_y <= self.rect.y + self.knob_radius):
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Update the knob's position based on mouse movement
                mouse_x, _ = event.pos
                self.knob_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width))

    def get_value(self):
        """
        Returns the current value of the slider based on the knob's position.

        Returns:
            float: The value corresponding to the current knob position.
        """
        # Calculate the relative position of the knob on the slider
        relative_x = (self.knob_x - self.rect.x) / self.rect.width
        return self.min_val + relative_x * (self.max_val - self.min_val)
