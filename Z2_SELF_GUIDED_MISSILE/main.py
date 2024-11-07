import asyncio
import json
import pygame
from Z2_SELF_GUIDED_MISSILE.map.terrain import Terrain
from Z2_SELF_GUIDED_MISSILE.setting_panel.panel import Panel
from Z2_SELF_GUIDED_MISSILE.models.missile import Missile
from models.launcher import Launcher
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO
import threading


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
    return Launcher(
        missiles_limit=5,
        default_reload_time=1,
        **LAUNCHER["DRAW"],
        color=LAUNCHER["COLOR"],
        range=LAUNCHER["SETUP"]["RANGE"],
        max_range=200
    )


async def handle_events(panel):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        for slider in panel.sliders.values():
            slider["model"].handle_event(event)
        for button in panel.buttons.values():
            button.handle_event(event)
    return True


def scan_in_background(launcher, detected_ufo_list):
    def scan():
        while True:
            detected_ufo_in_range = launcher.scan()
            detected_ufo_list.clear()
            detected_ufo_list.extend(detected_ufo_in_range)
            pygame.time.wait(500)  # Zmniejsza częstotliwość skanowania do 0.5 sekundy
    threading.Thread(target=scan, daemon=True).start()  # Użycie wątku, aby nie blokować głównej pętli gry


def get_threat_level_color(threat_level):
    if threat_level <= 40:
        return (0, 255, 0)
    elif threat_level <= 75:
        return (255, 255, 0)
    else:
        return (255, 0, 0)


def draw_detected_ufo(detected_ufo_in_range, screen):
    for ufo, threat_level, shot_rightness, required_missile in detected_ufo_in_range:
        rect = pygame.Rect(ufo.x - 10, ufo.y - 10, ufo.width + 20, ufo.height + 20)
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)

        bar_width = ufo.width
        bar_height = 5
        bar_x = ufo.x
        bar_y = ufo.y + ufo.height + 12
        filled_width = bar_width * threat_level / 100
        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(bar_x - 5, bar_y, bar_width - 5, bar_height))
        pygame.draw.rect(screen, get_threat_level_color(threat_level), pygame.Rect(bar_x - 5, bar_y, filled_width - 5, bar_height))

        shot_detected_color = (255, 0, 0) if shot_rightness > 0.5 else (0, 255, 0)
        dot_radius = 5
        dot_x = bar_x + bar_width + 2
        dot_y = bar_y + bar_height // 2
        pygame.draw.circle(screen, shot_detected_color, (dot_x, dot_y), dot_radius)


async def main_loop(screen, screen_width, config, panel, launcher):
    clock = pygame.time.Clock()
    model = UFO(speed=0, max_speed=600, altitude=500, temperature=70, x=screen_width + 25, y=1,
                screen_width=config["GAME"]["screen_width"], width=80, height=40)
    terrain = Terrain(screen_width, config["MAP"])
    detected_ufo_list = []
    scan_in_background(launcher, detected_ufo_list)  # Rozpoczynamy skanowanie w tle

    image_plane = pygame.image.load('texture/plane.png')
    image_plane = pygame.transform.scale(image_plane, (80, 40))
    image_model = image_plane.convert_alpha()
    image_model.set_alpha(128)

    while True:
        if not await handle_events(panel):
            break
        ufo_list = UFO.all()
        terrain.render(screen)
        values = panel.render(screen, ufo_list)
        altitude = values["altitude"]
        model.move_y(altitude)
        launcher.draw(screen)
        draw_detected_ufo(detected_ufo_list, screen)

        for ufo in ufo_list:
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
