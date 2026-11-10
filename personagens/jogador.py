from personagens.personagem import Personagem
from personagens.vocacao import VOCACOES
from personagens.inventario import Inventario


class Jogador(Personagem):
    """Protagonista: possui inventário e concentra progressão e habilidades."""

    def __init__(self, nome, classe="aventureiro"):
        if not isinstance(classe, str) or classe not in VOCACOES:
            raise ValueError("Classe de personagem inválida.")
        self._classe = classe
        self.vocacao = VOCACOES[classe]
        super().__init__(nome=nome, vida=self.vocacao.vida,
                         ataque=self.vocacao.ataque, defesa=self.vocacao.defesa)
        self.nivel = 1
        self.xp = 0
        self.xp_necessaria = 100
        self.mana_maxima = self.vocacao.mana
        self.mana = self.mana_maxima
        self.inventario = Inventario()
        self.habilidades = {h.nome: h for h in self.vocacao.habilidades}
        self._defendendo = False
        self.chance_esquiva = self.vocacao.esquiva

    @property
    def classe(self):
        return self._classe

    @property
    def habilidade_padrao(self):
        return next(iter(self.habilidades))

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, valor):
        self._mana = max(0, min(self.mana_maxima, int(valor)))

    def mostrar_status(self):
        return (f"{super().mostrar_status()}\nClasse: {self.vocacao.nome}\nNível: {self.nivel}\n"
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
        efeito = habilidade.aplicar(self, alvo, multiplicador)
        if efeito is not None:
            self.mana -= habilidade.custo_mana
        return efeito

    def usar_habilidade(self, alvo):
        return self.usar_habilidade_nome(self.habilidade_padrao, alvo)

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
        candidato = Jogador(nome, dados.get("classe", "aventureiro"))

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
        candidato._vida_maxima = inteiro("vida_maxima", candidato.vocacao.vida + 20 * nivel, 1)
        vida = inteiro("vida", candidato.vida_maxima)
        candidato.ataque = inteiro("ataque", candidato.vocacao.ataque + 4 * nivel)
        candidato.defesa = inteiro("defesa", candidato.vocacao.defesa + 2 * nivel)
        candidato.mana_maxima = inteiro("mana_maxima", candidato.vocacao.mana + 5 * nivel)
        mana = inteiro("mana", candidato.mana_maxima)
        if vida > candidato.vida_maxima or mana > candidato.mana_maxima:
            raise ValueError("Vida ou mana acima do máximo.")
        candidato.vida = vida
        candidato.mana = mana
        candidato.inventario.carregar(dados.get("inventario", {}))
        self.__dict__.update(candidato.__dict__)
