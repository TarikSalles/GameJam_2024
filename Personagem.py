import pygame
import random
from Vida import Vida
from Especial import Especial

class Personagem:
    def __init__(self, posicao_personagem, tamanho_personagem, max_vida, max_especial,
                 pasta_sprites_vida, pasta_sprites_especial, caminho_sprites, nome_personagem, 
                 num_cols_idle, num_cols_dano, num_cols_attack1, num_cols_attack2_3):
        self.nome_personagem = nome_personagem  # Para uso no debug
        self.posicao = posicao_personagem  # Posição do personagem (x, y)
        self.tamanho_desejada = tamanho_personagem  # Tamanho desejado (largura, altura)

        # Caminhos para as animações
        caminho_base = caminho_sprites + nome_personagem + "/" + nome_personagem
        caminho_idle = caminho_base + "_idle.png"
        caminho_dano = caminho_base + "_hurt.png"
        caminho_attack1 = caminho_base + "_attack1.png"  # Corrigido o nome
        caminho_attack2 = caminho_base + "_attack2.png"  # Corrigido o nome
        caminho_attack3 = caminho_base + "_attack3.png"  # Corrigido o nome

        # Carrega as spritesheets
        try:
            self.spritesheet_idle = pygame.image.load(caminho_idle).convert_alpha()
            self.spritesheet_dano = pygame.image.load(caminho_dano).convert_alpha()
            self.spritesheet_attack1 = pygame.image.load(caminho_attack1).convert_alpha()
            self.spritesheet_attack2 = pygame.image.load(caminho_attack2).convert_alpha()
            self.spritesheet_attack3 = pygame.image.load(caminho_attack3).convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar spritesheets: {e}")
            raise SystemExit(e)

        # Carrega as animações
        self.animacoes = {
            "idle": self.carregar_frames(self.spritesheet_idle, num_cols_idle),
            "hurt": self.carregar_frames(self.spritesheet_dano, num_cols_dano),
            "attack1": self.carregar_frames(self.spritesheet_attack1, num_cols_attack1),
            "attack2": self.carregar_frames(self.spritesheet_attack2, num_cols_attack2_3),
            "attack3": self.carregar_frames(self.spritesheet_attack3, num_cols_attack2_3),
        }

        # Define a animação atual
        self.animacao_atual = "idle"
        self.frames = self.animacoes[self.animacao_atual]
        self.frame_atual = 0
        self.contador_tempo = 0
        self.velocidade_animacao = 0.1  # Velocidade da animação (em segundos)

        # Flags de controle
        self.sofreu_dano = False
        self.em_ataque = False  # Flag para indicar se o personagem está atacando

        # Calcula o tamanho das barras de vida e especial proporcional ao tamanho do personagem
        largura_barra = self.tamanho_desejada[0]
        altura_barra = self.tamanho_desejada[1] * 0.1  # 10% da altura do personagem

        # Calcula a posição das barras acima do personagem
        posicao_vida = (self.posicao[0], self.posicao[1] - altura_barra * 2 - 10)
        posicao_especial = (self.posicao[0], self.posicao[1] - altura_barra - 5)

        # Inicializa vida e especial com as posições e tamanhos calculados
        self.vida = Vida(
            max_vida=max_vida,
            posicao=posicao_vida,
            tamanho_sprite=(largura_barra, altura_barra),
            pasta_sprites=pasta_sprites_vida
        )
        self.especial = Especial(
            max_especial=max_especial,
            posicao=posicao_especial,
            tamanho_sprite=(largura_barra, altura_barra),
            pasta_sprites=pasta_sprites_especial
        )

    def carregar_frames(self, spritesheet, num_cols):
        frames = []
        largura_spritesheet = spritesheet.get_width()
        altura_spritesheet = spritesheet.get_height()
        largura_frame = largura_spritesheet // num_cols

        for coluna in range(num_cols):
            frame_rect = pygame.Rect(
                coluna * largura_frame,
                0,
                largura_frame,
                altura_spritesheet
            )
            frame_image = spritesheet.subsurface(frame_rect)
            frame_image = self.escala_proporcional(frame_image, self.tamanho_desejada)
            frames.append(frame_image)
        return frames

    def escala_proporcional(self, imagem, tamanho_desejado):
        largura_desejada, altura_desejada = tamanho_desejado
        largura_original, altura_original = imagem.get_size()

        # Calcula fatores de escala mantendo a proporção
        fator_largura = largura_desejada / largura_original
        fator_altura = altura_desejada / altura_original
        fator = min(fator_largura, fator_altura)

        nova_largura = int(largura_original * fator)
        nova_altura = int(altura_original * fator)

        # Redimensiona a imagem mantendo a proporção
        imagem_redimensionada = pygame.transform.scale(imagem, (nova_largura, nova_altura))
        return imagem_redimensionada

    def atacar(self):
        if not self.em_ataque and self.vida.vida_atual > 0:
            animacoes_attack = ["attack1", "attack2", "attack3"]
            animacao_selecionada = random.choice(animacoes_attack)
            self.animacao_atual = animacao_selecionada
            self.frames = self.animacoes[self.animacao_atual]
            self.frame_atual = 0
            self.em_ataque = True

    def atualizar(self, delta_tempo):
        # Atualiza o contador de tempo
        self.contador_tempo += delta_tempo
        if self.contador_tempo >= self.velocidade_animacao:
            self.contador_tempo = 0
            # Avança para o próximo frame
            self.frame_atual += 1

            # Verifica se a animação terminou
            if self.frame_atual >= len(self.frames):
                if self.animacao_atual in ["hurt", "attack1", "attack2", "attack3"]:
                    # Retorna para a animação idle
                    self.animacao_atual = "idle"
                    self.frames = self.animacoes[self.animacao_atual]
                self.frame_atual = 0
                if self.em_ataque:
                    self.em_ataque = False  # Ataque finalizado

    def desenhar(self, tela):
        # Desenha o frame atual do personagem na tela
        tela.blit(self.frames[self.frame_atual], self.posicao)

        # Desenha as barras de vida e especial
        self.vida.desenhar(tela)
        self.especial.desenhar(tela)

    def levar_dano(self, dano):
        self.vida.levar_dano(dano)
        if self.vida.vida_atual > 0:
            self.animacao_atual = "hurt"
            self.frames = self.animacoes[self.animacao_atual]
            self.frame_atual = 0

    def mover(self, nova_posicao):
        # Atualiza a posição do personagem
        self.posicao = nova_posicao

        # Recalcula as posições das barras com base na nova posição
        altura_barra = self.tamanho_desejada[1] * 0.1
        self.vida.posicao = (self.posicao[0], self.posicao[1] - altura_barra * 2 - 10)
        self.especial.posicao = (self.posicao[0], self.posicao[1] - altura_barra - 5)