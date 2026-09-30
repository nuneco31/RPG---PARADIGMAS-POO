import pygame


class Eventos:
    """Centraliza a leitura dos eventos de teclado e mouse do jogo."""

    def __init__(self, jogo):
        # Guarda a referência ao jogo para alterar o estado do jogo.
        self.jogo = jogo

    def processar(self):
        """Lê todas as entradas do usuário e executa a ação correspondente."""
        for evento in pygame.event.get():

            # Quando o usuário fecha a janela, o jogo é encerrado.
            if evento.type == pygame.QUIT:
                self.jogo.rodando = False

            # Quando a tecla for pressionada, decide o que fazer.
            if evento.type == pygame.KEYDOWN:

                # Tecla 1: seleciona o Goblin 1.
                if evento.key == pygame.K_1:
                    self.jogo.selecionar_inimigo(1)

                # Tecla 2: seleciona o Goblin 2.
                if evento.key == pygame.K_2:
                    self.jogo.selecionar_inimigo(2)

                # Espaço: ataca o goblin selecionado.
                if evento.key == pygame.K_SPACE:
                    self.jogo.atacar_inimigo_selecionado()
