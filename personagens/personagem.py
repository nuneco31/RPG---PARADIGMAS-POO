class Personagem:
    """Classe base para todos os personagens do RPG."""

    def __init__(self, nome, vida, ataque, defesa):
        # Dados básicos de qualquer personagem.
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa

    def mostrar_status(self):
        """Mostra os atributos do personagem no console."""
        print(f"\n--- {self.nome} ---")
        print(f"Vida: {self.vida}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")

    def atacar(self, alvo):
        """Aplica dano ao alvo, considerando a defesa dele."""
        dano = self.ataque - alvo.defesa

        if dano < 0:
            dano = 0

        alvo.vida -= dano

        print(f"{self.nome} atacou {alvo.nome}!")
        print(f"Dano causado: {dano}")

    def esta_vivo(self):
        """Retorna verdadeiro se a vida for maior que zero."""
        return self.vida > 0
