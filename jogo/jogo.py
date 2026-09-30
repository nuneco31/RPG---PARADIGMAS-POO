import pygame

from graficos.renderizador import Renderizador
from personagens.inimigo import Inimigo
from personagens.jogador import Jogador

from .combate import Combate
from .eventos import Eventos


class Jogo:

    def __init__(self):

        pygame.init()

        self.largura = 1000
        self.altura = 600

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Meu RPG - Paradigmas POO")

        self.relogio = pygame.time.Clock()
        self.rodando = True

        self.jogador = Jogador("Arthur")

        self.inimigo = Inimigo(
            nome="Goblin 1",
            vida=50,
            ataque=15,
            defesa=3,
            xp_recompensa=25,
        )

        self.inimigo2 = Inimigo(
            nome="Goblin 2",
            vida=50,
            ataque=15,
            defesa=3,
            xp_recompensa=25,
        )

        self.jogador_x = 150
        self.jogador_y = 200
        self.velocidade = 5

        self.goblin_x = 650
        self.goblin_y = 100
        self.goblin2_x = 650
        self.goblin2_y = 350

        self.fonte = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 28)

        self.mensagem = "WASD mover | ESPACO = Goblin 1 | H = Goblin 2"

        self.combate = Combate(self)
        self.eventos = Eventos(self)
        self.renderizador = Renderizador(self)

    def executar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(60)

        pygame.quit()

    def processar_eventos(self):
        self.eventos.processar()

    def atacar_goblin1(self):
        self.combate.atacar_goblin1()

    def atacar_goblin2(self):
        self.combate.atacar_goblin2()

    def atualizar(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_w]:
            self.jogador_y -= self.velocidade

        if teclas[pygame.K_s]:
            self.jogador_y += self.velocidade

        if teclas[pygame.K_a]:
            self.jogador_x -= self.velocidade

        if teclas[pygame.K_d]:
            self.jogador_x += self.velocidade

        if self.jogador_x < 0:
            self.jogador_x = 0

        if self.jogador_x > self.largura - 150:
            self.jogador_x = self.largura - 150

        if self.jogador_y < 0:
            self.jogador_y = 0

        if self.jogador_y > self.altura - 250:
            self.jogador_y = self.altura - 250

    def desenhar(self):
        self.renderizador.desenhar()
