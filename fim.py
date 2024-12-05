import pygame
import sys

def exibir_tela_fim_jogo(tela, vencedor):
    fonte_titulo = pygame.font.Font(None, 74)
    fonte_instrucoes = pygame.font.Font(None, 36)
    
    # Renderiza a mensagem de vitória
    texto_vitoria = fonte_titulo.render(f"Jogador {vencedor} Venceu!", True, (255, 0, 0))
    texto_vitoria_rect = texto_vitoria.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2 - 50))
    
    # Renderiza a instrução para fechar o jogo
    texto_instrucoes = fonte_instrucoes.render("Pressione ENTER para fechar o jogo", True, (255, 255, 255))
    texto_instrucoes_rect = texto_instrucoes.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2 + 50))
    
    # Preenche a tela com preto
    tela.fill((0, 0, 0))
    
    # Desenha os textos na tela
    tela.blit(texto_vitoria, texto_vitoria_rect)
    tela.blit(texto_instrucoes, texto_instrucoes_rect)
    pygame.display.flip()  # Atualiza a tela
    
    # Loop para manter a tela de fim de jogo até o usuário fechar ou pressionar Enter
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()