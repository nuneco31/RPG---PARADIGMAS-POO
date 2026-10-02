import argparse


# Ponto de entrada do jogo.
# O programa cria uma instância da classe Jogo e inicia o loop principal.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPG didático com modo terminal e janela opcional.")
    parser.add_argument("--pygame", action="store_true", help="abre a versão gráfica original")
    argumentos = parser.parse_args()

    if argumentos.pygame:
        from jogo.jogo import Jogo

        Jogo().executar()
    else:
        from jogo.terminal import JogoTerminal

        JogoTerminal().executar()
