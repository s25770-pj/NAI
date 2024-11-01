from pydantic import BaseModel, conint, field_validator, Field
from uuid import UUID, uuid4
from Z2_SELF_GUIDED_MISSILE.models.missile import Missile
from typing import List, Any
import asyncio
import pygame

from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO


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

    @property
    def loaded_missiles(self) -> List[Missile]:
        return [missile for missile in self.missiles if not missile.is_launched]

    @property
    def launched_missiles(self) -> List[Missile]:
        return [missile for missile in self.missiles if missile.is_launched]

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

    def scan(self) -> List[List[float | complex | Any]]:
        """
        Search objects in range on the field
        :return: Lists of pairs of UFO objects and distances from launcher
        """
        # TODO: zrobić rozróżnienie na przyjazne i nieprzyjazne - poza tematyką zadania
        UFOs = UFO.get_deployed()
        list_of_ufo = []

        for ufo in UFOs:
            distance = ((ufo.x-self.x)**2+(ufo.y-self.y)**2)**(1/2)

            if distance <= max(self.missiles, key=lambda m: m.radius).radius:
                list_of_ufo.append([ufo, distance])
        return list_of_ufo

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
            raise ValueError(f"Cannot have more than {values.data['missiles_limit']} missiles.")
        return missiles