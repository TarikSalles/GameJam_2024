import pygame
import json
import os

class Music:
    def __init__(self, info_path, beatmap_path, audio_path):
        print("Inicializando a classe Music...")
        self.info = self.load_json(info_path)
        self.beatmap = self.load_json(beatmap_path)
        self.audio_path = audio_path
        self.bpm = self.info.get("_beatsPerMinute", 120.0)
        self.notes = self.parse_notes()
        pygame.mixer.init()
        print("Mixer inicializado.")
    
    def load_json(self, path):
        print(f"Carregando JSON: {path}")
        with open(path, 'r') as f:
            return json.load(f)
    
    def parse_notes(self):
        print("Parseando notas...")
        notes = []
        for note in self.beatmap.get("colorNotes", []):
            beat = note.get("b", 0)
            time = (beat / self.bpm) * 60  # Converte batida para segundos
            x = note.get("x", 0)
            y = note.get("y", 0)
            color = "red" if note.get("c", 0) == 0 else "blue"
            line = int(y * 4)  # Converte y em índice de linha (0-3)
            if 0 <= line < 4:  # Verifica se a linha é válida (0 a 3)
                notes.append({"time": time, "x": x, "y": y, "line": line, "color": color})
        sorted_notes = sorted(notes, key=lambda n: n["time"])
        print(f"Total de notas parseadas: {len(sorted_notes)}")
        return sorted_notes
    
    def tocar(self):
        """Inicia a reprodução da música."""
        try:
            print(f"Carregando música: {self.audio_path}")
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play()
            print(f"Música {self.audio_path} está tocando...")
        except pygame.error as e:
            print(f"Erro ao carregar a música: {e}")

class Game:
    def __init__(self, music):
        print("Inicializando a classe Game...")
        self.music = music
        self.running = True
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("A Sinfonia das Máquinas")
        self.clock = pygame.time.Clock()
        self.notes_on_screen = [[] for _ in range(4)]  # Lista de listas para 4 colunas
        self.finish_line_y = 500  # Posição da linha de chegada no eixo Y
        self.score = [0] * 4  # Pontuação para cada coluna
        self.key_mapping = {0: pygame.K_w, 1: pygame.K_a, 2: pygame.K_s, 3: pygame.K_d}  # Mapeamento das linhas para teclas
        self.font = pygame.font.Font(None, 36)  # Fonte para desenhar o texto na tela
    
    def spawn_notes(self):
        current_time = pygame.mixer.music.get_pos() / 1000.0  # Tempo da música em segundos
        while self.music.notes and self.music.notes[0]["time"] <= current_time + 2:  # Spawn 2s antes
            note = self.music.notes.pop(0)
            note_instance = {
                "time": note["time"],
                "x": note["x"],
                "y": 0,
                "line": note["line"],  # Utilize a linha já definida
                "color": note["color"]
            }
            self.notes_on_screen[note_instance["line"]].append(note_instance)  # Adiciona à lista da coluna correta
            print(f"Nota spawnada: {note_instance}")
    
    def update_notes(self):
        for i in range(4):
            for note in self.notes_on_screen[i]:
                note["y"] += 5  # Move down by 5 pixels por frame
        
        # Verificar se alguma nota alcançou ou passou a linha de chegada
        for i in range(4):
            for note in self.notes_on_screen[i][:]:  # Copia a lista para evitar modificar enquanto percorre
                if note["y"] >= self.finish_line_y:
                    print(f"Nota atingiu a linha de chegada: {note}")
                    self.notes_on_screen[i].remove(note)  # Remova a nota ou implemente lógica adicional
    
    def draw_notes(self):
        # Desenhar linha de chegada com hitbox
        hitbox_rect = pygame.Rect(0, self.finish_line_y - 10, 800, 20)  # Hitbox da linha de chegada
        pygame.draw.rect(self.screen, (255, 255, 255), hitbox_rect)  # Desenhar a linha de chegada
        
        # Desenhar notas e teclas correspondentes
        for i in range(4):
            for note in self.notes_on_screen[i]:
                color = (255, 0, 0) if note["color"] == "red" else (0, 0, 255)
                pos_x = i * 200 + 100  # Cada coluna ocupa 200 pixels
                pygame.draw.circle(self.screen, color, (pos_x, int(note["y"])), 20)
                
                # Desenhar a tecla correspondente abaixo da bolinha
                text = self.font.render(self.get_key_for_line(i), True, (255, 255, 255))
                self.screen.blit(text, (pos_x - 10, self.finish_line_y + 10))  # Ajuste a posição da tecla
    
    def get_key_for_line(self, line):
        """Retorna a tecla associada à linha da bolinha."""
        return {0: "W", 1: "A", 2: "S", 3: "D"}.get(line, "")
    
    def handle_input(self):
        """Verifica se o jogador apertou a tecla certa na hora certa."""
        keys = pygame.key.get_pressed()
        
        for i in range(4):
            for note in self.notes_on_screen[i][:]:  # Copia a lista para evitar modificar enquanto percorre
                if note["y"] >= self.finish_line_y - 20:  # Verifica se a bolinha está dentro da hitbox
                    # Verificar se a tecla correta foi pressionada para a linha correspondente
                    if keys[self.key_mapping[i]]:
                        print(f"Nota correta na linha {i}!")
                        self.score[i] += 1  # Incrementa o score da coluna correspondente
                        self.notes_on_screen[i].remove(note)  # Remove a nota do jogo
    
    def run(self):
        print("Iniciando a reprodução da música...")
        self.music.tocar()
        pygame.time.delay(500)  # Pequeno atraso para garantir que tudo esteja carregado
        print("Iniciando o loop principal do jogo...")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Atualizar jogo
            self.spawn_notes()
            self.update_notes()
            self.handle_input()  # Verificar entrada do jogador
            
            # Desenhar na tela
            self.screen.fill((0, 0, 0))  # Fundo preto
            self.draw_notes()
            
            # Desenhar pontuação
            for i in range(4):
                score_text = self.font.render(f"{self.get_key_for_line(i)}: {self.score[i]}", True, (255, 255, 255))
                self.screen.blit(score_text, (i * 200 + 80, self.finish_line_y + 50))  # Posição das pontuações
            
            pygame.display.flip()
            
            self.clock.tick(60)
        print("Loop principal encerrado.")

if __name__ == "__main__":
    pygame.init()
    # Defina o caminho correto para o arquivo de áudio convertido
    audio_file = "miser.mp3"  # Ou "miser.mp3" se você converteu para MP3
    # Verifique se o arquivo existe
    if not os.path.isfile(audio_file):
        print(f"Erro: O arquivo {audio_file} não foi encontrado.")
    else:
        music = Music("Info.dat", "ExpertPlusStandard.dat", audio_file)
        game = Game(music)
        game.run()
