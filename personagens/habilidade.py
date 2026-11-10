from dataclasses import dataclass


@dataclass(frozen=True)
class Habilidade:
    nome: str
    custo_mana: int
    poder: int
    tipo: str = "dano"
    fator_ataque: float = 1.0
    chance_critico: float = 0.0

    def calcular_poder(self, ataque):
        """Uma definição concentra o cálculo usado por todas as interfaces."""
        base = int(ataque * self.fator_ataque)
        return base + self.poder

    def aplicar(self, usuario, alvo=None, multiplicador=1):
        """Contrato: retorna o efeito real; None recusa a ação sem gastar mana."""
        if alvo is None:
            return None
        return alvo.receber_dano(self.calcular_poder(usuario.ataque) * multiplicador)


@dataclass(frozen=True)
class HabilidadeCura(Habilidade):
    tipo: str = "cura"

    def calcular_poder(self, ataque):
        return self.poder

    def aplicar(self, usuario, alvo=None, multiplicador=1):
        return usuario.curar(self.calcular_poder(usuario.ataque))


HABILIDADES = {
    "Golpe Poderoso": Habilidade("Golpe Poderoso", 8, 18),
    "Ataque Rápido": Habilidade("Ataque Rápido", 5, 8, fator_ataque=0.5, chance_critico=0.35),
    "Cura": HabilidadeCura("Cura", 7, 30),
}
