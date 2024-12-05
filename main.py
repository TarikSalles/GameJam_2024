import pygame
import sys
import random
from piano import Piano
from bola import ControladorEsferas
from music import Music
from Personagem import Personagem
from fim import exibir_tela_fim_jogo

# Inicialização do Pygame
pygame.init()

# Definir a resolução mínima e inicial da tela
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
background = pygame.image.load("./sprites/tela/background.png").convert()

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

# Classe Gerenciador de Personagens para facilitar a gestão de múltiplos personagens
class GerenciadorPersonagens:
    def __init__(self, tela_largura):
        # Inicialize os personagens com suas posições e configurações
        self.personagem1 = Personagem(
            posicao_personagem=(tela_largura // 2 - 150, 300),
            tamanho_personagem=(200, 300),
            caminho_sprites="./sprites/personagem1/",
            nome_personagem="Biker",
            invert_frames=False
        )
        self.personagem2 = Personagem(
            posicao_personagem=(tela_largura // 2 + 100, 300),
            tamanho_personagem=(200, 300),
            caminho_sprites="./sprites/personagem2/",
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
    music_player1 = Music("Info.dat", "ExpertPlusStandard.dat", "miser.mp3")
    music_player2 = Music("Info.dat", "ExpertPlusStandard.dat", "miser.mp3")
    
    # Iniciar a música
    music_player1.tocar()
    music_player2.tocar()
    
    # Inicialização dos Personagens
    gerenciador_personagens = GerenciadorPersonagens(LARGURA_INICIAL)
    
    # Inicialização do Controlador de Esferas
    gerenciador_esferas = ControladorEsferas()
    
    # Inicialização dos Componentes do Piano
    piano_player1 = Piano(...)  # Passe os parâmetros necessários
    piano_player2 = Piano(...)  # Passe os parâmetros necessários
    
    # Variáveis de Controle
    score_player1 = 0
    score_player2 = 0
    ataque_personagem1 = False
    ataque_personagem2 = False
    tempo_morte_p1 = None
    tempo_morte_p2 = None
    tempo_espera_game_over = 2000  # Tempo em milissegundos antes de exibir a tela de fim de jogo
    
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
                    gerenciador_personagens.personagem2.atacar()
                    ataque_personagem2 = True
                    if gerenciador_personagens.personagem1.vida.vida_atual == 0 and tempo_morte_p1 is None:
                        tempo_morte_p1 = pygame.time.get_ticks()
                if evento.key == pygame.K_r:  # Pressione R para reiniciar a vida
                    gerenciador_personagens.personagem1.vida.vida_atual = gerenciador_personagens.personagem1.vida.max_vida
                    gerenciador_personagens.personagem1.vida.atualizar_sprite()
                    tempo_morte_p1 = None

                if evento.key == pygame.K_e:  # Pressione E para carregar o especial
                    gerenciador_personagens.personagem1.especial.aumentar_especial(1)
                if evento.key == pygame.K_q and gerenciador_personagens.personagem1.especial.especial_atual == gerenciador_personagens.personagem1.especial.max_especial:
                    gerenciador_personagens.personagem1.especial.especial_atual = 0
                    gerenciador_personagens.personagem1.especial.atualizar_sprite()

                # Controle do Personagem 2
                if evento.key == pygame.K_f:  # Pressione F para o personagem2 atacar
                    gerenciador_personagens.personagem2.atacar()
                    ataque_personagem1 = True  # Indica que o ataque foi iniciado
                    if gerenciador_personagens.personagem2.vida.vida_atual == 0 and tempo_morte_p2 is None:
                        tempo_morte_p2 = pygame.time.get_ticks()
                if evento.key == pygame.K_t:  # Pressione T para reiniciar a vida
                    gerenciador_personagens.personagem2.vida.vida_atual = gerenciador_personagens.personagem2.vida.max_vida
                    gerenciador_personagens.personagem2.vida.atualizar_sprite()
                    tempo_morte_p2 = None

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

        # Atualização Pontuação
        score_player1 = piano_player1.get_score_geral()
        score_player2 = piano_player2.get_score_geral()
        
        # Determinação de Ataques Baseados na Pontuação
        if score_player1 > score_player2:
            gerenciador_personagens.personagem2.atacar()
            ataque_personagem2 = True
            if gerenciador_personagens.personagem1.vida.vida_atual == 0 and tempo_morte_p1 is None:
                tempo_morte_p1 = pygame.time.get_ticks()

        if score_player2 > score_player1:
            gerenciador_personagens.personagem1.atacar()
            ataque_personagem1 = True
            if gerenciador_personagens.personagem2.vida.vida_atual == 0 and tempo_morte_p2 is None:
                tempo_morte_p2 = pygame.time.get_ticks()
        
        # Aplicação de Dano Após o Ataque Completar
        if ataque_personagem1 and not gerenciador_personagens.personagem1.em_ataque:
            gerenciador_personagens.personagem2.levar_dano(1)  # Aplica dano ao personagem2
            ataque_personagem1 = False  # Reseta a flag
        
        elif ataque_personagem2 and not gerenciador_personagens.personagem2.em_ataque:
            gerenciador_personagens.personagem1.levar_dano(1)
            ataque_personagem2 = False

        # Redimensiona os personagens com base no tamanho da tela
        tela_largura, tela_altura = TELA.get_size()
        tela_largura = max(tela_largura, LARGURA_MINIMA)  # Garantir a largura mínima
        tela_altura = max(tela_altura, ALTURA_MINIMA)    # Garantir a altura mínima
        redimensionar_personagens(gerenciador_personagens.personagens, tela_largura, tela_altura)
        fundo_redimensionado = redimensionar_fundo(tela_largura, tela_altura)

        # Desenho na tela
        TELA.blit(fundo_redimensionado, (0, 0))  # Desenha o fundo
        gerenciador_esferas.desenhar(TELA)
        gerenciador_personagens.desenhar_personagens(TELA)
        piano_player1.desenhar(TELA)
        piano_player2.desenhar(TELA)
        piano_player1.desenhar_notes(TELA)
        piano_player2.desenhar_notes(TELA)
        
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

    pygame.quit()

if __name__ == "__main__":
    main()