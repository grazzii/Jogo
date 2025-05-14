import pygame
import math
import random
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
velocidade_angular = 0.06
angulo = 0 
running = True

# parâmetros da fatia do donut
raio_externo = 200
raio_interno = 150
percentual_fatia = 0.1
angulo_fatia = 2 * math.pi * percentual_fatia
cor_fatia = "#C94869"  # versão mais escura do rosa (#FB6286)

angulo_inicio = random.randint(0, 360)
angulo_fim = angulo_inicio + angulo_fatia

# main
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                percentual_fatia = random.uniform(0.1, 0.5)
                angulo_inicio = random.randint(0, 360)
                angulo_fim = angulo_inicio + angulo_fatia

    # att a posição do objeto em órbita
    angulo += velocidade_angular
    orbita_x = centro_x + raio_orbita * math.cos(angulo)
    orbita_y = centro_y + raio_orbita * math.sin(angulo)

    # tela 
    screen.fill("#FFD166")

    # desenho dos círculos
    pygame.draw.circle(screen, "#FB6286", (centro_x, centro_y), raio_externo)
    pygame.draw.circle(screen, "#FFD166", (centro_x, centro_y), raio_interno)

    # cria uma lista de pontos para formar o polígono da fatia
    pontos_fatia = []
    
    # Adiciona os pontos ao longo do arco externo
    num_segmentos = 20  # mais segmentos para uma curva mais suave
    for i in range(num_segmentos + 1):
        angulo_atual = angulo_inicio + (angulo_fim - angulo_inicio) * (i / num_segmentos)
        x = centro_x + raio_externo * math.cos(angulo_atual)
        y = centro_y + raio_externo * math.sin(angulo_atual)
        pontos_fatia.append((x, y))

    # Adiciona os pontos ao longo do arco interno (em ordem reversa)
    for i in range(num_segmentos, -1, -1):
        angulo_atual = angulo_inicio + (angulo_fim - angulo_inicio) * (i / num_segmentos)
        x = centro_x + raio_interno * math.cos(angulo_atual)
        y = centro_y + raio_interno * math.sin(angulo_atual)
        pontos_fatia.append((x, y))
    
    # Desenha o polígono preenchido
    pygame.draw.polygon(screen, cor_fatia, pontos_fatia)
    
    # objeto em órbita
    pygame.draw.circle(screen, "#073B4C", (int(orbita_x), int(orbita_y)), 25)

    # FPS
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))  
    screen.blit(fps_text, (10, 10))

    # att a tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
