import pygame
from pydantic import BaseModel, confloat, conint, Field
from uuid import UUID, uuid4
from typing import Literal


class Missile(BaseModel):
    """
    Represents a missile in the game with attributes for physical properties, type, and status.

    Attributes:
        serial_number (UUID): A unique identifier for the missile.
        strength (float): The destructive power of the missile, must be greater than 0.
        radius (float): The radius of the missile's visual representation, must be greater than 0.
        max_speed (int): The maximum speed of the missile, must be greater than 0.
        acceleration (int): The acceleration of the missile, must be greater than 0.
        type (str): The type of missile, one of 'short', 'medium', or 'long'.
        x (int): The X-coordinate of the missile's position on the screen.
        y (int): The Y-coordinate of the missile's position on the screen.
        is_launched (bool): Whether the missile has been launched, default is False.
    """

    serial_number: UUID = Field(default_factory=uuid4)
    strength: confloat(gt=0)
    radius: confloat(gt=0)
    max_speed: conint(gt=0)
    acceleration: conint(gt=0)
    type: Literal['short', 'medium', 'long']
    x: conint(ge=0)
    y: conint(ge=0)
    is_launched: bool = False

    @property
    def speed(self):
        """
        Returns the missile's speed.

        :return: The missile's speed as a negative value indicating upward movement.
        """
        return -self.max_speed

    def is_out_of_map(self, screen_height, screen_width):
        """
        Checks whether the missile is outside the bounds of the screen.

        :param screen_height: The height of the screen in pixels.
        :param screen_width: The width of the screen in pixels.
        :return: True if the missile is out of bounds, otherwise False.
        """
        return (self.y < 0) or (self.y > screen_height) or (self.x < 0) or (self.x > screen_width)

    def launch(self):
        """
        Marks the missile as launched.
        """
        self.is_launched = True

    def move(self):
        """
        Updates the missile's position if it has been launched. The movement is determined by the missile's speed.
        """
        if self.is_launched:
            self.y += self.speed

    def draw(self, screen, color):
        """
        Draws the missile on the screen.

        :param screen: The pygame surface where the missile will be drawn.
        :param color: The color of the missile as an RGB tuple.
        """
        pygame.draw.circle(screen, color, (self.x, int(self.y)), self.radius)
