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
        self.id_bola = 0
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
        self.width_teclas = width // 12
        self.width_setas = width // 24
        self.score = score
        self.tipo = tipo
        self.notes_on_screen = []
        self.acertos = 0
        self.music = music
        self.linhas = [init_x + 100, init_x + 200, init_x + 300, init_x + 400]  # Posições verticais das linhas relativas a init_x
        self.teclas = teclas
        self.tamanho_hitbox = 20
        self.min = 0
        self.teclas_processadas = {tecla: False for tecla in self.teclas}  # Inicializa como não processadas

        self.ball_speed = -2
        self.y_hitbox = self.init_y + self.init_y + self.tamanho_hitbox * 3
        self.hitboxes = [
            pygame.Rect(linha - self.tamanho_hitbox // 2, self.y_hitbox, self.tamanho_hitbox, self.tamanho_hitbox)
            for linha in self.linhas
        ]
   
    def desenhar(self, screen):
        


        for i, y in enumerate(self.linhas):
    
            key_text = self.key_map[self.teclas[i]] 
            tecla_surface = font.render(key_text, True, black)
            screen.blit(tecla_surface, (y - tecla_surface.get_width() / 2, self.init_x + tecla_surface.get_height()))
            if(key_text.lower() == "a" or key_text.lower() == "s" or key_text.lower() == "d" or key_text.lower() == "w"):
                img_placeholder = pygame.image.load(f"assets/{key_text.lower()}_normal.png")
                img_placeholder = pygame.transform.scale(img_placeholder, (self.width_teclas, self.width_teclas))
                screen.blit(img_placeholder, (self.hitboxes[i].x - self.tamanho_hitbox,self.hitboxes[i].y))
            if(key_text.lower() == "↑"):
                img_placeholder = pygame.image.load(f"assets/cima_normal.png")
                img_placeholder = pygame.transform.scale(img_placeholder, (self.width_setas, self.width_setas))
                screen.blit(img_placeholder, (self.hitboxes[i].x - self.tamanho_hitbox //3,self.hitboxes[i].y))
            if(key_text.lower() == "↓"):
                img_placeholder = pygame.image.load(f"assets/baixo_normal.png")
                img_placeholder = pygame.transform.scale(img_placeholder, (self.width_setas, self.width_setas))
                screen.blit(img_placeholder, (self.hitboxes[i].x - self.tamanho_hitbox // 3,self.hitboxes[i].y))
            if(key_text.lower() == "←"):
                img_placeholder = pygame.image.load(f"assets/esq_normal.png")
                img_placeholder = pygame.transform.scale(img_placeholder, (self.width_setas, self.width_setas))
                screen.blit(img_placeholder, (self.hitboxes[i].x - self.tamanho_hitbox // 3,self.hitboxes[i].y))
            if(key_text.lower() == "→"):
                img_placeholder = pygame.image.load(f"assets/dir_normal.png")
                img_placeholder = pygame.transform.scale(img_placeholder, (self.width_setas, self.width_setas))
                screen.blit(img_placeholder, (self.hitboxes[i].x - self.tamanho_hitbox // 3,self.hitboxes[i].y))
        # Desenhar hitboxes
        for hitbox in self.hitboxes:
            #pygame.draw.rect(screen, green, hitbox)
            pass


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
        width = self.width_teclas
        height = self.width_teclas
        esfera = Bola(self.id_bola,x, y, width, height,self.height,self.y_hitbox,velocidade_bola=self.ball_speed, tecla = self.teclas.index(letra), player=  self.player)
        self.id_bola += 1
        self.controlador.esferas.append(esfera)
        return esfera
    
    def get_score_geral(self):
        return self.score

    def verificar_colisao(self):
        """Verifica colisões de todas as esferas com as hitboxes para teclas pressionadas simultaneamente"""
        keys_pressed = pygame.key.get_pressed()
        acertouAlguma = False
        
        for i, hitbox in enumerate(self.hitboxes):  # Para cada hitbox
            tecla = self.teclas[i]  # Tecla associada à hitbox
            
            # Obtem o código da tecla diretamente do mapa
            tecla_code = tecla  # `teclas` já deve conter os códigos (como pygame.K_w)
            
            if keys_pressed[tecla_code]:  # Se a tecla está pressionada
                if not self.teclas_processadas[tecla]:  # Só processa se ainda não foi tratada
                    for esfera in self.controlador.esferas[:]:  # Verifique todas as esferas
                        if hitbox.colliderect(esfera.rect):  # Colisão com a hitbox
                            print(f"{self.key_map[tecla]} OK")  # Exibe a tecla correta
                            
                            # Lógica adicional ao acertar a tecla
                            self.score += self.incremento_score
                            
                            esfera.acertou = True
                            esfera.bola_acerto()
                            acertouAlguma = True
                            # self.controlador.remover_esfera(esfera)  # Remova a esfera
                       
                    
                    # Marca a tecla como processada
                    self.teclas_processadas[tecla] = True
            else:
                # Quando a tecla não está mais pressionada, redefine o estado
                self.teclas_processadas[tecla] = False
        if acertouAlguma:
                        self.score -= self.incremento_score
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