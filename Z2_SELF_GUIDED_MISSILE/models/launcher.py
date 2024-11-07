import asyncio
import math
import pygame
from pydantic import BaseModel, conint, field_validator, Field
from uuid import UUID, uuid4
from typing import List, Any, Optional, Tuple, Dict

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
    height: conint(ge=0)
    width: conint(ge=0)
    color: Tuple[int, int, int]
    range: Dict[str, int]
    max_range: conint(ge=0)
    danger_level: conint() = None
    @property
    def loaded_missiles(self) -> List[Missile]:
        return [missile for missile in self.missiles if not missile.is_launched]

    @property
    def launched_missiles(self) -> List[Missile]:
        return [missile for missile in self.missiles if missile.is_launched]

    def _add_missile(self, missile: Missile):
        # Add a missile to the launcher
        if len(self.missiles) >= self.missiles_limit:
            raise ValueError(f"Cannot add more missiles. Limit is {self.missiles_limit}.")
        self.missiles.append(missile)
    def ufo_in_range(self):
        detected_ufo_in_range = []
        for ufo in UFO.all():
            distance = ((self.x - (ufo.x if self.x < ufo.x + ufo.width // 2 else ufo.x + ufo.width)) ** 2 + (
                        ufo.y + ufo.height // 2 - self.y) ** 2) ** 0.5

            #print(f'{distance} <= {self.max_range}')
            if distance <= self.max_range:
                detected_ufo_in_range.append([ufo, distance])
        return detected_ufo_in_range

    def scan(self):
        scan_ufo = []
        for ufo_model in self.ufo_in_range():
            # Calculate distance
            ufo,distance = ufo_model
            threat_level = calculate_threat_level(motion=1, weapon=1, distance=distance * 10)
            # TODO: Implement a separate model for warnings that will be displayed later
            shot_rightness = calculate_shot_rightness(threat_level_input=threat_level, speed_input=ufo.speed,
                                                   altitude_input=ufo.altitude)
            # TODO: Add check if armed and custom movement check
            required_missile=0
            if shot_rightness > 0.5:
                required_missile = calculate_required_missile(distance_input=distance, speed_input=ufo.speed,
                                                              altitude_input=ufo.altitude)
                required_missile = self.get_missile_by_fuzzy_value(required_missile)
            scan_ufo.append([ufo,threat_level,shot_rightness,required_missile])
        #         print(f'Launcher: {self.uuid} detected UFO, details: {ufo.uuid} |'
        #               f' Decision - threat_level: {round(threat_level, 2)}%,'
        #               f' shot_rightness: {round(shot_rightness, 2) * 100}%,'
        #               f' required_missile: {required_missile.serial_number if required_missile else None}')

            #print(f'shot_rightness: {shot_rightness}')

        return scan_ufo

    def draw_dashed_circle(self, screen, color, center, radius, start_angle, end_angle, dash_length=10):
        """ Rysuje przerywane okręgi na powierzchni. """
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)

        # Obliczamy długość łuku
        arc_length = radius * (end_rad - start_rad)
        num_dashes = int(arc_length / dash_length)

        for i in range(num_dashes):
            # Obliczamy położenie startowe i końcowe segmentów
            dash_start_angle = start_rad + (i / num_dashes) * (end_rad - start_rad)
            dash_end_angle = start_rad + ((i + 0.5) / num_dashes) * (end_rad - start_rad)

            # Obliczamy współrzędne punktów końcowych segmentów
            start_x = center[0] + radius * math.cos(dash_start_angle)
            start_y = center[1] + radius * math.sin(dash_start_angle)
            end_x = center[0] + radius * math.cos(dash_end_angle)
            end_y = center[1] + radius * math.sin(dash_end_angle)

            # Rysujemy segment linii
            pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 2)

    def draw(self, screen):
        """
        Draws the launcher on the screen.
        :param screen: The screen object where the launcher will be drawn.
        """
        deg = 360
        self.draw_dashed_circle(screen, (255, 0, 0), ((self.x), self.y), self.range["SHORT"], 180, deg)
        self.draw_dashed_circle(screen, (200, 200, 0), ((self.x), self.y), self.range["MEDIUM"], 180, deg)
        self.draw_dashed_circle(screen, (0, 255, 0), ((self.x), self.y), self.range["LONG"], 180, deg)
        pygame.draw.rect(screen, self.color, (self.x-self.width//2, self.y-self.height//2, self.width, self.height))

    async def reload_missile(self, missile: Missile):
        """
        Reloads a missile after a certain time period.
        :param missile: The missile object to be reloaded.
        """
        await asyncio.sleep(self.default_reload_time)
        self._add_missile(missile)

    def get_missile_by_fuzzy_value(self, fuzzy_value: float) -> Optional[Missile]:
        missile_type = ''
        if fuzzy_value < 1:
            missile_type = 'short'
        elif fuzzy_value < 2:
            missile_type = 'medium'
        elif fuzzy_value < 3:
            missile_type = 'long'
        matching_missiles = [missile for missile in self.missiles if missile.type == missile_type]

        return matching_missiles[0] if matching_missiles else None

    # Validation
    @field_validator('missiles')
    @classmethod
    def validate_missile_count(cls, missiles, values):
        if missiles and len(missiles) > values.data['missiles_limit']:
            raise ValueError(f"Cannot have more than {values.data['missiles_limit']} missiles.")
        return missiles
