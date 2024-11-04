import asyncio
import json
import pygame

from Z2_SELF_GUIDED_MISSILE.map.terrain import Terrain
from Z2_SELF_GUIDED_MISSILE.setting_panel.panel import Panel
from Z2_SELF_GUIDED_MISSILE.models.missile import Missile
from models.launcher import Launcher
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO


def initialize_game(config):
    """Initializes Pygame and sets up the screen and other parameters."""
    pygame.init()
    screen_width, screen_height = config["GAME"]["screen_width"], config["GAME"]["screen_height"]
    screen = pygame.display.set_mode((screen_width * 2, screen_height))
    pygame.display.set_caption(config["GAME"]["title"])
    return screen, screen_width, screen_height


def load_missiles(launcher, types):
    """Loads missiles into the launcher."""
    missile1 = Missile(**types['LONG_RANGE'], type='long', x=launcher.x, y=launcher.y)
    missile2 = Missile(**types['SHORT_RANGE'], type='short', x=launcher.x, y=launcher.y)
    missile3 = Missile(**types['MEDIUM_RANGE'], type='medium', x=launcher.x, y=launcher.y)

    launcher._add_missile(missile1)
    launcher._add_missile(missile2)
    launcher._add_missile(missile3)


def create_launcher(config):
    """Creates a launcher object with settings from the configuration."""
    LAUNCHER = config["LAUNCHER"]
    launcher = Launcher(missiles_limit=5,
                        default_reload_time=1,
                        **LAUNCHER["DRAW"],
                        color=LAUNCHER["COLOR"],
                        range=LAUNCHER["SETUP"]["RANGE"])
    return launcher


async def handle_events(panel):
    """Handles Pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        for slider in panel.sliders.values():
            slider.handle_event(event)
        for button in panel.buttons.values():
            button.handle_event(event)
    return True


async def main_loop(screen, screen_width, screen_height, config, panel, launcher):
    """Main game loop."""
    clock = pygame.time.Clock()
    model = UFO(speed=1, max_speed=600, altitude=500, temperature=70, x=screen_width + 50, y=1,
                screen_width=config["GAME"]["screen_width"])
    UFO(speed=20, max_speed=600, altitude=500, temperature=70, x=screen_width + 50, y=1,
        screen_width=config["GAME"]["screen_width"])
    terrain = Terrain(screen_width,config["MAP"])

    while await handle_events(panel):

        # Draw terrain
        terrain.render(screen)
        # Draw sliders
        values = panel.redner(screen)

        position_y = values["position_y"]
        model.move_y(position_y)

        font = pygame.font.Font(None, 24)
        position_y_text = font.render(f'Position Y: {int(position_y)}', True, (0, 0, 0))
        screen.blit(position_y_text, (screen_width + 350, screen_height - 50))


        for ufo in UFO.all():
            pygame.draw.circle(screen, (255, 0, 0), (ufo.x, ufo.y), 10)
            ufo.move()

        launcher.draw(screen)

        # Update the display
        pygame.display.flip()
        await asyncio.sleep(0.01)
        clock.tick(60)


if __name__ == '__main__':
    """Main function to run the game."""
    with open('./config.json', 'r') as file:
        config = json.load(file)

    screen, screen_width, screen_height = initialize_game(config)
    launcher = create_launcher(config)
    load_missiles(launcher, config['MISSILE']['TYPES'])
    panel = Panel(screen_width, screen_height, config["MAP"]["GRASS"])

    asyncio.run(main_loop(screen, screen_width, screen_height, config, panel, launcher))
    pygame.quit()
