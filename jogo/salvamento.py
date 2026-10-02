import json
from pathlib import Path


class Salvamento:
    """Leitura e gravação de uma partida simples em JSON."""

    def __init__(self, caminho="save.json"):
        self.caminho = Path(caminho)

    def salvar(self, jogador, progresso):
        dados = {
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
            "progresso": progresso,
        }
        self.caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

    def carregar(self, jogador):
        dados = json.loads(self.caminho.read_text(encoding="utf-8"))
        if not isinstance(dados, dict) or "nivel" not in dados:
            raise ValueError("Arquivo de salvamento inválido.")
        jogador.restaurar_estado(dados)
        return dados.get("progresso", {})
