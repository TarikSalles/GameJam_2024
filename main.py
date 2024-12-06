import pygame
from piano import Piano
from bola import ControladorEsferas
from music import Music
from Personagem import Personagem
from fim import exibir_tela_fim_jogo

# Inicialização do Pygame
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Definir a resolução mínima e inicial da tela
LARGURA_MINIMA, ALTURA_MINIMA = 1280, 720  # Resolução mínima
LARGURA_INICIAL, ALTURA_INICIAL = screen_width, screen_height  # Resolução inicial
TELA = pygame.display.set_mode((LARGURA_INICIAL, ALTURA_INICIAL), pygame.RESIZABLE)
pygame.display.set_caption("Musical Fight")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Recursos de tempo e FPS
RELOGIO = pygame.time.Clock()
FPS = 60

# Fonte para textos
FONTE = pygame.font.Font(None, 50)  # Fonte padrão com tamanho 50

# Carregar a fonte tecnológica
try:
    fonte_tecnologica = pygame.font.Font("./sprites/fonts/tech_font.otf", 64)  # Carrega a fonte tecnológica
except FileNotFoundError:
    print("Fonte .otf não encontrada. Usando fonte padrão.")
    fonte_tecnologica = pygame.font.Font(None, 64)

# Carregar o fundo e elementos
background = pygame.image.load("./sprites/tela/background.png").convert()
quadro_imagem = pygame.image.load("./sprites/tela/quadro.png").convert_alpha()
vida_imagem = pygame.image.load("./sprites/tela/vida.png").convert_alpha()
energia_imagem = pygame.image.load("./sprites/tela/energia.png").convert_alpha()

def redimensionar_vida(tamanho):
    return pygame.transform.scale(vida_imagem, tamanho)

def redimensionar_energia(tamanho):
    return pygame.transform.scale(energia_imagem, tamanho)

def redimensionar_quadro(tela_largura, tela_altura):
    return pygame.transform.scale(quadro_imagem, (tela_largura, tela_altura))

# Função para redimensionar o fundo
def redimensionar_fundo(tela_largura, tela_altura):
    return pygame.transform.scale(background, (tela_largura, tela_altura))

# Função para redimensionar os personagens e suas barras
def redimensionar_personagens(personagens, tela_largura, tela_altura):
    fator_largura = tela_largura / LARGURA_INICIAL
    fator_altura = tela_altura / ALTURA_INICIAL
    for p in personagens:
        # Atualiza o tamanho desejado dos personagens
        nova_largura = int(p.tamanho_desejada[0] * fator_largura)
        nova_altura = int(p.tamanho_desejada[1] * fator_altura)
        p.tamanho_desejada = (nova_largura, nova_altura)  # Atualiza o tamanho desejado
        # Atualiza a posição do personagem se necessário
        p.posicao = (
            p.posicao[0],  # Mantém a posição x original
            p.posicao[1]   # Mantém a posição y original
        )

# Função para desenhar o round
def desenhar_round(tela, round_atual, fonte, cor, posicao_base, quadro_tamanho):
    texto = f"Round {round_atual}"
    texto_renderizado = fonte.render(texto, True, cor)
    largura_texto, altura_texto = texto_renderizado.get_size()
    posicao_final = (
        posicao_base[0] + (quadro_tamanho[0] // 2) - (largura_texto // 2),
        posicao_base[1] + 20  # 20 pixels abaixo do topo do quadro
    )
    tela.blit(texto_renderizado, posicao_final)

# Classe Gerenciador de Personagens para facilitar a gestão de múltiplos personagens
class GerenciadorPersonagens:
    def __init__(self, tela_largura):
        # Inicialize os personagens com suas posições e configurações
        self.personagem1 = Personagem(
            posicao_personagem=(tela_largura // 2 - 180, 300),
            tamanho_personagem=(300, 450),
            caminho_sprites="./sprites/personagem/Jogador_1/",
            nome_personagem="Biker",
            invert_frames=False
        )
        self.personagem2 = Personagem(
            posicao_personagem=(tela_largura // 2 - 40, 300),
            tamanho_personagem=(300, 450),
            caminho_sprites="./sprites/personagem/Jogador_2/",
            nome_personagem="Punk",
            invert_frames=True
        )
        self.personagens = [self.personagem1, self.personagem2]
    
    def atualizar_personagens(self, delta_tempo):
        for personagem in self.personagens:
            personagem.atualizar(delta_tempo)
    
    def desenhar_personagens(self, tela):
        for personagem in self.personagens:
            personagem.desenhar(tela)

def main():
    # Inicialização das Classes
    # Inicialização da Música
    music_player1 = Music("musica_easy/Info.dat", "musica_easy/EasyStandard.dat", "musica_easy/song.mp3")
    music_player2 = Music("musica_hard/Info.dat", "musica_easy/EasyStandard.dat", "musica_easy/song.mp3")
    
    # Iniciar a música
    music_player1.tocar()
    music_player2.tocar()
    
    # Inicialização dos Personagens
    gerenciador_personagens = GerenciadorPersonagens(LARGURA_INICIAL)
    
    # Inicialização do Controlador de Esferas
    controlador_esferas_player_1 = ControladorEsferas()
    controlador_esferas_player_2 = ControladorEsferas()
    
    # Inicialização dos Componentes do Piano
    score_player1 = 10
    score_player2 = 10
    ganhouUltimoRound_player1 = False
    tempoAtual = 0.0
    tempoDuracao = 15.0
    turnoPlayer1 = True
    incremento_score = 1
    tamanho_linha_width = 700
    tamanho_linha_height = 100

    piano_player1 = Piano(
        controlador_esferas_player_1,
        incremento_score=incremento_score,
        width=LARGURA_INICIAL / 2,
        height=ALTURA_INICIAL / 2,
        tamanho_linha_width=tamanho_linha_width,
        tamanho_linha_height=tamanho_linha_height,
        score=score_player1,
        tipo="ataque",
        music=music_player1,
        teclas=[pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    )
    
    piano_player2 = Piano(
        controlador_esferas_player_2,
        incremento_score=incremento_score,
        width=LARGURA_INICIAL / 2,
        height=ALTURA_INICIAL / 2,
        tamanho_linha_width=tamanho_linha_width,
        tamanho_linha_height=tamanho_linha_height,
        score=score_player2,
        tipo="ataque",
        music=music_player2,
        init_x=LARGURA_INICIAL - 500,
        init_y=0,
        teclas=[pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT],
        player=2
    )
    
    # Variáveis de Controle
    score_player1 = 0
    score_player2 = 0
    ataque_personagem1 = False
    ataque_personagem2 = False
    tempo_morte_p1 = None
    tempo_morte_p2 = None
    tempo_espera_game_over = 5000  # Tempo em milissegundos antes de exibir a tela de fim de jogo
    tempo_espera_round = 2000
    tempo_rodando = pygame.time.get_ticks()
    rodando = True
    round_atual = 1  # Variável para controlar o round
    
    while rodando:
        delta_tempo = RELOGIO.tick(FPS) / 1000.0  # Delta de tempo em segundos
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e:  # Pressione E para carregar o especial
                    gerenciador_personagens.personagem1.especial.aumentar_especial(1)
                if evento.key == pygame.K_q and gerenciador_personagens.personagem1.especial.especial_atual == gerenciador_personagens.personagem1.especial.max_especial:
                    gerenciador_personagens.personagem1.especial.especial_atual = 0
                    gerenciador_personagens.personagem1.especial.atualizar_sprite()

                # Controle do Personagem 2
                if evento.key == pygame.K_g:  # Pressione G para carregar o especial
                    gerenciador_personagens.personagem2.especial.aumentar_especial(1)
                if evento.key == pygame.K_h and gerenciador_personagens.personagem2.especial.especial_atual == gerenciador_personagens.personagem2.especial.max_especial:
                    gerenciador_personagens.personagem2.especial.especial_atual = 0
                    gerenciador_personagens.personagem2.especial.atualizar_sprite()
        
        # Atualização dos Componentes do Piano
        piano_player1.spawn_notes()
        piano_player2.spawn_notes()
        piano_player1.update_notes()
        piano_player2.update_notes()

        piano_player1.verificar_colisao()
        piano_player2.verificar_colisao()

        # Redimensiona os personagens com base no tamanho da tela
        tela_largura, tela_altura = TELA.get_size()
        tela_largura = max(tela_largura, LARGURA_MINIMA)  # Garantir a largura mínima
        tela_altura = max(tela_altura, ALTURA_MINIMA)    # Garantir a altura mínima
        redimensionar_personagens(gerenciador_personagens.personagens, tela_largura, tela_altura)
        fundo_redimensionado = redimensionar_fundo(tela_largura, tela_altura)

        # Desenho na tela
        TELA.blit(fundo_redimensionado, (0, 0))  # Desenha o fundo
        
        largura_quadro = 1400 // 2.5          # Defina a largura
        altura_quadro = 2000 // 2.5           # Defina a altura

        quadro_redimensionado = redimensionar_quadro(largura_quadro, altura_quadro)
        posicao_quadro_x = tela_largura // 2 - 250
        posicao_quadro_y = tela_altura // 2 - 400
        TELA.blit(quadro_redimensionado, (posicao_quadro_x, posicao_quadro_y)) 
        
        largura_vida = 430 / 2
        altura_vida = 180 / 2
        
        vida_redimensionada = redimensionar_vida((int(largura_vida), int(altura_vida)))
        TELA.blit(vida_redimensionada, (tela_largura // 2 - 80, tela_altura // 2 - 350))

        largura_energia = 730 / 2
        altura_energia = 180 / 2
        
        energia_redimensionada = redimensionar_energia((int(largura_energia), int(altura_energia)))
        TELA.blit(energia_redimensionada, (tela_largura // 2 - 150, tela_altura - 400 ))
        
        # Desenhar o Round por cima do quadro usando fonte normal
        desenhar_round(
            tela=TELA,
            round_atual=round_atual,
            fonte=FONTE,           # Usando a fonte normal
            cor=BRANCO,
            posicao_base=(posicao_quadro_x, posicao_quadro_y),
            quadro_tamanho=(largura_quadro, altura_quadro)
        )
        
        # Atualização e desenho das esferas
        for esfera in controlador_esferas_player_1.esferas:
            esfera.mover() 
            if esfera.update():
                if not esfera.acerto:
                    print(f"Player 1 Perdeu por conta de {esfera.id_unico}")
                    piano_player1.score -= incremento_score
                controlador_esferas_player_1.remover_esfera(esfera)

        for esfera in controlador_esferas_player_2.esferas:
            esfera.mover() 
            if esfera.update():
                if not esfera.acerto:
                    piano_player2.score -= incremento_score
                controlador_esferas_player_2.remover_esfera(esfera)
        
        score_player1 = piano_player1.score
        score_player2 = piano_player2.score
        
        # Controle de Incremento do Round
        if pygame.time.get_ticks() - tempo_rodando > tempo_espera_round and not gerenciador_personagens.personagem1.morto and not gerenciador_personagens.personagem2.morto:
            tempo_rodando = pygame.time.get_ticks()
            print(f"Score Player 1: {score_player1},   Score Player 2: {score_player2}")
            round_atual += 1
            if score_player1 > score_player2:
                gerenciador_personagens.personagem1.atacar()
                gerenciador_personagens.personagem2.levar_dano(1)
                ataque_personagem2 = True
                if gerenciador_personagens.personagem2.vida.vida_atual == 0 and tempo_morte_p2 is None:
                    gerenciador_personagens.personagem1.correr()
                    tempo_morte_p2 = pygame.time.get_ticks()

            if score_player2 > score_player1:
                gerenciador_personagens.personagem2.atacar()
                gerenciador_personagens.personagem1.levar_dano(1)
                ataque_personagem1 = True
                if gerenciador_personagens.personagem1.vida.vida_atual == 0 and tempo_morte_p1 is None:
                    # Adicione lógica adequada aqui
                    pass

            if score_player1 == 0 and score_player2 == 0:
                if ganhouUltimoRound_player1:
                    # Adicione lógica adequada aqui
                    pass
                else:
                    # Adicione lógica adequada aqui
                    pass

            ganhouUltimoRound_player1 = score_player1 > score_player2

            piano_player1.score = 0
            piano_player2.score = 0
            score_player1 = 0
            score_player2 = 0

        # Atualização e desenho dos personagens
        gerenciador_personagens.atualizar_personagens(delta_tempo)
        gerenciador_personagens.desenhar_personagens(TELA)
        piano_player1.desenhar(TELA)
        piano_player2.desenhar(TELA)
        
        # Atualizar a display
        pygame.display.flip()
        
        # Verificação de "Game Over" para Personagem 1
        if gerenciador_personagens.personagem1.vida.vida_atual == 0:
            if tempo_morte_p1 and pygame.time.get_ticks() - tempo_morte_p1 > tempo_espera_game_over:
                vencedor = '2'
                exibir_tela_fim_jogo(TELA, vencedor)
                rodando = False

        # Verificação de "Game Over" para Personagem 2
        if gerenciador_personagens.personagem2.vida.vida_atual == 0:
            if tempo_morte_p2 and pygame.time.get_ticks() - tempo_morte_p2 > tempo_espera_game_over:
                vencedor = '1'
                exibir_tela_fim_jogo(TELA, vencedor)
                rodando = False

        # Controle de Incremento do Round por Tempo
        tempoAtual += delta_tempo
        if tempoAtual >= tempoDuracao:
            round_atual += 1
            tempoAtual = 0.0
            print(f"Round {round_atual} iniciado!")
            # Resetar ou ajustar outras variáveis conforme necessário

    pygame.quit()

if __name__ == "__main__":
    main()