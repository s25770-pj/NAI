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

import pygame
import asyncio

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from models.launcher import Launcher
from models.missile import Missile
from map.terrain import generate_terrain, draw_terrain
from styles.variables.colors import WHITE


# Pygame settings
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Launcher and Missiles')

font = pygame.font.Font(None, 36)

# Launcher initialization
launcher = Launcher(missiles_limit=5, default_reload_time=1)

# Missile image loading
bullet_image = pygame.image.load('bullet.svg')
bullet_image = pygame.transform.scale(bullet_image, (20, 20))

# # Fuzzy inputs
# temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'temperature')
# motion = ctrl.Antecedent(np.arange(0, 2, 1), 'motion')
distance = ctrl.Antecedent(np.arange(0, 10001, 1), 'distance')
speed = ctrl.Antecedent(np.arange(0, 1501, 1), 'speed')

# Fuzzy outputs
fire_missile = ctrl.Consequent(np.arange(0, 6, 1), 'fire_missile')

# # Membership function definition
# temperature['low'] = fuzz.trimf(temperature.universe, [0, 0, 50])
# temperature['medium'] = fuzz.trimf(temperature.universe, [50, 75, 100])
# temperature['high'] = fuzz.trimf(temperature.universe, [75, 100, 100])
#
# motion['no'] = fuzz.trimf(motion.universe, [0, 0, 1])
# motion['yes'] = fuzz.trimf(motion.universe, [0, 1, 1])

distance['close'] = fuzz.trimf(distance.universe, [0, 0, 1500])
distance['medium'] = fuzz.trimf(distance.universe, [1000, 2000, 3000])
distance['far'] = fuzz.trimf(distance.universe, [2000, 3000, 3000])
distance['out_of_range'] = fuzz.trimf(distance.universe, [3000, 7000, 10000])

fire_missile['no'] = fuzz.trimf(fire_missile.universe, [0, 0, 1])
fire_missile['short'] = fuzz.trimf(fire_missile.universe, [1, 1, 2])
fire_missile['medium'] = fuzz.trimf(fire_missile.universe, [1.5, 2, 2.5])
fire_missile['long'] = fuzz.trimf(fire_missile.universe, [2, 3, 4])

speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 500])
speed['medium'] = fuzz.trimf(speed.universe, [250, 500, 750])
speed['fast'] = fuzz.trimf(speed.universe, [500, 1500, 1500])

# Fuzzy rules
rule0 = ctrl.Rule(distance['out_of_range'], fire_missile['no'])
rule1 = ctrl.Rule(distance['close'] & speed['slow'], fire_missile['short'])
rule2 = ctrl.Rule(distance['close'] & speed['medium'], fire_missile['short'])
rule3 = ctrl.Rule(distance['close'] & speed['fast'], fire_missile['short'])

rule4 = ctrl.Rule(distance['medium'] & speed['slow'], fire_missile['medium'])
rule5 = ctrl.Rule(distance['medium'] & speed['medium'], fire_missile['medium'])
rule6 = ctrl.Rule(distance['medium'] & speed['fast'], fire_missile['medium'])

rule7 = ctrl.Rule(distance['far'] & speed['slow'], fire_missile['long'])
rule8 = ctrl.Rule(distance['far'] & speed['medium'], fire_missile['long'])
rule9 = ctrl.Rule(distance['far'] & speed['fast'], fire_missile['long'])

# Control system
fire_missile_ctrl = ctrl.ControlSystem([rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
# print(f'fire_missile_ctrl: {fire_missile_ctrl}')
fire_missile_sim = ctrl.ControlSystemSimulation(fire_missile_ctrl)
# print(f'fire_missile_sim: {fire_missile_sim}')


def test(distance_input, speed_input, temperature_input=None, motion_input=None):
    # Wprowadzenie danych do logiki rozmytej
    fire_missile_sim.input['distance'] = distance_input
    fire_missile_sim.input['speed'] = speed_input
    # Print input values
    # print(f"Inputs - Temperature: {temperature_input}, Motion: {motion_input}, Distance: {distance_input}")
    # print(f"Distance - Speed: {speed['slow'].mf[speed_input]}, Medium: {speed['medium'].mf[speed_input]}, Far: {speed['fast'].mf[speed_input]}")
    # Check membership values
    # print(f"Distance - Close: {distance['close'].mf[distance_input]}, Medium: {distance['medium'].mf[distance_input]}, Far: {distance['far'].mf[distance_input]}")

    # Compute output
    fire_missile_sim.compute()

    # Print the output
    print(fire_missile_sim.output)  # Check if there's any output
    missile_type = fire_missile_sim.output['fire_missile']
    # print(f'missile_type: {missile_type}')
    # print(f'missile_type round: {round(missile_type)}')

    # Sprawdzanie, czy należy strzelać
    if missile_type > 0 and len(launcher.loaded_missiles) > 0:
        if missile_type < 1:
            print("Strzel krótki pocisk!")
            launcher.loaded_missiles[0].launch()
        elif missile_type < 2:
            print("Strzel średni pocisk!")
            launcher.loaded_missiles[0].launch()
        elif missile_type < 3:
            print("Strzel długi pocisk!")
            launcher.loaded_missiles[0].launch()

print('=======LONG RANGE========')
test(3000, 600)
test(2900, 600)
test(2800, 600)
test(2700, 600)
test(2600, 600)
test(2500, 600)
test(2400, 600)
test(2300, 600)
test(2200, 600)
test(2100, 600)
test(2000, 600)

print('=======MEDIUM RANGE=======')
test(1900, 600)
test(1800, 600)
test(1700, 600)
test(1600, 600)
test(1500, 600)
test(1400, 600)
test(1300, 600)
test(1200, 600)
test(1100, 600)
test(1000, 600)

print('=======CLOSE RANGE========')
test(900, 600)
test(800, 600)
test(700, 600)
test(600, 600)
test(500, 600)
test(400, 600)
test(300, 600)
test(200, 600)
test(100, 600)
test(0, 600)

# Tasks
# async def reload_missile_task(missile):
#     # print(f"Starting reload for missile {missile}")
#     await launcher.reload_missile(missile)
#     # print(f"Reload complete for missile {missile}")
#
# # Main game loop
# async def main_loop():
#     clock = pygame.time.Clock()
#
#     # Generate initial terrain
#     terrain_points = generate_terrain(screen_width)
#
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#             # Adding the missile to launcher using r key
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_r:
#                     try:
#                         missile = Missile(strength=100, radius=5, max_speed=5, acceleration=1, x=screen_width // 2, y=screen_height - 50)
#                         asyncio.create_task(reload_missile_task(missile))
#                     except ValueError as e:
#                         print('Error', e)
#
#         draw_terrain(terrain_points, screen, screen_width, screen_height)
#
#         # Updating
#         for missile in launcher.missiles[:]:
#             missile.move()
#             if missile.is_out_of_map(screen_height, screen_width):
#                 launcher.missiles.remove(missile)
#
#         # Drawing
#         for index, _ in enumerate(launcher.loaded_missiles):
#             screen.blit(bullet_image, (25*index, 0))
#
#         launcher.draw(screen, WHITE, screen_width, screen_height)
#         for missile in launcher.launched_missiles:
#             missile.draw(screen, WHITE)
#
#         pygame.display.flip()
#         await asyncio.sleep(0.01)
#         clock.tick(30)
#
# if __name__ == '__main__':
#     asyncio.run(main_loop())
#     pygame.quit()