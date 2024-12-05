import pygame
from vida import Vida
from especial import Especial

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo com Vida e Especial")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# Recursos de tempo e FPS
RELOGIO = pygame.time.Clock()
FPS = 60

# Carregar a barra de vida
vida_personagem = Vida(
    max_vida=4,
    posicao=(50, 50),  # Posição da barra de vida
    tamanho_sprite=(200, 40),  # Tamanho dos sprites de vida
    pasta_sprites="sprites/vida"  # Pasta onde estão os sprites de vida
)

# Carregar o especial
especial_personagem = Especial(
    max_especial=4,  # Especial máximo
    posicao=(50, 100),  # Posição da barra especial na tela
    tamanho_sprite=(200, 40),  # Tamanho dos sprites de especial
    pasta_sprites="sprites/especial"  # Pasta onde estão os sprites de especial
)

# Texto para exibir informações
FONTE = pygame.font.Font(None, 50)

# Variáveis de controle para o estado de "Game Over"
tempo_morte = None  # Armazena o tempo em que o personagem morreu
tempo_espera_game_over = 2000  # Tempo em milissegundos para exibir "Game Over"

# Loop Principal
rodando = True
while rodando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            # Sistema de Vida
            if evento.key == pygame.K_SPACE:  # Pressione Espaço para simular dano
                vida_personagem.levar_dano(1)  # Perde 1 de vida
                if vida_personagem.vida_atual == 0 and tempo_morte is None:
                    tempo_morte = pygame.time.get_ticks()  # Marca o tempo de morte
            if evento.key == pygame.K_r:  # Pressione R para reiniciar a vida
                vida_personagem.vida_atual = vida_personagem.max_vida
                vida_personagem.atualizar_sprite()
                tempo_morte = None  # Reseta o tempo de morte

            # Sistema de Especial
            if evento.key == pygame.K_e:  # Pressione E para carregar o especial
                especial_personagem.aumentar_especial(1)
            if evento.key == pygame.K_q and especial_personagem.especial_atual == especial_personagem.max_especial:
                # Usar especial quando está carregado
                especial_personagem.especial_atual = 0  # Reinicia o especial
                especial_personagem.atualizar_sprite()

    # Lógica de Game Over
    if tempo_morte:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_morte >= tempo_espera_game_over:
            texto_game_over = FONTE.render("Game Over!", True, VERMELHO)
            TELA.fill(PRETO)
            TELA.blit(texto_game_over, (LARGURA // 2 - 100, ALTURA // 2 - 25))
            pygame.display.flip()
            pygame.time.wait(3000)
            rodando = False  # Sai do jogo

    # Atualização da Tela
    TELA.fill(PRETO)  # Limpa a tela

    # Desenhar a barra de vida e especial
    vida_personagem.desenhar(TELA)
    especial_personagem.desenhar(TELA)

    # Exibir texto indicando o status do especial
    texto_especial = FONTE.render(f"Especial: {especial_personagem.especial_atual}/{especial_personagem.max_especial}", True, BRANCO)
    TELA.blit(texto_especial, (50, 150))

    # Atualiza a tela e controla o FPS
    pygame.display.flip()
    RELOGIO.tick(FPS)

# Encerra o Pygame
pygame.quit()
