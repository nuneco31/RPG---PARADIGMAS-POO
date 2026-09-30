class Combate:

    def __init__(self, jogo):
        self.jogo = jogo

    def atacar_inimigo(self, inimigo, nome_inimigo):

        if not inimigo.esta_vivo():
            self.jogo.mensagem = f"{nome_inimigo} já foi derrotado!"
            return False

        vida_antes = inimigo.vida

        self.jogo.jogador.atacar(inimigo)

        if not inimigo.esta_vivo():
            self.jogo.jogador.ganhar_xp(inimigo.xp_recompensa)
            self.jogo.mensagem = (
                f"{nome_inimigo.upper()} DERROTADO! "
                f"+{inimigo.xp_recompensa} XP"
            )
            return True

        dano = vida_antes - inimigo.vida

        vida_antes_jogador = self.jogo.jogador.vida
        inimigo.atacar(self.jogo.jogador)

        dano_inimigo = vida_antes_jogador - self.jogo.jogador.vida

        self.jogo.mensagem = (
            f"{nome_inimigo} causou {dano_inimigo} de dano! "
            f"Arthur: {self.jogo.jogador.vida} HP"
        )

        if not self.jogo.jogador.esta_vivo():
            self.jogo.mensagem = "ARTHUR FOI DERROTADO!"

        return True

    def atacar_goblin1(self):
        return self.atacar_inimigo(self.jogo.inimigo, "Goblin 1")

    def atacar_goblin2(self):
        return self.atacar_inimigo(self.jogo.inimigo2, "Goblin 2")
