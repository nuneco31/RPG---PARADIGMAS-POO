"""Contratos, extensão de habilidades e persistência das classes jogáveis."""
import json
import random
import tempfile
import unittest
from pathlib import Path

from jogo.batalha import Batalha
from jogo.campanha import Campanha
from jogo.salvamento import Salvamento
from jogo.terminal import JogoTerminal
from personagens.habilidade import Habilidade
from personagens.inimigo import Goblin, Orc, Mago, Chefe
from personagens.jogador import Jogador
from personagens.vocacao import CLASSES_JOGAVEIS


class TestClassesEHabilidades(unittest.TestCase):
    def test_classes_tem_atributos_e_habilidades_proprios(self):
        jogadores = [Jogador("Lia", classe) for classe in CLASSES_JOGAVEIS]
        self.assertEqual(len({j.vida_maxima for j in jogadores}), 3)
        for jogador, habilidade in zip(jogadores, ("Golpe Poderoso", "Bola de Fogo", "Flecha Precisa")):
            with self.subTest(classe=jogador.classe):
                self.assertEqual(jogador.habilidade_padrao, habilidade)
                mana = jogador.mana
                alvo = Goblin(vida=200)
                dano = jogador.aplicar_habilidade(habilidade, alvo)
                self.assertGreater(dano, 0)
                self.assertEqual(jogador.mana, mana - jogador.habilidades[habilidade].custo_mana)

    def test_habilidade_de_outra_classe_nao_gasta_mana_nem_turno(self):
        jogador = Jogador("Lia", "mago")
        alvo = Goblin()
        batalha = Batalha(jogador, alvo, random.Random(7))
        antes = jogador.vida, jogador.mana, alvo.vida
        mensagem = batalha.executar_acao("2", habilidade="Golpe Poderoso")
        self.assertIn("inválida", mensagem)
        self.assertEqual((jogador.vida, jogador.mana, alvo.vida), antes)

    def test_habilidade_nova_e_aceita_sem_alterar_motor(self):
        class Dreno(Habilidade):
            def aplicar(self, usuario, alvo=None, multiplicador=1):
                if alvo is None:
                    return None
                dano = alvo.receber_dano(self.poder)
                usuario.curar(dano)
                return dano

        jogador = Jogador("Lia", "mago")
        jogador.vida = 20
        jogador.habilidades["Dreno"] = Dreno("Dreno", 4, 12)
        alvo = Goblin(vida=10, defesa=0, xp_recompensa=0)
        batalha = Batalha(jogador, alvo, random.Random(7))
        self.assertIn("Dreno", batalha.executar_acao("2", habilidade="Dreno"))
        self.assertEqual(jogador.vida, 30)
        self.assertEqual(jogador.mana, 56)
        self.assertEqual(batalha.resultado, "vitoria")

    def test_habilidade_sem_alvo_e_recusada_sem_gastar_mana(self):
        jogador = Jogador("Lia", "arqueiro")
        self.assertIsNone(jogador.aplicar_habilidade("Flecha Precisa"))
        self.assertEqual(jogador.mana, jogador.mana_maxima)

    def test_cura_da_classe_respeita_vida_maxima_e_custo(self):
        for classe in CLASSES_JOGAVEIS:
            with self.subTest(classe=classe):
                jogador = Jogador("Lia", classe)
                jogador.vida -= 5
                self.assertEqual(jogador.aplicar_habilidade("Cura"), 5)
                self.assertEqual(jogador.vida, jogador.vida_maxima)
                self.assertEqual(jogador.mana, jogador.mana_maxima - 7)

    def test_inimigos_substituem_contrato_de_personagem(self):
        for tipo in (Goblin, Orc, Mago, Chefe):
            with self.subTest(tipo=tipo.__name__):
                alvo = Jogador("Lia", "guerreiro")
                inimigo = tipo()
                for _ in range(3):
                    antes = alvo.vida
                    dano = inimigo.acao_turno(alvo)
                    self.assertEqual(dano, antes - alvo.vida)
                    self.assertGreaterEqual(dano, 0)
                    self.assertGreaterEqual(alvo.vida, 0)

    def test_menu_cria_classe_e_rejeita_escolha_invalida(self):
        respostas = iter(("x", "2", "Lia", "3", "7"))
        mensagens = []
        jogo = JogoTerminal(input_fn=lambda _: next(respostas), output_fn=mensagens.append,
                            escolher_personagem=True)
        jogo.executar()
        self.assertEqual(jogo.jogador.classe, "mago")
        self.assertEqual(jogo.jogador.nome, "Lia")
        self.assertIn("Bola de Fogo", jogo.jogador.habilidades)
        self.assertTrue(any("Classe inválida" in texto for texto in mensagens))
        self.assertEqual(jogo.jogador.inventario.quantidade("Poção de Vida"), 2)


class TestPersistenciaDasClasses(unittest.TestCase):
    def test_roundtrip_preserva_classe_progressao_e_equipamento(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = Salvamento(Path(pasta) / "partida.json")
            for classe in CLASSES_JOGAVEIS:
                with self.subTest(classe=classe):
                    original = Jogador("Lia", classe)
                    original.ganhar_xp(120)
                    original.inventario.adicionar("Espada de Ferro")
                    original.inventario.equipar("Espada de Ferro", original)
                    original.vida -= 12
                    original.mana -= 3
                    repo.salvar(original, {"encontros": 2, "chefe_derrotado": False})
                    carregado = Jogador("Outro", "guerreiro")
                    for _ in range(2):
                        repo.carregar(carregado)
                        for atributo in ("nome", "classe", "vida", "vida_maxima", "mana", "mana_maxima",
                                         "ataque", "defesa", "nivel", "xp", "chance_esquiva", "habilidades"):
                            self.assertEqual(getattr(original, atributo), getattr(carregado, atributo))

    def test_save_antigo_sem_classe_preserva_aventureiro(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "antigo.json"
            caminho.write_text(json.dumps({"versao": 1, "nome": "Arthur", "nivel": 1}), encoding="utf-8")
            jogador = Jogador("Lia", "mago")
            Salvamento(caminho).carregar(jogador)
            self.assertEqual(jogador.classe, "aventureiro")
            self.assertEqual(jogador.vida_maxima, 100)
            self.assertEqual(len(jogador.habilidades), 3)

    def test_classe_invalida_ou_ausente_nao_modifica_partida(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "invalido.json"
            jogador = Jogador("Lia", "mago")
            for classe in ("inexistente", [], None):
                dados = {"versao": 2, "nome": "Outro", "nivel": 1}
                if classe is not None:
                    dados["classe"] = classe
                caminho.write_text(json.dumps(dados), encoding="utf-8")
                with self.assertRaises(ValueError):
                    Salvamento(caminho).carregar(jogador)
                self.assertEqual(jogador.nome, "Lia")
                self.assertEqual(jogador.classe, "mago")


class TestPortasDePersistencia(unittest.TestCase):
    def test_leitor_e_gravador_independentes_sem_arquivo(self):
        class SomenteLeitor:
            def carregar(self, jogador):
                jogador.restaurar_estado({"nome": "Salvo", "classe": "arqueiro"})
                return {"encontros": 2, "chefe_derrotado": False}

        class SomenteGravador:
            def __init__(self):
                self.registro = None

            def salvar(self, jogador, progresso):
                self.registro = (jogador.nome, dict(progresso))

        gravador = SomenteGravador()
        campanha = Campanha(leitor=SomenteLeitor(), gravador=gravador)
        campanha.acionar("carregar")
        self.assertEqual(campanha.jogador.classe, "arqueiro")
        campanha.acionar("salvar")
        self.assertEqual(gravador.registro, ("Salvo", {"encontros": 2, "chefe_derrotado": False}))

    def test_falha_de_gravacao_e_apresentada_sem_encerrar_jogo(self):
        class GravadorIndisponivel:
            def salvar(self, jogador, progresso):
                raise OSError("Sem espaço")

        class LeitorIndisponivel:
            def carregar(self, jogador):
                raise ValueError("Dados inválidos")

        campanha = Campanha(leitor=LeitorIndisponivel(), gravador=GravadorIndisponivel())
        for acao in ("salvar", "carregar"):
            campanha.acionar(acao)
            self.assertIn("Não foi possível", campanha.mensagem)
            self.assertTrue(campanha.rodando)
            self.assertEqual(campanha.jogador.nome, "Arthur")
