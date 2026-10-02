import random
import tempfile
import unittest
from pathlib import Path

from jogo.batalha_terminal import Batalha
from jogo.salvamento import Salvamento
from jogo.terminal import JogoTerminal
from personagens.inimigo import Chefe, Goblin, Mago, Orc
from personagens.jogador import Jogador


class TestPersonagensEProgressao(unittest.TestCase):
    def test_ataque_dano_morte_e_limite_de_vida(self):
        jogador = Jogador("Lia")
        goblin = Goblin()
        jogador.atacar(goblin)
        self.assertEqual(goblin.vida, 27)
        goblin.receber_dano(1000)
        self.assertEqual(goblin.vida, 0)
        self.assertFalse(goblin.esta_vivo())
        jogador.vida = -50
        self.assertEqual(jogador.vida, 0)

    def test_xp_e_level_up(self):
        jogador = Jogador("Lia")
        ataque_inicial = jogador.ataque
        jogador.ganhar_xp(40)
        self.assertEqual(jogador.ataque, ataque_inicial)
        jogador.ganhar_xp(60)
        self.assertEqual(jogador.nivel, 2)
        self.assertEqual(jogador.ataque, ataque_inicial + 4)
        self.assertEqual(jogador.vida, jogador.vida_maxima)

    def test_inimigos_usam_acoes_especializadas(self):
        jogador = Jogador("Lia")
        mago = Mago()
        chefe = Chefe()
        self.assertGreater(mago.acao_turno(jogador), 0)
        chefe.acao_turno(jogador)
        chefe.acao_turno(jogador)
        chefe.acao_turno(jogador)
        self.assertEqual(chefe._ultima_acao, "Golpe do Rei Goblin")
        self.assertEqual(Orc().vida_maxima, 85)


class TestInventarioEHabilidades(unittest.TestCase):
    def test_pocao_equipamento_e_habilidade(self):
        jogador = Jogador("Lia")
        jogador.vida = 50
        jogador.inventario.adicionar("Poção de Vida")
        self.assertTrue(jogador.inventario.usar("Poção de Vida", jogador))
        self.assertEqual(jogador.vida, 85)
        jogador.inventario.adicionar("Espada de Ferro")
        self.assertTrue(jogador.inventario.equipar("Espada de Ferro", jogador))
        self.assertEqual(jogador.ataque, 25)
        alvo = Goblin()
        self.assertTrue(jogador.usar_habilidade_nome("Golpe Poderoso", alvo))
        self.assertLess(alvo.vida, alvo.vida_maxima)
        self.assertEqual(jogador.mana, 22)

    def test_habilidade_sem_mana_e_recusada(self):
        jogador = Jogador("Lia")
        jogador.mana = 0
        alvo = Goblin()
        vida_alvo = alvo.vida
        self.assertFalse(jogador.usar_habilidade_nome("Golpe Poderoso", alvo))
        self.assertEqual(alvo.vida, vida_alvo)


class TestCombateTerminal(unittest.TestCase):
    def test_entrada_invalida_nao_consume_turno_e_vitoria_da_xp(self):
        jogador = Jogador("Lia")
        goblin = Goblin(vida=10, defesa=0, xp_recompensa=30)
        batalha = Batalha(jogador, goblin, random.Random(4))
        vida_inicial = jogador.vida
        self.assertIn("inválida", batalha.executar_acao("x"))
        self.assertEqual(jogador.vida, vida_inicial)
        jogador.ataque = 100
        self.assertIn("derrotado", batalha.executar_acao("1"))
        self.assertEqual(jogador.xp, 30)
        self.assertTrue(batalha.encerrada)

    def test_derrota_e_defesa(self):
        jogador = Jogador("Lia")
        jogador.chance_esquiva = 0
        jogador.vida = 20
        orc = Orc(vida=100, ataque=30, defesa=0)
        batalha = Batalha(jogador, orc, random.Random(3))
        batalha.executar_acao("4")
        self.assertEqual(jogador.vida, 10)
        jogador.vida = 1
        batalha.executar_acao("1")
        self.assertTrue(batalha.encerrada)
        self.assertFalse(jogador.esta_vivo())

    def test_chefe_derrotado_recompensa_xp(self):
        jogador = Jogador("Lia")
        jogador.ataque = 1000
        batalha = Batalha(jogador, Chefe(vida=1), random.Random(1))
        batalha.executar_acao("1")
        self.assertEqual(jogador.xp, 25)
        self.assertEqual(jogador.nivel, 3)

    def test_fuga_encerra_sem_recompensa(self):
        jogador = Jogador("Lia")
        batalha = Batalha(jogador, Goblin(), random.Random(1))
        self.assertIn("escapou", batalha.executar_acao("5"))
        self.assertTrue(batalha.encerrada)
        self.assertEqual(jogador.xp, 0)


class TestSaveLoad(unittest.TestCase):
    def test_salva_carrega_estado_inventario_e_progresso(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "save.json"
            jogador = Jogador("Lia")
            jogador.ganhar_xp(120)
            jogador.inventario.adicionar("Poção de Vida", 2)
            jogador.inventario.adicionar("Escudo de Ferro")
            jogador.inventario.equipar("Escudo de Ferro", jogador)
            Salvamento(caminho).salvar(jogador, {"encontros": 2, "chefe_derrotado": False})

            carregado = Jogador("Outro")
            progresso = Salvamento(caminho).carregar(carregado)
            self.assertEqual(carregado.nome, "Lia")
            self.assertEqual(carregado.nivel, jogador.nivel)
            self.assertEqual(carregado.defesa, jogador.defesa)
            self.assertEqual(carregado.inventario.quantidade("Poção de Vida"), 2)
            self.assertEqual(carregado.inventario.equipamentos["escudo"], "Escudo de Ferro")
            self.assertEqual(progresso["encontros"], 2)


class TestExploracao(unittest.TestCase):
    def test_tesouro_armadilha_e_desbloqueio_do_chefe(self):
        respostas = iter(("1",))
        jogo = JogoTerminal(input_fn=lambda _prompt="": next(respostas), output_fn=lambda _texto: None)
        vida_inicial = jogo.jogador.vida
        jogo._resolver_evento("tesouro")
        self.assertTrue(jogo.jogador.inventario.itens)
        jogo._resolver_evento("armadilha")
        self.assertLess(jogo.jogador.vida, vida_inicial)
        jogo.jogador.vida = 1
        jogo._resolver_evento("armadilha")
        self.assertEqual(jogo.jogador.vida, 1)

        chefes = []

        def batalha_falsa(inimigo):
            chefes.append(inimigo)
            return "vitória"

        jogo._combater = batalha_falsa
        jogo.progresso["encontros"] = 3
        jogo.explorar()
        self.assertIsInstance(chefes[0], Chefe)
        self.assertTrue(jogo.progresso["chefe_derrotado"])

    def test_menu_invalido_nao_encerra_o_jogo(self):
        respostas = iter(("x", "7"))
        mensagens = []
        jogo = JogoTerminal(input_fn=lambda _prompt="": next(respostas), output_fn=mensagens.append)
        jogo.executar()
        self.assertTrue(any("Opção inválida" in mensagem for mensagem in mensagens))


if __name__ == "__main__":
    unittest.main()
