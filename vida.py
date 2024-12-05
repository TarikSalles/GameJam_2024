import pygame

class Vida:
    def __init__(self, max_vida, posicao, tamanho_sprite, pasta_sprites):
        """
        Inicializa a vida do personagem.

        :param max_vida: Vida máxima do personagem.
        :param posicao: Posição do sprite de vida na tela (x, y).
        :param tamanho_sprite: Tamanho do sprite (largura, altura).
        :param pasta_sprites: Caminho para a pasta contendo os sprites de vida.
        """
        self.max_vida = max_vida
        self.vida_atual = max_vida
        self.posicao = posicao
        self.tamanho_sprite = tamanho_sprite
        self.sprites = self.carregar_sprites(pasta_sprites)
        self.sprite_atual = self.sprites[self.vida_atual]

    def carregar_sprites(self, pasta_sprites):
        """
        Carrega os sprites de vida a partir da pasta.

        :param pasta_sprites: Caminho para a pasta dos sprites de vida.
        :return: Um dicionário com os sprites indexados por níveis de vida.
        """
        sprites = {}
        for i in range(0, self.max_vida + 1):
            caminho = f"{pasta_sprites}/vida_{i}.png"
            sprite = pygame.image.load(caminho)
            sprite = pygame.transform.scale(sprite, self.tamanho_sprite)
            sprites[i] = sprite
        return sprites

    def levar_dano(self, dano):
        """
        Reduz a vida com base no dano recebido.

        :param dano: Quantidade de dano recebido.
        """
        self.vida_atual -= dano
        if self.vida_atual < 1:
            self.vida_atual = 0
        self.atualizar_sprite()

    def atualizar_sprite(self):
        """
        Atualiza o sprite com base na vida atual.
        """
        if self.vida_atual >= 0:
            self.sprite_atual = self.sprites[self.vida_atual]
        else:
            self.sprite_atual = None  # Vida zerada, sem sprite.

    def desenhar(self, tela):
        """
        Desenha o sprite de vida na tela.

        :param tela: Superfície onde o sprite será desenhado.
        """
        if self.sprite_atual:
            tela.blit(self.sprite_atual, self.posicao)
