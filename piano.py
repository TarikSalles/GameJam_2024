import pygame
from bola import Bola, ControladorEsferas

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

font = pygame.font.Font(None, 36)

class Piano:
    def __init__(self, controlador, init_x=0, init_y=0, width=800, height=600, tamanho_linha_width=0, tamanho_linha_height=0, score=0, tipo="ataque", incremento_score=0, music=None):
        self.controlador = controlador
        self.init_x = init_x
        self.init_y = init_y
        self.width = width
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
        self.teclas = ["W", "A", "S", "D"]  # Teclas que controlam as esferas
        self.tamanho_hitbox = 20
        self.min = 0
        self.ball_speed = -2
        self.hitboxes = [
            pygame.Rect(linha - self.tamanho_hitbox // 2, init_y + self.init_y + self.tamanho_hitbox * 3, self.tamanho_hitbox, self.tamanho_hitbox)
            for linha in self.linhas
        ]
    def desenhar(self, screen):
        """Desenha o piano na tela"""
        screen.fill(white)

        # Desenhar as linhas verticais
        for i, y in enumerate(self.linhas):
    
            #pygame.draw.line(screen, black, (y, 0), (y, self.height), 3)

            tecla_surface = font.render(self.teclas[i], True, black)
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
        pygame.time.delay(500)  # Pequeno atraso para garantir que tudo esteja carregado
        print("Iniciando o loop principal do jogo...")
    def piano_loop_principal(self):
        if True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Atualizar jogo
            self.spawn_notes()
            self.update_notes()
            self.draw_notes()
            
            
            # Desenhar pontuação
            
    def criar_esfera(self, letra):
        x = self.linhas[self.teclas.index(letra)]
        y = self.height
        width = 10
        height = 10
        esfera = Bola(x, y, width, height,self.height,velocidade_bola=self.ball_speed)
        self.controlador.esferas.append(esfera)
        return esfera
    def verificar_colisao(self, keys_pressed):
        for i, hitbox in enumerate(self.hitboxes):
            tecla_correta = keys_pressed[pygame.key.key_code(self.teclas[i].lower())]
            for esfera in self.controlador.esferas:
                if hitbox.colliderect(esfera.rect):
                    if tecla_correta:
                        print(f"{self.teclas[i]} OK")
                        if self.tipo == "ataque":
                            self.score += self.incremento_score
                        esfera.acertou = True
                        self.controlador.remover_esfera(esfera)
                    return

    def get_score_geral(self):
        return self.score

    def spawn_notes(self):
        # Use o tempo da música para calcular o tempo atual
        current_time = pygame.mixer.music.get_pos() / 1000.0  # Tempo da música em segundos
        while self.music.notes and self.music.notes[0]["time"] <= current_time + 2:  # Spawn 2s antes
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