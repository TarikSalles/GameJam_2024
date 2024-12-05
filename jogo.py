import pygame
from Personagem import Personagem
from fim import exibir_tela_fim_jogo

# Inicialização do Pygame
pygame.init()

# Definir a resolução mínima da tela
LARGURA_MINIMA, ALTURA_MINIMA = 1280, 720  # Resolução mínima
LARGURA_INICIAL, ALTURA_INICIAL = 1920, 1080  # Resolução inicial
TELA = pygame.display.set_mode((LARGURA_INICIAL, ALTURA_INICIAL), pygame.RESIZABLE)
pygame.display.set_caption("Jogo com Vida e Especial")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Recursos de tempo e FPS
RELOGIO = pygame.time.Clock()
FPS = 60

# Fonte para textos
FONTE = pygame.font.Font(None, 50)

# Carregar o fundo
background = pygame.image.load("./sprites/tela/background.png")

# Função para redimensionar o fundo
def redimensionar_fundo(tela_largura, tela_altura):
    return pygame.transform.scale(background, (tela_largura, tela_altura))

# Função para redimensionar os personagens e suas barras
def redimensionar_personagens(personagens, tela_largura, tela_altura):
    fator_largura = tela_largura / LARGURA_INICIAL
    fator_altura = tela_altura / ALTURA_INICIAL
    for p in personagens:
        # Atualiza o tamanho desejado dos personagens, mas mantém a posição x
        nova_largura = int(p.tamanho_desejada[0] * fator_largura)
        nova_altura = int(p.tamanho_desejada[1] * fator_altura)
        p.tamanho_desejada = (nova_largura, nova_altura)  # Atualiza o tamanho desejado
        p.posicao = (
            p.posicao[0],  # Mantém a posição x original
            p.posicao[1]   # Mantém a posição y original
        )
        
        # Atualiza a posição das barras de vida e especial com base no novo tamanho e posição do personagem
        p.vida.posicao = (p.posicao[0], p.posicao[1] - 30)  # Ajuste a posição vertical conforme necessário
        p.especial.posicao = (p.posicao[0], p.posicao[1] - 60)  # Ajuste a posição vertical conforme necessário

# Definir um pequeno deslocamento para a esquerda e direita do centro
deslocamento_esquerda = -150  # Personagem 1 ficará um pouco à esquerda
deslocamento_direita = 100    # Personagem 2 ficará um pouco à direita
tela_largura = pygame.display.get_surface().get_width()

jogador1 = "Biker"
jogador2 = "Punk"

# Criação dos personagens com a nova posição
personagem1 = Personagem(
    posicao_personagem=((tela_largura // 2) + deslocamento_esquerda, 300),
    tamanho_personagem=(200, 300),
    caminho_sprites="sprites/personagem/Jogador_1/",
    nome_personagem=jogador1,
)

personagem2 = Personagem(
    posicao_personagem=((tela_largura // 2) + deslocamento_direita, 300),
    tamanho_personagem=(200, 300),
    caminho_sprites="sprites/personagem/Jogador_2/",
    nome_personagem=jogador2,
    invert_frames=True
)


# Lista de personagens para redimensionamento fácil
personagens = [personagem1, personagem2]

# Variáveis de controle para o estado de "Game Over"
tempo_morte_p1 = None
tempo_morte_p2 = None
tempo_espera_game_over = 2000
vencedor = None

# Flags para controlar a aplicação de dano após ataque
ataque_personagem1 = False
ataque_personagem2 = False

# Loop Principal
rodando = True
while rodando:
    delta_tempo = RELOGIO.tick(FPS) / 1000.0  # Delta de tempo em segundos

    # Redimensionamento dinâmico da tela
    tela_largura, tela_altura = TELA.get_size()
    tela_largura = max(tela_largura, LARGURA_MINIMA)  # Garantir a largura mínima
    tela_altura = max(tela_altura, ALTURA_MINIMA)    # Garantir a altura mínima
    fundo_redimensionado = redimensionar_fundo(tela_largura, tela_altura)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            # Controle do Personagem 1
            if evento.key == pygame.K_SPACE:  # Pressione Espaço para simular dano
                personagem2.atacar()
                ataque_personagem2 = True
                if personagem1.vida.vida_atual == 0 and tempo_morte_p1 is None:
                    tempo_morte_p1 = pygame.time.get_ticks()
            if evento.key == pygame.K_r:  # Pressione R para reiniciar a vida
                personagem1.vida.vida_atual = personagem1.vida.max_vida
                personagem1.vida.atualizar_sprite()
                tempo_morte_p1 = None

            if evento.key == pygame.K_e:  # Pressione E para carregar o especial
                personagem1.especial.aumentar_especial(1)
            if evento.key == pygame.K_q and personagem1.especial.especial_atual == personagem1.especial.max_especial:
                personagem1.especial.especial_atual = 0
                personagem1.especial.atualizar_sprite()

            # Controle do Personagem 2
            if evento.key == pygame.K_f:  # Pressione F para o personagem1 atacar
                personagem1.atacar()
                ataque_personagem1 = True  # Indica que o ataque foi iniciado
                if personagem2.vida.vida_atual == 0 and tempo_morte_p2 is None:
                    tempo_morte_p2 = pygame.time.get_ticks()
            if evento.key == pygame.K_t:  # Pressione T para reiniciar a vida
                personagem2.vida.vida_atual = personagem2.vida.max_vida
                personagem2.vida.atualizar_sprite()
                tempo_morte_p2 = None

            if evento.key == pygame.K_g:  # Pressione G para carregar o especial
                personagem2.especial.aumentar_especial(1)
            if evento.key == pygame.K_h and personagem2.especial.especial_atual == personagem2.especial.max_especial:
                personagem2.especial.especial_atual = 0
                personagem2.especial.atualizar_sprite()

    # Atualização dos personagens
    personagem1.atualizar(delta_tempo)
    personagem2.atualizar(delta_tempo)

    # Aplicação de dano após o ataque completar
    if ataque_personagem1 and not personagem1.em_ataque:
        personagem2.levar_dano(1)  # Aplica dano ao personagem2
        ataque_personagem1 = False  # Reseta a flag
        
    elif ataque_personagem2 and not personagem2.em_ataque:
        personagem1.levar_dano(1)
        ataque_personagem2 = False

    # Redimensiona os personagens com base no tamanho da tela
    redimensionar_personagens(personagens, tela_largura, tela_altura)

    # Desenho na tela
    TELA.blit(fundo_redimensionado, (0, 0))  # Desenha o fundo
    personagem1.desenhar(TELA)
    personagem2.desenhar(TELA)

    # Verificação de "Game Over" para Personagem 1
    if personagem1.vida.vida_atual == 0:
        if tempo_morte_p1 and pygame.time.get_ticks() - tempo_morte_p1 > tempo_espera_game_over:
            vencedor = '2'
            rodando = False
    else:
        tempo_morte_p1 = None

    # Verificação de "Game Over" para Personagem 2
    if personagem2.vida.vida_atual == 0:
        if tempo_morte_p2 and pygame.time.get_ticks() - tempo_morte_p2 > tempo_espera_game_over:
            vencedor = '1'
            rodando = False
    else:
        tempo_morte_p2 = None
    
    if not rodando:
        exibir_tela_fim_jogo(TELA, vencedor)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()