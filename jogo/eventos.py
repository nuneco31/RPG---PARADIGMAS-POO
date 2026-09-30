import pygame


class Eventos:

    def __init__(self, jogo):
        self.jogo = jogo

    def processar(self):
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.jogo.rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.jogo.atacar_goblin1()

                if evento.key == pygame.K_h:
                    self.jogo.atacar_goblin2()
