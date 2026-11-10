"""Executa o CLI e renderiza sua saída real para a documentação (requer pygame-ce)."""
import os
from pathlib import Path
import subprocess
import sys

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "docs" / "imagens"


def executar(argumentos, entradas):
    resultado = subprocess.run(
        [sys.executable, "-X", "utf8", str(RAIZ / "main.py"), *argumentos],
        input=entradas, capture_output=True, text=True, encoding="utf-8",
        cwd=RAIZ, timeout=15, check=True,
    )
    return resultado.stdout


def imagem(nome, titulo, texto):
    # Registros de stdout renderizados, não capturas de uma janela do sistema.
    pygame.font.init()
    fonte = pygame.font.SysFont("consolas,dejavusansmono,monospace", 19)
    linhas = texto.strip().splitlines()
    largura = max(900, *(fonte.size(linha)[0] + 56 for linha in [titulo, *linhas]))
    tela = pygame.Surface((largura, 85 + len(linhas) * 27))
    tela.fill((17, 24, 32))
    pygame.draw.rect(tela, (33, 46, 59), (0, 0, largura, 48))
    tela.blit(fonte.render(titulo, True, (145, 218, 174)), (28, 13))
    for numero, linha in enumerate(linhas):
        tela.blit(fonte.render(linha, True, (230, 237, 243)), (28, 67 + numero * 27))
    pygame.image.save(tela, str(DESTINO / nome))
    pygame.font.quit()


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    inicio = executar([], "2\nLia\n3\n7\n")
    batalha = executar(["--classe", "mago", "--nome", "Lia", "--seed", "7"],
                       "1\n2\n2\n\n1\n7\n")
    (DESTINO / "console-inicio.txt").write_text(inicio, encoding="utf-8")
    (DESTINO / "console-combate.txt").write_text(batalha, encoding="utf-8")
    imagem("console-inicio.png", "python main.py | escolha de personagem",
           inicio.split("Lia | Nv.")[0])
    trecho = batalha[batalha.index("=== BATALHA:"):].split("\nLia | Nv.")[0]
    imagem("console-combate.png", "python main.py --classe mago --nome Lia --seed 7", trecho)
    print("Registros de execução atualizados em docs/imagens.")


if __name__ == "__main__":
    main()
