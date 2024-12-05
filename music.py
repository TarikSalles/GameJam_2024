
import json

import pygame
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
            time = (beat / self.bpm) * 60 
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