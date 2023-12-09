import sys
import time
import pygame
import math

window = pygame.display.set_mode((500, 500))

angle = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    window.fill((255, 255, 255))

    origin = pygame.math.Vector2(250, 250)
    end = pygame.math.Vector2(150, 0)

    new_end = origin + end.rotate_rad(-angle)

    print(angle, new_end)

    pygame.draw.line(window, (50, 50, 50), origin, new_end, 10)

    pygame.display.flip()

    angle = (angle + 0.01) % (math.pi * 2)

    time.sleep(0.1)

pygame.quit()
sys.exit()
