import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from jogo.interface import JogoInterface
from personagens.inimigo import Chefe, Goblin


class RNGDeterministico:
    def random(self):
        return 0.99

    def choice(self, opcoes):
        if opcoes[0] == "inimigo":
            return "inimigo"
        if opcoes[0] is Goblin:
            return Goblin
        return opcoes[0]


class TestInterfaceGrafica(unittest.TestCase):
    def setUp(self):
        self.jogo = JogoInterface(rng=RNGDeterministico(), caminho_save="save-teste.json")

    def tearDown(self):
        self.jogo.pygame.quit()

    def test_clique_abre_exploracao_e_telas_sao_desenhadas(self):
        pygame = self.jogo.pygame
        self.jogo.renderizador.desenhar()
        botao_explorar = next(rect for rect, acao in self.jogo.botoes if acao == "explorar")
        pygame.event.post(pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=botao_explorar.center
        ))
        self.jogo.eventos.processar()
        self.assertEqual(self.jogo.estado, "exploracao")

        self.jogo.renderizador.desenhar()
        self.jogo.acionar("procurar")
        self.assertEqual(self.jogo.estado, "evento")
        self.jogo.renderizador.desenhar()
        self.jogo.acionar("inventario")
        self.jogo.renderizador.desenhar()
        self.jogo.acionar("status")
        self.jogo.renderizador.desenhar()

    def test_combate_e_chefe_sao_acessiveis_pela_interface(self):
        self.jogo._evento("inimigo")
        self.assertEqual(self.jogo.estado, "combate")
        self.assertIsInstance(self.jogo.inimigo, Goblin)
        self.jogo.acionar("abrir_habilidades_combate")
        self.assertEqual(self.jogo.estado, "selecionar_habilidade")
        self.jogo.acionar("habilidade:Golpe Poderoso")
        self.assertLess(self.jogo.inimigo.vida, self.jogo.inimigo.vida_maxima)
        self.assertEqual(self.jogo.estado, "combate")
        self.jogo.jogador.ataque = 1000
        self.jogo._acao_combate("1")
        self.assertEqual(self.jogo.estado, "fim_batalha")
        self.jogo._continuar_apos_batalha()
        self.assertEqual(self.jogo.progresso["encontros"], 1)

        self.jogo.progresso["encontros"] = 3
        self.jogo.acionar("estrada")
        self.assertIsInstance(self.jogo.inimigo, Chefe)
        self.jogo.renderizador.desenhar()

    def test_fila_de_cliques_nao_reutiliza_botoes_da_tela_anterior(self):
        pygame = self.jogo.pygame
        self.jogo._evento("npc")
        self.jogo.renderizador.desenhar()
        retangulo = next(rect for rect, acao in self.jogo.botoes if acao == "aceitar_pocao")
        quantidade = self.jogo.jogador.inventario.quantidade("Poção de Vida")
        pygame.event.clear()
        for _ in range(2):
            pygame.event.post(pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, button=1, pos=retangulo.center
            ))
        self.jogo.eventos.processar()
        self.assertEqual(self.jogo.jogador.inventario.quantidade("Poção de Vida"), quantidade + 1)

    def test_fechar_janela_e_processado_apos_um_clique(self):
        pygame = self.jogo.pygame
        self.jogo.renderizador.desenhar()
        retangulo = next(rect for rect, acao in self.jogo.botoes if acao == "explorar")
        pygame.event.clear()
        pygame.event.post(pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=1, pos=retangulo.center
        ))
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.jogo.eventos.processar()
        self.assertFalse(self.jogo.rodando)

    def test_escape_retorna_a_origem_e_preserva_batalha(self):
        pygame = self.jogo.pygame
        self.jogo.acionar("explorar")
        self.jogo.acionar("caderno")
        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        self.jogo.eventos.processar()
        self.assertEqual(self.jogo.estado, "exploracao")
        self.jogo._evento("inimigo")
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        self.jogo.eventos.processar()
        self.assertEqual(self.jogo.estado, "combate")

    def test_pocao_de_mana_permanece_acessivel_sem_pocao_de_vida(self):
        self.jogo.jogador.inventario.remover("Poção de Vida", 2)
        self.jogo.jogador.mana = 0
        self.jogo._evento("inimigo")
        self.jogo.renderizador.desenhar()
        self.assertTrue(any(acao == "combate:3" for _, acao in self.jogo.botoes))
        self.jogo.acionar("combate:3")
        self.assertEqual(self.jogo.jogador.mana, 15)
        self.assertEqual(self.jogo.jogador.inventario.quantidade("Poção de Mana"), 0)


if __name__ == "__main__":
    unittest.main()
