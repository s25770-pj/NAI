from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from typing import List


# Map settings
class MapSettings(BaseModel):
    colors: dict[str, List[int]] = {
        "grass": [34, 139, 34],
        "sky": [135, 206, 235],
        "black": [0, 0, 0],
        "brown": [139, 69, 19]
    }
    sizes: dict[str, float] = {
        "terrain_height": 0,
        "mountain_height": 300,
        "scale": 0.2,
        "octaves": 6
    }


# Launcher settings
class LauncherSettings(BaseModel):
    color: List[int] = [255, 205, 255]
    setup: dict[str, int] = {"missiles_limit": 100}


# Missile settings
class MissileTypes(BaseModel):
    short_range: dict[str, int] = {
        "strength": 500,
        "radius": 1000,
        "max_speed": 1000,
        "acceleration": 50
    }
    medium_range: dict[str, int] = {
        "strength": 500,
        "radius": 1800,
        "max_speed": 1000,
        "acceleration": 50
    }
    long_range: dict[str, int] = {
        "strength": 500,
        "radius": 3000,
        "max_speed": 1000,
        "acceleration": 50
    }


class MissileSettings(BaseModel):
    color: List[int] = [255, 255, 255]
    types: MissileTypes = MissileTypes()


# Fuzzy settings
class FuzzyRules(BaseModel):
        threat: dict[str, str] = {
            "url": "./fuzzy_logic/rules/threat_level.json"
        }
        shot_decision: dict[str, str] = {
            "url": "./fuzzy_logic/rules/do_shot.json"
        }
        missile_choice: dict[str, str] = {
            "url": "./fuzzy_logic/rules/missile_choice.json"
        }

class FuzzySettings(BaseModel):
    fuzzy_rules: FuzzyRules = FuzzyRules()

class Settings(BaseSettings):
    map_settings: MapSettings = MapSettings()
    launcher_settings: LauncherSettings = LauncherSettings()
    missile_settings: MissileSettings = MissileSettings()
    fuzzy_settings: FuzzySettings = FuzzySettings()
    model_config = SettingsConfigDict()
