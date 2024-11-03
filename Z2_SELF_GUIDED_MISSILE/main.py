"""
System obronny z użyciem logiki rozmytej.
Autorzy: Jan Kowalski, Anna Nowak

System podejmuje decyzję o wystrzeleniu pocisku na podstawie wykrytej temperatury,
ruchu i odległości do wrogiego obiektu. Logika rozmyta służy do oceny ryzyka
zagrożenia i typowania rodzaju pocisku w zależności od odległości.

Przygotowanie środowiska:
1. Zainstaluj Python 3.7 lub nowszy.
2. Zainstaluj wymagane biblioteki:
   pip install numpy scikit-fuzzy
"""
import asyncio
import json

import pygame

from Z2_SELF_GUIDED_MISSILE.map.terrain import draw_terrain
from Z2_SELF_GUIDED_MISSILE.models.missile import Missile
from models.launcher import Launcher
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO

with open('./config.json', 'r') as file:
    config = json.load(file)

# Pygame settings
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Launcher and Missiles')

font = pygame.font.Font(None, 36)

# Launcher initialization
launcher = Launcher(missiles_limit=5, default_reload_time=1, x=300, y=300)
missile = Missile(
    strength=config['MISSILE']['TYPES']['LONG_RANGE']['STRENGTH'],
    radius=config['MISSILE']['TYPES']['LONG_RANGE']['RADIUS'],
    max_speed=config['MISSILE']['TYPES']['LONG_RANGE']['MAX_SPEED'],
    acceleration=config['MISSILE']['TYPES']['LONG_RANGE']['ACCELERATION'],
    type='long',
    x=launcher.x,
    y=launcher.y)
missile2 = Missile(
    strength=config['MISSILE']['TYPES']['SHORT_RANGE']['STRENGTH'],
    radius=config['MISSILE']['TYPES']['SHORT_RANGE']['RADIUS'],
    max_speed=config['MISSILE']['TYPES']['SHORT_RANGE']['MAX_SPEED'],
    acceleration=config['MISSILE']['TYPES']['SHORT_RANGE']['ACCELERATION'],
    type='short',
    x=launcher.x,
    y=launcher.y)
missile3 = Missile(
    strength=config['MISSILE']['TYPES']['MEDIUM_RANGE']['STRENGTH'],
    radius=config['MISSILE']['TYPES']['MEDIUM_RANGE']['RADIUS'],
    max_speed=config['MISSILE']['TYPES']['MEDIUM_RANGE']['MAX_SPEED'],
    acceleration=config['MISSILE']['TYPES']['MEDIUM_RANGE']['ACCELERATION'],
    type='medium',
    x=launcher.x,
    y=launcher.y)
# TODO: change for reload_missile()
launcher._add_missile(missile)
launcher._add_missile(missile2)
launcher._add_missile(missile3)

ufo = UFO(speed=200, max_speed=600, altitude=500, temperature=70, x=350, y=120)
ufo2 = UFO(speed=250, max_speed=400, altitude=5200, temperature=50, x=3050, y=920)

# Missile image loading
bullet_image = pygame.image.load('bullet.svg')
bullet_image = pygame.transform.scale(bullet_image, (20, 20))

# Tasks
async def reload_missile_task(missile):
    # print(f"Starting reload for missile {missile}")
    await launcher.reload_missile(missile)
    # print(f"Reload complete for missile {missile}")

# Main game loop
async def main_loop():
    clock = pygame.time.Clock()

    # Generate initial terrain
    # terrain_points = generate_terrain(screen_width)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Adding the missile to launcher using r key
            # if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_r:
                #     try:
                #         # TODO: resp pocisku ustawic na kordy wyrzutni
                #         missile = Missile(
                #             strength=config['MISSILE']['TYPES']['MID_RANGE']['STRENGTH'],
                #             radius=config['MISSILE']['TYPES']['MID_RANGE']['RADIUS'],
                #             max_speed=config['MISSILE']['TYPES']['MID_RANGE']['MAX_SPEED'],
                #             acceleration=config['MISSILE']['TYPES']['MID_RANGE']['ACCELERATION'],)
                #         asyncio.create_task(reload_missile_task(missile))
                #     except ValueError as e:
                #         print('Error', e)

        draw_terrain(screen, screen_width, screen_height)

        # Updating
        for missile in launcher.missiles[:]:
            missile.move()
            if missile.is_out_of_map(screen_height, screen_width):
                launcher.missiles.remove(missile)

        # Drawing
        for index, _ in enumerate(launcher.loaded_missiles):
            screen.blit(bullet_image, (25 * index, 0))

        launcher.draw(screen, Settings().launcher_settings.color, screen_width, screen_height)
        for missile in launcher.launched_missiles:
            missile.draw(screen, Settings.missile_settings.color)
        launcher.scan()

        pygame.display.flip()
        await asyncio.sleep(0.01)
        clock.tick(30)


if __name__ == '__main__':
    asyncio.run(main_loop())
    pygame.quit()
