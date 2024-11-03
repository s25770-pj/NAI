import asyncio
import pygame

from pydantic import BaseModel, conint, field_validator, Field
from uuid import UUID, uuid4
from typing import List, Any

from Z2_SELF_GUIDED_MISSILE.fuzzy_logic.threat_level import calculate_threat_level
from Z2_SELF_GUIDED_MISSILE.fuzzy_logic.shot_decision import calculate_shot_rightness
from Z2_SELF_GUIDED_MISSILE.fuzzy_logic.missile_choice import calculate_required_missile
from Z2_SELF_GUIDED_MISSILE.models.missile import Missile
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO


class Launcher(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    missiles_limit: conint(ge=0, le=100)
    missiles: List[Missile] = []
    default_reload_time: conint(ge=0)
    x: conint(ge=0)
    y: conint(ge=0)

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

    def get_missile_by_fuzzy_value(self, fuzzy_value: float) -> Missile:
        type = ''
        if fuzzy_value < 1:
            type = 'short'
        elif fuzzy_value < 2:
            type = 'medium'
        elif fuzzy_value < 3:
            type = 'long'
        print('self.missiles:', self.missiles)
        print(f'missile_type: {self.missiles[0].type}')
        print(f'type: {type}')
        print(f'fuzzy_value: {fuzzy_value}')
        print(f'missile list: {[missile for missile in self.missiles if missile.type == type]}')
        return [missile for missile in self.missiles if missile.type == type][0]

    def _add_missile(self, missile: Missile):
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
        def _calc_distance(x1, x2, y1, y2):
            return ((x2-x1)**2+(y2-y1)**2)**(1/2)

        # TODO: zrobić rozróżnienie na przyjazne i nieprzyjazne - poza tematyką zadania
        UFOs = UFO.all()
        detected_ufo_in_range = []

        for ufo in UFOs:
            ufo_speed = ufo.speed
            ufo_altitude = ufo.altitude
            # TODO: Można zrobić oddzielny model od ostrzeżeń, które będą później wyświetlane
            distance = _calc_distance(ufo.x, self.x, ufo.y, self.y)
            # TODO: Dodać sprawdzanie czy uzbrojony i customowe czy sie rusza
            threat_level = calculate_threat_level(
                motion=1,
                weapon=1,
                distance=distance*10
            )
            # TODO: Można się zastanowić nad dodaniem własnego obliczania prędkości
            shot_rightness = calculate_shot_rightness(
                threat_level_input=threat_level,
                speed_input=ufo_speed,
                altitude_input=ufo_altitude
            )
            if distance * 10 <= max(self.missiles, key=lambda m: m.radius).radius:
                detected_ufo_in_range.append([ufo, distance * 10])
            if shot_rightness > 0.5:
                required_missile = calculate_required_missile(
                    distance_input=distance,
                    speed_input=ufo_speed,
                    altitude_input=ufo_altitude
                )
                required_missile = self.get_missile_by_fuzzy_value(required_missile)
                print(f'Launcher: {self.uuid} detected UFO, details: {ufo.uuid} |'
                      f' Decision - threat_level: {round(threat_level, 2)}%,'
                      f' shot_rightness: {round(shot_rightness, 2)*100}%,'
                      f' required_missile: {required_missile.serial_number},')
        return detected_ufo_in_range


    async def reload_missile(self, missile: Missile):
        """
        Reloads missile, depends on reload time
        :param missile: missile object
        :return:
        """
        await asyncio.sleep(self.reload_time)
        self._add_missile(missile)

    def draw(self, screen, color, screen_width, screen_height):
        """
        Draws object
        :param screen: screen object
        :param color: object color
        :param screen_width:
        :param screen_height:
        :return:
        """
        pygame.draw.rect(screen, color, (screen_width // 2 - 10, screen_height - 50, 20, 10))

    # validation
    @field_validator('missiles')
    @classmethod
    def validate_missile_count(cls, missiles, values):
        if missiles and len(missiles) > values.data['missiles_limit']:
            raise ValueError(f"Cannot have more than {values.data['missiles_limit']} missiles.")
        return missiles