import pygame
import math

pygame.init()

# configurações da tela
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Órbita Interativa")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 16)  

# parâmetros da órbita
centro_x, centro_y = width // 2, height // 2
raio_orbita = 175
velocidade_angular = 0.02
angulo = 0 
running = True

# main
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # att a posição do objeto em órbita
    angulo += velocidade_angular
    orbita_x = centro_x + raio_orbita * math.cos(angulo)
    orbita_y = centro_y + raio_orbita * math.sin(angulo)

    # tela 
    screen.fill("#FFD166")

    # desenho dos círculos
    pygame.draw.circle(screen, "#FB6286", (centro_x, centro_y), 200)
    pygame.draw.circle(screen, "#FFD166", (centro_x, centro_y), 150)
    pygame.draw.circle(screen, "#073B4C", (int(orbita_x), int(orbita_y)), 25)

    # FPS
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))  
    screen.blit(fps_text, (10, 10))

    # att a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
