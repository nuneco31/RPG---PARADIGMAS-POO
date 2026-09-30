import pygame

from graficos.renderizador import Renderizador
from personagens.inimigo import Inimigo
from personagens.jogador import Jogador

from .combate import Combate
from .eventos import Eventos


class Jogo:
    """Classe principal que controla a lógica geral do RPG."""

    def __init__(self):
        # Inicializa a biblioteca gráfica do Pygame.
        pygame.init()

        # Configura a área de exibição da janela do jogo.
        self.largura = 1000
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Meu RPG - Paradigmas POO")

        # Controle de tempo e estado do jogo.
        self.relogio = pygame.time.Clock()
        self.rodando = True

        # Criação do jogador principal.
        self.jogador = Jogador("Arthur")

        # Criação dos dois inimigos disponíveis no combate.
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

        # Define o goblin selecionado inicialmente.
        self.alvo_atual = self.inimigo

        # Posição do jogador e velocidade de movimentação.
        self.jogador_x = 150
        self.jogador_y = 200
        self.velocidade = 5

        # Posição dos goblins na tela.
        self.goblin_x = 650
        self.goblin_y = 100
        self.goblin2_x = 650
        self.goblin2_y = 350

        # Fontes utilizadas para mostrar textos na tela.
        self.fonte = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 28)

        # Mensagem que orienta o jogador no início da partida.
        self.mensagem = "1 = Goblin 1 | 2 = Goblin 2 | ESPACO = atacar"

        # Instancia os módulos responsáveis por combate, eventos e renderização.
        self.combate = Combate(self)
        self.eventos = Eventos(self)
        self.renderizador = Renderizador(self)

    def executar(self):
        """Loop principal do jogo."""
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(60)

        pygame.quit()

    def processar_eventos(self):
        """Encaminha eventos do teclado para o módulo de eventos."""
        self.eventos.processar()

    def selecionar_inimigo(self, numero):
        """Seleciona qual goblin será atacado."""
        if numero == 1:
            alvo = self.inimigo
        elif numero == 2:
            alvo = self.inimigo2
        else:
            return

        # Se o inimigo escolhido já morreu, tenta selecionar outro vivo.
        if not alvo.esta_vivo():
            for inimigo in (self.inimigo, self.inimigo2):
                if inimigo.esta_vivo():
                    self.alvo_atual = inimigo
                    self.mensagem = (
                        f"{alvo.nome} já foi derrotado! "
                        f"Novo alvo: {inimigo.nome}"
                    )
                    return

            self.alvo_atual = None
            self.mensagem = "Todos os goblins foram derrotados!"
            return

        self.alvo_atual = alvo
        self.mensagem = f"Alvo selecionado: {alvo.nome}"

    def atacar_inimigo_selecionado(self):
        """Executa o combate contra o alvo atual."""
        self.combate.atacar_inimigo_selecionado()

    def atacar_goblin1(self):
        """Compatibilidade com chamadas antigas do código."""
        self.selecionar_inimigo(1)
        self.atacar_inimigo_selecionado()

    def atacar_goblin2(self):
        """Compatibilidade com chamadas antigas do código."""
        self.selecionar_inimigo(2)
        self.atacar_inimigo_selecionado()

    def atualizar(self):
        """Atualiza a posição do jogador conforme as teclas pressionadas."""
        teclas = pygame.key.get_pressed()

        # Movimentação para cima.
        if teclas[pygame.K_w]:
            self.jogador_y -= self.velocidade

        # Movimentação para baixo.
        if teclas[pygame.K_s]:
            self.jogador_y += self.velocidade

        # Movimentação para esquerda.
        if teclas[pygame.K_a]:
            self.jogador_x -= self.velocidade

        # Movimentação para direita.
        if teclas[pygame.K_d]:
            self.jogador_x += self.velocidade

        # Limita a movimentação dentro da tela.
        if self.jogador_x < 0:
            self.jogador_x = 0

        if self.jogador_x > self.largura - 150:
            self.jogador_x = self.largura - 150

        if self.jogador_y < 0:
            self.jogador_y = 0

        if self.jogador_y > self.altura - 250:
            self.jogador_y = self.altura - 250

    def desenhar(self):
        """Solicita a renderização da tela completa."""
        self.renderizador.desenhar()
