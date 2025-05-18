import pygame
import math
import random
import sys
import time
pygame.init()

# configurações da tela
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lumon Órbita")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 16)

# intro lumon
def desenha_mark(surface, x, y, expressao=None):
    pygame.draw.rect(surface, (20, 30, 60), (x + 4, y - 30, 10, 20))
    pygame.draw.rect(surface, (20, 30, 60), (x + 16, y - 30, 10, 20))
    pygame.draw.rect(surface, (10, 10, 10), (x + 4, y - 10, 10, 5))
    pygame.draw.rect(surface, (10, 10, 10), (x + 16, y - 10, 10, 5))
    pygame.draw.rect(surface, (0, 51, 102), (x, y - 70, 30, 40))
    pygame.draw.rect(surface, (255, 255, 255), (x + 12, y - 50, 6, 20))
    pygame.draw.rect(surface, (0, 51, 102), (x - 10, y - 70, 10, 25))
    pygame.draw.rect(surface, (0, 51, 102), (x + 30, y - 70, 10, 25))
    pygame.draw.circle(surface, (240, 224, 200), (x + 15, y - 85), 15)
    pygame.draw.rect(surface, (30, 30, 30), (x + 2, y - 100, 26, 10))

    cor_olho = (0, 0, 0)
    if expressao == "erro":
        cor_olho = (255, 0, 0)
    elif expressao == "bom":
        cor_olho = (255, 165, 0)
    elif expressao == "perfeito":
        cor_olho = (0, 200, 0)

    pygame.draw.circle(surface, cor_olho, (x + 9, y - 88), 2)
    pygame.draw.circle(surface, cor_olho, (x + 21, y - 88), 2)

def desenha_hud(pontuacao):
    id_func = "FUNC-" + str(7000 + pontuacao // 10)
    conformidade = min(100, pontuacao // 10)

    pygame.draw.rect(screen, (50, 50, 50), (10, 10, 120, 15))
    pygame.draw.rect(screen, (100, 200, 100), (10, 10, int(120 * conformidade / 100), 15))
    label = font.render("Conformidade", True, (0, 0, 0))
    screen.blit(label, (140, 8))

    id_text = font.render(f"ID: {id_func}", True, (0, 0, 0))
    screen.blit(id_text, (width - id_text.get_width() - 10, 35))


def mostrar_relatorio_final(pontuacao, setor):
    screen.fill((240, 240, 240))
    relatorio_font = pygame.font.SysFont("Courier New", 20, bold=True)
    id_func = "FUNC-" + str(7000 + pontuacao // 10)
    textos = [
        "RELATÓRIO FINAL - LUMON",
        f"ID do Funcionário: {id_func}",
        f"Pontuação Final: {pontuacao}",
        f"Setor Final: {setor}",
        "",
        "Seu desempenho foi satisfatório.",
        "A dor te faz inteiro.",
        "",
        "Pressione qualquer tecla para encerrar."
    ]
    for i, linha in enumerate(textos):
        texto = relatorio_font.render(linha, True, (30, 30, 30))
        rect = texto.get_rect(center=(width // 2, 80 + i * 40))
        screen.blit(texto, rect)

    pygame.display.flip()
    aguardando = True
    while aguardando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                aguardando = False
    pygame.quit()
    sys.exit()

def mostrar_intro_lumon():
    intro_font = pygame.font.SysFont("Courier New", 20, bold=True)
    intro_maior = pygame.font.SysFont("Courier New", 24, bold=True)
    COR_FUNDO = (236, 239, 244)
    COR_TEXTO = (30, 30, 30)
    COR_SOMBRA = (180, 180, 180)

    mensagens_intro = [
        "INICIANDO PROTOCOLO DE SEVERANCE...",
        "ACESSO AO EU EXTERNO: NEGADO.",
        "CREDENCIAIS DE FUNCIONÁRIO: ATIVADAS.",
        "",
        "VOCÊ AGORA É UM COLABORADOR DA LUMON.",
        "SUA PRESENÇA AQUI REPRESENTA UMA ESCOLHA.",
        "MESMO QUE VOCÊ NÃO A LEMBRE.",
        "",
        "FUNÇÃO ATRIBUÍDA: REFINAMENTO COMPORTAMENTAL.",
        "SEU DESEMPENHO SERÁ MONITORADO E REGISTRADO.",
        "",
        "O BEM DA LUMON É O BEM DE TODOS.",
        "",
        "PRESSIONE QUALQUER TECLA PARA INICIAR SUA FUNÇÃO."
    ]

    def desenhar_texto(texto, fonte, cor, y, alpha=255):
        superficie = fonte.render(texto, True, cor)
        superficie.set_alpha(alpha)
        rect = superficie.get_rect(center=(width // 2, y))
        screen.blit(superficie, rect)

    screen.fill(COR_FUNDO)
    y_inicial = height // 2 - (len(mensagens_intro) * 25) // 2
    for i, linha in enumerate(mensagens_intro):
        alpha = 0
        while alpha < 255:
            screen.fill(COR_FUNDO)
            for j in range(i + 1):
                if j < i:
                    desenhar_texto(mensagens_intro[j], intro_font, (30, 30, 30), y_inicial + j * 35)
                elif j == i:
                    desenhar_texto(linha, intro_font, (30, 30, 30), y_inicial + j * 35, alpha)
            pygame.display.flip()
            alpha += 15
            clock.tick(30)
        time.sleep(0.6)

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                esperando = False
        desenhar_texto("A Lumon agradece sua colaboração.", intro_maior, COR_SOMBRA, height - 40)
        desenha_mark(screen, width // 2 - 15, height - 30)
        pygame.display.flip()
        clock.tick(60)

mostrar_intro_lumon()

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
som_perfeito = pygame.mixer.Sound("../perfeito.wav")
som_bom = pygame.mixer.Sound("../bom.wav")
som_erro = pygame.mixer.Sound("../erro.wav")

# pontuação
pontuacao = 0

def desenha_seta(screen, x, y, direcao, tamanho, largura, cor):
    if direcao == "up":
        pontos = [(x, y - tamanho), (x - largura//2, y), (x + largura//2, y)]
    elif direcao == "down":
        pontos = [(x, y + tamanho), (x - largura//2, y), (x + largura//2, y)]
    elif direcao == "left":
        pontos = [(x - tamanho, y), (x, y - largura//2), (x, y + largura//2)]
    elif direcao == "right":
        pontos = [(x + tamanho, y), (x, y - largura//2), (x, y + largura//2)]
    pygame.draw.polygon(screen, cor, pontos)

angulo_inicio = random.uniform(0, 2 * math.pi)
angulo_fim = angulo_inicio + angulo_fatia

setas_para_direcao = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}

fase = 1
fase_texto = "Refinamento de Dados"

def atualizar_fase(pontuacao):
    global fase, velocidade_angular, fase_texto
    if pontuacao <= 300:
        fase = 1
        velocidade_angular = 0.1
        fase_texto = "Fase 1 - Refinamento de Dados"
    elif pontuacao <= 600:
        fase = 2
        velocidade_angular = 0.2
        fase_texto = "Fase 2 - Mapeamento de MacroDados"
    else:
        fase = 3
        velocidade_angular = -0.2
        fase_texto = "Fase 3 - Sala de Quebra"

# main
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in setas_para_direcao:
                if setas_para_direcao[event.key] == direcao_seta:
                    angulo_bolinha = angulo % (2 * math.pi)
                    inicio = angulo_inicio % (2 * math.pi)
                    fim = (angulo_inicio + angulo_fatia) % (2 * math.pi)

                    if inicio < fim:
                        dentro_da_fatia = inicio <= angulo_bolinha <= fim
                    else:
                        dentro_da_fatia = angulo_bolinha >= inicio or angulo_bolinha <= fim

                    if dentro_da_fatia:
                        centro_fatia = (inicio + (angulo_fatia / 2)) % (2 * math.pi)
                        angulo_bolinha_graus = math.degrees(angulo_bolinha)
                        centro_fatia_graus = math.degrees(centro_fatia)
                        distancia = abs((angulo_bolinha_graus - centro_fatia_graus + 180) % 360 - 180)

                        if distancia < 15:
                            feedback_texto = "Perfeito!"
                            som_perfeito.play()
                            pontuacao += 100
                        else:
                            feedback_texto = "Bom!"
                            som_bom.play()
                            pontuacao += 50
                    else:
                        feedback_texto = "Erro!"
                        som_erro.play()

                    feedback_timer = pygame.time.get_ticks()
                    percentual_fatia = random.uniform(0.05, 0.3)
                    angulo_fatia = 2 * math.pi * percentual_fatia
                    angulo_inicio = random.uniform(0, 2 * math.pi)
                    angulo_fim = angulo_inicio + angulo_fatia
                    direcao_seta = random.choice(["up", "down", "left", "right"])
                else:
                    feedback_texto = "Erro!"
                    som_erro.play()
                    feedback_timer = pygame.time.get_ticks()
                    pygame.time.wait(1000)

    atualizar_fase(pontuacao)

    if pontuacao >= 1000:
        mostrar_relatorio_final(pontuacao, fase_texto)

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
    screen.blit(fps_text, (10, 30))

    desenha_hud(pontuacao)
    desenha_mark(screen, width - 60, height - 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
