import pygame
import os

class Especial:
    def __init__(self, max_especial, posicao, tamanho_sprite, pasta_sprites):
        """
        Inicializa o especial do personagem.

        :param max_especial: Especial máximo do personagem.
        :param posicao: Posição do sprite de especial na tela (x, y).
        :param tamanho_sprite: Tamanho máximo do sprite (largura, altura).
        :param pasta_sprites: Caminho para a pasta contendo os sprites de especial.
        """
        self.max_especial = max_especial
        self.especial_atual = 0
        self.posicao = posicao
        self.tamanho_sprite = tamanho_sprite
        self.sprites = self.carregar_sprites(pasta_sprites)
        self.sprite_atual = self.sprites[self.especial_atual]

    def carregar_sprites(self, pasta_sprites):
        """
        Carrega e redimensiona os sprites de especial mantendo a proporção.

        :param pasta_sprites: Caminho para a pasta contendo os sprites de especial.
        :return: Dicionário de sprites com a chave sendo o valor de especial.
        """
        sprites = {}
        for i in range(self.max_especial + 1):
            caminho_sprite = os.path.join(pasta_sprites, f"especial_{i}.png")
            try:
                imagem = pygame.image.load(caminho_sprite).convert_alpha()
                imagem_redimensionada = self.escala_proporcional(imagem, self.tamanho_sprite)
                sprites[i] = imagem_redimensionada
            except pygame.error as e:
                print(f"Erro ao carregar o sprite de especial: {caminho_sprite}\n{e}")
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

    def aumentar_especial(self, soma):
        """
        Aumenta o valor atual do especial do personagem.

        :param soma: Quantidade a ser adicionada ao especial atual.
        """
        self.especial_atual += soma
        if self.especial_atual < 0:
            self.especial_atual = 0
        elif self.especial_atual > self.max_especial:
            self.especial_atual = self.max_especial
        self.atualizar_sprite()

    def atualizar_sprite(self):
        """
        Atualiza o sprite atual com base no especial atual.
        """
        if 0 <= self.especial_atual <= self.max_especial:
            self.sprite_atual = self.sprites.get(self.especial_atual, self.sprites[0])
        else:
            self.sprite_atual = None

    def desenhar(self, tela):
        """
        Desenha o sprite de especial na tela.

        :param tela: Surface do Pygame onde o sprite será desenhado.
        """
        if self.sprite_atual:
            tela.blit(self.sprite_atual, self.posicao)