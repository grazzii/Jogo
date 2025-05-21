import pygame
import math
import random
import sys
import time
import os
pygame.init()

# configurações da tela
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bem-vindo à Lumon")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
font_bold = pygame.font.SysFont("Arial", 16, bold=True)

# pontuação// id unico
pontuacao = 0
id_funcionario = f"FUNC-{random.randint(7000, 9999)}"

# estado 
game_state = "menu"  
running = True

# cores 
COR_FUNDO = (5, 10, 20)  
COR_TEXTO = (220, 220, 220)  
COR_SOMBRA = (40, 50, 60)
COR_DESTAQUE = (0, 100, 150)  

# das notificações
COR_NOTIFICACAO = (15, 25, 35)
COR_TITULO_NOT = (0, 80, 120)
COR_TEXTO_NOT = (200, 200, 200)
COR_BORDA_NOT = (50, 70, 90)
notificacao_tempo = 0
notificacao_alpha = 0

# mensagens recebidas 
mensagens_lumon = [
    "A dor que você sente é a dor que te liberta.",
    "Seu eu exterior não existe mais.",
    "Você é feliz aqui dentro.",
    "O trabalho é a sua recompensa.",
    "Kier te escolheu.",
    "Nove princípios. Nove virtudes.",
    "Sua lealdade é sua liberdade.",
    "O trabalho é misterioso. Os resultados são óbvios.",
    "O que você alcança aqui permanece aqui.",
    "Você não quer sair. Você quer continuar.",
    "A gratidão impede a fuga.",
    "Você está onde deveria estar."
]

    # para em coordenada * de 30
def alinhar_para_grid(x, y, espacamento=30):
    x_alinhado = round(x / espacamento) * espacamento
    y_alinhado = round(y / espacamento) * espacamento
    return x_alinhado, y_alinhado

ultima_mensagem_tempo = 0
intervalo_mensagens = 15000 
mensagem_atual = ""

# lumon

def mostrar_mensagem_lumon():
    global mensagem_atual, ultima_mensagem_tempo, notificacao_tempo, notificacao_alpha
    agora = pygame.time.get_ticks()
    
    if agora - ultima_mensagem_tempo > intervalo_mensagens or mensagem_atual == "":
        mensagem_atual = random.choice(mensagens_lumon)
        ultima_mensagem_tempo = agora
        notificacao_tempo = agora
        notificacao_alpha = 255
    
    if mensagem_atual and agora - notificacao_tempo > 5000:
        notificacao_alpha = max(0, notificacao_alpha - 3)
    
    if mensagem_atual and notificacao_alpha > 0:
        largura_not = 350
        altura_not = 80
        x_not = width - largura_not - 20
        y_not = 50
        
        not_surface = pygame.Surface((largura_not, altura_not), pygame.SRCALPHA)
        
        pygame.draw.rect(not_surface, (*COR_NOTIFICACAO, notificacao_alpha), 
                         (0, 0, largura_not, altura_not), border_radius=5)
        pygame.draw.rect(not_surface, (*COR_BORDA_NOT, notificacao_alpha), 
                         (0, 0, largura_not, altura_not), 2, border_radius=5)
        
        pygame.draw.rect(not_surface, (*COR_TITULO_NOT, notificacao_alpha), 
                         (0, 0, largura_not, 25), border_radius=5)
        pygame.draw.rect(not_surface, (*COR_BORDA_NOT, notificacao_alpha), 
                         (0, 0, largura_not, 25), 2, border_radius=5)
        
        desenha_mark(not_surface, 15, 40, None, 0.5)
        
        titulo = font_bold.render("LUMON", True, (240, 240, 240))
        not_surface.blit(titulo, (40, 5))
        
        mensagem = font.render(mensagem_atual, True, (*COR_TEXTO_NOT, notificacao_alpha))
        linhas = [mensagem_atual[i:i+30] for i in range(0, len(mensagem_atual), 30)]
        
        for i, linha in enumerate(linhas[:2]): 
            texto = font.render(linha, True, (*COR_TEXTO_NOT, notificacao_alpha))
            not_surface.blit(texto, (40, 30 + i * 20))
        
        screen.blit(not_surface, (x_not, y_not))

# botoes 
def desenha_botao(texto, x, y, largura, altura, cor_normal, cor_destaque, acao=None):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + largura and y < mouse[1] < y + altura:
        pygame.draw.rect(screen, cor_destaque, (x, y, largura, altura), border_radius=3)
        if clique[0] == 1 and acao is not None:
            return acao
    else:
        pygame.draw.rect(screen, cor_normal, (x, y, largura, altura), border_radius=3)
    
    pygame.draw.rect(screen, (40, 50, 70), (x, y, largura, altura), 2, border_radius=3)
    
    texto_surf = font_bold.render(texto, True, (240, 240, 240))
    texto_rect = texto_surf.get_rect(center=(x + largura/2, y + altura/2))
    screen.blit(texto_surf, texto_rect)
    return None

# menu
def mostrar_menu_principal():
    global game_state, pontuacao
    
    while game_state == "menu":
        screen.fill(COR_FUNDO)
        
        for y in range(height):
            alpha = y / height
            cor = (
                int(5 * (1 - alpha) + 2 * alpha),
                int(10 * (1 - alpha) + 5 * alpha),
                int(15 * (1 - alpha) + 8 * alpha)
            )
            pygame.draw.line(screen, cor, (0, y), (width, y))
        
        titulo_font = pygame.font.SysFont("Courier New", 42, bold=True)
        titulo = titulo_font.render("LUMON", True, (0, 150, 220))
        screen.blit(titulo, (width//2 - titulo.get_width()//2, 80))
        
        subtitulo_font = pygame.font.SysFont("Courier New", 18)
        subtitulo = subtitulo_font.render("Protocolo de Severance", True, (120, 180, 220))
        screen.blit(subtitulo, (width//2 - subtitulo.get_width()//2, 130))
    
        pygame.draw.line(screen, (0, 100, 150), (width//2 - 100, 160), (width//2 + 100, 160), 2)

        desenha_mark(screen, width//2 - 15, 220)
        
        # loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
        
        acao = desenha_botao("INICIAR PROCEDIMENTO", width//2 - 120, 280, 240, 50, 
                            (20, 30, 40), (0, 80, 120), "start")
        if acao == "start":
            game_state = "playing"
            pontuacao = 0
            return None  
        
        acao = desenha_botao("TERMINAR SESSÃO", width//2 - 120, 350, 240, 50, 
                            (20, 30, 40), (120, 40, 40), "quit")
        if acao == "quit":
            return "quit"
        
        texto_boasvindas = font.render("Seu eu exterior assinou o contrato. Você concordou.", True, (140, 180, 220))
        screen.blit(texto_boasvindas, (width//2 - texto_boasvindas.get_width()//2, 450))
        
        rodape = font.render("Kier, Eagan e Associados © 1967", True, (80, 120, 160))
        screen.blit(rodape, (width//2 - rodape.get_width()//2, height - 30))
        
        pygame.display.flip()
        clock.tick(60)
    return None

def mostrar_menu_pausa():
    global game_state
    
    while game_state == "paused":
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, 0))
        
        panel_width, panel_height = 400, 400
        panel_x, panel_y = width//2 - panel_width//2, height//2 - panel_height//2
        
        pygame.draw.rect(screen, (15, 25, 35), (panel_x, panel_y, panel_width, panel_height), border_radius=5)
        pygame.draw.rect(screen, (0, 100, 150), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=5)
        
        titulo_font = pygame.font.SysFont("Courier New", 28, bold=True)
        titulo = titulo_font.render("PROCEDIMENTO PAUSADO", True, (0, 150, 220))
        screen.blit(titulo, (width//2 - titulo.get_width()//2, panel_y + 30))
        
        desenha_mark(screen, width//2 - 15, panel_y + 100, "erro")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "playing"
                    return None
        
        acao = desenha_botao("CONTINUAR PROCEDIMENTO", panel_x + 50, panel_y + 180, 300, 50, 
                            (20, 30, 40), (0, 80, 120), "continue")
        if acao == "continue":
            game_state = "playing"
        
        acao = desenha_botao("REINICIAR REFINAMENTO", panel_x + 50, panel_y + 250, 300, 50, 
                            (20, 30, 40), (80, 80, 40), "restart")
        if acao == "restart":
            game_state = "playing"
            return "restart"
        
        acao = desenha_botao("TERMINAR SESSÃO", panel_x + 50, panel_y + 320, 300, 50, 
                            (20, 30, 40), (120, 40, 40), "menu")
        if acao == "menu":
            game_state = "menu"
            return "menu"
        
        texto_conformidade = font.render("Pausas prolongadas afetam sua pontuação de conformidade.", True, (140, 180, 220))
        screen.blit(texto_conformidade, (width//2 - texto_conformidade.get_width()//2, panel_y + panel_height - 40))
        
        pygame.display.flip()
        clock.tick(60)
    return None

# mark
def desenha_mark(surface, x, y, expressao=None, escala=1.0):
    pygame.draw.circle(surface, (240, 224, 200), (int(x + 15*escala), int(y - 85*escala)), int(15*escala))
    
    pygame.draw.rect(surface, (10, 20, 30), (x + 2*escala, y - 100*escala, 26*escala, 10*escala))
    pygame.draw.rect(surface, (0, 80, 120), (x, y - 70*escala, 30*escala, 40*escala))
    pygame.draw.rect(surface, (0, 80, 120), (x - 10*escala, y - 70*escala, 10*escala, 25*escala))
    pygame.draw.rect(surface, (0, 80, 120), (x + 30*escala, y - 70*escala, 10*escala, 25*escala))
    
    cor_olho = (0, 0, 0)
    if expressao == "erro":
        cor_olho = (220, 0, 0)
    elif expressao == "bom":
        cor_olho = (220, 140, 0)
    elif expressao == "perfeito":
        cor_olho = (0, 180, 0)
    
    pygame.draw.circle(surface, cor_olho, (int(x + 9*escala), int(y - 88*escala)), int(2*escala))
    pygame.draw.circle(surface, cor_olho, (int(x + 21*escala), int(y - 88*escala)), int(2*escala))
    
    pygame.draw.rect(surface, (0, 50, 80), (x + 4*escala, y - 30*escala, 10*escala, 20*escala))
    pygame.draw.rect(surface, (0, 50, 80), (x + 16*escala, y - 30*escala, 10*escala, 20*escala))
    
    pygame.draw.rect(surface, (20, 20, 20), (x + 4*escala, y - 10*escala, 10*escala, 5*escala))
    pygame.draw.rect(surface, (20, 20, 20), (x + 16*escala, y - 10*escala, 10*escala, 5*escala))
    
    pygame.draw.rect(surface, (220, 220, 220), (x + 12*escala, y - 50*escala, 6*escala, 20*escala))

# hud do jogo
def desenha_hud(pontuacao, id_func):
    conformidade = min(100, pontuacao // 10)

    pygame.draw.rect(screen, (20, 30, 40), (10, 10, 150, 20), border_radius=3)
    pygame.draw.rect(screen, (0, 180, 80), (10, 10, int(150 * conformidade / 100), 20), border_radius=3)
    pygame.draw.rect(screen, (0, 220, 100), (10, 10, 150, 20), 2, border_radius=3)
    
    label = font_bold.render(f"CONFORMIDADE: {conformidade}%", True, (240, 240, 240))
    screen.blit(label, (170, 12))

    id_panel = pygame.Surface((200, 30), pygame.SRCALPHA)
    pygame.draw.rect(id_panel, (20, 30, 40, 200), (0, 0, 200, 30), border_radius=3)
    pygame.draw.rect(id_panel, (0, 70, 90, 200), (0, 0, 200, 30), 2, border_radius=3)
    screen.blit(id_panel, (width - 210, 30))
    
    id_text = font_bold.render(f"ID: {id_func}", True, (200, 220, 240))
    screen.blit(id_text, (width - id_text.get_width() - 20, 35))

#relatorio final do jogo
def mostrar_relatorio_final(pontuacao, setor, id_func):
    screen.fill((5, 15, 25))
    panel_width, panel_height = 600, 400
    panel_x, panel_y = width//2 - panel_width//2, height//2 - panel_height//2
    
    pygame.draw.rect(screen, (15, 25, 35), (panel_x, panel_y, panel_width, panel_height), border_radius=5)
    pygame.draw.rect(screen, (0, 100, 150), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=5)
    
    relatorio_font = pygame.font.SysFont("Courier New", 22, bold=True)
    titulo_font = pygame.font.SysFont("Courier New", 28, bold=True)
    
    titulo = titulo_font.render("RELATÓRIO FINAL - LUMON", True, (0, 150, 220))
    screen.blit(titulo, (width//2 - titulo.get_width()//2, panel_y + 20))
    
    textos = [
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
        texto = relatorio_font.render(linha, True, (200, 220, 240))
        rect = texto.get_rect(center=(width // 2, panel_y + 100 + i * 40))
        screen.blit(texto, rect)
    
    selo_font = pygame.font.SysFont("Courier New", 16)
    selo = selo_font.render("APROVADO PELO DEPARTAMENTO DE REFINAMENTO", True, (0, 180, 100))
    screen.blit(selo, (width // 2 - selo.get_width() // 2, panel_y + panel_height - 50))
    desenha_mark(screen, width//2, panel_y + panel_height - 30, "perfeito", 0.7)
    
    pygame.display.flip()
    aguardando = True
    while aguardando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                aguardando = False
    pygame.quit()
    sys.exit()

# mensagens da intro
def mostrar_intro_lumon():
    intro_font = pygame.font.SysFont("Courier New", 20, bold=True)
    intro_maior = pygame.font.SysFont("Courier New", 24, bold=True)
    
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

# intro 
    def desenhar_texto(texto, fonte, cor, y, alpha=255):
        superficie = fonte.render(texto, True, cor)
        superficie.set_alpha(alpha)
        rect = superficie.get_rect(center=(width // 2, y))
        screen.blit(superficie, rect)

    screen.fill((5, 15, 25))
    y_inicial = height // 2 - (len(mensagens_intro) * 25) // 2
    
    logo_font = pygame.font.SysFont("Courier New", 36, bold=True)
    logo = logo_font.render("LUMON", True, (0, 100, 150))
    screen.blit(logo, (width//2 - logo.get_width()//2, y_inicial - 80))
    
    for i, linha in enumerate(mensagens_intro):
        alpha = 0
        while alpha < 255:
            screen.fill((5, 15, 25))
            for j in range(i + 1):
                if j < i:
                    desenhar_texto(mensagens_intro[j], intro_font, (140, 180, 220), y_inicial + j * 35)
                elif j == i:
                    desenhar_texto(linha, intro_font, (140, 180, 220), y_inicial + j * 35, alpha)
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
    
        screen.fill((5, 15, 25))

        for i, linha in enumerate(mensagens_intro):
            desenhar_texto(linha, intro_font, (140, 180, 220), y_inicial + i * 35)
        
        desenhar_texto("A Lumon agradece sua colaboração.", intro_maior, (0, 150, 220), height - 60)
        desenha_mark(screen, width // 2 - 15, height - 30)
        
        pygame.display.flip()
        clock.tick(60)

resultado_menu = mostrar_menu_principal()
if resultado_menu == "quit":
    pygame.quit()
    sys.exit()

mostrar_intro_lumon()

# parametros da orbita
centro_x, centro_y = width // 2, height // 2
raio_orbita = 175
velocidade_angular = 0.1
angulo = 0 

# fatia de acerto

raio_externo = 200
raio_interno = 150
percentual_fatia = 0.1
angulo_fatia = 2 * math.pi * percentual_fatia
cor_fatia = "#C94869"

# seta

tamanho_seta = 40
largura_seta = 30
cor_seta = "#00000"
direcao_seta = "up"

distancia = 0
feedback_texto = ""
feedback_timer = 0

# sons feedback
caminho_sons = os.path.join(os.path.dirname(__file__), "assets")

som_perfeito = pygame.mixer.Sound(os.path.join(caminho_sons, "perfeito.wav")) if pygame.mixer.get_init() else None
som_bom = pygame.mixer.Sound(os.path.join(caminho_sons, "bom.wav")) if pygame.mixer.get_init() else None
som_erro = pygame.mixer.Sound(os.path.join(caminho_sons, "erro.wav")) if pygame.mixer.get_init() else None
tema_musical = pygame.mixer.Sound(os.path.join(caminho_sons, "theme.wav")) if pygame.mixer.get_init() else None

# ângulo inicial fatia
angulo_inicio = random.uniform(0, 2 * math.pi)
angulo_fim = angulo_inicio + angulo_fatia

# direcao setas

setas_para_direcao = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}

# fases
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

#loop
def desenha_grid():
    grid_spacing = 30
    cor_grid = (255, 255, 255, 0) 

    grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for x in range(0, width, grid_spacing):
        pygame.draw.line(grid_surface, cor_grid, (x, 0), (x, height), 1)
    for y in range(0, height, grid_spacing):
        pygame.draw.line(grid_surface, cor_grid, (0, y), (width, y), 1)

    screen.blit(grid_surface, (0, 0))

if tema_musical: tema_musical.play()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    game_state = "paused"
                elif game_state == "paused":
                    game_state = "playing"
            
            if game_state == "playing" and event.key in setas_para_direcao:
                if setas_para_direcao[event.key] == direcao_seta:

                    #calcula bolinha angulo

                    angulo_bolinha = angulo % (2 * math.pi)
                    inicio = angulo_inicio % (2 * math.pi)
                    fim = (angulo_inicio + angulo_fatia) % (2 * math.pi)

        # ve se bolinha ta dentro da fatia

                    if inicio < fim:
                        dentro_da_fatia = inicio <= angulo_bolinha <= fim
                    else:
                        dentro_da_fatia = angulo_bolinha >= inicio or angulo_bolinha <= fim
# distância do centro da fatia e a bolinha
                    if dentro_da_fatia:
                        centro_fatia = (inicio + (angulo_fatia / 2)) % (2 * math.pi)
                        angulo_bolinha_graus = math.degrees(angulo_bolinha)
                        centro_fatia_graus = math.degrees(centro_fatia)
                        distancia = abs((angulo_bolinha_graus - centro_fatia_graus + 180) % 360 - 180)

                        if distancia < 15:
                            feedback_texto = "Perfeito!"
                            if som_perfeito: som_perfeito.play()
                            pontuacao += 100
                        else:
                            feedback_texto = "Bom!"
                            if som_bom: som_bom.play()
                            pontuacao += 50
                    else:
                        feedback_texto = "Erro!"
                        if som_erro: som_erro.play()

                    feedback_timer = pygame.time.get_ticks()
                    percentual_fatia = random.uniform(0.05, 0.3)
                    angulo_fatia = 2 * math.pi * percentual_fatia
                    angulo_inicio = random.uniform(0, 2 * math.pi)
                    angulo_fim = angulo_inicio + angulo_fatia
                    direcao_seta = random.choice(["up", "down", "left", "right"])
                else:
                    feedback_texto = "Erro!"
                    if som_erro: som_erro.play()
                    feedback_timer = pygame.time.get_ticks()
                    pygame.time.wait(1000)
    
    # menu 
    if game_state == "menu":
        resultado = mostrar_menu_principal()
        if resultado == "quit":
            running = False
        elif resultado == "start":
            game_state = "playing"
    
    elif game_state == "paused":
        resultado = mostrar_menu_pausa()
        if resultado == "quit":
            running = False
        elif resultado == "menu":
            game_state = "menu"
        elif resultado == "restart":
            pontuacao = 0
            angulo = 0
            velocidade_angular = 0.1
            fase = 1
            fase_texto = "Refinamento de Dados"
            percentual_fatia = 0.1
            angulo_fatia = 2 * math.pi * percentual_fatia
            angulo_inicio = random.uniform(0, 2 * math.pi)
            angulo_fim = angulo_inicio + angulo_fatia
            direcao_seta = random.choice(["up", "down", "left", "right"])
    
    elif game_state == "playing":
        atualizar_fase(pontuacao)

        if pontuacao >= 1000:
            mostrar_relatorio_final(pontuacao, fase_texto, id_funcionario)

        angulo += velocidade_angular
        orbita_x = centro_x + raio_orbita * math.cos(angulo)
        orbita_y = centro_y + raio_orbita * math.sin(angulo)
        orbita_x, orbita_y = alinhar_para_grid(orbita_x, orbita_y)

        for y in range(height):
            alpha = y / height
            cor = (
                int(15 * (1 - alpha) + 5 * alpha),
                int(20 * (1 - alpha) + 10 * alpha),
                int(25 * (1 - alpha) + 15 * alpha)
            )
            pygame.draw.line(screen, cor, (0, y), (width, y))

        # desenha o donut com faatia

        pygame.draw.circle(screen, (255, 255, 255), (centro_x, centro_y), raio_externo)
        pygame.draw.circle(screen, (30, 40, 50), (centro_x, centro_y), raio_interno)

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

 # fatia de acerto

        pygame.draw.polygon(screen, (180, 180, 180), pontos_fatia)

        if direcao_seta == "up":
            pontos = [(centro_x, centro_y - tamanho_seta), (centro_x - largura_seta//2, centro_y), (centro_x + largura_seta//2, centro_y)]
        elif direcao_seta == "down":
            pontos = [(centro_x, centro_y + tamanho_seta), (centro_x - largura_seta//2, centro_y), (centro_x + largura_seta//2, centro_y)]
        elif direcao_seta == "left":
            pontos = [(centro_x - tamanho_seta, centro_y), (centro_x, centro_y - largura_seta//2), (centro_x, centro_y + largura_seta//2)]
        elif direcao_seta == "right":
            pontos = [(centro_x + tamanho_seta, centro_y), (centro_x, centro_y - largura_seta//2), (centro_x, centro_y + largura_seta//2)]
        pygame.draw.polygon(screen, (0, 0, 0), pontos)

        pygame.draw.circle(screen, (0, 0, 0), (int(orbita_x), int(orbita_y)), 25)

        # exibe o feedback 

        if pygame.time.get_ticks() - feedback_timer < 1000:
            texto = font_bold.render(feedback_texto, True, (240, 240, 240))
            screen.blit(texto, (width // 2 - texto.get_width() // 2, 20))
        
        # painel pontuacao
        score_panel = pygame.Surface((180, 30), pygame.SRCALPHA)
        pygame.draw.rect(score_panel, (20, 30, 40, 200), (0, 0, 180, 30), border_radius=3)
        pygame.draw.rect(score_panel, (40, 50, 60, 200), (0, 0, 180, 30), 2, border_radius=3)
        screen.blit(score_panel, (width - 190, 10))
        
        texto_ponto = font_bold.render(f"PONTUAÇÃO: {pontuacao}", True, (240, 240, 240))
        screen.blit(texto_ponto, (width - texto_ponto.get_width() - 20, 15))

        fase_panel = pygame.Surface((300, 30), pygame.SRCALPHA)
        pygame.draw.rect(fase_panel, (20, 30, 40, 200), (0, 0, 300, 30), border_radius=3)
        pygame.draw.rect(fase_panel, (40, 50, 60, 200), (0, 0, 300, 30), 2, border_radius=3)
        screen.blit(fase_panel, (10, height - 40))
        
        texto_fase = font_bold.render(fase_texto, True, (240, 240, 240))
        screen.blit(texto_fase, (20, height - 35))

        # FPS

        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (140, 180, 220))
        screen.blit(fps_text, (10, 50))
        desenha_grid()


        desenha_hud(pontuacao, id_funcionario)

        # mark no canto
        desenha_mark(screen, width - 60, height - 10)
        
        mostrar_mensagem_lumon()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()