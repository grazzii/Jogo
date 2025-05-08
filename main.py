# Example file showing a basic pygame "game loop"
import pygame
import math

# pygame setup
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

centro_x, centro_y = width // 2, height // 2
raio_orbita = 175
velocidade_angular = 0.02
angulo = 0 #angulo inicial

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    angulo += velocidade_angular

    orbita_x = centro_x + raio_orbita * math.cos(angulo)
    orbita_y = centro_y + raio_orbita * math.sin(angulo)
                    
    screen.fill("#FFD166")

    pygame.draw.circle(screen, "#FB6286", (centro_x, centro_y), 200)
    pygame.draw.circle(screen, "#FFD166", (centro_x, centro_y), 150)
    pygame.draw.circle(screen, "#073B4C", (int(orbita_x), int(orbita_y)), 25)

    pygame.draw.flip()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
