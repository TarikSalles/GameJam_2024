import pygame
import os

class Vida:
    def __init__(self, max_vida, posicao, tamanho_sprite, pasta_sprites):
        """
        Inicializa a vida do personagem.

        :param max_vida: Vida máxima do personagem.
        :param posicao: Posição do sprite de vida na tela (x, y).
        :param tamanho_sprite: Tamanho máximo do sprite (largura, altura).
        :param pasta_sprites: Caminho para a pasta contendo os sprites de vida.
        """
        self.max_vida = max_vida
        self.vida_atual = max_vida
        self.posicao = posicao
        self.tamanho_maxima = tamanho_sprite
        self.sprites = self.carregar_sprites(pasta_sprites)
        self.sprite_atual = self.sprites[self.vida_atual]

    def carregar_sprites(self, pasta_sprites):
        """
        Carrega e redimensiona os sprites de vida mantendo a proporção.

        :param pasta_sprites: Caminho para a pasta contendo os sprites de vida.
        :return: Dicionário de sprites com a chave sendo o valor de vida.
        """
        sprites = {}
        for i in range(self.max_vida + 1):
            caminho_sprite = os.path.join(pasta_sprites, f"vida_{i}.png")
            try:
                imagem = pygame.image.load(caminho_sprite).convert_alpha()
                imagem_redimensionada = self.escala_proporcional(imagem, self.tamanho_maxima)
                sprites[i] = imagem_redimensionada
            except pygame.error as e:
                print(f"Erro ao carregar o sprite de vida: {caminho_sprite}\n{e}")
        return sprites

    def escala_proporcional(self, imagem, tamanho_maximo):
        """
        Redimensiona a imagem mantendo a proporção original.

        :param imagem: Surface do Pygame a ser redimensionada.
        :param tamanho_maximo: Tupla (largura, altura) representando o tamanho máximo.
        :return: Surface redimensionada.
        """
        largura_max, altura_max = tamanho_maximo
        largura_original, altura_original = imagem.get_size()

        # Calcula os fatores de escala
        fator_largura = largura_max / largura_original
        fator_altura = altura_max / altura_original
        fator = min(fator_largura, fator_altura)

        # Calcula os novos tamanhos
        nova_largura = int(largura_original * fator)
        nova_altura = int(altura_original * fator)

        # Redimensiona a imagem
        imagem_redimensionada = pygame.transform.scale(imagem, (nova_largura, nova_altura))
        return imagem_redimensionada

    def levar_dano(self, dano):
        """
        Reduz a vida atual do personagem.

        :param dano: Quantidade de dano a ser infligido.
        """
        self.vida_atual = max(self.vida_atual - dano, 0)
        self.atualizar_sprite()

    def atualizar_sprite(self):
        """
        Atualiza o sprite atual com base na vida atual.
        """
        self.sprite_atual = self.sprites.get(self.vida_atual, self.sprites[0])

    def desenhar(self, tela):
        """
        Desenha o sprite de vida na tela.

        :param tela: Surface do Pygame onde o sprite será desenhado.
        """
        tela.blit(self.sprite_atual, self.posicao)