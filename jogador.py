from personagem import Personagem


class Jogador(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=100,
            ataque=20,
            defesa=5
        )

        self.nivel = 1
        self.xp = 0
        self.xp_proximo_nivel = 100

    def mostrar_status(self):
        print(f"\n--- {self.nome} ---")
        print(f"Nivel: {self.nivel}")
        print(f"Vida: {self.vida}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"XP: {self.xp}/{self.xp_proximo_nivel}")

    def ganhar_xp(self, quantidade):

        self.xp += quantidade

        print(f"\n{self.nome} ganhou {quantidade} XP!")

        self.verificar_level_up()

    def verificar_level_up(self):

        while self.xp >= self.xp_proximo_nivel:

            self.xp -= self.xp_proximo_nivel

            self.nivel += 1

            self.vida += 20
            self.ataque += 5
            self.defesa += 2

            self.xp_proximo_nivel += 50

            print("\n==============================")
            print("         LEVEL UP!")
            print("==============================")

            print(f"{self.nome} chegou ao nivel {self.nivel}!")

            print("\nNovos atributos:")
            print("+20 Vida")
            print("+5 Ataque")
            print("+2 Defesa")

    def usar_habilidade(self, alvo):

        dano = self.ataque * 2

        alvo.vida -= dano

        print(f"\n{self.nome} usou uma habilidade especial!")
        print(f"Dano causado: {dano}")