from pydantic import BaseModel, confloat, conint, Field
from uuid import UUID, uuid4
import pygame


class Missile(BaseModel):
    serial_number: UUID = Field(default_factory=uuid4)
    strength: confloat(gt=0)
    radius: confloat(gt=0)
    max_speed: conint(gt=0)
    acceleration: conint(gt=0)
    x: conint(ge=0)
    y: conint(ge=0)
    is_launched: bool = False

    @property
    def speed(self):
        return -self.max_speed

    def launch(self):
        self.is_launched = True

    def move(self):
        if self.is_launched:
            self.y += self.speed

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.x, int(self.y)), self.radius)

    def __repr__(self):
        return f'Missile - serial number: {self.serial_number}, strength: {self.strength}, radius: {self.radius}, max_speed: {self.max_speed}'


