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

        # Controla o número do próximo goblin que aparecerá após uma derrota.
        self.proximo_numero_goblin = 3

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

    def gerar_novo_goblin(self, inimigo_derrotado=None):
        """Cria um novo goblin em lugar do inimigo derrotado para continuar a escalada."""
        if inimigo_derrotado is None:
            if self.inimigo is None or not self.inimigo.esta_vivo():
                inimigo_derrotado = self.inimigo
            elif self.inimigo2 is None or not self.inimigo2.esta_vivo():
                inimigo_derrotado = self.inimigo2
            else:
                return

        alvo_anterior = self.alvo_atual

        # Ajusta as estatísticas do novo goblin usando a escala progressiva
        # pedida pelo jogador: vida +15% e ataque +10% em relação ao goblin
        # que foi derrotado.
        base_vida = getattr(inimigo_derrotado, "vida", 50)
        base_ataque = getattr(inimigo_derrotado, "ataque", 15)

        novo_goblin = Inimigo(
            nome=f"Goblin {self.proximo_numero_goblin}",
            vida=int(base_vida * 1.15) if base_vida > 0 else 50,
            ataque=int(base_ataque * 1.10) if base_ataque > 0 else 15,
            defesa=max(3, int(getattr(inimigo_derrotado, "defesa", 3) * 1.10)),
            xp_recompensa=25 + (self.jogador.nivel - 1) * 10,
        )

        if inimigo_derrotado is self.inimigo:
            self.inimigo = novo_goblin
            self.mensagem = f"Novo inimigo apareceu: {self.inimigo.nome}"
        elif inimigo_derrotado is self.inimigo2:
            self.inimigo2 = novo_goblin
            self.mensagem = f"Novo inimigo apareceu: {self.inimigo2.nome}"
        else:
            self.mensagem = f"Novo inimigo apareceu: {novo_goblin.nome}"

        # Importante: o alvo selecionado não deve ser sobrescrito só porque um
        # goblin diferente foi substituído. Mantemos a seleção atual enquanto ela
        # estiver viva; somente quando o alvo derrotado era o selecionado o novo
        # goblin assume esse papel.
        if alvo_anterior is inimigo_derrotado:
            self.alvo_atual = novo_goblin
        elif self.alvo_atual is None or not self.alvo_atual.esta_vivo():
            if self.inimigo is not None and self.inimigo.esta_vivo():
                self.alvo_atual = self.inimigo
            elif self.inimigo2 is not None and self.inimigo2.esta_vivo():
                self.alvo_atual = self.inimigo2
            else:
                self.alvo_atual = None

        self.proximo_numero_goblin += 1

    def atacar_inimigo_selecionado(self):
        """Executa o combate contra o alvo atual."""
        self.combate.atacar_inimigo_selecionado()

        # Se o alvo atual morreu, cria um novo goblin para continuar o desafio.
        if self.alvo_atual is not None and not self.alvo_atual.esta_vivo():
            self.gerar_novo_goblin(self.alvo_atual)

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
