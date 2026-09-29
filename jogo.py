
import pygame

from jogador import Jogador
from inimigo import Inimigo


class Jogo:

    def __init__(self):

        pygame.init()

        # ==============================
        # CONFIGURAÇÕES DA TELA
        # ==============================

        self.largura = 1000
        self.altura = 600

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura)
        )

        pygame.display.set_caption(
            "Meu RPG - Paradigmas POO"
        )

        self.relogio = pygame.time.Clock()

        self.rodando = True

        # ==============================
        # JOGADOR
        # ==============================

        self.jogador = Jogador("Arthur")

        # ==============================
        # GOBLIN 1
        # ==============================

        self.inimigo = Inimigo(
            nome="Goblin 1",
            vida=50,
            ataque=15,
            defesa=3,
            xp_recompensa=25
        )

        # ==============================
        # GOBLIN 2
        # ==============================

        self.inimigo2 = Inimigo(
            nome="Goblin 2",
            vida=50,
            ataque=15,
            defesa=3,
            xp_recompensa=25
        )

        # ==============================
        # POSIÇÃO DO JOGADOR
        # ==============================

        self.jogador_x = 150
        self.jogador_y = 200

        self.velocidade = 5

        # ==============================
        # POSIÇÃO DO GOBLIN 1
        # ==============================

        self.goblin_x = 650
        self.goblin_y = 100

        # ==============================
        # POSIÇÃO DO GOBLIN 2
        # ==============================

        self.goblin2_x = 650
        self.goblin2_y = 350

        # ==============================
        # FONTES
        # ==============================

        self.fonte = pygame.font.Font(
            None,
            36
        )

        self.fonte_pequena = pygame.font.Font(
            None,
            28
        )

        # ==============================
        # MENSAGEM
        # ==============================

        self.mensagem = (
            "WASD mover | ESPACO = Goblin 1 | H = Goblin 2"
        )

    # ==============================
    # LOOP PRINCIPAL
    # ==============================

    def executar(self):

        while self.rodando:

            self.processar_eventos()

            self.atualizar()

            self.desenhar()

            self.relogio.tick(60)

        pygame.quit()

    # ==============================
    # EVENTOS
    # ==============================

    def processar_eventos(self):

        for evento in pygame.event.get():

            # ==============================
            # FECHAR JOGO
            # ==============================

            if evento.type == pygame.QUIT:

                self.rodando = False

            # ==============================
            # TECLAS
            # ==============================

            if evento.type == pygame.KEYDOWN:

                # ESPAÇO = atacar Goblin 1
                if evento.key == pygame.K_SPACE:

                    self.atacar_goblin1()

                # H = atacar Goblin 2
                if evento.key == pygame.K_h:

                    self.atacar_goblin2()

    # ==============================
    # ATAQUE GOBLIN 1
    # ==============================

    def atacar_goblin1(self):

        # Verifica se está vivo

        if not self.inimigo.esta_vivo():

            self.mensagem = (
                "Goblin 1 já foi derrotado!"
            )

            return

        # ==============================
        # ARTHUR ATACA
        # ==============================

        vida_antes = self.inimigo.vida

        self.jogador.atacar(
            self.inimigo
        )

        dano = (
            vida_antes -
            self.inimigo.vida
        )

        # ==============================
        # GOBLIN MORREU
        # ==============================

        if not self.inimigo.esta_vivo():

            self.jogador.ganhar_xp(
                self.inimigo.xp_recompensa
            )

            self.mensagem = (
                "GOBLIN 1 DERROTADO! "
                "+25 XP"
            )

            return

        # ==============================
        # GOBLIN CONTRA-ATACA
        # ==============================

        vida_antes = self.jogador.vida

        self.inimigo.atacar(
            self.jogador
        )

        dano_goblin = (
            vida_antes -
            self.jogador.vida
        )

        self.mensagem = (
            f"Goblin 1 causou "
            f"{dano_goblin} de dano! "
            f"Arthur: {self.jogador.vida} HP"
        )

        # ==============================
        # ARTHUR MORREU
        # ==============================

        if not self.jogador.esta_vivo():

            self.mensagem = (
                "ARTHUR FOI DERROTADO!"
            )

    # ==============================
    # ATAQUE GOBLIN 2
    # ==============================

    def atacar_goblin2(self):

        # Verifica se está vivo

        if not self.inimigo2.esta_vivo():

            self.mensagem = (
                "Goblin 2 já foi derrotado!"
            )

            return

        # ==============================
        # ARTHUR ATACA
        # ==============================

        vida_antes = self.inimigo2.vida

        self.jogador.atacar(
            self.inimigo2
        )

        dano = (
            vida_antes -
            self.inimigo2.vida
        )

        # ==============================
        # GOBLIN MORREU
        # ==============================

        if not self.inimigo2.esta_vivo():

            self.jogador.ganhar_xp(
                self.inimigo2.xp_recompensa
            )

            self.mensagem = (
                "GOBLIN 2 DERROTADO! "
                "+25 XP"
            )

            return

        # ==============================
        # GOBLIN CONTRA-ATACA
        # ==============================

        vida_antes = self.jogador.vida

        self.inimigo2.atacar(
            self.jogador
        )

        dano_goblin = (
            vida_antes -
            self.jogador.vida
        )

        self.mensagem = (
            f"Goblin 2 causou "
            f"{dano_goblin} de dano! "
            f"Arthur: {self.jogador.vida} HP"
        )

        # ==============================
        # ARTHUR MORREU
        # ==============================

        if not self.jogador.esta_vivo():

            self.mensagem = (
                "ARTHUR FOI DERROTADO!"
            )

    # ==============================
    # ATUALIZAÇÃO
    # ==============================

    def atualizar(self):

        teclas = pygame.key.get_pressed()

        # ==============================
        # W - CIMA
        # ==============================

        if teclas[pygame.K_w]:

            self.jogador_y -= self.velocidade

        # ==============================
        # S - BAIXO
        # ==============================

        if teclas[pygame.K_s]:

            self.jogador_y += self.velocidade

        # ==============================
        # A - ESQUERDA
        # ==============================

        if teclas[pygame.K_a]:

            self.jogador_x -= self.velocidade

        # ==============================
        # D - DIREITA
        # ==============================

        if teclas[pygame.K_d]:

            self.jogador_x += self.velocidade

        # ==============================
        # LIMITES DA TELA
        # ==============================

        if self.jogador_x < 0:

            self.jogador_x = 0

        if self.jogador_x > self.largura - 150:

            self.jogador_x = (
                self.largura - 150
            )

        if self.jogador_y < 0:

            self.jogador_y = 0

        if self.jogador_y > self.altura - 250:

            self.jogador_y = (
                self.altura - 250
            )

    # ==============================
    # DESENHAR
    # ==============================

    def desenhar(self):

        # ==============================
        # FUNDO
        # ==============================

        self.tela.fill(
            (30, 30, 40)
        )

        # ==============================
        # ARTHUR
        # ==============================

        pygame.draw.rect(
            self.tela,
            (50, 100, 255),
            (
                self.jogador_x,
                self.jogador_y,
                150,
                150
            )
        )

        # ==============================
        # GOBLIN 1
        # ==============================

        if self.inimigo.esta_vivo():

            pygame.draw.rect(
                self.tela,
                (200, 50, 50),
                (
                    self.goblin_x,
                    self.goblin_y,
                    150,
                    150
                )
            )

        # ==============================
        # GOBLIN 2
        # ==============================

        if self.inimigo2.esta_vivo():

            pygame.draw.rect(
                self.tela,
                (180, 50, 180),
                (
                    self.goblin2_x,
                    self.goblin2_y,
                    150,
                    150
                )
            )

        # ==============================
        # NOME ARTHUR
        # ==============================

        texto_jogador = self.fonte.render(
            self.jogador.nome,
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            texto_jogador,
            (
                self.jogador_x + 35,
                self.jogador_y - 40
            )
        )

        # ==============================
        # NOME GOBLIN 1
        # ==============================

        if self.inimigo.esta_vivo():

            texto_inimigo = self.fonte.render(
                self.inimigo.nome,
                True,
                (255, 255, 255)
            )

            self.tela.blit(
                texto_inimigo,
                (
                    self.goblin_x + 20,
                    self.goblin_y - 40
                )
            )

        # ==============================
        # NOME GOBLIN 2
        # ==============================

        if self.inimigo2.esta_vivo():

            texto_inimigo2 = self.fonte.render(
                self.inimigo2.nome,
                True,
                (255, 255, 255)
            )

            self.tela.blit(
                texto_inimigo2,
                (
                    self.goblin2_x + 20,
                    self.goblin2_y - 40
                )
            )

        # ==============================
        # VIDA ARTHUR
        # ==============================

        vida_jogador = self.fonte_pequena.render(
            f"Vida: {self.jogador.vida}",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            vida_jogador,
            (
                self.jogador_x + 20,
                self.jogador_y + 165
            )
        )

        # ==============================
        # ATAQUE ARTHUR
        # ==============================

        ataque_jogador = self.fonte_pequena.render(
            f"Ataque: {self.jogador.ataque}",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            ataque_jogador,
            (
                self.jogador_x + 20,
                self.jogador_y + 195
            )
        )

        # ==============================
        # VIDA GOBLIN 1
        # ==============================

        if self.inimigo.esta_vivo():

            vida_inimigo = self.fonte_pequena.render(
                f"Vida: {self.inimigo.vida}",
                True,
                (255, 255, 255)
            )

            self.tela.blit(
                vida_inimigo,
                (
                    self.goblin_x + 20,
                    self.goblin_y + 165
                )
            )

        # ==============================
        # VIDA GOBLIN 2
        # ==============================

        if self.inimigo2.esta_vivo():

            vida_inimigo2 = self.fonte_pequena.render(
                f"Vida: {self.inimigo2.vida}",
                True,
                (255, 255, 255)
            )

            self.tela.blit(
                vida_inimigo2,
                (
                    self.goblin2_x + 20,
                    self.goblin2_y + 165
                )
            )

        # ==============================
        # NÍVEL
        # ==============================

        nivel = self.fonte_pequena.render(
            f"Nível: {self.jogador.nivel}",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            nivel,
            (30, 30)
        )

        # ==============================
        # XP
        # ==============================

        xp = self.fonte_pequena.render(
            f"XP: {self.jogador.xp}/"
            f"{self.jogador.xp_necessaria}",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            xp,
            (30, 60)
        )

        # ==============================
        # INSTRUÇÕES
        # ==============================

        instrucoes = self.fonte_pequena.render(
            "ESPACO = atacar Goblin 1 | "
            "H = atacar Goblin 2",
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            instrucoes,
            (250, 20)
        )

        # ==============================
        # MENSAGEM
        # ==============================

        texto_mensagem = self.fonte_pequena.render(
            self.mensagem,
            True,
            (255, 255, 255)
        )

        self.tela.blit(
            texto_mensagem,
            (250, 520)
        )

        # ==============================
        # ATUALIZA TELA
        # ==============================

        pygame.display.flip()
