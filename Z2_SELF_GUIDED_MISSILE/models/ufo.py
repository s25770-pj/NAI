from pydantic import BaseModel, confloat, Field, conint
from uuid import UUID, uuid4
from typing import ClassVar


class UFOManager:
    def __init__(self):
        self.UFOs = {}

    def add_instance(self, ufo: 'UFO'):
        self.UFOs[ufo.uuid] = ufo

    def get_instance(self, ufo_uuid: UUID) -> 'UFO':
        return self.UFOs.get(ufo_uuid)

    def get_all(self) -> list['UFO']:
        return list(self.UFOs.values())


class UFO(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    speed: confloat() = None
    max_speed: confloat(gt=0) = None
    altitude: confloat(gt=0) = None
    temperature: confloat(gt=0) = None
    x: confloat(gt=0) = None
    y: confloat(gt=0) = None
    screen_width: conint(ge=0)
    # Class variable to hold all instances
    manager: ClassVar[UFOManager] = UFOManager()

    def __init__(self, **data):
        super().__init__(**data)
        # Append each created instance to the _instances list
        UFO.manager.add_instance(self)
    def move(self):
        self.x -= (self.speed * 0.0027778)
        if self.x < 0:
            del UFO.manager.UFOs[self.uuid]
    def move_y(self,position_y):
        self.y=position_y
    @classmethod
    def all(cls):
        return cls.manager.get_all()
