import pygame
from especial import Especial  # Importa a classe Especial do arquivo 'especial.py'

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sistema de Especial")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Recursos de tempo e FPS
RELOGIO = pygame.time.Clock()
FPS = 60

# Carregar o especial
especial_personagem = Especial(
    max_especial=4,  # Especial máximo
    posicao=(50, 100),  # Posição da barra especial na tela
    tamanho_sprite=(200, 40),  # Tamanho dos sprites de especial
    pasta_sprites="sprites/especial"  # Pasta onde estão os sprites de especial
)

# Texto para exibir informações
FONTE = pygame.font.Font(None, 50)

# Loop Principal
rodando = True
while rodando:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e:  # Pressione E para carregar o especial
                especial_personagem.aumentar_especial(1)
            if evento.key == pygame.K_q and especial_personagem.especial_atual == especial_personagem.max_especial:
                # Usar especial quando está carregado
                especial_personagem.especial_atual = 0  # Reinicia o especial
                especial_personagem.atualizar_sprite()

    # Atualização da Tela
    TELA.fill(PRETO)  # Limpa a tela

    # Desenhar a barra de especial
    especial_personagem.desenhar(TELA)

    # Exibir texto indicando o status do especial
    texto_especial = FONTE.render(f"Especial: {especial_personagem.especial_atual}/{especial_personagem.max_especial}", True, BRANCO)
    TELA.blit(texto_especial, (50, 50))

    # Atualiza a tela e controla o FPS
    pygame.display.flip()
    RELOGIO.tick(FPS)

# Encerra o Pygame
pygame.quit()
