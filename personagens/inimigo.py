from personagens.personagem import Personagem


class Inimigo(Personagem):
    """Representa qualquer inimigo do jogo."""

    def __init__(self, nome, vida, ataque, defesa, xp_recompensa):
        # Chama o construtor da classe base com os atributos principais.
        super().__init__(
            nome=nome,
            vida=vida,
            ataque=ataque,
            defesa=defesa,
        )

        # XP concedida ao jogador ao derrotar esse inimigo.
        self.xp_recompensa = xp_recompensa

    def escalar(self, fator_vida=1.0, ataque_extra=0, xp_extra=0):
        """Ajusta a dificuldade sem expor a implementação interna da vida."""
        self._vida_maxima = max(1, int(self._vida_maxima * fator_vida))
        self.vida = self.vida_maxima
        self.ataque += ataque_extra
        self.xp_recompensa += xp_extra

    def provocar(self):
        """Mensagem de provocação do inimigo."""
        return f"{self.nome}: Você não vai conseguir me derrotar!"

    def acao_turno(self, alvo):
        """Comportamento padrão: ataque direto, substituível por subclasses."""
        return self.atacar(alvo)
    @property
    def ultima_acao(self):
        return getattr(self, "_ultima_acao", "ataque")


class Goblin(Inimigo):
    def __init__(self, nome="Goblin", vida=45, ataque=12, defesa=2, xp_recompensa=30):
        super().__init__(nome, vida, ataque, defesa, xp_recompensa)


class Orc(Inimigo):
    def __init__(self, nome="Orc", vida=85, ataque=19, defesa=5, xp_recompensa=55):
        super().__init__(nome, vida, ataque, defesa, xp_recompensa)


class Mago(Inimigo):
    def __init__(self, nome="Mago Sombrio", vida=55, ataque=21, defesa=2, xp_recompensa=60):
        super().__init__(nome, vida, ataque, defesa, xp_recompensa)

    def acao_turno(self, alvo):
        """O ataque mágico atravessa parte da defesa do alvo."""
        self._ultima_acao = "Rajada Arcana"
        return alvo.receber_dano(self.ataque + alvo.defesa // 2)


class Chefe(Inimigo):
    """Chefe com golpe especial periódico e grande recompensa."""

    def __init__(self, nome="Rei Goblin", vida=250, ataque=30, defesa=15, xp_recompensa=250):
        super().__init__(nome, vida, ataque, defesa, xp_recompensa)
        self._turnos = 0
        self._ultima_acao = "ataque"

    def acao_turno(self, alvo):
        self._turnos += 1
        if self._turnos % 3 == 0:
            self._ultima_acao = "Golpe do Rei Goblin"
            return alvo.receber_dano(self.ataque + 12)
        self._ultima_acao = "ataque"
        return self.atacar(alvo)
