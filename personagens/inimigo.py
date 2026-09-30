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

    def provocar(self):
        """Mensagem de provocação do inimigo."""
        print(f"{self.nome}: Você não vai conseguir me derrotar!")
