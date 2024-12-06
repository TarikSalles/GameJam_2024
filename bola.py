import pygame

class Bola(pygame.sprite.Sprite):
    def __init__(self, id,x, y, width, height, final_height, y_hitbox, velocidade_bola, image_path="Sprites/sphere.png", tecla = 1, player = 1):
        self.tecla = tecla
        self.player = player
        self.y_hitbox = y_hitbox
        super().__init__()
        if(tecla == 1 and player == 1):
            image_path="assets/a_subindo.png"
        elif(tecla == 2 and player == 1):
            image_path="assets/s_subindo.png"
        elif(tecla == 3 and player == 1):
            image_path="assets/d_subindo.png"
        elif(tecla == 0 and player == 1):
            image_path="assets/w_subindo.png"
        elif(tecla == 0 and player == 2):
            image_path="assets/cima_subindo.png"
        elif(tecla == 2 and player == 2):
            image_path="assets/baixo_subindo.png"
        elif(tecla == 1 and player == 2):
            image_path="assets/esq_subindo.png"
        elif(tecla == 3 and player == 2):
            image_path="assets/dir_subindo.png"

        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        if(self.player == 2):
             self.image = pygame.transform.scale(self.image, (width //2, height //2))
        self.width_ball = width
        self.height_ball = height
        self.rect = self.image.get_rect(center=(x, y))
        self.mover_y = velocidade_bola  # Definindo movimento para a esquerda
        self.height = final_height
        self.x = x
        self.y = y
        self.acerto = False
        self.id_unico = id
        
    def update(self):
        # Verifica se a esfera ultrapassou o limite superior ou inferior da caixa de colisão
        if self.rect.top + self.height_ball < 0:
            self.kill()
            return True
        if self.rect.top < self.y_hitbox and self.acerto == False:
            if(self.tecla == 1 and self.player == 1):
                image_path="assets/a_clicado.png"
            elif(self.tecla == 2 and self.player == 1):
                    image_path="assets/s_clicado.png"
            elif(self.tecla == 3 and self.player == 1):
                    image_path="assets/d_clicado.png"
            elif(self.tecla == 0 and self.player == 1):
                    image_path="assets/w_clicado.png"
            elif(self.tecla == 0 and self.player == 2):
                    image_path="assets/cima_clicado.png"
            elif(self.tecla == 2 and self.player == 2):
                    image_path="assets/baixo_clicado.png"
            elif(self.tecla == 1 and self.player == 2):
                    image_path="assets/esq_clicado.png"
            elif(self.tecla == 3 and self.player == 2):
                    image_path="assets/dir_clicado.png"
            return True
            
        return False 
    def mover(self):
        """Atualiza a posição da bola"""
        self.rect.y += self.mover_y
    
    def bola_acerto(self):
        if(self.tecla == 1 and self.player == 1):
            image_path="assets/a_acerto.png"
        elif(self.tecla == 2 and self.player == 1):
            image_path="assets/s_acerto.png"
        elif(self.tecla == 3 and self.player == 1):
            image_path="assets/d_acerto.png"
        elif(self.tecla == 0 and self.player == 1):
            image_path="assets/w_acerto.png"
        elif(self.tecla == 0 and self.player == 2):
            image_path="assets/cima_acerto.png"
        elif(self.tecla == 2 and self.player == 2):
            image_path="assets/baixo_acerto.png"
        elif(self.tecla == 1 and self.player == 2):
            image_path="assets/esq_acerto.png"
        elif(self.tecla == 3 and self.player == 2):
            image_path="assets/dir_acerto.png"

        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width_ball, self.height_ball))
        if(self.player == 2):
             self.image = pygame.transform.scale(self.image, (self.width_ball, self.height_ball ))

        self.rect = self.image.get_rect(center=self.rect.center)
        self.acerto = True



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
   

