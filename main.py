import pygame
from piano import Piano
from bola import ControladorEsferas

# Função principal
def main():
    screen_width = 800
    screen_height = 600
    tamanho_linha_width = 700
    tamanho_linha_height = 100

    # Inicializa o controlador de esferas
    controlador = ControladorEsferas()

    # Cria uma instância do piano com os tamanhos desejados
    piano = Piano(controlador, width=screen_width, height=screen_height / 2, 
                  tamanho_linha_width=tamanho_linha_width, tamanho_linha_height=tamanho_linha_height)

    # Configura a tela
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Piano Interativo")

    # Criação de uma esfera para testar a funcionalidade
    piano.criar_esfera("A")  # Criando uma esfera na linha A

    # Loop principal
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                piano.verificar_colisao(event.key)
            

        # Atualiza as esferas
        for esfera in controlador.esferas:
            esfera.mover(0, 2)  # Move as esferas para baixo
            if esfera.update():
                controlador.remover_esfera(esfera)
            


        
        piano.desenhar(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
