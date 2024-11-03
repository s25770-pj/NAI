from pydantic import BaseModel, confloat, conint, Field, constr
from uuid import UUID, uuid4
import pygame
from typing import Literal


class Missile(BaseModel):
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
        return -self.max_speed

    def is_out_of_map(self, screen_height, screen_width):
        """
        Checks if object is out of the map
        :param screen_height:
        :param screen_width:
        :return: bool
        """
        return (self.y < 0) or (self.y > screen_height) or (self.x < 0) or (self.x > screen_width)

    def launch(self):
        """
        Sets a missile as launched
        :return:
        """
        self.is_launched = True

    def move(self):
        """
        makes missile move
        :return:
        """
        if self.is_launched:
            self.y += self.speed

    def draw(self, screen, color):
        """
        Draws a missile
        :param screen:
        :param color:
        :return:
        """
        pygame.draw.circle(screen, color, (self.x, int(self.y)), self.radius)

    def __repr__(self):
        return f'Missile - serial number: {self.serial_number}, strength: {self.strength}, radius: {self.radius}, max_speed: {self.max_speed}'


