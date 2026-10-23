"""Entrada da aventura. A escolha da interface não altera as regras do jogo."""

import argparse
import random
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Crônicas da Floresta — RPG didático de POO.")
    parser.add_argument("--terminal", action="store_true", help="joga no console, sem Pygame")
    parser.add_argument("--seed", type=int, help="fixa a aleatoriedade para demonstrações")
    parser.add_argument(
        "--save", type=Path, default=Path(__file__).resolve().with_name("save.json"),
        help="caminho do salvamento (padrão: save.json ao lado de main.py)",
    )
    argumentos = parser.parse_args(argv)
    rng = random.Random(argumentos.seed)
    if argumentos.terminal:
        from jogo.terminal import JogoTerminal

        JogoTerminal(rng=rng, caminho_save=argumentos.save).executar()
        return 0

    try:
        from jogo.interface import JogoInterface

        jogo = JogoInterface(rng=rng, caminho_save=argumentos.save)
    except ModuleNotFoundError as erro:
        if erro.name != "pygame":
            raise
        parser.exit(1, "Modo gráfico requer pygame-ce. Execute: python -m pip install -r requirements.txt\n"
                       "Você também pode jogar com: python main.py --terminal\n")
    jogo.executar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
