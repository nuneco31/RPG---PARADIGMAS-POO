from personagens.personagem import Personagem
from personagens.habilidade import HABILIDADES
from personagens.inventario import Inventario


class Jogador(Personagem):
    """Representa o protagonista do jogo."""

    def __init__(self, nome):
        # Chama o construtor da classe base com os atributos iniciais.
        super().__init__(
            nome=nome,
            vida=100,
            ataque=20,
            defesa=5,
        )

        # Sistema de nível e progresso do personagem.
        self.nivel = 1
        self.xp = 0
        self.xp_necessaria = 100
        self.mana = 30
        self.mana_maxima = 30
        self.inventario = Inventario()
        self.habilidades = HABILIDADES
        self._defendendo = False
        self.chance_esquiva = 0.08

    def mostrar_status(self):
        """Mostra o status do jogador no console."""
        print("\n==============================")
        print(f"        {self.nome}")
        print("==============================")

        print(f"Nível: {self.nivel}")
        print(f"Vida: {self.vida}/{self.vida_maxima}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"XP: {self.xp}/{self.xp_necessaria}")

    def ganhar_xp(self, quantidade):
        """Acrescenta experiência e aumenta os atributos conforme as regras do jogo."""
        if quantidade < 0:
            raise ValueError("A quantidade de XP não pode ser negativa.")
        self.xp += quantidade
        print(f"\n{self.nome} ganhou {quantidade} XP!")
        self.verificar_level_up()

    def verificar_level_up(self):
        """Aumenta o nível e reforça os atributos quando a XP supera o limite."""
        while self.xp >= self.xp_necessaria:
            xp_usada = self.xp_necessaria
            self.xp -= xp_usada
            self.nivel += 1

            # Cada nível aumenta os atributos de forma previsível.
            self._vida_maxima += 20
            self.vida = self.vida_maxima
            self.ataque += 4
            self.defesa += 2
            self.mana_maxima += 5
            self.mana = self.mana_maxima
            self.xp_necessaria = int(self.xp_necessaria * 1.25)

            print("\n==============================")
            print("          LEVEL UP!")
            print("==============================")
            print(f"{self.nome} chegou ao nível {self.nivel}!")
            print(f"Vida máxima: {self.vida_maxima} | Ataque: {self.ataque} | Defesa: {self.defesa}")
            print(f"\nPróximo nível: {self.xp_necessaria} XP")

    def usar_habilidade(self, alvo):
        """Habilidade especial do jogador, com dano ampliado."""
        habilidade = HABILIDADES["Golpe Poderoso"]
        if self.mana < habilidade.custo_mana:
            return False
        self.mana -= habilidade.custo_mana
        dano = max(1, self.ataque + habilidade.poder - alvo.defesa)
        alvo.vida -= dano
        print(f"\n{self.nome} usou {habilidade.nome}! Dano causado: {dano}")
        return True

    def acao_turno(self, alvo):
        return self.atacar(alvo)

    def receber_dano(self, quantidade):
        if self._defendendo:
            quantidade = max(1, int(quantidade) // 2)
            self._defendendo = False
        return super().receber_dano(quantidade)

    def defender(self):
        """Reduz pela metade o próximo golpe recebido."""
        self._defendendo = True

    def usar_habilidade_nome(self, nome, alvo=None):
        habilidade = HABILIDADES.get(nome)
        if habilidade is None or self.mana < habilidade.custo_mana:
            return False
        if habilidade.tipo == "cura":
            alvo = self
            self.mana -= habilidade.custo_mana
            self.curar(habilidade.poder)
        else:
            if alvo is None:
                return False
            self.mana -= habilidade.custo_mana
            alvo.receber_dano(self.ataque + habilidade.poder)
        return True

    def restaurar_estado(self, dados):
        self._nome = str(dados.get("nome", self.nome))
        self.nivel = max(1, int(dados.get("nivel", 1)))
        self.xp = max(0, int(dados.get("xp", 0)))
        self.xp_necessaria = max(1, int(dados.get("xp_necessaria", 100)))
        self._vida_maxima = max(1, int(dados.get("vida_maxima", 100 + 20 * (self.nivel - 1))))
        self.vida = int(dados.get("vida", self.vida_maxima))
        self.ataque = int(dados.get("ataque", 20 + 4 * (self.nivel - 1)))
        self.defesa = int(dados.get("defesa", 5 + 2 * (self.nivel - 1)))
        self.mana_maxima = max(0, int(dados.get("mana_maxima", 30 + 5 * (self.nivel - 1))))
        self.mana = max(0, min(self.mana_maxima, int(dados.get("mana", self.mana_maxima))))
        self.inventario.carregar(dados.get("inventario", {}))
