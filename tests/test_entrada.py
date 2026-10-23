"""A entrada funciona sem abrir uma janela nem instalar a dependência gráfica."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]


class TestEntrada(unittest.TestCase):
    def test_terminal_inicia_de_outra_pasta_sem_pygame(self):
        with tempfile.TemporaryDirectory() as pasta:
            resultado = subprocess.run(
                [sys.executable, str(RAIZ / "main.py"), "--terminal", "--seed", "7"],
                cwd=pasta, input="7\n", capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=15,
                env={chave: valor for chave, valor in os.environ.items() if chave != "PYTHONPATH"},
            )
        # O subprocesso não herda a dependência gráfica local usada pelos testes.
        self.assertEqual(resultado.returncode, 0, resultado.stderr)

    def test_ajuda_documenta_as_opcoes(self):
        resultado = subprocess.run(
            [sys.executable, str(RAIZ / "main.py"), "--help"],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(resultado.returncode, 0)
        for opcao in ("--terminal", "--seed", "--save"):
            self.assertIn(opcao, resultado.stdout)
