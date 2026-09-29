
from personagem import Personagem


class Jogador(Personagem):

    def __init__(self, nome):

        super().__init__(
            nome=nome,
            vida=100,
            ataque=20,
            defesa=5
        )

        # ==============================
        # SISTEMA DE NÍVEL
        # ==============================

        self.nivel = 1

        # XP atual
        self.xp = 0

        # XP necessária para o próximo nível
        self.xp_necessaria = 100

    # ==============================
    # MOSTRAR STATUS
    # ==============================

    def mostrar_status(self):

        print("\n==============================")
        print(f"        {self.nome}")
        print("==============================")

        print(f"Nível: {self.nivel}")
        print(f"Vida: {self.vida}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"XP: {self.xp}/{self.xp_necessaria}")

    # ==============================
    # GANHAR XP
    # ==============================

    def ganhar_xp(self, quantidade):

        self.xp += quantidade

        print(
            f"\n{self.nome} ganhou "
            f"{quantidade} XP!"
        )

        self.verificar_level_up()

    # ==============================
    # VERIFICAR LEVEL UP
    # ==============================

    def verificar_level_up(self):

        while self.xp >= self.xp_necessaria:

            # Guarda a XP necessária
            xp_usada = self.xp_necessaria

            # Retira a XP utilizada
            self.xp -= xp_usada

            # Aumenta o nível
            self.nivel += 1

            # ==============================
            # AUMENTA OS ATRIBUTOS
            # ==============================

            self.vida += 20

            self.ataque += 5

            # ==============================
            # AUMENTA A XP NECESSÁRIA
            # ==============================

            self.xp_necessaria = int(
                self.xp_necessaria * 1.25
            )

            # ==============================
            # MENSAGEM
            # ==============================

            print("\n==============================")
            print("          LEVEL UP!")
            print("==============================")

            print(
                f"{self.nome} chegou ao "
                f"nível {self.nivel}!"
            )

            print("\nNovos atributos:")

            print("+20 Vida")
            print("+5 Ataque")

            print(
                f"\nPróximo nível: "
                f"{self.xp_necessaria} XP"
            )

    # ==============================
    # HABILIDADE ESPECIAL
    # ==============================

    def usar_habilidade(self, alvo):

        dano = self.ataque * 2

        alvo.vida -= dano

        print(
            f"\n{self.nome} usou "
            f"uma habilidade especial!"
        )

        print(
            f"Dano causado: {dano}"
        )
