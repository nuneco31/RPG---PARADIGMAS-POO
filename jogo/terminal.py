"""Apresentação textual da mesma campanha usada pela janela Pygame."""
from jogo.batalha_terminal import Batalha
from jogo.campanha import Campanha


class JogoTerminal:
    """Lê escolhas e apresenta respostas; Campanha decide as regras da aventura."""

    def __init__(self, input_fn=input, output_fn=print, rng=None, caminho_save=None):
        self.input = input_fn
        self.output = output_fn
        self.campanha = Campanha(rng=rng, caminho_save=caminho_save)

    @property
    def jogador(self):
        return self.campanha.jogador

    @property
    def progresso(self):
        return self.campanha.progresso

    @property
    def rng(self):
        return self.campanha.rng

    @property
    def salvamento(self):
        return self.campanha.salvamento

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
        self._titulo("CRÔNICAS DA FLORESTA — RPG DE PARADIGMAS")
        while True:
            self.output(f"\n{self.jogador.nome} | Nv. {self.jogador.nivel} | HP {self.jogador.vida}/{self.jogador.vida_maxima}")
            self.output("1 - Explorar\n2 - Inventário\n3 - Status\n4 - Habilidades\n5 - Salvar jogo\n6 - Carregar jogo\n7 - Sair")
            escolha = self._ler()
            if escolha == "1":
                self.explorar()
            elif escolha == "2":
                self.menu_inventario()
            elif escolha == "3":
                self.output(self.jogador.mostrar_status())
            elif escolha == "4":
                self.output("Habilidades: " + ", ".join(f"{h.nome} ({h.custo_mana} mana)" for h in self.jogador.habilidades.values()))
                self.output("Digite Cura para recuperar vida, ou Enter para voltar.")
                if self._ler("Habilidade: ").lower() == "cura":
                    self.campanha.acionar("habilidades")
                    self.campanha.acionar("habilidade:Cura")
                    self.output(self.campanha.mensagem)
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
            self.campanha.acionar("equipar:" + self._ler("Nome do equipamento: "))
            self.output(self.campanha.mensagem)
        elif escolha and escolha != "sair":
            self.campanha.acionar("usar:" + escolha)
            self.output(self.campanha.mensagem)

    def explorar(self):
        self._titulo("FLORESTA SOMBRIA")
        self.output("1 - Seguir pela estrada\n2 - Entrar na floresta\n3 - Procurar itens\n4 - Voltar")
        escolha = self._ler()
        if escolha in ("4", "sair"):
            return
        if escolha not in ("1", "2", "3"):
            self.output("Escolha inválida; você permanece em segurança.")
            return
        self.campanha.estado = "exploracao"
        # O chefe e os eventos seguem exatamente as mesmas regras da interface.
        if escolha == "3" and not (self.progresso["encontros"] >= 3 and not self.progresso["chefe_derrotado"]):
            self.campanha._evento("tesouro")
        else:
            self.campanha._explorar_rota("estrada" if escolha != "2" else "floresta")
        self._apresentar_evento()

    def _resolver_evento(self, evento):
        """Fachada preservada para exemplos e testes da versão anterior."""
        self.campanha._evento(evento)
        self._apresentar_evento()

    def _apresentar_evento(self):
        if self.campanha.estado == "combate":
            resultado = self._combater(self.campanha.inimigo)
            self.campanha.encerrar_batalha(resultado)
            self.output(self.campanha.mensagem)
        elif self.campanha.estado == "npc":
            self.output(self.campanha.mensagem)
            self.output("1 - Aceitar poção | 2 - Seguir")
            self.campanha.acionar("aceitar_pocao" if self._ler() == "1" else "recusar_npc")
            self.output(self.campanha.mensagem)
        else:
            self.output(self.campanha.mensagem)

    def _combater(self, inimigo):
        batalha = Batalha(self.jogador, inimigo, self.rng)
        self.campanha.batalha = batalha
        nivel_anterior = self.jogador.nivel
        resultado = batalha.lutar(self.input, self.output)
        if self.jogador.nivel > nivel_anterior:
            self.output(f"Você chegou ao nível {self.jogador.nivel}!")
        return resultado

    def salvar(self):
        self.campanha._salvar()
        self.output(self.campanha.mensagem)

    def carregar(self):
        self.campanha._carregar()
        self.output(self.campanha.mensagem)
