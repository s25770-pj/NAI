import asyncio
import json
import pygame
from scipy.signal.windows import lanczos

from Z2_SELF_GUIDED_MISSILE.map.terrain import Terrain
from Z2_SELF_GUIDED_MISSILE.setting_panel.panel import Panel
from Z2_SELF_GUIDED_MISSILE.models.missile import Missile
from models.launcher import Launcher
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO


def initialize_game(config):
    pygame.init()
    screen_width, screen_height = config["GAME"]["screen_width"], config["GAME"]["screen_height"]
    screen = pygame.display.set_mode((screen_width * 2, screen_height))
    pygame.display.set_caption(config["GAME"]["title"])
    return screen, screen_width, screen_height


def load_missiles(launcher, types):
    missile1 = Missile(**types['LONG_RANGE'], type='long', x=launcher.x, y=launcher.y)
    missile2 = Missile(**types['SHORT_RANGE'], type='short', x=launcher.x, y=launcher.y)
    missile3 = Missile(**types['MEDIUM_RANGE'], type='medium', x=launcher.x, y=launcher.y)

    launcher._add_missile(missile1)
    launcher._add_missile(missile2)
    launcher._add_missile(missile3)


def create_launcher(config):
    LAUNCHER = config["LAUNCHER"]
    launcher = Launcher(missiles_limit=5,
                        default_reload_time=1,
                        **LAUNCHER["DRAW"],
                        color=LAUNCHER["COLOR"],
                        range=LAUNCHER["SETUP"]["RANGE"],
                        max_range=200)
    return launcher


async def handle_events(panel):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        for slider in panel.sliders.values():
            slider["model"].handle_event(event)
        for button in panel.buttons.values():
            button.handle_event(event)
    return True


async def scan_in_background(launcher, detected_ufo_list):
    while True:
        detected_ufo_in_range = await asyncio.to_thread(launcher.scan)
        detected_ufo_list.clear()
        detected_ufo_list.extend(detected_ufo_in_range)
        await asyncio.sleep(0.5)


def draw_detected_ufo(detected_ufo_in_range, screen):
    for ufo, threat_level, shot_rightness, required_missile in detected_ufo_in_range:
        # Rysowanie ramki wokół UFO
        rect = pygame.Rect(ufo.x - 10, ufo.y - 10, ufo.width + 20, ufo.height + 20)
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)

        # Rysowanie paska pod UFO
        bar_width = ufo.width  # Szerokość paska odpowiada szerokości UFO
        bar_height = 5  # Wysokość paska
        bar_x = ufo.x  # X pozycji paska, wyśrodkowany względem UFO
        bar_y = ufo.y + ufo.height + 12  # Y pozycji paska (tuż pod UFO)

        # Wypełnienie paska zielonym kolorem, proporcjonalnie do threat_level
        filled_width = bar_width * threat_level/100  # Proporcja wypełnienia paska
        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(bar_x-5, bar_y, bar_width-5, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(bar_x-5, bar_y, filled_width-5, bar_height))

        # Rysowanie obok paska czerwonej kropki, jeśli shot_rightness > 0.5
        if shot_rightness > 0.5:
            dot_radius = 5  # Promień kropki
            dot_x = bar_x + bar_width + 2  # X pozycji kropki (poza paskiem)
            dot_y = bar_y + bar_height // 2  # Y pozycji kropki (na środku paska)
            pygame.draw.circle(screen, (255, 0, 0), (dot_x, dot_y), dot_radius)



async def main_loop(screen, screen_width, config, panel, launcher):
    clock = pygame.time.Clock()
    model = UFO(speed=0, max_speed=600, altitude=500, temperature=70, x=screen_width + 25, y=1,
                screen_width=config["GAME"]["screen_width"], width=80, height=40)
    terrain = Terrain(screen_width, config["MAP"])
    detected_ufo_list = []
    scan_task = asyncio.create_task(scan_in_background(launcher, detected_ufo_list))

    image_plane = pygame.image.load('texture/plane.png')
    image_plane = pygame.transform.scale(image_plane, (80, 40))

    image_model = image_plane.convert_alpha()
    image_model.set_alpha(128)

    while True:
        if not await handle_events(panel):
            break

        terrain.render(screen)

        values = panel.render(screen)

        altitude = values["altitude"]
        model.move_y(altitude)
        launcher.draw(screen)

        draw_detected_ufo(detected_ufo_list, screen)

        for ufo in UFO.all():
            if ufo.uuid != model.uuid:
                pygame.draw.line(screen, (0, 0, 0), ((ufo.x if launcher.x < ufo.x + ufo.width // 2 else ufo.x + ufo.width), ufo.y + ufo.height // 2),
                                 (launcher.x, launcher.y), 1)

            screen.blit(image_model if ufo.uuid == model.uuid else image_plane, (ufo.x, ufo.y))
            ufo.move()

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0.01)


if __name__ == '__main__':
    with open('./config.json', 'r') as file:
        config = json.load(file)

    screen, screen_width, screen_height = initialize_game(config)
    launcher = create_launcher(config)
    load_missiles(launcher, config['MISSILE']['TYPES'])
    panel = Panel(screen_width, screen_height, config["MAP"]["GRASS"]["height"])

    asyncio.run(main_loop(screen, screen_width, config, panel, launcher))
    pygame.quit()
