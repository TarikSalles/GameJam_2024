import pygame
import json
import os

class Game:
    def __init__(self, music):
        self.music = music
        self.running = True
        self.screen_width, self.screen_height = 800, 600  # Define a largura e altura da tela
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("A Sinfonia das Máquinas")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        self.key_map = {pygame.K_w: 0, pygame.K_a: 1, pygame.K_s: 2, pygame.K_d: 3}
        self.col_width = self.screen_width // 4
        self.finish_line_y = 500
        self.hitbox_tolerance = 30
        self.score = 0
        self.notes_on_screen = []
        self.bpm = self.music.bpm
        self.song_time_offset = self.music.song_time_offset

    def spawn_notes(self):
        current_time = pygame.mixer.music.get_pos() / 1000.0  # Tempo da música em segundos
        while self.music.notes and self.music.notes[0]["time"] <= current_time + 2:
            note = self.music.notes.pop(0)
            note_instance = {
                "time": note["time"],
                "x": note["x"],
                "y": -100,  # Começa fora da tela
                "color": note["color"]
            }
            self.notes_on_screen.append(note_instance)

    def update_notes(self, delta_time):
        # Atualiza a posição de cada nota com base no tempo restante
        current_time = pygame.mixer.music.get_pos() / 1000.0
        for note in self.notes_on_screen[:]:
            time_remaining = note["time"] - current_time

            # Atualizar a posição Y da nota
            note["y"] = self.finish_line_y - (300 * time_remaining)

            # Verificar se a nota está fora da tela (muito abaixo)
            if note["y"] > self.screen_height:
                self.notes_on_screen.remove(note)

    def check_hit(self, key_pressed):
        # Verificar se o jogador pressionou a tecla correta no momento certo
        current_time = pygame.mixer.music.get_pos() / 1000.0
        for note in self.notes_on_screen[:]:
            time_difference = abs(note["time"] - current_time)
            if time_difference <= self.hitbox_tolerance:
                # Verificar se a tecla corresponde à nota
                if key_pressed == note["key"]:
                    self.notes_on_screen.remove(note)  # Remove a nota se o hit foi bem-sucedido
                    self.score += 10  # Incrementa a pontuação
                    return True  # Retorna que o hit foi bem-sucedido
        return False

    def handle_key_press(self, key):
        if key in self.key_map:
            col = self.key_map[key]
            for note in self.notes_on_screen[:]:
                if (
                    note["x"] == col
                    and self.finish_line_y - self.hitbox_tolerance <= note["y"] <= self.finish_line_y + self.hitbox_tolerance
                ):
                    self.score += 1
                    self.notes_on_screen.remove(note)

    def draw_notes(self):
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.finish_line_y), (800, self.finish_line_y), 2)
        for note in self.notes_on_screen:
            color = (255, 0, 0) if note["color"] == "red" else (0, 0, 255)
            pos_x = note["x"] * self.col_width + self.col_width // 2
            pygame.draw.circle(self.screen, color, (pos_x, int(note["y"])), 20)

    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def run(self):
        self.music.tocar()
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)

            self.spawn_notes()
            self.update_notes(delta_time)
            self.screen.fill((0, 0, 0))
            self.draw_notes()
            self.draw_ui()
            pygame.display.flip()

class Music:
    def __init__(self, info_file, notes_file, audio_file):
        with open(info_file, "r") as f:
            info = json.load(f)
        self.bpm = info["_beatsPerMinute"]
        self.song_time_offset = info["_songTimeOffset"]
        self.audio_file = audio_file
        with open(notes_file, "r") as f:
            raw_notes = json.loads(f.read())
        self.notes = [
            {
                "time": (note["b"] / self.bpm) * 60 + self.song_time_offset,
                "x": note["x"],
                "color": "red" if note["c"] == 0 else "blue"
            }
            for note in raw_notes["colorNotes"]
        ]

    def tocar(self):
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()

if __name__ == "__main__":
    pygame.init()
    music = Music("Info.dat", "ExpertPlusStandard.dat", "miser.mp3")
    game = Game(music)
    game.run()
    pygame.quit()
