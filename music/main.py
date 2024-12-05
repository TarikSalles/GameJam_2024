import pygame
import random

# Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Música - Sequência de Setas")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Configurações de fonte
FONTE = pygame.font.Font(None, 50)

# Configurações do jogo
FPS = 60
RELOGIO = pygame.time.Clock()

# Recursos de setas
SETAS = ["UP", "DOWN", "LEFT", "RIGHT"]
IMAGENS_SETAS = {
    "UP": pygame.image.load("music/seta/seta_up.png"),
    "DOWN": pygame.image.load("music/seta/seta_down.png"),
    "LEFT": pygame.image.load("music/seta/seta_left.png"),
    "RIGHT": pygame.image.load("music/seta/seta_right.png"),
}

# Redimensionar as imagens das setas
for key in IMAGENS_SETAS:
    IMAGENS_SETAS[key] = pygame.transform.scale(IMAGENS_SETAS[key], (50, 50))

# Função para gerar sequência de setas
def gerar_sequencia(tamanho):
    return [random.choice(SETAS) for _ in range(tamanho)]

# Função para desenhar as setas
def desenhar_sequencia(sequencia, posicoes, cor=BRANCO):
    for i, seta in enumerate(sequencia):
        TELA.blit(IMAGENS_SETAS[seta], posicoes[i])

# Função principal
def jogo_musical():
    rodando = True
    sequencia = gerar_sequencia(5)  # Começa com 5 setas
    posicoes = [(100 + i * 120, ALTURA // 2 - 25) for i in range(len(sequencia))]
    indice_atual = 0
    pontos = 0
    timer = 3  # Tempo entre sequências em segundos
    tempo_inicio = pygame.time.get_ticks()

    while rodando:
        TELA.fill(PRETO)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                tecla = None
                if evento.key == pygame.K_UP:
                    tecla = "UP"
                elif evento.key == pygame.K_DOWN:
                    tecla = "DOWN"
                elif evento.key == pygame.K_LEFT:
                    tecla = "LEFT"
                elif evento.key == pygame.K_RIGHT:
                    tecla = "RIGHT"

                if tecla:
                    # Verificar se a tecla está correta
                    if tecla == sequencia[indice_atual]:
                        pontos += 1
                        indice_atual += 1
                    else:
                        rodando = False  # Game over

        # Desenhar sequência
        desenhar_sequencia(sequencia, posicoes)

        # Checar se o jogador completou a sequência
        if indice_atual >= len(sequencia):
            sequencia = gerar_sequencia(len(sequencia) + 1)
            posicoes = [(100 + i * 120, ALTURA // 2 - 25) for i in range(len(sequencia))]
            indice_atual = 0
            pontos += 5  # Bônus por completar
            tempo_inicio = pygame.time.get_ticks()

        # Exibir pontuação
        texto_pontos = FONTE.render(f"Pontos: {pontos}", True, BRANCO)
        TELA.blit(texto_pontos, (10, 10))

        # Atualizar tela
        pygame.display.flip()
        RELOGIO.tick(FPS)

    # Fim de jogo
    TELA.fill(PRETO)
    texto_game_over = FONTE.render("Game Over!", True, VERMELHO)
    texto_final = FONTE.render(f"Pontos Finais: {pontos}", True, BRANCO)
    TELA.blit(texto_game_over, (LARGURA // 2 - 100, ALTURA // 2 - 50))
    TELA.blit(texto_final, (LARGURA // 2 - 130, ALTURA // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000)

# Executar o jogo
jogo_musical()
pygame.quit()
