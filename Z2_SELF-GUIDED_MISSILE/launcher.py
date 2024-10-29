from pydantic import BaseModel, conint, field_validator, Field
from uuid import UUID, uuid4
from missile import Missile
from typing import List
import asyncio
import pygame


class Launcher(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    missiles_limit: conint(ge=0, le=100)
    missiles: List[Missile] = []
    default_reload_time: conint(ge=0)

    @property
    def reload_time(self) -> conint(ge=0):
        """
        Calculated reload time
        :return:
        """
        return self.default_reload_time

    def display_missiles(self):
        """
        Display all missiles on console
        :return:
        """
        for missile in self.missiles:
            print(missile)

    def add_missile(self, missile: Missile):
        """
        Adds missile to launcher.
        :param missile: missile object to add
        :return:
        """
        if len(self.missiles) >= self.missiles_limit:
            raise ValueError(f"Cannot add more missiles. Limit is {self.missiles_limit}.")
        self.missiles.append(missile)

    async def reload_missile(self, missile: Missile):
        """
        Reloads missile, depends on reload time
        :param missile: missile object
        :return:
        """
        await asyncio.sleep(self.reload_time)
        self.add_missile(missile)

    def draw(self, screen, color, screen_width, screen_height):
        pygame.draw.rect(screen, color, (screen_width // 2 - 10, screen_height - 50, 20, 10))

    # validation
    @field_validator('missiles')
    @classmethod
    def validate_missile_count(cls, missiles, values):
        if missiles and len(missiles) > values.data['missiles_limit']:
            raise ValueError("Cannot have more than 10 missiles.")
        return missiles