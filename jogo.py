import pygame

from jogador import Jogador
from inimigo import Inimigo


class Jogo:

    def __init__(self):

        pygame.init()

        self.largura = 1000
        self.altura = 600

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura)
        )

        pygame.display.set_caption("Meu RPG")

        self.relogio = pygame.time.Clock()

        self.rodando = True

        # ==============================
        # CRIANDO OS PERSONAGENS
        # ==============================

        self.jogador = Jogador("Arthur")

        self.inimigo = Inimigo(
            nome="Goblin",
            vida=50,
            ataque=15,
            defesa=3,
            xp_recompensa=100
        )

        # Fonte para os textos
        self.fonte = pygame.font.Font(None, 36)

    def executar(self):

        while self.rodando:

            self.processar_eventos()

            self.atualizar()

            self.desenhar()

            self.relogio.tick(60)

        pygame.quit()

    def processar_eventos(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.rodando = False

    def atualizar(self):

        pass

    def desenhar(self):

        # Fundo
        self.tela.fill((30, 30, 40))

        # ==============================
        # JOGADOR
        # ==============================

        pygame.draw.rect(
            self.tela,
            (50, 100, 255),
            (150, 200, 200, 200)
        )

        # ==============================
        # INIMIGO
        # ==============================

        pygame.draw.rect(
            self.tela,
            (200, 50, 50),
            (650, 200, 200, 200)
        )

        # ==============================
        # NOME DO JOGADOR
        # ==============================

        texto_jogador = self.fonte.render(
            self.jogador.nome,
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            texto_jogador,
            (190, 160)
        )

        # ==============================
        # NOME DO INIMIGO
        # ==============================

        texto_inimigo = self.fonte.render(
            self.inimigo.nome,
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            texto_inimigo,
            (700, 160)
        )

        # ==============================
        # VIDA DO JOGADOR
        # ==============================

        vida_jogador = self.fonte.render(
            f"Vida: {self.jogador.vida}",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            vida_jogador,
            (190, 420)
        )

        # ==============================
        # VIDA DO INIMIGO
        # ==============================

        vida_inimigo = self.fonte.render(
            f"Vida: {self.inimigo.vida}",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            vida_inimigo,
            (700, 420)
        )

        pygame.display.flip()