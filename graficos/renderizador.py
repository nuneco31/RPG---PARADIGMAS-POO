import pygame


class Renderizador:

    def __init__(self, jogo):
        self.jogo = jogo

    def desenhar(self):
        tela = self.jogo.tela
        tela.fill((30, 30, 40))

        pygame.draw.rect(
            tela,
            (50, 100, 255),
            (self.jogo.jogador_x, self.jogo.jogador_y, 150, 150),
        )

        if self.jogo.inimigo.esta_vivo():
            pygame.draw.rect(
                tela,
                (200, 50, 50),
                (self.jogo.goblin_x, self.jogo.goblin_y, 150, 150),
            )

        if self.jogo.inimigo2.esta_vivo():
            pygame.draw.rect(
                tela,
                (180, 50, 180),
                (self.jogo.goblin2_x, self.jogo.goblin2_y, 150, 150),
            )

        texto_jogador = self.jogo.fonte.render(self.jogo.jogador.nome, True, (255, 255, 255))
        tela.blit(texto_jogador, (self.jogo.jogador_x + 35, self.jogo.jogador_y - 40))

        if self.jogo.inimigo.esta_vivo():
            texto_inimigo = self.jogo.fonte.render(self.jogo.inimigo.nome, True, (255, 255, 255))
            tela.blit(texto_inimigo, (self.jogo.goblin_x + 20, self.jogo.goblin_y - 40))

        if self.jogo.inimigo2.esta_vivo():
            texto_inimigo2 = self.jogo.fonte.render(self.jogo.inimigo2.nome, True, (255, 255, 255))
            tela.blit(texto_inimigo2, (self.jogo.goblin2_x + 20, self.jogo.goblin2_y - 40))

        vida_jogador = self.jogo.fonte_pequena.render(
            f"Vida: {self.jogo.jogador.vida}", True, (255, 255, 255)
        )
        tela.blit(vida_jogador, (self.jogo.jogador_x + 20, self.jogo.jogador_y + 165))

        ataque_jogador = self.jogo.fonte_pequena.render(
            f"Ataque: {self.jogo.jogador.ataque}", True, (255, 255, 255)
        )
        tela.blit(ataque_jogador, (self.jogo.jogador_x + 20, self.jogo.jogador_y + 195))

        if self.jogo.inimigo.esta_vivo():
            vida_inimigo = self.jogo.fonte_pequena.render(
                f"Vida: {self.jogo.inimigo.vida}", True, (255, 255, 255)
            )
            tela.blit(vida_inimigo, (self.jogo.goblin_x + 20, self.jogo.goblin_y + 165))

        if self.jogo.inimigo2.esta_vivo():
            vida_inimigo2 = self.jogo.fonte_pequena.render(
                f"Vida: {self.jogo.inimigo2.vida}", True, (255, 255, 255)
            )
            tela.blit(vida_inimigo2, (self.jogo.goblin2_x + 20, self.jogo.goblin2_y + 165))

        nivel = self.jogo.fonte_pequena.render(f"Nível: {self.jogo.jogador.nivel}", True, (255, 255, 255))
        tela.blit(nivel, (30, 30))

        xp = self.jogo.fonte_pequena.render(
            f"XP: {self.jogo.jogador.xp}/{self.jogo.jogador.xp_necessaria}",
            True,
            (255, 255, 255),
        )
        tela.blit(xp, (30, 60))

        instrucoes = self.jogo.fonte_pequena.render(
            "ESPACO = atacar Goblin 1 | H = atacar Goblin 2",
            True,
            (255, 255, 255),
        )
        tela.blit(instrucoes, (250, 20))

        texto_mensagem = self.jogo.fonte_pequena.render(self.jogo.mensagem, True, (255, 255, 255))
        tela.blit(texto_mensagem, (250, 520))

        pygame.display.flip()
