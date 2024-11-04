import asyncio
import json
import pygame

from Z2_SELF_GUIDED_MISSILE.map.terrain import draw_terrain
from Z2_SELF_GUIDED_MISSILE.setting_panel.panel import Panel
from Z2_SELF_GUIDED_MISSILE.models.missile import Missile
from models.launcher import Launcher
from Z2_SELF_GUIDED_MISSILE.models.ufo import UFO

# Initialize Pygame and settings
pygame.init()
with open('./config.json', 'r') as file:
    config = json.load(file)

screen_width, screen_height = config["GAME"]["screen_width"], config["GAME"]["screen_height"]
screen = pygame.display.set_mode((screen_width*2, screen_height))
pygame.display.set_caption(config["GAME"]["title"])
font = pygame.font.Font(None, 36)
# Initialize launcher and missiles
LAUNCHER = config["LAUNCHER"]
launcher = Launcher(missiles_limit=5,
                    default_reload_time=1,
                    **LAUNCHER["DRAW"],
                    color = LAUNCHER["COLOR"],
                    range = LAUNCHER["SETUP"]["RANGE"])
types = config['MISSILE']['TYPES']

missile1 = Missile(**types['LONG_RANGE'], type='long', x=launcher.x, y=launcher.y)
missile2 = Missile(**types['SHORT_RANGE'], type='short', x=launcher.x, y=launcher.y)
missile3 = Missile(**types['MEDIUM_RANGE'], type='medium', x=launcher.x, y=launcher.y)

# Add missiles to launcher
launcher._add_missile(missile1)
launcher._add_missile(missile2)
launcher._add_missile(missile3)

#ufo1 = UFO(speed=200, max_speed=600, altitude=500, temperature=70, x=350, y=120, screen_width = config["GAME"]["screen_width"])
#ufo2 = UFO(speed=250, max_speed=400, altitude=5200, temperature=50, x=305, y=92, screen_width = config["GAME"]["screen_width"])
print(UFO.all())
bullet_image = pygame.image.load('bullet.svg')
bullet_image = pygame.transform.scale(bullet_image, (20, 20))

# Asynchronous task for missile reload
async def reload_missile_task(missile):
    # print(f"Starting reload for missile {missile}")
    await launcher.reload_missile(missile)
    # print(f"Reload complete for missile {missile}")

# Main game loop
async def main_loop():
    clock = pygame.time.Clock()
    panel = Panel(screen_width,screen_height,config["MAP"]["GRASS"])
    sliders = panel.sliders
    running = True
    model = UFO(speed=1, max_speed=600, altitude=500, temperature=70, x=screen_width+50, y=1,
        screen_width=config["GAME"]["screen_width"])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for slider in sliders:
                slider.handle_event(event)
        # Draw terrain
        draw_terrain(screen, screen_width, screen_height,config["MAP"])
        values = panel.draw_and_update_sliders(screen)
        position_y = values[0]
        font = pygame.font.Font(None, 24)
        position_y_text = font.render(f'Position Y: {int(position_y)}', True, (0, 0, 0))
        screen.blit(position_y_text, (screen_width+350, screen_height-50))

        # Update and draw detected objects
        detected_objects = launcher.scan()
        model.move_y(position_y)
        for ufo in UFO.all():
            pygame.draw.circle(screen, (255, 0, 0), (ufo.x, ufo.y), 10)
            ufo.move()
        # Update missiles
        # for missile in launcher.missiles[:]:
        #     missile.move()
        #     if missile.is_out_of_map(screen_height, screen_width):
        #         launcher.missiles.remove(missile)

        # Draw missiles in the loading bar
        # for index, _ in enumerate(launcher.loaded_missiles):
        #     screen.blit(bullet_image, (25 * index, 0))

        launcher.draw(screen)
        # for missile in launcher.launched_missiles:
        #     missile.draw(screen, Settings.missile_settings.color)

        # Update the display
        pygame.display.flip()
        await asyncio.sleep(0.01)
        clock.tick(60)

if __name__ == '__main__':
    asyncio.run(main_loop())
    pygame.quit()
