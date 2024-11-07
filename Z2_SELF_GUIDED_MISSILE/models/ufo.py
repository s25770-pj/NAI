from pydantic import BaseModel, confloat, Field, conint
from uuid import UUID, uuid4
from typing import ClassVar


class UFOManager:
    """
    A class to manage all UFO instances.

    Attributes:
        UFOs (dict): A dictionary holding all UFO objects with their UUIDs as keys.
    """
    def __init__(self):
        """Initializes an empty manager for UFOs."""
        self.UFOs = {}

    def add_instance(self, ufo: 'UFO'):
        """
        Adds a UFO instance to the manager.

        :param ufo: An instance of the UFO class to add.
        """
        self.UFOs[ufo.uuid] = ufo

    def get_instance(self, ufo_uuid: UUID) -> 'UFO':
        """
        Retrieves a UFO instance by its UUID.

        :param ufo_uuid: The UUID of the UFO to retrieve.
        :return: The UFO instance if found, otherwise None.
        """
        return self.UFOs.get(ufo_uuid)

    def get_all(self) -> list['UFO']:
        """
        Retrieves all UFO instances managed by this class.

        :return: A list of all UFO instances.
        """
        return list(self.UFOs.values())


def altitude_to_y(altitude: float) -> int:
    """
    Converts altitude into a Y-coordinate for screen representation.

    :param altitude: The altitude value (0 to 10,000 meters).
    :return: The corresponding Y-coordinate (scaled between 1 and 400 pixels).
    """
    altitude = max(0, min(altitude, 10_000))
    normalized_altitude = altitude / 10_000
    y_position = max(400 * (1 - normalized_altitude), 1)
    return round(y_position)


class UFO(BaseModel):
    """
    Represents a UFO with attributes for speed, altitude, dimensions, and screen position.

    Attributes:
        uuid (UUID): Unique identifier for the UFO.
        speed (float): Current speed of the UFO in km/h.
        max_speed (float): Maximum speed of the UFO in km/h.
        altitude (float): Altitude of the UFO in meters.
        temperature (float): Temperature of the UFO's surface in degrees Celsius.
        width (float): Width of the UFO in pixels (for screen representation).
        height (float): Height of the UFO in pixels (for screen representation).
        x (float): Current X-coordinate of the UFO on the screen.
        y (float): Current Y-coordinate of the UFO on the screen.
        screen_width (int): Width of the screen in pixels.
        manager (ClassVar[UFOManager]): A class-level manager for all UFO instances.
        weapon (int): Weapon state of the UFO, either 0 (off) or 1 (on).
    """
    uuid: UUID = Field(default_factory=uuid4)
    speed: confloat() = None
    max_speed: confloat(gt=0) = None
    altitude: confloat() = None
    temperature: confloat() = None
    width: confloat() = None
    height: confloat() = None
    x: confloat() = None
    y: confloat() = None
    weapon: conint(ge=0, le=1) = 0
    screen_width: conint(ge=0)
    manager: ClassVar[UFOManager] = UFOManager()

    def __init__(self, **data):
        """
        Initializes a new UFO instance and registers it with the UFOManager.

        :param data: Keyword arguments to initialize the UFO attributes.
        """
        super().__init__(**data)
        UFO.manager.add_instance(self)

    def move(self):
        """
        Updates the X-coordinate of the UFO based on its speed.
        Removes the UFO from the manager if it moves off the left edge of the screen.
        """
        self.x -= (self.speed * 0.0027778)  # Convert speed to pixels per frame
        if self.x + 80 < 0:  # Check if UFO is off the screen
            del UFO.manager.UFOs[self.uuid]

    def move_y(self, altitude: float):
        """
        Updates the Y-coordinate of the UFO based on a new altitude.

        :param altitude: The new altitude value in meters.
        """
        self.y = altitude_to_y(altitude) - 20

    @classmethod
    def all(cls):
        """
        Retrieves all UFO instances currently managed.

        :return: A list of all UFO instances.
        """
        return cls.manager.get_all()
