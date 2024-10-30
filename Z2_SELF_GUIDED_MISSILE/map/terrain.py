import noise
import pygame

from Z2_SELF_GUIDED_MISSILE.styles.variables.colors import GREEN

# Map control
terrain_height = 150
mountain_height = 300
scale = 0.02
octaves = 6

# Generate mountain terrain points
def generate_terrain(screen_width):
    terrain_points = []
    for x in range(screen_width):
        # Generate a y value using Perlin noise
        y = int(terrain_height / 2 + noise.pnoise1(x * scale, octaves=octaves) * mountain_height)
        terrain_points.append((x, y))
    return terrain_points

# Draw the terrain on screen
def draw_terrain(points, screen, screen_width, screen_height):
    # Draw the sky and ground colors
    screen.fill((135, 206, 235))  # Light blue sky
    pygame.draw.rect(screen, GREEN, (0, screen_height // 2, screen_width, screen_height // 2))  # Ground

    # Draw mountains
    # pygame.draw.polygon(screen, BROWN, [(0, screen_height)] + points + [(screen_width, screen_height)])