from personagens.personagem import Personagem
from personagens.habilidade import HABILIDADES
from personagens.inventario import Inventario


class Jogador(Personagem):
    """Protagonista: possui inventário e concentra progressão e habilidades."""

    def __init__(self, nome):
        super().__init__(nome=nome, vida=100, ataque=20, defesa=5)
        self.nivel = 1
        self.xp = 0
        self.xp_necessaria = 100
        self.mana_maxima = 30
        self.mana = 30
        self.inventario = Inventario()
        self.habilidades = dict(HABILIDADES)
        self._defendendo = False
        self.chance_esquiva = 0.08

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, valor):
        self._mana = max(0, min(self.mana_maxima, int(valor)))

    def mostrar_status(self):
        return (f"{super().mostrar_status()}\nNível: {self.nivel}\n"
                f"XP: {self.xp}/{self.xp_necessaria}\n"
                f"Mana: {self.mana}/{self.mana_maxima}")

    def ganhar_xp(self, quantidade):
        """Retorna quantos níveis foram conquistados, sem imprimir na interface."""
        if quantidade < 0:
            raise ValueError("A quantidade de XP não pode ser negativa.")
        self.xp += quantidade
        return self.verificar_level_up()

    def verificar_level_up(self):
        nivel_anterior = self.nivel
        while self.xp >= self.xp_necessaria:
            self.xp -= self.xp_necessaria
            self.nivel += 1
            self._vida_maxima += 20
            self.vida = self.vida_maxima
            self.ataque += 4
            self.defesa += 2
            self.mana_maxima += 5
            self.mana = self.mana_maxima
            self.xp_necessaria = int(self.xp_necessaria * 1.25)
        return self.nivel - nivel_anterior

    def aplicar_habilidade(self, nome, alvo=None, multiplicador=1):
        """Retorna efeito real; None significa ação recusada sem gastar mana."""
        habilidade = self.habilidades.get(nome)
        if habilidade is None or self.mana < habilidade.custo_mana:
            return None
        if habilidade.tipo != "cura" and alvo is None:
            return None
        self.mana -= habilidade.custo_mana
        poder = habilidade.calcular_poder(self.ataque)
        if habilidade.tipo == "cura":
            return self.curar(poder)
        return alvo.receber_dano(poder * multiplicador)

    def usar_habilidade(self, alvo):
        return self.usar_habilidade_nome("Golpe Poderoso", alvo)

    def usar_habilidade_nome(self, nome, alvo=None):
        return self.aplicar_habilidade(nome, alvo) is not None

    def acao_turno(self, alvo):
        return self.atacar(alvo)

    def receber_dano(self, quantidade):
        if self._defendendo:
            quantidade = max(1, int(quantidade) // 2)
            self._defendendo = False
        return super().receber_dano(quantidade)

    def defender(self):
        """Reduz o próximo golpe recebido, inclusive em um turno posterior."""
        self._defendendo = True

    def encerrar_combate(self):
        self._defendendo = False

    def restaurar_estado(self, dados):
        """Valida uma cópia inteira antes de modificar o jogador atual."""
        if not isinstance(dados, dict):
            raise ValueError("Dados do jogador devem ser um objeto.")
        nome = dados.get("nome", self.nome)
        if not isinstance(nome, str):
            raise ValueError("Nome do jogador inválido.")
        candidato = Jogador(nome)

        def inteiro(chave, padrao, minimo=0):
            valor = dados.get(chave, padrao)
            if isinstance(valor, bool) or not isinstance(valor, int) or valor < minimo:
                raise ValueError(f"Atributo inválido: {chave}.")
            return valor

        candidato.nivel = inteiro("nivel", 1, 1)
        candidato.xp = inteiro("xp", 0)
        candidato.xp_necessaria = inteiro("xp_necessaria", 100, 1)
        if candidato.xp >= candidato.xp_necessaria:
            raise ValueError("XP incompatível com o próximo nível.")
        nivel = candidato.nivel - 1
        candidato._vida_maxima = inteiro("vida_maxima", 100 + 20 * nivel, 1)
        vida = inteiro("vida", candidato.vida_maxima)
        candidato.ataque = inteiro("ataque", 20 + 4 * nivel)
        candidato.defesa = inteiro("defesa", 5 + 2 * nivel)
        candidato.mana_maxima = inteiro("mana_maxima", 30 + 5 * nivel)
        mana = inteiro("mana", candidato.mana_maxima)
        if vida > candidato.vida_maxima or mana > candidato.mana_maxima:
            raise ValueError("Vida ou mana acima do máximo.")
        candidato.vida = vida
        candidato.mana = mana
        candidato.inventario.carregar(dados.get("inventario", {}))
        self.__dict__.update(candidato.__dict__)
