import pygame
from Personagem import Personagem

class GerenciadorPersonagens:
    def __init__(self, tela_largura):
        # Inicialize os personagens com suas posições e configurações
        self.personagem1 = Personagem(
            posicao_personagem=(tela_largura // 2 - 150, 300),
            tamanho_personagem=(200, 300),
            caminho_sprites="./sprites/personagem/Jogador_1/",
            nome_personagem="Biker",
            invert_frames=False
        )
        self.personagem2 = Personagem(
            posicao_personagem=(tela_largura // 2 + 100, 300),
            tamanho_personagem=(200, 300),
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