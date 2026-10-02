from personagens.habilidade import HABILIDADES


class Batalha:
    """Regras de combate independentes da leitura do terminal."""

    def __init__(self, jogador, inimigo, rng):
        self.jogador = jogador
        self.inimigo = inimigo
        self.rng = rng
        self._encerrada = False
        self._recompensou = False

    @property
    def encerrada(self):
        return self._encerrada

    def executar_acao(self, acao, habilidade=None, item=None):
        if self._encerrada:
            return "Esta batalha já terminou."

        if acao == "1":
            critico = self.rng.random() < 0.15
            dano_base = self.jogador.ataque * (2 if critico else 1)
            dano = self.inimigo.receber_dano(dano_base)
            mensagem = f"Ataque causou {dano} de dano" + (" crítico!" if critico else ".")
        elif acao == "2":
            habilidade = habilidade or "Golpe Poderoso"
            dados = HABILIDADES.get(habilidade)
            if dados is None or self.jogador.mana < dados.custo_mana:
                return "Habilidade inválida ou mana insuficiente; o inimigo não agiu."
            self.jogador.mana -= dados.custo_mana
            if dados.tipo == "cura":
                recuperada = self.jogador.curar(dados.poder)
                mensagem = f"{habilidade}: você recuperou {recuperada} HP."
            else:
                critico = habilidade == "Ataque Rápido" and self.rng.random() < 0.35
                poder = dados.poder + (self.jogador.ataque if habilidade == "Golpe Poderoso" else self.jogador.ataque // 2)
                dano = self.inimigo.receber_dano(poder * (2 if critico else 1))
                mensagem = f"{habilidade} causou {dano} de dano" + (" crítico!" if critico else ".")
        elif acao == "3":
            item = item or next((nome for nome in self.jogador.inventario.itens
                                 if nome in ("Poção de Vida", "Poção de Mana")), None)
            if item is None or not self.jogador.inventario.usar(item, self.jogador):
                return "Você não tem uma poção utilizável; o inimigo não agiu."
            mensagem = f"Você usou {item}."
        elif acao == "4":
            self.jogador.defender()
            mensagem = "Você se preparou para defender o próximo ataque."
        elif acao == "5":
            if self.rng.random() < 0.65:
                self._encerrada = True
                return "Você escapou da batalha."
            mensagem = "A fuga falhou!"
        else:
            return "Opção inválida. Escolha de 1 a 5; o turno não foi consumido."

        if not self.inimigo.esta_vivo():
            self._encerrada = True
            if not self._recompensou:
                self.jogador.ganhar_xp(self.inimigo.xp_recompensa)
                self._recompensou = True
            return f"{mensagem}\n{self.inimigo.nome} foi derrotado! +{self.inimigo.xp_recompensa} XP."

        if acao == "5" and self._encerrada:
            return mensagem

        if self.rng.random() < self.jogador.chance_esquiva:
            mensagem += f"\nVocê esquivou do ataque de {self.inimigo.nome}!"
            golpe = 0
        else:
            golpe = self.inimigo.acao_turno(self.jogador)
            acao_inimigo = self.inimigo.ultima_acao
            mensagem += f"\n{self.inimigo.nome} usou {acao_inimigo} e causou {golpe} de dano."
        if not self.jogador.esta_vivo():
            self._encerrada = True
            mensagem += " Você foi derrotado."
        return mensagem

    def lutar(self, input_fn=input, output_fn=print):
        output_fn(f"\n=== BATALHA: {self.inimigo.nome} ===")
        while not self._encerrada:
            output_fn(f"\nVocê: {self.jogador.vida}/{self.jogador.vida_maxima} HP | Mana: {self.jogador.mana}/{self.jogador.mana_maxima}")
            output_fn(f"{self.inimigo.nome}: {self.inimigo.vida}/{self.inimigo.vida_maxima} HP")
            output_fn("1 - Ataque | 2 - Habilidade | 3 - Poção | 4 - Defender | 5 - Fugir")
            try:
                escolha = input_fn("Escolha: ").strip()
            except (EOFError, KeyboardInterrupt):
                self._encerrada = True
                return "fuga"
            if escolha == "2":
                output_fn("Habilidades: " + ", ".join(HABILIDADES))
                try:
                    habilidade = input_fn("Habilidade (Enter para Golpe Poderoso): ").strip() or "Golpe Poderoso"
                except (EOFError, KeyboardInterrupt):
                    habilidade = "Golpe Poderoso"
                mensagem = self.executar_acao(escolha, habilidade=habilidade)
            elif escolha == "3":
                pocoes = [nome for nome in self.jogador.inventario.itens
                           if nome in ("Poção de Vida", "Poção de Mana")]
                output_fn("Poções: " + (", ".join(pocoes) or "nenhuma"))
                try:
                    item = input_fn("Poção (Enter para escolher automaticamente): ").strip() or None
                except (EOFError, KeyboardInterrupt):
                    item = None
                mensagem = self.executar_acao(escolha, item=item)
            else:
                mensagem = self.executar_acao(escolha)
            output_fn(mensagem)
        return "vitória" if not self.inimigo.esta_vivo() else "derrota" if not self.jogador.esta_vivo() else "fuga"
