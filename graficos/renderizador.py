import pygame


class Renderizador:
    """Responsável por desenhar tudo que aparece na tela do jogo."""

    def __init__(self, jogo):
        # Guarda a referência ao jogo para acessar personagens e posições.
        self.jogo = jogo

    def desenhar(self):
        """Desenha o fundo, personagens, vida e instruções na tela."""
        tela = self.jogo.tela

        # Fundo da tela.
        tela.fill((30, 30, 40))

        # Desenha o jogador principal.
        pygame.draw.rect(
            tela,
            (50, 100, 255),
            (self.jogo.jogador_x, self.jogo.jogador_y, 150, 150),
        )

        # Desenha o Goblin 1 se ainda estiver vivo.
        if self.jogo.inimigo.esta_vivo():
            pygame.draw.rect(
                tela,
                (200, 50, 50),
                (self.jogo.goblin_x, self.jogo.goblin_y, 150, 150),
            )

        # Desenha o Goblin 2 se ainda estiver vivo.
        if self.jogo.inimigo2.esta_vivo():
            pygame.draw.rect(
                tela,
                (180, 50, 180),
                (self.jogo.goblin2_x, self.jogo.goblin2_y, 150, 150),
            )

        # Destaca o goblin selecionado com borda amarela.
        if self.jogo.alvo_atual is not None and self.jogo.alvo_atual.esta_vivo():
            if self.jogo.alvo_atual == self.jogo.inimigo:
                pygame.draw.rect(
                    tela,
                    (255, 255, 0),
                    (self.jogo.goblin_x - 5, self.jogo.goblin_y - 5, 160, 160),
                    4,
                )
            elif self.jogo.alvo_atual == self.jogo.inimigo2:
                pygame.draw.rect(
                    tela,
                    (255, 255, 0),
                    (self.jogo.goblin2_x - 5, self.jogo.goblin2_y - 5, 160, 160),
                    4,
                )

        # Nome do jogador.
        texto_jogador = self.jogo.fonte.render(
            self.jogo.jogador.nome, True, (255, 255, 255)
        )
        tela.blit(
            texto_jogador,
            (self.jogo.jogador_x + 35, self.jogo.jogador_y - 40),
        )

        # Nome do Goblin 1.
        if self.jogo.inimigo.esta_vivo():
            texto_inimigo = self.jogo.fonte.render(
                self.jogo.inimigo.nome, True, (255, 255, 255)
            )
            tela.blit(
                texto_inimigo,
                (self.jogo.goblin_x + 20, self.jogo.goblin_y - 40),
            )

        # Nome do Goblin 2.
        if self.jogo.inimigo2.esta_vivo():
            texto_inimigo2 = self.jogo.fonte.render(
                self.jogo.inimigo2.nome, True, (255, 255, 255)
            )
            tela.blit(
                texto_inimigo2,
                (self.jogo.goblin2_x + 20, self.jogo.goblin2_y - 40),
            )

        # Vida e ataque do jogador.
        vida_jogador = self.jogo.fonte_pequena.render(
            f"Vida: {self.jogo.jogador.vida}", True, (255, 255, 255)
        )
        tela.blit(
            vida_jogador,
            (self.jogo.jogador_x + 20, self.jogo.jogador_y + 165),
        )

        ataque_jogador = self.jogo.fonte_pequena.render(
            f"Ataque: {self.jogo.jogador.ataque}", True, (255, 255, 255)
        )
        tela.blit(
            ataque_jogador,
            (self.jogo.jogador_x + 20, self.jogo.jogador_y + 195),
        )

        # Vida dos goblins vivos.
        if self.jogo.inimigo.esta_vivo():
            vida_inimigo = self.jogo.fonte_pequena.render(
                f"Vida: {self.jogo.inimigo.vida}", True, (255, 255, 255)
            )
            tela.blit(
                vida_inimigo,
                (self.jogo.goblin_x + 20, self.jogo.goblin_y + 165),
            )

        if self.jogo.inimigo2.esta_vivo():
            vida_inimigo2 = self.jogo.fonte_pequena.render(
                f"Vida: {self.jogo.inimigo2.vida}", True, (255, 255, 255)
            )
            tela.blit(
                vida_inimigo2,
                (self.jogo.goblin2_x + 20, self.jogo.goblin2_y + 165),
            )

        # Exibe nível e XP.
        nivel = self.jogo.fonte_pequena.render(
            f"Nível: {self.jogo.jogador.nivel}", True, (255, 255, 255)
        )
        tela.blit(nivel, (30, 30))

        xp = self.jogo.fonte_pequena.render(
            f"XP: {self.jogo.jogador.xp}/{self.jogo.jogador.xp_necessaria}",
            True,
            (255, 255, 255),
        )
        tela.blit(xp, (30, 60))

        # Instruções de seleção e ataque.
        instrucoes = self.jogo.fonte_pequena.render(
            "1 = Goblin 1 | 2 = Goblin 2 | ESPACO = atacar",
            True,
            (255, 255, 255),
        )
        tela.blit(instrucoes, (200, 20))

        # Mensagem atual do jogo.
        texto_mensagem = self.jogo.fonte_pequena.render(
            self.jogo.mensagem, True, (255, 255, 255)
        )
        tela.blit(texto_mensagem, (200, 520))

        # Atualiza a tela para mostrar o próximo frame.
        pygame.display.flip()
