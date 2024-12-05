import pygame
from piano import Piano
from bola import ControladorEsferas
import random
from music import Music

def main():
    screen_width = 1000
    screen_height = 600
    tamanho_linha_width = 700
    tamanho_linha_height = 100
    music_player1 =  Music("Info.dat", "ExpertPlusStandard.dat", "miser.mp3")
    music_player2 =  Music("Info.dat", "ExpertPlusStandard.dat", "miser.mp3")

    score_player1 = 0
    score_player2 = 0
    tempoAtual = 0.0
    tempoDuracao = 15.0
    turnoPlayer1 = True
    controlador_esferas_player_1 = ControladorEsferas()
    controlador_esferas_player_2 = ControladorEsferas()


    beats_player1 = Piano(controlador_esferas_player_1, width=screen_width / 2, height=screen_height / 2, tamanho_linha_width=tamanho_linha_width, tamanho_linha_height=tamanho_linha_height, score = score_player1, tipo = "ataque",music=music_player1,teclas = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d])
    beats_player2 = Piano(controlador_esferas_player_2, width=screen_width / 2, height=screen_height / 2, tamanho_linha_width=tamanho_linha_width, tamanho_linha_height=tamanho_linha_height, score = score_player2, tipo = "ataque",music=music_player2,init_x= screen_width / 2 + 50, init_y=0,teclas = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT])

    beats_player1.run_music()
    beats_player2.run_music()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("")
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        

        for esfera in controlador_esferas_player_1.esferas:
                esfera.mover() 
                if (esfera.update()):
                    controlador_esferas_player_1.remover_esfera(esfera)
        

      
        for esfera in controlador_esferas_player_2.esferas:
                esfera.mover() 
                if esfera.update():
                    controlador_esferas_player_2.remover_esfera(esfera)
        
        #beats_player1.piano_loop_principal()
        #beats_player2.piano_loop_principal()
    
        #beats_player1.spawn_notes()
        beats_player2.spawn_notes()

        beats_player1.spawn_notes()
        beats_player1.update_notes()
        beats_player2.update_notes()

        beats_player1.verificar_colisao() 
        beats_player2.verificar_colisao()
        score_player1 = beats_player1.get_score_geral()
        score_player2 = beats_player2.get_score_geral()
        beats_player1.desenhar(screen)
        beats_player2.desenhar(screen)
    

        pygame.display.flip()
        clock.tick(60)
        

    pygame.quit()

if __name__ == "__main__":
    main()
