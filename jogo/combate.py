class Combate:
    """Responsável por controlar o turno do jogador e a resposta do inimigo."""

    def __init__(self, jogo):
        # Guarda a referência ao jogo para acessar jogador, inimigos e mensagens.
        self.jogo = jogo

    def atacar_inimigo_selecionado(self):
        """Ataca apenas o alvo atual e aplica a contra-ataque do inimigo."""
        alvo = self.jogo.alvo_atual

        # Caso não exista alvo selecionado, informa ao jogador.
        if alvo is None:
            self.jogo.mensagem = "Selecione um goblin antes de atacar."
            return False

        # Se o alvo já foi derrotado, não permite atacar novamente.
        if not alvo.esta_vivo():
            self.jogo.mensagem = f"{alvo.nome} já foi derrotado!"
            return False

        # O jogador causa dano ao alvo selecionado.
        vida_antes = alvo.vida
        self.jogo.jogador.atacar(alvo)

        # Se o inimigo morrer, o jogador ganha XP e o combate termina para ele.
        if not alvo.esta_vivo():
            self.jogo.jogador.ganhar_xp(alvo.xp_recompensa)
            self.jogo.mensagem = (
                f"{alvo.nome.upper()} DERROTADO! "
                f"+{alvo.xp_recompensa} XP"
            )
            return True

        # Após o ataque do jogador, o alvo selecionado contra-ataca.
        vida_antes_jogador = self.jogo.jogador.vida
        alvo.atacar(self.jogo.jogador)

        dano_inimigo = vida_antes_jogador - self.jogo.jogador.vida

        self.jogo.mensagem = (
            f"{alvo.nome} causou {dano_inimigo} de dano! "
            f"Arthur: {self.jogo.jogador.vida} HP"
        )

        # Se o jogador morrer, exibe a mensagem final.
        if not self.jogo.jogador.esta_vivo():
            self.jogo.mensagem = "ARTHUR FOI DERROTADO!"

        return True

    def atacar_inimigo(self, inimigo, nome_inimigo):
        """Método legado para manter compatibilidade com chamadas anteriores."""
        self.jogo.alvo_atual = inimigo
        return self.atacar_inimigo_selecionado()

    def atacar_goblin1(self):
        """Seleciona e ataca o Goblin 1."""
        self.jogo.selecionar_inimigo(1)
        return self.atacar_inimigo_selecionado()

    def atacar_goblin2(self):
        """Seleciona e ataca o Goblin 2."""
        self.jogo.selecionar_inimigo(2)
        return self.atacar_inimigo_selecionado()
