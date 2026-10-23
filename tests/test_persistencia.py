import json
import os
import tempfile
import unittest
from pathlib import Path

from jogo.salvamento import Salvamento
from personagens.jogador import Jogador


class TestPersistenciaSegura(unittest.TestCase):
    def test_arquivo_invalido_nao_modifica_o_jogador(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "partida.json"
            jogador = Jogador("Lia")
            jogador.vida = 47
            jogador.inventario.adicionar("Espada de Ferro", 2)
            salvamento = Salvamento(caminho)
            salvamento.salvar(jogador, {"encontros": 2, "chefe_derrotado": False})
            original = json.loads(caminho.read_text(encoding="utf-8"))
            invalido = dict(original, nome="Nome indevido", xp="não é um número")
            caminho.write_text(json.dumps(invalido), encoding="utf-8")

            with self.assertRaises((ValueError, TypeError)):
                salvamento.carregar(jogador)

            salvamento.salvar(jogador, {"encontros": 2, "chefe_derrotado": False})
            self.assertEqual(json.loads(caminho.read_text(encoding="utf-8")), original)

    def test_armas_na_mochila_e_equipamento_sobrevivem_ao_carregamento(self):
        with tempfile.TemporaryDirectory() as pasta:
            jogador = Jogador("Lia")
            jogador.inventario.adicionar("Espada de Ferro", 3)
            jogador.inventario.adicionar("Escudo de Ferro", 2)
            jogador.inventario.equipar("Espada de Ferro", jogador)
            jogador.inventario.equipar("Escudo de Ferro", jogador)
            salvamento = Salvamento(Path(pasta) / "partida.json")
            progresso = {"encontros": 2, "chefe_derrotado": False}
            salvamento.salvar(jogador, progresso)

            carregado = Jogador("Outro")
            self.assertEqual(salvamento.carregar(carregado), progresso)
            self.assertEqual(carregado.inventario.quantidade("Espada de Ferro"), 2)
            self.assertEqual(carregado.inventario.quantidade("Escudo de Ferro"), 1)
            self.assertEqual(carregado.inventario.equipamentos, jogador.inventario.equipamentos)
            self.assertEqual(carregado.ataque, jogador.ataque)
            self.assertEqual(carregado.defesa, jogador.defesa)

            # Recarregar a mesma partida não pode somar o bônus novamente.
            salvamento.carregar(carregado)
            self.assertEqual(carregado.ataque, jogador.ataque)
            self.assertEqual(carregado.defesa, jogador.defesa)

    def test_caminho_padrao_independe_da_pasta_de_execucao(self):
        antes = Path(Salvamento().caminho)
        pasta_original = Path.cwd()
        with tempfile.TemporaryDirectory() as pasta:
            try:
                os.chdir(pasta)
                depois = Path(Salvamento().caminho)
            finally:
                os.chdir(pasta_original)
        self.assertTrue(antes.is_absolute())
        self.assertEqual(antes, depois)


if __name__ == "__main__":
    unittest.main()
