import pygame
from bola import Bola, ControladorEsferas

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

font = pygame.font.Font(None, 36)


class Piano:
    def __init__(self, controlador, init_x=0, init_y=0, width=800, height=600, tamanho_linha_width=0, tamanho_linha_height=0, score=0, tipo="ataque", incremento_score=0, music=None,teclas = ["W","A","S","D"], player = 1):
        self.controlador = controlador
        self.init_x = init_x
        self.player = player
        self.init_y = init_y
        self.width_player2 = width // 32
        self.width_player1 = width // 16

        self.width = width
        self.key_map = {
    pygame.K_w: 'W',
    pygame.K_a: 'A',
    pygame.K_s: 'S',
    pygame.K_d: 'D',
    pygame.K_UP: '↑',    # Up arrow
    pygame.K_DOWN: '↓',  # Down arrow
    pygame.K_LEFT: '←',  # Left arrow
    pygame.K_RIGHT: '→'  # Right arrow
}
        self.height = height
        self.incremento_score = incremento_score
        self.tamanho_linha_width = tamanho_linha_width  
        self.tamanho_linha_height = tamanho_linha_height  
        self.score = score
        self.tipo = tipo
        self.notes_on_screen = []
        self.acertos = 0
        self.music = music
        self.linhas = [init_x + 100, init_x + 200, init_x + 300, init_x + 400]  # Posições verticais das linhas relativas a init_x
        self.teclas = teclas
        self.tamanho_hitbox = 20
        self.min = 0
        self.ball_speed = -2
        self.y_hitbox = self.init_y + self.init_y + self.tamanho_hitbox * 3
        self.hitboxes = [
            pygame.Rect(linha - self.tamanho_hitbox // 2, self.y_hitbox, self.tamanho_hitbox, self.tamanho_hitbox)
            for linha in self.linhas
        ]
   
    def desenhar(self, screen):
        


        for i, y in enumerate(self.linhas):
    
            key_text = self.key_map[self.teclas[i]]
            if(self.player == 1):
                image = pygame.image.load(f"assets/{key_text.lower()}_normal.png")
                image = pygame.transform.scale(image, (self.width_player2, self.width_player2))
                screen.blit(image, self.hitboxes[i].topleft)
            if(self.player == 2):
                if(key_text == "↑"):
                    image = pygame.image.load(f"assets/cima_normal.png")
                if(key_text == "→"):
                    image = pygame.image.load(f"assets/dir_normal.png")
                if(key_text == "←"):
                    image = pygame.image.load(f"assets/esq_normal.png")
                if(key_text == "→"):
                    image = pygame.image.load(f"assets/dir_normal.png")
                image = pygame.transform.scale(image, (self.width_player2, self.width_player2))
                screen.blit(image, self.hitboxes[i].topleft)
            tecla_surface = font.render(key_text, True, black)
            screen.blit(tecla_surface, (y - tecla_surface.get_width() / 2, self.init_x + tecla_surface.get_height()))

        # Desenhar hitboxes
        for hitbox in self.hitboxes:
            pygame.draw.rect(screen, green, hitbox)

        # Desenhar esferas
        for esfera in self.controlador.esferas:
            screen.blit(esfera.image, esfera.rect)

    def run_music(self):
        print("Iniciando a reprodução da música...")
        self.music.tocar()
    def piano_loop_principal(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

       
        self.spawn_notes()
        self.update_notes()
        self.verificar_colisao()  # Verifique colisões para todas as teclas pressionadas


            
    def criar_esfera(self, letra):
        
        x = self.linhas[self.teclas.index(letra)]

        y = self.height
        width = 50
        height = 50
        esfera = Bola(x, y, width, height,self.height,self.y_hitbox,velocidade_bola=self.ball_speed, tecla = self.teclas.index(letra), player=  self.player)
        self.controlador.esferas.append(esfera)
        return esfera
    def verificar_colisao(self):
        """Verifica colisões de todas as esferas com as hitboxes para teclas pressionadas simultaneamente"""
        keys_pressed = pygame.key.get_pressed()
        
        for i, hitbox in enumerate(self.hitboxes):  # Para cada hitbox
            tecla = self.teclas[i]  # Tecla associada à hitbox
            if keys_pressed[tecla]:  # Se a tecla está pressionada
                for esfera in self.controlador.esferas[:]:  # Verifique todas as esferas
                    if hitbox.colliderect(esfera.rect):  # Colisão com a hitbox
                        print(f"{tecla} OK")
                        
                        # Lógica adicional ao acertar a tecla
                        self.score += self.incremento_score
                        
                        esfera.acertou = True
                        esfera.bola_acerto()
                        #self.controlador.remover_esfera(esfera)  # Remova a esfera

    def get_score_geral(self):
        return self.score

    def spawn_notes(self):
        # Use o tempo da música para calcular o tempo atual
        current_time = pygame.mixer.music.get_pos() / 1000.0  # Tempo da música em segundos
      
        if self.music.notes and self.music.notes[0]["time"] <= current_time + 2:  # Spawn 2s antes
           
            note = self.music.notes.pop(0)
            note_instance = {"time": note["time"], "x": note["x"], "y": 0, "line": int(note["y"] * 4), "color": note["color"]}
            self.notes_on_screen.append(note_instance)
            

            pos_x = self.teclas[note["x"]]  # Ajuste conforme necessário

            print(f"Nota spawnada: {note_instance}")
            self.criar_esfera(pos_x)

    
   
        # Verificar se alguma nota alcançou ou passou a linha de chegada
        for note in self.notes_on_screen[:]:  # Copia a lista para evitar modificar enquanto percorre
            if note["y"] >= self.height:
                print(f"Nota atingiu a linha de chegada: {note}")
                self.notes_on_screen.remove(note)  # Remova a nota ou implemente lógica adicional

    
    def draw_notes(self):
        
        for note in self.notes_on_screen:
            pass

    def update_notes(self):
        for note in self.notes_on_screen:
            note["y"] += self.ball_speed  # Move down by 5 pixels por frame
        
        # Verificar se alguma nota alcançou ou passou a linha de chegada
        for note in self.notes_on_screen[:]:  # Copia a lista para evitar modificar enquanto percorre
            if note["y"] >= self.height:
                print(f"Nota atingiu a linha de chegada: {note}")
                self.notes_on_screen.remove(note)  # Remova a nota ou implemente lógica adicional
            

    def handle_input(self):
        
        for note in self.notes_on_screen[:]:  # Copia a lista para evitar modificar enquanto percorre
            if note["y"] >= self.height:  # Se pressionou a tecla correta
                self.notes_on_screen.remove(note)  # Remove a nota do jogo