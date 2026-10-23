from abc import ABC, abstractmethod


class Personagem(ABC):
    """Contrato comum de personagens; mantém seus atributos em faixas válidas."""

    def __init__(self, nome, vida, ataque, defesa):
        # Dados básicos de qualquer personagem.
        if not nome.strip() or vida <= 0:
            raise ValueError("Personagem precisa de nome e vida positiva.")
        self._nome = nome.strip()
        self._vida_maxima = vida
        self._vida = vida
        self._ataque = max(0, ataque)
        self._defesa = max(0, defesa)

    @property
    def nome(self):
        return self._nome

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        self._vida = max(0, min(self._vida_maxima, int(valor)))

    @property
    def vida_maxima(self):
        return self._vida_maxima

    @property
    def ataque(self):
        return self._ataque

    @ataque.setter
    def ataque(self, valor):
        self._ataque = max(0, int(valor))

    @property
    def defesa(self):
        return self._defesa

    @defesa.setter
    def defesa(self, valor):
        self._defesa = max(0, int(valor))

    def receber_dano(self, quantidade):
        vida_anterior = self.vida
        dano = max(0, int(quantidade) - self.defesa)
        self.vida -= dano
        return vida_anterior - self.vida

    def curar(self, quantidade):
        vida_anterior = self.vida
        self.vida += max(0, int(quantidade))
        return self.vida - vida_anterior

    def mostrar_status(self):
        """Retorna texto para que cada interface escolha como apresentá-lo."""
        return (f"{self.nome}\nVida: {self.vida}/{self.vida_maxima}\n"
                f"Ataque: {self.ataque}\nDefesa: {self.defesa}")

    def atacar(self, alvo):
        """Aplica dano ao alvo, considerando a defesa dele."""
        return alvo.receber_dano(self.ataque)

    def esta_vivo(self):
        """Retorna verdadeiro se a vida for maior que zero."""
        return self.vida > 0

    @abstractmethod
    def acao_turno(self, alvo):
        """Executa a ação padrão desse tipo de personagem."""
