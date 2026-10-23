"""Adaptador Pygame: janela e interação; as regras pertencem à Campanha."""

import os

from jogo.campanha import Campanha
from jogo.interface_eventos import EventosInterface
from graficos.interface_renderizador import InterfaceRenderizador


class JogoInterface:
    """Compõe uma campanha com entrada e desenho, sem duplicar suas regras.

    As propriedades expõem somente os dados que a apresentação consulta.
    Assim a Campanha também pode ser usada pelo terminal e pelos testes.
    """

    def __init__(self, rng=None, caminho_save=None):
        os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
        import pygame

        self.campanha = Campanha(rng=rng, caminho_save=caminho_save)
        self.pygame = pygame
        # Não inicializamos áudio: a aventura não precisa de um dispositivo sonoro.
        pygame.display.init()
        pygame.font.init()
        self.tela = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Crônicas da Floresta • RPG de Paradigmas")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 32)
        self.fonte_pequena = pygame.font.Font(None, 24)
        self.fonte_menor = pygame.font.Font(None, 20)
        self.botoes = []
        self.eventos = EventosInterface(self)
        self.renderizador = InterfaceRenderizador(self)

    def executar(self):
        redesenhar = True
        try:
            while self.rodando:
                redesenhar = self.eventos.processar() or redesenhar
                if self.rodando and redesenhar:
                    self.renderizador.desenhar()
                    redesenhar = False
                self.relogio.tick(30)
        finally:
            self.pygame.quit()

    def acionar(self, acao):
        if acao.startswith("pagina:"):
            if self.estado == "inventario":
                passo = 1 if acao == "pagina:proxima" else -1
                self.renderizador.pagina_inventario = max(
                    0, self.renderizador.pagina_inventario + passo
                )
            return
        if acao == "inventario" and self.estado != "inventario":
            self.renderizador.pagina_inventario = 0
        self.campanha.acionar(acao)

    @property
    def jogador(self):
        return self.campanha.jogador

    @property
    def progresso(self):
        return self.campanha.progresso

    @property
    def inimigo(self):
        return self.campanha.inimigo

    @property
    def batalha(self):
        return self.campanha.batalha

    @property
    def resultado_batalha(self):
        return self.campanha.resultado_batalha

    @property
    def mensagem(self):
        return self.campanha.mensagem

    @property
    def estado(self):
        return self.campanha.estado

    @estado.setter
    def estado(self, valor):
        self.campanha.estado = valor

    @property
    def rodando(self):
        return self.campanha.rodando

    @rodando.setter
    def rodando(self, valor):
        self.campanha.rodando = valor

    # Fachadas curtas preservam os exemplos e os testes da versão anterior.
    def _evento(self, evento):
        return self.campanha._evento(evento)

    def _acao_combate(self, acao, habilidade=None):
        return self.campanha._acao_combate(acao, habilidade)

    def _continuar_apos_batalha(self):
        return self.campanha._continuar_apos_batalha()
