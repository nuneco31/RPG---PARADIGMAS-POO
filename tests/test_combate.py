import unittest

from jogo.combate import Combate
from jogo.jogo import Jogo


class JogadorFake:
    def __init__(self):
        self.vida = 100
        self.ataque = 20
        self.defesa = 5
        self.xp = 0
        self.xp_necessaria = 100
        self.nivel = 1

    def atacar(self, alvo):
        alvo.vida -= max(self.ataque - alvo.defesa, 0)

    def ganhar_xp(self, quantidade):
        self.xp += quantidade

    def esta_vivo(self):
        return self.vida > 0


class InimigoFake:
    def __init__(self, nome, vida=50, ataque=15, defesa=3, xp_recompensa=25):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.xp_recompensa = xp_recompensa

    def atacar(self, alvo):
        alvo.vida -= max(self.ataque - alvo.defesa, 0)

    def esta_vivo(self):
        return self.vida > 0


class TestCombate(unittest.TestCase):
    def setUp(self):
        self.jogo = type('JogoFake', (), {})()
        self.jogo.jogador = JogadorFake()
        self.jogo.inimigo = InimigoFake('Goblin 1')
        self.jogo.inimigo2 = InimigoFake('Goblin 2')
        self.jogo.alvo_atual = self.jogo.inimigo
        self.jogo.mensagem = ''

        def selecionar_inimigo(numero):
            if numero == 1:
                self.jogo.alvo_atual = self.jogo.inimigo
            elif numero == 2:
                self.jogo.alvo_atual = self.jogo.inimigo2

        self.jogo.selecionar_inimigo = selecionar_inimigo
        self.combate = Combate(self.jogo)

    def test_selecionar_inimigo_no_jogo(self):
        self.jogo.selecionar_inimigo(2)
        self.assertIs(self.jogo.alvo_atual, self.jogo.inimigo2)

    def test_atacar_inimigo_selecionado_retorna_ataque_do_inimigo(self):
        vida_inicial = self.jogo.jogador.vida
        self.jogo.selecionar_inimigo(1)
        self.combate.atacar_inimigo_selecionado()

        self.assertLess(self.jogo.inimigo.vida, 50)
        self.assertLess(self.jogo.jogador.vida, vida_inicial)


class TestRespawn(unittest.TestCase):
    def test_gerar_novo_goblin_substitui_o_derrotado(self):
        jogo = object.__new__(Jogo)
        jogo.jogador = type('JogadorFake', (), {'nivel': 1})()
        jogo.inimigo = InimigoFake('Goblin 1', vida=0)
        jogo.inimigo2 = InimigoFake('Goblin 2', vida=50)
        jogo.alvo_atual = jogo.inimigo
        jogo.proximo_numero_goblin = 3

        jogo.gerar_novo_goblin(jogo.inimigo)

        self.assertTrue(jogo.inimigo.esta_vivo())
        self.assertEqual(jogo.inimigo.nome, 'Goblin 3')

    def test_percentuais_de_progressao_do_jogador_e_inimigo(self):
        jogador = type('JogadorFake', (), {'nivel': 1, 'ataque': 20, 'vida': 100})()
        jogador.vida = 100
        jogador.ataque = 20

        novo_ataque = jogador.ataque * 1.25
        nova_vida = jogador.vida * 1.23
        vida_goblin = 50 * 1.15
        ataque_goblin = 15 * 1.10

        self.assertAlmostEqual(novo_ataque, 25.0)
        self.assertAlmostEqual(nova_vida, 123.0)
        self.assertAlmostEqual(vida_goblin, 57.5)
        self.assertAlmostEqual(ataque_goblin, 16.5)


if __name__ == '__main__':
    unittest.main()
