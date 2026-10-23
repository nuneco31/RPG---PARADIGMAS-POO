"""Persistência JSON compatível com saves anteriores e aplicação transacional."""
import json
import os
from pathlib import Path
import tempfile

from personagens.jogador import Jogador


CAMINHO_PADRAO = Path(__file__).resolve().parents[1] / "save.json"


class Salvamento:
    """Só substitui o arquivo e o estado quando todos os dados são válidos."""

    def __init__(self, caminho=None):
        self.caminho = Path(caminho) if caminho is not None else CAMINHO_PADRAO

    @staticmethod
    def validar_progresso(progresso):
        if not isinstance(progresso, dict):
            raise ValueError("Progresso inválido.")
        encontros = progresso.get("encontros", 0)
        chefe = progresso.get("chefe_derrotado", False)
        if isinstance(encontros, bool) or not isinstance(encontros, int) or encontros < 0:
            raise ValueError("Quantidade de encontros inválida.")
        if not isinstance(chefe, bool):
            raise ValueError("Estado do chefe inválido.")
        return {"encontros": encontros, "chefe_derrotado": chefe}

    def salvar(self, jogador, progresso):
        dados = {
            "versao": 1,
            "nome": jogador.nome,
            "nivel": jogador.nivel,
            "xp": jogador.xp,
            "xp_necessaria": jogador.xp_necessaria,
            "vida": jogador.vida,
            "vida_maxima": jogador.vida_maxima,
            "ataque": jogador.ataque,
            "defesa": jogador.defesa,
            "mana": jogador.mana,
            "mana_maxima": jogador.mana_maxima,
            "inventario": jogador.inventario.salvar(),
            "progresso": self.validar_progresso(progresso),
        }
        # O temporário fica no mesmo diretório para permitir substituição atômica.
        caminho_temporario = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.caminho.parent,
                                             prefix=self.caminho.name + ".", suffix=".tmp",
                                             delete=False) as arquivo:
                caminho_temporario = Path(arquivo.name)
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
                arquivo.flush()
                os.fsync(arquivo.fileno())
            caminho_temporario.replace(self.caminho)
        finally:
            if caminho_temporario is not None:
                caminho_temporario.unlink(missing_ok=True)

    def carregar(self, jogador):
        dados = json.loads(self.caminho.read_text(encoding="utf-8-sig"))
        if not isinstance(dados, dict) or "nivel" not in dados:
            raise ValueError("Arquivo de salvamento inválido.")
        versao = dados.get("versao", 1)
        if isinstance(versao, bool) or not isinstance(versao, int) or versao != 1:
            raise ValueError("Versão de salvamento incompatível.")
        progresso = self.validar_progresso(dados.get("progresso", {}))
        candidato = Jogador(jogador.nome)
        candidato.restaurar_estado(dados)
        jogador.__dict__.update(candidato.__dict__)
        return progresso
