import pygame

class Bola(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, final_height, velocidade_bola, image_path="Sprites/sphere.png"):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.mover_y = velocidade_bola  # Definindo movimento para a esquerda
        self.height = final_height
        
    def update(self):
        # Verifica se a esfera ultrapassou o limite superior ou inferior da caixa de colisão
        if self.rect.top > self.height:
            self.kill() 
            return True
        return False 
    def mover(self):
        """Atualiza a posição da bola"""
        self.rect.y += self.mover_y


class ControladorEsferas:
    def __init__(self):
        self.esferas = []
        self.contador = 0

    def criar_esfera(self, x, y, width, height, final_height, velocidade_bola):
        """Cria uma nova esfera e a adiciona à lista"""
        esfera = Bola(x, y, width, height,final_height,velocidade_bola)
        self.esferas.append(esfera)
        self.contador += 1
        return esfera

    def remover_esfera(self, esfera):
        """Remove uma esfera da lista"""
        if esfera in self.esferas:
            esfera.kill()  
            self.esferas.remove(esfera)
            self.contador -= 1
   

