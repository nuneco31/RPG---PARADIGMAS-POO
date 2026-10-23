from dataclasses import dataclass


@dataclass(frozen=True)
class Habilidade:
    nome: str
    custo_mana: int
    poder: int
    tipo: str = "dano"

    def calcular_poder(self, ataque):
        """Uma definição concentra o cálculo usado por todas as interfaces."""
        if self.tipo == "cura":
            return self.poder
        base = ataque // 2 if self.nome == "Ataque Rápido" else ataque
        return base + self.poder


HABILIDADES = {
    "Golpe Poderoso": Habilidade("Golpe Poderoso", 8, 18),
    "Ataque Rápido": Habilidade("Ataque Rápido", 5, 8),
    "Cura": Habilidade("Cura", 7, 30, "cura"),
}
