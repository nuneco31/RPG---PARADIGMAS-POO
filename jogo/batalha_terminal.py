from jogo.batalha import Batalha as RegrasBatalha


class Batalha(RegrasBatalha):
    """Adaptador de terminal; as regras compartilhadas estão em jogo.batalha."""

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
                output_fn("Habilidades: " + ", ".join(
                    f"{h.nome} ({h.custo_mana} mana)" for h in self.jogador.habilidades.values()))
                padrao = self.jogador.habilidade_padrao
                try:
                    habilidade = input_fn(f"Habilidade (Enter para {padrao}): ").strip() or padrao
                except (EOFError, KeyboardInterrupt):
                    habilidade = padrao
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
