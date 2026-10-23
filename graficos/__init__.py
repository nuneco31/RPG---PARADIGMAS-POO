"""Apresentação gráfica. Importar o pacote não inicializa o Pygame."""
__all__ = ["Renderizador"]


def __getattr__(nome):
    if nome == "Renderizador":
        from .renderizador import Renderizador
        return Renderizador
    raise AttributeError(f"module {__name__!r} has no attribute {nome!r}")
