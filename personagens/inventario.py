from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    nome: str
    tipo: str = "item"
    valor: int = 0


ITENS = {
    "Poção de Vida": Item("Poção de Vida", "cura", 35),
    "Poção de Mana": Item("Poção de Mana", "mana", 15),
    "Espada de Ferro": Item("Espada de Ferro", "arma", 5),
    "Escudo de Ferro": Item("Escudo de Ferro", "escudo", 5),
}


class Inventario:
    """Componente do jogador: mantém itens em quantidade e equipamento ativo."""

    def __init__(self):
        self._itens = {}
        self._equipamentos = {}

    @property
    def itens(self):
        return dict(self._itens)

    @property
    def equipamentos(self):
        return dict(self._equipamentos)

    def _item_dados(self, nome):
        return ITENS[nome]

    def adicionar(self, nome, quantidade=1):
        if nome not in ITENS or quantidade < 1:
            return False
        self._itens[nome] = self._itens.get(nome, 0) + quantidade
        return True

    def quantidade(self, nome):
        return self._itens.get(nome, 0)

    def remover(self, nome, quantidade=1):
        if quantidade < 1 or self.quantidade(nome) < quantidade:
            return False
        restante = self._itens[nome] - quantidade
        if restante:
            self._itens[nome] = restante
        else:
            del self._itens[nome]
        return True

    def usar(self, nome, jogador):
        item = ITENS.get(nome)
        if item is None or item.tipo not in ("cura", "mana") or not self.remover(nome):
            return False
        if item.tipo == "cura":
            jogador.curar(item.valor)
        else:
            jogador.mana = min(jogador.mana_maxima, jogador.mana + item.valor)
        return True

    def equipar(self, nome, jogador):
        item = ITENS.get(nome)
        if item is None or item.tipo not in ("arma", "escudo") or not self.remover(nome):
            return False
        anterior = self._equipamentos.get(item.tipo)
        if anterior:
            self.adicionar(anterior)
            jogador.ataque -= ITENS[anterior].valor if item.tipo == "arma" else 0
            jogador.defesa -= ITENS[anterior].valor if item.tipo == "escudo" else 0
        self._equipamentos[item.tipo] = nome
        if item.tipo == "arma":
            jogador.ataque += item.valor
        else:
            jogador.defesa += item.valor
        return True

    def salvar(self):
        return {"itens": dict(self._itens), "equipamentos": dict(self._equipamentos)}

    def carregar(self, dados):
        itens = dados.get("itens", {})
        self._itens = {nome: int(qtd) for nome, qtd in itens.items()
                       if nome in ITENS and ITENS[nome].tipo in ("cura", "mana") and int(qtd) > 0}
        self._equipamentos = {}
        for tipo, nome in dados.get("equipamentos", {}).items():
            if tipo in ("arma", "escudo") and nome in ITENS and ITENS[nome].tipo == tipo:
                self._equipamentos[tipo] = nome
