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

# parâmetros da seta
tamanho_seta = 40
largura_seta = 30
cor_seta = "#073B4C"
direcao_seta = "up"  # pode ser "up", "down", "left", "right"

def desenha_seta(screen, x, y, direcao, tamanho, largura, cor):
    """
    Desenha uma seta na direção especificada
    :param screen: superfície do pygame
    :param x: posição x do centro
    :param y: posição y do centro
    :param direcao: 'up', 'down', 'left', 'right'
    :param tamanho: altura/comprimento da seta
    :param largura: largura da base da seta
    :param cor: cor da seta
    """
    if direcao == "up":
        pontos = [
            (x, y - tamanho),      # ponta
            (x - largura//2, y),   # base esquerda
            (x + largura//2, y)    # base direita
        ]
    elif direcao == "down":
        pontos = [
            (x, y + tamanho),      # ponta
            (x - largura//2, y),   # base esquerda
            (x + largura//2, y)    # base direita
        ]
    elif direcao == "left":
        pontos = [
            (x - tamanho, y),      # ponta
            (x, y - largura//2),   # base superior
            (x, y + largura//2)    # base inferior
        ]
    elif direcao == "right":
        pontos = [
            (x + tamanho, y),      # ponta
            (x, y - largura//2),   # base superior
            (x, y + largura//2)    # base inferior
        ]
    
    pygame.draw.polygon(screen, cor, pontos)

angulo_inicio = random.randint(0, 360)
angulo_fim = angulo_inicio + angulo_fatia

# mapeia as setas do teclado para as direções da seta
setas_para_direcao = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}

# main
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key in [
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_LEFT,
                pygame.K_RIGHT
            ]:
                # se a direção da seta é a mesma, muda a direção e o ângulo
                if setas_para_direcao[event.key] == direcao_seta:
                    percentual_fatia = random.uniform(0.1, 0.5)
                    angulo_inicio = random.randint(0, 360)
                    angulo_fim = angulo_inicio + angulo_fatia
                    direcao_seta = random.choice(["up", "down", "left", "right"])
                else:
                    # para de girar por 1 segundo
                    pygame.time.wait(1000)

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
    
    # Desenha a seta na direção atual
    desenha_seta(screen, centro_x, centro_y, direcao_seta, tamanho_seta, largura_seta, cor_seta)
    
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
