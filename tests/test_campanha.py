import json
import tempfile
import unittest
from pathlib import Path

from jogo.montagem import criar_campanha
from personagens.inimigo import Chefe, Goblin


class SorteioPrevisivel:
    def random(self):
        return 0.99

    def choice(self, opcoes):
        return opcoes[0]


class TestTransicoesDaCampanha(unittest.TestCase):
    def setUp(self):
        self.temporario = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporario.cleanup)
        self.campanha = criar_campanha(
            rng=SorteioPrevisivel(),
            caminho_save=Path(self.temporario.name) / "partida.json",
        )

    def test_combater_impede_explorar_ou_abandonar_turnos_pelo_menu(self):
        self.campanha._iniciar_batalha(Goblin())
        batalha = self.campanha.batalha
        for acao in ("explorar", "estrada", "floresta", "procurar", "voltar_menu"):
            with self.subTest(acao=acao):
                self.campanha.acionar(acao)
                self.assertEqual(self.campanha.estado, "combate")
                self.assertIs(self.campanha.batalha, batalha)

        self.campanha.acionar("abrir_habilidades_combate")
        self.assertEqual(self.campanha.estado, "selecionar_habilidade")
        self.campanha.acionar("voltar_menu")
        self.assertEqual(self.campanha.estado, "selecionar_habilidade")
        self.campanha.acionar("voltar_combate")
        self.assertEqual(self.campanha.estado, "combate")

    def test_vitoria_concede_xp_e_conta_encontro_uma_unica_vez(self):
        self.campanha._iniciar_batalha(Goblin(vida=1, xp_recompensa=30))
        self.campanha.acionar("combate:1")
        self.assertEqual(self.campanha.estado, "fim_batalha")
        self.assertEqual(self.campanha.jogador.xp, 30)
        self.campanha.acionar("combate:1")
        self.assertEqual(self.campanha.jogador.xp, 30)
        self.campanha.acionar("voltar_menu")
        self.assertEqual(self.campanha.estado, "fim_batalha")
        self.campanha.acionar("continuar")
        self.campanha.acionar("continuar")
        self.assertEqual(self.campanha.progresso["encontros"], 1)
        self.assertEqual(self.campanha.estado, "exploracao")

    def test_tres_encontros_desbloqueiam_chefe_e_vitoria_conclui_aventura(self):
        self.campanha.progresso["encontros"] = 3
        self.campanha.acionar("explorar")
        self.campanha.acionar("estrada")
        self.assertIsInstance(self.campanha.inimigo, Chefe)
        self.campanha.jogador.ataque = 1000
        self.campanha.acionar("combate:1")
        self.campanha.acionar("continuar")
        self.assertEqual(self.campanha.estado, "conclusao")
        self.assertTrue(self.campanha.progresso["chefe_derrotado"])
        self.campanha.acionar("continuar")
        self.assertEqual(self.campanha.progresso["encontros"], 3)

    def test_save_com_progresso_invalido_nao_aplica_jogador(self):
        self.campanha.acionar("salvar")
        caminho = self.campanha.gravador.caminho
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        dados["nome"] = "Não deve carregar"
        dados["progresso"] = {"encontros": -5, "chefe_derrotado": False}
        caminho.write_text(json.dumps(dados), encoding="utf-8")
        self.campanha.acionar("carregar")
        self.assertEqual(self.campanha.jogador.nome, "Arthur")
        self.assertEqual(self.campanha.progresso, {"encontros": 0, "chefe_derrotado": False})
        self.assertIn("Não foi possível", self.campanha.mensagem)

    def test_carregamento_valido_retorna_ao_menu_com_progresso_restaurado(self):
        self.campanha.progresso["encontros"] = 2
        self.campanha.jogador.vida = 65
        self.campanha.acionar("salvar")
        self.campanha.progresso["encontros"] = 0
        self.campanha.jogador.vida = 10
        self.campanha.acionar("habilidades")
        self.campanha.acionar("carregar")
        self.assertEqual(self.campanha.estado, "menu")
        self.assertEqual(self.campanha.estado_anterior, "menu")
        self.assertEqual(self.campanha.progresso["encontros"], 2)
        self.assertEqual(self.campanha.jogador.vida, 65)
        self.assertIsNone(self.campanha.batalha)


if __name__ == "__main__":
    unittest.main()
