import pygame
from bola import Bola, ControladorEsferas

# Inicializa o Pygame
pygame.init()

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

# Fonte
font = pygame.font.Font(None, 36)

# Classe Piano
class Piano:
    def __init__(self, controlador, width=800, height=600, tamanho_linha_width=700, tamanho_linha_height=100):
        self.controlador = controlador
        self.width = width
        self.height = height
        self.tamanho_linha_width = tamanho_linha_width  # Largura das linhas verticais
        self.tamanho_linha_height = tamanho_linha_height  # Distância vertical entre as linhas
        self.linhas = [100, 200, 300, 400]  # Posições verticais das linhas
        self.teclas = ["W", "A", "S", "D"]  # Teclas que controlam as esferas
        self.tamanho_hitbox = 20
        self.hitboxes = [pygame.Rect(linha - self.tamanho_hitbox // 2, self.height - self.tamanho_hitbox, self.tamanho_hitbox, self.tamanho_hitbox) for i, linha in enumerate(self.linhas)]

    def desenhar(self, screen):
        """Desenha o piano na tela"""
        screen.fill(white)

        # Desenhar as linhas verticais
        for i, y in enumerate(self.linhas):
    
            pygame.draw.line(screen, black, (y, 0), (y, self.height), 3)
            tecla_surface = font.render(self.teclas[i], True, black)
            screen.blit(tecla_surface, (y, self.height - 50))

        # Desenhar hitboxes
        for hitbox in self.hitboxes:
            pygame.draw.rect(screen, green, hitbox)

        # Desenhar esferas
        for esfera in self.controlador.esferas:
            screen.blit(esfera.image, esfera.rect)
    def criar_esfera(self, letra):
        print(self.teclas.index(letra))
        x = self.linhas[self.teclas.index(letra)]
        y = 0
        width = 30
        height = 30
        esfera = Bola(x, y, width, height,self.height)
        self.controlador.esferas.append(esfera)
        return esfera
    def verificar_colisao(self, key_pressed):
        """Verifica colisão das esferas com as hitboxes"""
        for i, hitbox in enumerate(self.hitboxes):
            tecla_correta = pygame.key.name(key_pressed).upper() == self.teclas[i]
            for esfera in self.controlador.esferas:
                if hitbox.colliderect(esfera.rect):
                    if tecla_correta:
                        print(f"{self.teclas[i]} OK")
                        esfera.acertou = True
                        self.controlador.remover_esfera(esfera)
                    
                    return


