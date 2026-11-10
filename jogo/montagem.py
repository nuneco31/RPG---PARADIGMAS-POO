"""Ponto de composição: escolhe os adaptadores concretos fora das regras."""
from jogo.campanha import Campanha
from jogo.salvamento import Salvamento


def criar_campanha(rng=None, caminho_save=None, jogador=None):
    repositorio = Salvamento(caminho_save)
    return Campanha(rng=rng, jogador=jogador, leitor=repositorio, gravador=repositorio)
