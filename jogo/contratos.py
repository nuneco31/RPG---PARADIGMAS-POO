"""Portas pequenas definidas pelo núcleo, implementadas por adaptadores externos."""
from typing import Protocol
from personagens.jogador import Jogador


class LeitorPartida(Protocol):
    def carregar(self, jogador: Jogador) -> dict:
        """Valida tudo antes de restaurar o jogador e devolver o progresso."""
        ...


class GravadorPartida(Protocol):
    def salvar(self, jogador: Jogador, progresso: dict) -> None:
        """Grava uma fotografia da partida ou lança erro sem corromper a anterior."""
        ...
