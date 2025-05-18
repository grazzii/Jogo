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
velocidade_angular = 0.1
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

# variáveis de feedback
distancia = 0
feedback_texto = ""
feedback_timer = 0

# sons de feedback
som_perfeito = pygame.mixer.Sound("perfeito.wav")
som_bom = pygame.mixer.Sound("bom.wav")
som_ruim = pygame.mixer.Sound("ruim.wav")
som_erro = pygame.mixer.Sound("erro.wav")

# pontuação
pontuacao = 0

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
            (x, y - tamanho),
            (x - largura//2, y),
            (x + largura//2, y)
        ]
    elif direcao == "down":
        pontos = [
            (x, y + tamanho),
            (x - largura//2, y),
            (x + largura//2, y)
        ]
    elif direcao == "left":
        pontos = [
            (x - tamanho, y),
            (x, y - largura//2),
            (x, y + largura//2)
        ]
    elif direcao == "right":
        pontos = [
            (x + tamanho, y),
            (x, y - largura//2),
            (x, y + largura//2)
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

# === ADIÇÃO: controle de fases ===
fase = 1
fase_texto = "Fase 1"

def atualizar_fase(pontuacao):
    global fase, velocidade_angular, fase_texto
    if pontuacao <= 300:
        fase = 1
        velocidade_angular = 0.1
        fase_texto = "Fase 1"
    elif pontuacao <= 600:
        fase = 2
        velocidade_angular = 0.2
        fase_texto = "Fase 2 - Velocidade Aumentada"
    else:
        fase = 3
        velocidade_angular = -0.2
        fase_texto = "Fase 3 - Rotação Invertida"
# ================================

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
                if setas_para_direcao[event.key] == direcao_seta:
                    # CORREÇÃO: conversão correta para graus
                    angulo_objeto = math.degrees(angulo % (2 * math.pi))
                    angulo_fatia_graus = math.degrees(angulo_fatia)
                    inicio = angulo_inicio % 360
                    fim = (angulo_inicio + angulo_fatia_graus) % 360
                    centro_fatia = (inicio + (fim - inicio) / 2) % 360
                    distancia = abs((angulo_objeto - centro_fatia + 180) % 360 - 180)

                    if distancia < 10:
                        feedback_texto = "Perfeito!"
                        som_perfeito.play()
                        pontuacao += 100
                    elif distancia < 25:
                        feedback_texto = "Bom!"
                        som_bom.play()
                        pontuacao += 50
                    elif distancia < 45:
                        feedback_texto = "Ruim!"
                        som_ruim.play()
                        pontuacao += 10
                    else:
                        feedback_texto = "Acertou fora da fatia."
                        som_erro.play()

                    feedback_timer = pygame.time.get_ticks()

                    percentual_fatia = random.uniform(0.05, 0.3)
                    angulo_fatia = 2 * math.pi * percentual_fatia
                    angulo_inicio = random.randint(0, 360)
                    angulo_fim = angulo_inicio + angulo_fatia
                    direcao_seta = random.choice(["up", "down", "left", "right"])
                else:
                    feedback_texto = "Errou a direção!"
                    som_erro.play()
                    feedback_timer = pygame.time.get_ticks()
                    pygame.time.wait(1000)

    # ATUALIZA FASE
    atualizar_fase(pontuacao)

    angulo += velocidade_angular
    orbita_x = centro_x + raio_orbita * math.cos(angulo)
    orbita_y = centro_y + raio_orbita * math.sin(angulo)

    screen.fill("#FFD166")

    pygame.draw.circle(screen, "#FB6286", (centro_x, centro_y), raio_externo)
    pygame.draw.circle(screen, "#FFD166", (centro_x, centro_y), raio_interno)

    pontos_fatia = []
    num_segmentos = 20
    for i in range(num_segmentos + 1):
        angulo_atual = angulo_inicio + (angulo_fim - angulo_inicio) * (i / num_segmentos)
        x = centro_x + raio_externo * math.cos(angulo_atual)
        y = centro_y + raio_externo * math.sin(angulo_atual)
        pontos_fatia.append((x, y))

    for i in range(num_segmentos, -1, -1):
        angulo_atual = angulo_inicio + (angulo_fim - angulo_inicio) * (i / num_segmentos)
        x = centro_x + raio_interno * math.cos(angulo_atual)
        y = centro_y + raio_interno * math.sin(angulo_atual)
        pontos_fatia.append((x, y))
    
    pygame.draw.polygon(screen, cor_fatia, pontos_fatia)
    desenha_seta(screen, centro_x, centro_y, direcao_seta, tamanho_seta, largura_seta, cor_seta)
    pygame.draw.circle(screen, "#073B4C", (int(orbita_x), int(orbita_y)), 25)

    if pygame.time.get_ticks() - feedback_timer < 1000:
        texto = font.render(feedback_texto, True, (0, 0, 0))
        screen.blit(texto, (width // 2 - texto.get_width() // 2, 20))

    texto_ponto = font.render(f"Pontuação: {pontuacao}", True, (0, 0, 0))
    screen.blit(texto_ponto, (width - 150, 10))

    texto_fase = font.render(fase_texto, True, (0, 0, 0))
    screen.blit(texto_fase, (10, height - 30))

    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))  
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
