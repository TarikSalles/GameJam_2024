import pygame

class Especial:
    def __init__(self, max_especial, posicao, tamanho_sprite, pasta_sprites):
        self.max_especial = max_especial
        self.especial_atual = 0
        self.posicao = posicao
        self.tamanho_sprite = tamanho_sprite
        self.sprites = self.carregar_sprites(pasta_sprites)
        self.sprite_atual = self.sprites[self.especial_atual]

    def carregar_sprites(self, pasta_sprites):
        sprites = {}
        for i in range(0, self.max_especial + 1):
            caminho = f"{pasta_sprites}/especial_{i}.png"
            sprite = pygame.image.load(caminho)
            sprite = pygame.transform.scale(sprite, self.tamanho_sprite)
            sprites[i] = sprite
        return sprites

    def aumentar_especial(self, soma):
        self.especial_atual += soma
        if self.especial_atual < 1:
            self.especial_atual = 0
        elif self.especial_atual > self.max_especial:
            self.especial_atual = self.max_especial
        self.atualizar_sprite()

    def atualizar_sprite(self):
        if 0 <= self.especial_atual <= self.max_especial:
            self.sprite_atual = self.sprites[self.especial_atual]
        else:
            self.sprite_atual = None

    def desenhar(self, tela):
        if self.sprite_atual:
            tela.blit(self.sprite_atual, self.posicao)
