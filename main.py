import pygame
from piano import Piano
from bola import ControladorEsferas
import random
from music import Music

def main():
    screen_width = 800
    screen_height = 600
    tamanho_linha_width = 700
    tamanho_linha_height = 100
    Score_Geral = 0

    controlador = ControladorEsferas()

    music =  Music("Info.dat", "ExpertPlusStandard.dat", "miser.mp3")
    piano = Piano(controlador, width=screen_width, height=screen_height / 2, 
                  
                  tamanho_linha_width=tamanho_linha_width, tamanho_linha_height=tamanho_linha_height, score = Score_Geral, tipo = "ataque",music=music)

    piano.run_music()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Piano Interativo")

    

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    print("Score Geral: ", piano.get_score_geral())
                    letra_aleatoria = ["W", "A", "S", "D"]
                    piano.criar_esfera(random.choice(letra_aleatoria))

        keys_pressed = pygame.key.get_pressed()
        piano.verificar_colisao(keys_pressed)
            


        for esfera in controlador.esferas:
            esfera.mover() 
            if esfera.update():
                controlador.remover_esfera(esfera)
            


        
        piano.desenhar(screen)
        piano.piano_loop_principal()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
