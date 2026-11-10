"""Entrada da aventura. A escolha da interface não altera as regras do jogo."""

import argparse
import random
from pathlib import Path
from personagens.jogador import Jogador
from personagens.vocacao import CLASSES_JOGAVEIS


def main(argv=None):
    parser = argparse.ArgumentParser(description="Crônicas da Floresta — RPG didático de POO.")
    modos = parser.add_mutually_exclusive_group()
    modos.add_argument("--terminal", action="store_true", help="joga no console (padrão), sem Pygame")
    modos.add_argument("--grafico", action="store_true", help="abre a interface opcional Pygame")
    parser.add_argument("--classe", choices=CLASSES_JOGAVEIS, help="escolhe a classe sem o menu inicial")
    parser.add_argument("--nome", default="Arthur", help="nome usado junto com --classe")
    parser.add_argument("--seed", type=int, help="fixa a aleatoriedade para demonstrações")
    parser.add_argument(
        "--save", type=Path, default=Path(__file__).resolve().with_name("save.json"),
        help="caminho do salvamento (padrão: save.json ao lado de main.py)",
    )
    argumentos = parser.parse_args(argv)
    if not argumentos.nome.strip():
        parser.error("--nome não pode ser vazio.")
    rng = random.Random(argumentos.seed)
    jogador = Jogador(argumentos.nome, argumentos.classe or "guerreiro")
    if not argumentos.grafico:
        from jogo.terminal import JogoTerminal

        JogoTerminal(rng=rng, caminho_save=argumentos.save, jogador=jogador,
                     escolher_personagem=argumentos.classe is None).executar()
        return 0

    try:
        from jogo.interface import JogoInterface

        jogo = JogoInterface(rng=rng, caminho_save=argumentos.save, jogador=jogador)
    except ModuleNotFoundError as erro:
        if erro.name != "pygame":
            raise
        parser.exit(1, "Modo gráfico requer pygame-ce. Execute: python -m pip install -r requirements.txt\n"
                       "Você também pode jogar com: python main.py --terminal\n")
    jogo.executar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
