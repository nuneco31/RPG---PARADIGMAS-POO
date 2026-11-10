"""Tipos de jogador por composição: dados imutáveis e habilidades polimórficas."""
from dataclasses import dataclass
from personagens.habilidade import Habilidade, HabilidadeCura, HABILIDADES


@dataclass(frozen=True)
class Vocacao:
    nome: str
    vida: int
    ataque: int
    defesa: int
    mana: int
    esquiva: float
    habilidades: tuple[Habilidade, ...]


VOCACOES = {
    # Perfil reservado para carregar partidas e exemplos do protótipo.
    "aventureiro": Vocacao("Aventureiro", 100, 20, 5, 30, 0.08, tuple(HABILIDADES.values())),
    "guerreiro": Vocacao("Guerreiro", 120, 22, 8, 25, 0.05,
                         (HABILIDADES["Golpe Poderoso"], HABILIDADES["Cura"])),
    "mago": Vocacao("Mago", 80, 16, 3, 60, 0.08,
                    (Habilidade("Bola de Fogo", 10, 30), HabilidadeCura("Cura", 7, 40))),
    "arqueiro": Vocacao("Arqueiro", 95, 24, 4, 35, 0.20,
                        (Habilidade("Flecha Precisa", 7, 12, chance_critico=0.35),
                         HABILIDADES["Ataque Rápido"], HABILIDADES["Cura"])),
}

CLASSES_JOGAVEIS = ("guerreiro", "mago", "arqueiro")
