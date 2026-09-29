
from personagem import Personagem

class Inimigo(Personagem):

    def __init__(
        self,
        nome,
        vida,
        ataque,
        defesa,
        xp_recompensa
    ):

        super().__init__(
            nome=nome,
            vida=vida,
            ataque=ataque,
            defesa=defesa
        )

        self.xp_recompensa = xp_recompensa

    def provocar(self):

        print(
            f"{self.nome}: "
            "Você não vai conseguir me derrotar!"
        )

