import argparse


# Ponto de entrada do jogo.
# O programa cria uma instância da classe Jogo e inicia o loop principal.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPG didático com modos Pygame e terminal.")
    parser.add_argument("--terminal", action="store_true", help="abre a aventura de terminal")
    argumentos = parser.parse_args()

    if argumentos.terminal:
        from jogo.terminal import JogoTerminal

        JogoTerminal().executar()
    else:
        from jogo.jogo import Jogo

        Jogo().executar()
