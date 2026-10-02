import random
import os
import io
from contextlib import redirect_stdout

from personagens.inimigo import Chefe, Goblin, Mago, Orc
from personagens.jogador import Jogador
from jogo.batalha_terminal import Batalha
from jogo.salvamento import Salvamento
from jogo.interface_eventos import EventosInterface
from graficos.interface_renderizador import InterfaceRenderizador


class JogoInterface:
    """Coordena a campanha gráfica e reaproveita as regras do domínio."""

    def __init__(self, rng=None, caminho_save="save.json"):
        os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
        import pygame

        pygame.init()
        self.pygame = pygame
        self.tela = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("RPG Aventura — Floresta Sombria")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 38)
        self.fonte_pequena = pygame.font.Font(None, 27)
        self.fonte_menor = pygame.font.Font(None, 22)
        self.rodando = True

        self.jogador = Jogador("Arthur")
        self.jogador.inventario.adicionar("Poção de Vida", 2)
        self.jogador.inventario.adicionar("Poção de Mana")
        self.jogador.inventario.adicionar("Espada de Ferro")
        self.jogador.inventario.adicionar("Escudo de Ferro")
        self.progresso = {"encontros": 0, "chefe_derrotado": False}
        self.rng = rng or random.Random()
        self.salvamento = Salvamento(caminho_save)

        self.estado = "menu"
        self.estado_anterior = "menu"
        self.mensagem = "A Floresta Sombria guarda um perigo antigo. Prepare-se para explorar."
        self.inimigo = None
        self.batalha = None
        self.resultado_batalha = None
        self.botoes = []
        self.eventos = EventosInterface(self)
        self.renderizador = InterfaceRenderizador(self)

    def executar(self):
        while self.rodando:
            self.eventos.processar()
            self.renderizador.desenhar()
            self.relogio.tick(60)
        self.pygame.quit()

    def acionar(self, acao):
        """Executa uma ação indicada por botão; as regras ficam nos objetos de domínio."""
        if acao == "sair":
            self.rodando = False
        elif acao == "explorar":
            self.estado = "exploracao"
        elif acao == "inventario":
            self.estado_anterior = self.estado
            self.estado = "inventario"
        elif acao == "status":
            self.estado_anterior = self.estado
            self.estado = "status"
        elif acao == "habilidades":
            self.estado_anterior = self.estado
            self.estado = "habilidades"
        elif acao == "salvar":
            self._salvar()
        elif acao == "carregar":
            self._carregar()
        elif acao == "estrada" or acao == "floresta":
            self._explorar_rota(acao)
        elif acao == "procurar":
            self._evento("tesouro")
        elif acao == "voltar_menu":
            self.estado = "menu"
        elif acao == "voltar_anterior":
            self.estado = self.estado_anterior
        elif acao == "voltar_exploracao":
            self.estado = "exploracao"
        elif acao == "abrir_habilidades_combate":
            self.estado = "selecionar_habilidade"
        elif acao == "voltar_combate":
            self.estado = "combate"
        elif acao == "aceitar_pocao":
            self.jogador.inventario.adicionar("Poção de Vida")
            self.mensagem = "A curandeira lhe entregou uma Poção de Vida."
            self.estado = "evento"
        elif acao == "recusar_npc":
            self.mensagem = "Você agradece e segue pela floresta."
            self.estado = "evento"
        elif acao.startswith("usar:"):
            nome = acao.split(":", 1)[1]
            if self.jogador.inventario.usar(nome, self.jogador):
                self.mensagem = f"Você usou {nome}."
            else:
                self.mensagem = "Esse item não pode ser usado agora."
        elif acao.startswith("equipar:"):
            nome = acao.split(":", 1)[1]
            if self.jogador.inventario.equipar(nome, self.jogador):
                self.mensagem = f"{nome} equipado. Seus atributos foram atualizados."
            else:
                self.mensagem = "Esse equipamento não está disponível."
        elif acao.startswith("habilidade:"):
            self._usar_habilidade(acao.split(":", 1)[1])
        elif acao.startswith("combate:"):
            self._acao_combate(acao.split(":", 1)[1])
        elif acao == "continuar":
            self._continuar_apos_batalha()

    def _explorar_rota(self, rota):
        if self.progresso["encontros"] >= 3 and not self.progresso["chefe_derrotado"]:
            self._iniciar_batalha(Chefe())
            return
        if rota == "estrada":
            eventos = ["inimigo"] * 3 + ["tesouro"] * 3 + ["npc"] * 4 + ["armadilha", "raro"]
        else:
            eventos = ["inimigo"] * 6 + ["tesouro"] * 2 + ["npc", "armadilha"] * 2 + ["raro"]
        evento = self.rng.choice(eventos)
        self._evento(evento)

    def _evento(self, evento):
        if evento == "inimigo":
            classe = self.rng.choice((Goblin, Orc, Mago))
            inimigo = classe()
            etapa = self.progresso["encontros"]
            inimigo.escalar(1 + etapa * 0.08, etapa * 2, etapa * 10)
            self._iniciar_batalha(inimigo)
        elif evento in ("tesouro", "raro"):
            nome = self.rng.choice(("Poção de Vida", "Poção de Mana", "Espada de Ferro", "Escudo de Ferro"))
            quantidade = 2 if evento == "raro" else 1
            self.jogador.inventario.adicionar(nome, quantidade)
            self.mensagem = f"Você encontrou {nome}" + (f" x{quantidade}!" if quantidade > 1 else "!")
            self.estado = "evento"
        elif evento == "npc":
            self.mensagem = "Uma curandeira oferece uma Poção de Vida. Aceitar?"
            self.estado = "npc"
        else:
            dano = min(max(0, self.jogador.vida - 1), max(1, self.jogador.vida_maxima // 10))
            self.jogador.vida -= dano
            self.mensagem = f"Uma armadilha causa {dano} de dano. Você consegue voltar em segurança."
            self.estado = "evento"

    def _iniciar_batalha(self, inimigo):
        self.inimigo = inimigo
        self.batalha = Batalha(self.jogador, inimigo, self.rng)
        self.resultado_batalha = None
        self.mensagem = f"{inimigo.nome} bloqueia seu caminho! Escolha uma ação."
        self.estado = "combate"

    def _acao_combate(self, acao, habilidade=None):
        if self.batalha is None or self.batalha.encerrada:
            return
        nivel_anterior = self.jogador.nivel
        with redirect_stdout(io.StringIO()):
            self.mensagem = self.batalha.executar_acao(acao, habilidade=habilidade)
        if self.jogador.nivel > nivel_anterior:
            self.mensagem += f"\nLevel up! Você chegou ao nível {self.jogador.nivel}."
        if self.batalha.encerrada:
            if not self.inimigo.esta_vivo():
                self.resultado_batalha = "vitoria"
            elif not self.jogador.esta_vivo():
                self.resultado_batalha = "derrota"
            else:
                self.resultado_batalha = "fuga"
            self.estado = "fim_batalha"

    def _usar_habilidade(self, nome):
        if self.estado == "selecionar_habilidade":
            self.estado = "combate"
            self._acao_combate("2", habilidade=nome)
        elif nome == "Cura":
            if self.jogador.usar_habilidade_nome(nome):
                self.mensagem = "Você usou Cura e recuperou vida."
            else:
                self.mensagem = "Mana insuficiente para usar Cura."
            self.estado = "habilidades"
        else:
            self.mensagem = "Habilidades de ataque só podem ser usadas durante um combate."

    def _continuar_apos_batalha(self):
        if self.resultado_batalha == "vitoria":
            if isinstance(self.inimigo, Chefe):
                self.progresso["chefe_derrotado"] = True
                self.estado = "conclusao"
                self.mensagem = "O Rei Goblin foi derrotado! A Floresta Sombria está livre."
                return
            self.progresso["encontros"] += 1
        elif self.resultado_batalha == "derrota":
            self.mensagem = "Você foi levado para um lugar seguro e recuperou parte da vida."
            self.jogador.vida = max(1, self.jogador.vida_maxima // 2)
        else:
            self.mensagem = "Você escapou e voltou para a trilha."
        self.estado = "exploracao"
        self.inimigo = None
        self.batalha = None

    def _salvar(self):
        try:
            self.salvamento.salvar(self.jogador, self.progresso)
            self.mensagem = "Jogo salvo com sucesso."
        except OSError as erro:
            self.mensagem = f"Não foi possível salvar o jogo: {erro}"

    def _carregar(self):
        try:
            self.progresso = self.salvamento.carregar(self.jogador)
            self.mensagem = "Jogo carregado com sucesso."
        except (OSError, ValueError, TypeError, KeyError) as erro:
            self.mensagem = f"Não foi possível carregar o jogo: {erro}"
