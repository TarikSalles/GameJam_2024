import pygame
import random

# Inicializar o Pygame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Piano Tiles Style Game")

# Cores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Carregar música
pygame.mixer.music.load('Mary Had a Little Lamb - Super Easy Piano.mp3')
pygame.mixer.music.play()

# Classe para notas
class Note:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.size = 50

    def draw(self):
        pygame.draw.rect(screen, red, (self.x, self.y, self.size, self.size))

    def update(self):
        self.y += 5  # Velocidade de descida

# Lista de notas
notes = []
keys = {pygame.K_w: 0, pygame.K_a: 1, pygame.K_s: 2, pygame.K_d: 3}
positions = [100, 300, 500, 700]  # Posições das notas

# Função para gerar notas
def generate_notes():
    if random.randint(1, 30) == 1:  # Chance de gerar uma nova nota
        x = positions[random.randint(0, 3)]  # Escolhe uma posição aleatória
        notes.append(Note(x))

# Função principal do jogo
def game_loop():
    clock = pygame.time.Clock()
    running = True
    score = 0

    while running:
        screen.fill(black)
        generate_notes()

        for note in notes:
            note.update()
            note.draw()

        # Verificar se as notas chegaram à linha de acerto
        for note in notes[:]:
            if note.y > screen_height:
                notes.remove(note)  # Remover notas que saem da tela

        # Detecção de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in keys:  # Verifica se a tecla pressionada é uma das notas
                    for note in notes[:]:
                        if note.x == positions[keys[event.key]] and note.y + note.size > screen_height - 100:  # Verifica se a nota está na linha de acerto
                            notes.remove(note)  # Remove a nota se o jogador acertar
                            score += 1  # Aumenta a pontuação
                            print(f"Pontos: {score}")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Iniciar o jogo
game_loop()