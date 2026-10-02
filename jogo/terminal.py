import random

from personagens.inimigo import Chefe, Goblin, Mago, Orc
from personagens.jogador import Jogador
from jogo.batalha_terminal import Batalha
from jogo.salvamento import Salvamento


class JogoTerminal:
    """Interface de terminal e orquestração da pequena aventura."""

    def __init__(self, input_fn=input, output_fn=print, rng=None, caminho_save="save.json"):
        self.input = input_fn
        self.output = output_fn
        self.rng = rng or random.Random()
        self.jogador = Jogador("Arthur")
        self.jogador.inventario.adicionar("Poção de Vida", 2)
        self.jogador.inventario.adicionar("Poção de Mana", 1)
        self.jogador.inventario.adicionar("Espada de Ferro")
        self.jogador.inventario.adicionar("Escudo de Ferro")
        self.progresso = {"encontros": 0, "chefe_derrotado": False}
        self.salvamento = Salvamento(caminho_save)

    def _ler(self, prompt="Escolha: "):
        try:
            return self.input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return "sair"

    def _titulo(self, texto):
        self.output("\n" + "=" * 48)
        self.output(f" {texto}")
        self.output("=" * 48)

    def executar(self):
        self._titulo("RPG AVENTURA — FLORESTA SOMBRIA")
        while True:
            self.output(f"\n{self.jogador.nome} | Nv. {self.jogador.nivel} | HP {self.jogador.vida}/{self.jogador.vida_maxima}")
            self.output("1 - Explorar\n2 - Inventário\n3 - Status\n4 - Habilidades\n5 - Salvar jogo\n6 - Carregar jogo\n7 - Sair")
            escolha = self._ler()
            if escolha == "1":
                self.explorar()
            elif escolha == "2":
                self.menu_inventario()
            elif escolha == "3":
                self.jogador.mostrar_status()
                self.output(f"Mana: {self.jogador.mana}/{self.jogador.mana_maxima}")
            elif escolha == "4":
                self.output("Habilidades: " + ", ".join(f"{h.nome} ({h.custo_mana} mana)" for h in self.jogador.habilidades.values()))
            elif escolha == "5":
                self.salvar()
            elif escolha == "6":
                self.carregar()
            elif escolha in ("7", "sair"):
                self.output("A aventura foi encerrada. Até a próxima!")
                return
            else:
                self.output("Opção inválida. Digite um número de 1 a 7.")

    def menu_inventario(self):
        self._titulo("INVENTÁRIO")
        itens = self.jogador.inventario.itens
        if not itens and not self.jogador.inventario.equipamentos:
            self.output("Inventário vazio.")
        for nome, quantidade in itens.items():
            self.output(f"{nome} x{quantidade}")
        for tipo, nome in self.jogador.inventario.equipamentos.items():
            self.output(f"Equipado ({tipo}): {nome}")
        self.output("Digite o nome de uma poção para usar, E para equipar item, ou Enter para voltar.")
        escolha = self._ler("Item: ")
        if escolha.lower() == "e":
            nome = self._ler("Nome do equipamento: ")
            if self.jogador.inventario.equipar(nome, self.jogador):
                self.output(f"{nome} equipado.")
            else:
                self.output("Equipamento indisponível.")
        elif escolha:
            if self.jogador.inventario.usar(escolha, self.jogador):
                self.output(f"{escolha} usado.")
            else:
                self.output("Item indisponível ou não utilizável.")

    def explorar(self):
        self._titulo("FLORESTA SOMBRIA")
        self.output("1 - Seguir pela estrada\n2 - Entrar na floresta\n3 - Procurar itens\n4 - Voltar")
        escolha = self._ler()
        if escolha == "4":
            return
        if escolha not in ("1", "2", "3"):
            self.output("Escolha inválida; você permanece em segurança.")
            return
        if self.progresso["encontros"] >= 3 and not self.progresso["chefe_derrotado"]:
            resultado = self._combater(Chefe())
            if resultado == "vitória":
                self.progresso["chefe_derrotado"] = True
                self.output("A floresta está livre. Você concluiu esta aventura!")
            return
        evento = "tesouro" if escolha == "3" else self.rng.choice(
            ["inimigo"] * 5 + ["tesouro"] * 3 + ["npc"] * 2 + ["armadilha", "raro"]
        )
        self._resolver_evento(evento)

    def _resolver_evento(self, evento):
        if evento == "inimigo":
            classe = self.rng.choice((Goblin, Orc, Mago))
            inimigo = classe()
            etapa = self.progresso["encontros"]
            inimigo.escalar(fator_vida=1 + etapa * 0.08, ataque_extra=etapa * 2, xp_extra=etapa * 10)
            if self._combater(inimigo) == "vitória":
                self.progresso["encontros"] += 1
        elif evento in ("tesouro", "raro"):
            nome = self.rng.choice(("Poção de Vida", "Poção de Mana", "Espada de Ferro", "Escudo de Ferro"))
            qtd = 2 if evento == "raro" else 1
            self.jogador.inventario.adicionar(nome, qtd)
            self.output(f"Você encontrou {nome}" + (f" x{qtd}!" if qtd > 1 else "!"))
        elif evento == "npc":
            self.output("Uma curandeira oferece ajuda. 1 - Aceitar poção | 2 - Seguir")
            if self._ler() == "1":
                self.jogador.inventario.adicionar("Poção de Vida")
                self.output("Você recebeu uma Poção de Vida.")
        else:
            dano = min(max(0, self.jogador.vida - 1), max(1, self.jogador.vida_maxima // 10))
            self.jogador.vida -= dano
            self.output(f"Uma armadilha causa {dano} de dano. Você encontra o caminho de volta em segurança.")

    def _combater(self, inimigo):
        batalha = Batalha(self.jogador, inimigo, self.rng)
        resultado = batalha.lutar(self.input, self.output)
        if resultado == "derrota":
            self.output("Você foi levado para um lugar seguro. Recuperou metade da vida.")
            self.jogador.vida = max(1, self.jogador.vida_maxima // 2)
        return resultado

    def salvar(self):
        try:
            self.salvamento.salvar(self.jogador, self.progresso)
            self.output("Jogo salvo com sucesso.")
        except OSError as erro:
            self.output(f"Não foi possível salvar: {erro}")

    def carregar(self):
        try:
            self.progresso = self.salvamento.carregar(self.jogador)
            self.output("Jogo carregado com sucesso.")
        except (OSError, ValueError, TypeError, KeyError) as erro:
            self.output(f"Não foi possível carregar o jogo: {erro}")
