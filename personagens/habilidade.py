from dataclasses import dataclass


@dataclass(frozen=True)
class Habilidade:
    nome: str
    custo_mana: int
    poder: int
    tipo: str = "dano"


HABILIDADES = {
    "Golpe Poderoso": Habilidade("Golpe Poderoso", 8, 18),
    "Ataque Rápido": Habilidade("Ataque Rápido", 5, 8),
    "Cura": Habilidade("Cura", 7, 30, "cura"),
}
