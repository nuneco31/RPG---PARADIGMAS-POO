from personagens.personagem import Personagem


class Jogador(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=100,
            ataque=20,
            defesa=5,
        )

        self.nivel = 1
        self.xp = 0
        self.xp_necessaria = 100

    def mostrar_status(self):
        print("\n==============================")
        print(f"        {self.nome}")
        print("==============================")

        print(f"Nível: {self.nivel}")
        print(f"Vida: {self.vida}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"XP: {self.xp}/{self.xp_necessaria}")

    def ganhar_xp(self, quantidade):
        self.xp += quantidade

        print(f"\n{self.nome} ganhou {quantidade} XP!")

        self.verificar_level_up()

    def verificar_level_up(self):
        while self.xp >= self.xp_necessaria:
            xp_usada = self.xp_necessaria
            self.xp -= xp_usada
            self.nivel += 1
            self.vida += 20
            self.ataque += 5
            self.xp_necessaria = int(self.xp_necessaria * 1.25)

            print("\n==============================")
            print("          LEVEL UP!")
            print("==============================")
            print(f"{self.nome} chegou ao nível {self.nivel}!")
            print("\nNovos atributos:")
            print("+20 Vida")
            print("+5 Ataque")
            print(f"\nPróximo nível: {self.xp_necessaria} XP")

    def usar_habilidade(self, alvo):
        dano = self.ataque * 2
        alvo.vida -= dano
        print(f"\n{self.nome} usou uma habilidade especial!")
        print(f"Dano causado: {dano}")
