__all__ = ["Jogo"]


def __getattr__(nome):
    """Carrega a interface gráfica apenas quando alguém solicita Jogo."""
    if nome == "Jogo":
        from .jogo import Jogo

        return Jogo
    raise AttributeError(f"módulo {__name__!r} não possui o atributo {nome!r}")
