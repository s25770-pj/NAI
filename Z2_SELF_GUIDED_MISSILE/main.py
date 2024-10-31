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

from models.launcher import Launcher
from Z2_SELF_GUIDED_MISSILE.fuzzy_logic.missile_choice import test_missile_choice
from Z2_SELF_GUIDED_MISSILE.fuzzy_logic.shot_decision import test_do_shot


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

print('=======DO SHOT========')
# Test Case 1: Low Threat, No Motion
result1 = test_do_shot(speed_input=100, temperature_input=20, motion_input=0, altitude_input=500, distance_input=3000, threat_level_input=10)
print(f"Test Case 1: Fire Missile Decision = {result1}")

# Test Case 2: Medium Threat, Slow Motion
result2 = test_do_shot(speed_input=300, temperature_input=45, motion_input=1, altitude_input=800, distance_input=5000, threat_level_input=50)
print(f"Test Case 2: Fire Missile Decision = {result2}")

# Test Case 3: High Threat, Fast Motion, High Altitude
result3 = test_do_shot(speed_input=600, temperature_input=90, motion_input=1, altitude_input=10000, distance_input=14999, threat_level_input=80)
print(f"Test Case 3: Fire Missile Decision = {result3}")

# Test Case 4: Low Threat, Fast Motion, Medium Altitude
# result4 = test_do_shot(speed_input=1200, temperature_input=70, motion_input=1, altitude_input=4000, distance_input=20000, threat_level_input=20)
# print(f"Test Case 4: Fire Missile Decision = {result4}")

# Test Case 5: High Threat, Medium Speed, Close Distance
result5 = test_do_shot(speed_input=800, temperature_input=60, motion_input=1, altitude_input=3000, distance_input=4000, threat_level_input=90)
print(f"Test Case 5: Fire Missile Decision = {result5}")

# Test Case 6: No Motion, Medium Threat
# result6 = test_do_shot(speed_input=200, temperature_input=50, motion_input=0, altitude_input=600, distance_input=10000, threat_level_input=30)
# print(f"Test Case 6: Fire Missile Decision = {result6}")

# Test Case 7: Fast Motion, Low Altitude, High Threat
result7 = test_do_shot(speed_input=1200, temperature_input=85, motion_input=1, altitude_input=1000, distance_input=2000, threat_level_input=95)
print(f"Test Case 7: Fire Missile Decision = {result7}")

# print('=======LONG RANGE========')
# test_missile_choice(2500, 600)
# test_missile_choice(2400, 600)
# test_missile_choice(2300, 600)
# test_missile_choice(2200, 600)
#
# print('=======MEDIUM RANGE=======')
# test_missile_choice(2100, 600)
# test_missile_choice(2000, 600)
# test_missile_choice(1600, 600)
# test_missile_choice(1500, 600)
#
# print('=======CLOSE RANGE========')
# test_missile_choice(1400, 600)
# test_missile_choice(1300, 600)
# test_missile_choice(100, 600)
# test_missile_choice(0, 600)

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