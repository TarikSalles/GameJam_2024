import pygame
from Personagem import Personagem

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
LARGURA, ALTURA = 1920, 1080  # Ajustei para uma resolução mais comum
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo com Vida e Especial")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Recursos de tempo e FPS
RELOGIO = pygame.time.Clock()
FPS = 60

# Fonte para textos
FONTE = pygame.font.Font(None, 50)

# Criação dos personagens com posição e tamanho
personagem1 = Personagem(
    posicao_personagem=(200, 300),
    tamanho_personagem=(200, 300),
    max_vida=10,
    max_especial=10,
    pasta_sprites_vida="sprites/vida",
    pasta_sprites_especial="sprites/especial",
    caminho_sprites="sprites/personagem/Jogador_1/",  # Verifique se está correto
    nome_personagem="Punk",
    num_cols_idle=4,  # Número de colunas na spritesheet idle
    num_cols_dano=2,
    num_cols_attack1=6,
    num_cols_attack2_3=8,
)

personagem2 = Personagem(
    posicao_personagem=(500, 300),
    tamanho_personagem=(200, 300),
    max_vida=10,
    max_especial=10,
    pasta_sprites_vida="sprites/vida",
    pasta_sprites_especial="sprites/especial",
    caminho_sprites="sprites/personagem/Jogador_2/",  # Verifique se está correto
    nome_personagem="Biker",
    num_cols_idle=4,
    num_cols_dano=2,
    num_cols_attack1=6,
    num_cols_attack2_3=8,
    invert_frames=True
)

tempo_morte_p1 = None  # Tempo de morte do personagem 1
tempo_morte_p2 = None  # Tempo de morte do personagem 2
tempo_espera_game_over = 2000  # Tempo em milissegundos para exibir "Game Over"
vencedor = None  # Armazena o vencedor da partida

# Flags para controlar a aplicação de dano após ataque
ataque_personagem1 = False
ataque_personagem2 = False  # Se necessário

# Loop Principal
rodando = True
while rodando:
    delta_tempo = RELOGIO.tick(FPS) / 1000.0  # Delta de tempo em segundos

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

    # Desenho na tela
    TELA.fill(PRETO)
    personagem1.desenhar(TELA)
    personagem2.desenhar(TELA)

    # Verificação de "Game Over" para Personagem 1
    if personagem1.vida.vida_atual == 0:
        if tempo_morte_p1 and pygame.time.get_ticks() - tempo_morte_p1 > tempo_espera_game_over:
            vencedor = "Punk"
            rodando = False
    else:
        tempo_morte_p1 = None

    # Verificação de "Game Over" para Personagem 2
    if personagem2.vida.vida_atual == 0:
        if tempo_morte_p2 and pygame.time.get_ticks() - tempo_morte_p2 > tempo_espera_game_over:
            vencedor = "Biker"
            rodando = False
    else:
        tempo_morte_p2 = None

    # Atualiza a tela
    pygame.display.flip()

# Tela de vitória
if vencedor:
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Pressione Enter para sair
                    rodando = False

        TELA.fill(PRETO)
        texto_vitoria = FONTE.render(f"{vencedor} venceu!", True, BRANCO)
        TELA.blit(texto_vitoria, (
            LARGURA // 2 - texto_vitoria.get_width() // 2, 
            ALTURA // 2 - texto_vitoria.get_height() // 2
        ))
        texto_instrucao = FONTE.render("Pressione Enter para sair", True, BRANCO)
        TELA.blit(texto_instrucao, (
            LARGURA // 2 - texto_instrucao.get_width() // 2, 
            ALTURA // 2 + texto_vitoria.get_height()
        ))

        pygame.display.flip()

pygame.quit()