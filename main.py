import pygame
import sys

pygame.init()

screen_width, screen_height = 640, 480

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Teste 123")

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 74)  

text = font.render("Hello World", True, white)

text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(black)
    
    screen.blit(text, text_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
