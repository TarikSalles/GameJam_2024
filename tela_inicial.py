import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Definindo as dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600

# Criando a tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tela Inicial do Jogo")

# Carregando as imagens
background = pygame.image.load("telaInicial/background_inicial.png")
titulo = pygame.image.load("telaInicial/componente_inicial.png")
botao_jogar = pygame.image.load("telaInicial/botao_jogar.png")
botao_sair = pygame.image.load("telaInicial/botao_sair.png")

# Redimensionando a imagem do título
LARGURA_TITULO, ALTURA_TITULO = titulo.get_size()
novo_tamanho_titulo = (int(LARGURA_TITULO * 0.2), int(ALTURA_TITULO * 0.2))  # Reduzir o tamanho em 20%
titulo = pygame.transform.scale(titulo, novo_tamanho_titulo)

# Redimensionando os botões (opcional, caso necessário)
LARGURA_BOTAO, ALTURA_BOTAO = botao_jogar.get_size()
novo_tamanho_botao = (int(LARGURA_BOTAO * 0.4), int(ALTURA_BOTAO * 0.4))
botao_jogar = pygame.transform.scale(botao_jogar, novo_tamanho_botao)
botao_sair = pygame.transform.scale(botao_sair, novo_tamanho_botao)

# Centralizando a imagem do título
titulo_rect = titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2.5))

# Posicionando os botões abaixo do título
botao_jogar_rect = botao_jogar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 1.7))
botao_sair_rect = botao_sair.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 1.5))

# Função para exibir a tela inicial
def tela_inicial():
    # Loop principal da tela inicial
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Verificando se o clique foi nos botões
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar_rect.collidepoint(evento.pos):
                    print("Botão Jogar pressionado!")
                    # Aqui você pode chamar a função para iniciar o jogo
                elif botao_sair_rect.collidepoint(evento.pos):
                    print("Botão Sair pressionado!")
                    pygame.quit()
                    sys.exit()

        # Desenhando o fundo na tela
        tela.blit(background, (0, 0))
        
        # Desenhando a imagem do título
        tela.blit(titulo, titulo_rect)

        # Desenhando os botões
        tela.blit(botao_jogar, botao_jogar_rect)
        tela.blit(botao_sair, botao_sair_rect)

        # Atualizando a tela
        pygame.display.update()

# Executando a tela inicial
if __name__ == "__main__":
    tela_inicial()
