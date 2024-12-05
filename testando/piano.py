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
        self.bolinhas = []
        self.tempo_inicio = None
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
            time = (beat / self.bpm) * 60  # Convert beat to seconds
            x = note.get("x", 0)
            y = note.get("y", 0)
            color = "red" if note.get("c", 0) == 0 else "blue"
            notes.append({"time": time, "x": x, "y": y, "color": color})
        sorted_notes = sorted(notes, key=lambda n: n["time"])
        print(f"Total de notas parseadas: {len(sorted_notes)}")
        return sorted_notes
    
    def tocar(self):
        """Inicia a reprodução da música."""
        try:
            print(f"Carregando música: {self.audio_path}")
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play()
            self.tempo_inicio = pygame.time.get_ticks() / 1000.0  # Tempo inicial em segundos
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
        self.start_time = None  # Será definido quando a música começar a tocar
        self.notes_on_screen = []
        self.finish_line_y = 500  # Posição da linha de chegada no eixo Y
        self.score = 0  # Contador de pontos
        self.key_mapping = {0: pygame.K_w, 1: pygame.K_a, 2: pygame.K_s, 3: pygame.K_d}  # Mapeamento das linhas para teclas
        self.font = pygame.font.Font(None, 36)  # Fonte para desenhar o texto na tela
    
    def spawn_notes(self):
        # Use o tempo da música para calcular o tempo atual
        current_time = pygame.mixer.music.get_pos() / 1000.0  # Tempo da música em segundos
        while self.music.notes and self.music.notes[0]["time"] <= current_time + 2:  # Spawn 2s antes
            note = self.music.notes.pop(0)
            note_instance = {"time": note["time"], "x": note["x"], "y": 0, "line": int(note["y"] * 4), "color": note["color"]}
            self.notes_on_screen.append(note_instance)
            print(f"Nota spawnada: {note_instance}")
    
    def update_notes(self):
        for note in self.notes_on_screen:
            note["y"] += 5  # Move down by 5 pixels por frame
        
        # Verificar se alguma nota alcançou ou passou a linha de chegada
        for note in self.notes_on_screen[:]:  # Copia a lista para evitar modificar enquanto percorre
            if note["y"] >= self.finish_line_y:
                print(f"Nota atingiu a linha de chegada: {note}")
                self.notes_on_screen.remove(note)  # Remova a nota ou implemente lógica adicional
    
    def draw_notes(self):
        # Desenhar linha de chegada
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.finish_line_y), (800, self.finish_line_y), 2)
        
        # Desenhar notas e teclas correspondentes
        for note in self.notes_on_screen:
            color = (255, 0, 0) if note["color"] == "red" else (0, 0, 255)
            pos_x = note["x"] * 200 + 100  # Ajuste conforme necessário
            pygame.draw.circle(self.screen, color, (pos_x, int(note["y"])), 20)
            
            # Desenhar a tecla correspondente abaixo da bolinha
            text = self.font.render(self.get_key_for_line(note["line"]), True, (255, 255, 255))
            self.screen.blit(text, (pos_x - 10, self.finish_line_y + 10))  # Ajuste a posição da tecla
    
    def get_key_for_line(self, line):
        """Retorna a tecla associada à linha da bolinha."""
        return {0: "W", 1: "A", 2: "S", 3: "D"}.get(line, "")
    
    def handle_input(self):
        """Verifica se o jogador apertou a tecla certa na hora certa."""
        keys = pygame.key.get_pressed()
        
        for note in self.notes_on_screen[:]:  # Copia a lista para evitar modificar enquanto percorre
            if note["y"] >= self.finish_line_y and keys[self.key_mapping[note["line"]]]:  # Se pressionou a tecla correta
                print(f"Nota correta na linha {note['line']}!")
                self.score += 1  # Incrementa o score
                self.notes_on_screen.remove(note)  # Remove a nota do jogo
    
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
            score_text = self.font.render(f"Pontos: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            
            pygame.display.flip()
            
            self.clock.tick(60)
        print("Loop principal encerrado.")

if __name__ == "__main__":
    pygame.init()
    # Defina o caminho correto para o arquivo de áudio convertido
    audio_file = "miser.mp3"  # Ou "miser.mp3" se você converteu para MP3
    # Verifique se o arquivo existe
    if not os.path.exists(audio_file):
        print(f"Arquivo de áudio não encontrado: {audio_file}")
    else:
        print(f"Arquivo de áudio encontrado: {audio_file}")
        music = Music("Info.dat", "ExpertPlusStandard.dat", audio_file)
        game = Game(music)
        game.run()
    pygame.quit()
    print("Pygame encerrado.")
