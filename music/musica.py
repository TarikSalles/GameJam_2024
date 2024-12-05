import pygame
from pygame.locals import *
import time

class Musica:
    def __init__(self, partitura, mapeamento_teclas, tempo_base):
        """
        Inicializa a música.
        :param partitura: String com as teclas e tempos da música.
        :param mapeamento_teclas: Dicionário mapeando teclas para sons.
        :param tempo_base: Duração de uma unidade de tempo (em segundos).
        """
        self.partitura = self._processar_partitura(partitura)
        self.mapeamento_teclas = mapeamento_teclas
        self.tempo_base = tempo_base
        self.index_atual = 0
        self.ultimo_tempo = time.time()
        self.sons = self._carregar_sons()

    def _processar_partitura(self, partitura):
        """
        Processa a partitura para separar notas e tempos.
        :param partitura: String com as teclas e tempos.
        :return: Lista de dicionários contendo a tecla e o tempo relativo.
        """
        partitura_processada = []
        for bloco in partitura.split():
            tempo, tecla = self._extrair_tempo_tecla(bloco)
            partitura_processada.append({"tecla": tecla, "tempo": tempo})
        return partitura_processada

    def _extrair_tempo_tecla(self, bloco):
        """
        Extrai o tempo e a tecla de um bloco da partitura.
        :param bloco: Exemplo: "[6u]"
        :return: (tempo, tecla)
        """
        tempo = int(bloco[1])  
        tecla = bloco[2]  
        return tempo, tecla

    def _carregar_sons(self):
        """
        Carrega os sons associados às teclas.
        :return: Dicionário com os sons carregados.
        """
        sons = {}
        for tecla, arquivo_som in self.mapeamento_teclas.items():
            sons[tecla] = pygame.mixer.Sound(arquivo_som)
        return sons

    def tocar(self):
        """
        Toca a música com base na partitura.
        """
        if self.index_atual >= len(self.partitura):
            return 

        bloco_atual = self.partitura[self.index_atual]
        tempo_esperado = bloco_atual["tempo"] * self.tempo_base
        if time.time() - self.ultimo_tempo >= tempo_esperado:
            self.exibir_tecla(bloco_atual["tecla"])
            self.index_atual += 1
            self.ultimo_tempo = time.time()

    def exibir_tecla(self, tecla):
        """
        Mostra a tecla na tela e verifica a interação do jogador.
        :param tecla: A tecla a ser exibida.
        """
        print(f"Pressione a tecla: {tecla}")

    def verificar_interacao(self, tecla_press):
        """
        Verifica se o jogador pressionou a tecla correta.
        :param tecla_press: Tecla pressionada pelo jogador.
        """
        bloco_atual = self.partitura[self.index_atual - 1]
        if bloco_atual["tecla"] == tecla_press:
            print("Acerto! Som tocado.")
            self.sons[tecla_press].play()
        else:
            print("Erro! Nenhum som.")

