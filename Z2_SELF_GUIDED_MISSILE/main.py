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
from Z2_SELF_GUIDED_MISSILE.fuzzy_logic.shot_decision import threat_level


with open('./config.json', 'r') as file:
    config = json.load(file)

# Pygame settings
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Launcher and Missiles')

font = pygame.font.Font(None, 36)

# # Launcher initialization
launcher = Launcher(missiles_limit=5, default_reload_time=1)
#
# # Missile image loading
bullet_image = pygame.image.load('bullet.svg')
bullet_image = pygame.transform.scale(bullet_image, (20, 20))

# print('=======DO SHOT========')
# Test Case 1: Low Threat, No Motion
# count = 0
# for motion in range(2):
#     for altitude in range(11):
#         for distance in range(10):
#             for threat_level.json in range(6):
#                 try:
#                     result1 = do_shot(
#                         motion_input=motion,
#                         altitude_input=altitude*500,
#                         distance_input=distance*2500,
#                         threat_level_input=threat_level.json*20
#                     )
#                     count += 1
#                     if count%1000 == 0:
#                         print(f'{count} records successfully processed.')
#                 except Exception as e:
#                     print(f'Error {e} occurred!')
#                     print(f' motion: {motion},'
#                           f' altitude: {altitude*500},'
#                           f' distance: {distance*2500},'
#                           f' threat_level.json: {threat_level.json*20}')

# Tasks
async def reload_missile_task(missile):
    # print(f"Starting reload for missile {missile}")
    await launcher.reload_missile(missile)
    # print(f"Reload complete for missile {missile}")

def scan_tick(motion_input, weapon_input, distance_input):
    # TODO: funkcja sprawdzająca pokolei czy coś wykrywa, czy jest jakieś zagrożenie, czy strzelić, wybrać pocisk etc.
    #  Do przeniesienia potem do modelu wyrzutni.
    #  Dopisać funkcję wykrywającą obiekty
    if threat_level(motion_input, weapon_input, distance_input):
        pass

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    try:
                        # TODO: x i y pojawiania się pocisku do zmiany na x i y wyrzutni
                        missile = Missile(
                            strength=config['MISSILE']['TYPES']['MID_RANGE']['STRENGTH'],
                            radius=config['MISSILE']['TYPES']['MID_RANGE']['RADIUS'],
                            max_speed=config['MISSILE']['TYPES']['MID_RANGE']['MAX_SPEED'],
                            acceleration=config['MISSILE']['TYPES']['MID_RANGE']['ACCELERATION'],
                            x=screen_width // 2,
                            y=screen_height - 50)
                        asyncio.create_task(reload_missile_task(missile))
                    except ValueError as e:
                        print('Error', e)

        draw_terrain(screen, screen_width, screen_height)

        # Updating
        for missile in launcher.missiles[:]:
            missile.move()
            if missile.is_out_of_map(screen_height, screen_width):
                launcher.missiles.remove(missile)

        # Drawing
        for index, _ in enumerate(launcher.loaded_missiles):
            screen.blit(bullet_image, (25*index, 0))

        launcher.draw(screen, config['LAUNCHER']['COLOR'], screen_width, screen_height)
        for missile in launcher.launched_missiles:
            missile.draw(screen, config['MISSILE']['COLOR'])

        pygame.display.flip()
        await asyncio.sleep(0.01)
        clock.tick(30)

if __name__ == '__main__':
    asyncio.run(main_loop())
    pygame.quit()