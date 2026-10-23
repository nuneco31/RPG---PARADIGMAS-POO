"""Componentes de desenho, sem regras de combate ou inventário."""

from collections import OrderedDict

from graficos.tema import Tema as T


class Componentes:
    def __init__(self, jogo):
        self.jogo = jogo
        self.pg = jogo.pygame
        self.fontes = {
            "titulo": self.pg.font.Font(None, 40),
            "grande": self.pg.font.Font(None, 32),
            "normal": self.pg.font.Font(None, 25),
            "pequena": self.pg.font.Font(None, 21),
            "micro": self.pg.font.Font(None, 18),
        }
        self._textos = OrderedDict()

    def texto(self, texto, x, y, estilo="normal", cor=T.TEXTO):
        chave = (str(texto), estilo, cor)
        imagem = self._textos.get(chave)
        if imagem is None:
            imagem = self.fontes[estilo].render(str(texto), True, cor)
            self._textos[chave] = imagem
            if len(self._textos) > 320:
                self._textos.popitem(last=False)
        else:
            self._textos.move_to_end(chave)
        self.jogo.tela.blit(imagem, (x, y))
        return imagem.get_width()

    def paragrafo(self, texto, x, y, largura, estilo="pequena", cor=T.SUAVE, limite=4):
        fonte = self.fontes[estilo]
        linhas = []
        for bloco in str(texto).splitlines() or [""]:
            linha = ""
            for palavra in bloco.split():
                tentativa = f"{linha} {palavra}".strip()
                if linha and fonte.size(tentativa)[0] > largura:
                    linhas.append(linha)
                    linha = palavra
                else:
                    linha = tentativa
            linhas.append(linha)
        if len(linhas) > limite:
            linhas = linhas[:limite]
            while linhas[-1] and fonte.size(linhas[-1] + "…")[0] > largura:
                linhas[-1] = linhas[-1][:-1]
            linhas[-1] += "…"
        for linha in linhas:
            self.texto(linha, x, y, estilo, cor)
            y += fonte.get_linesize() + 2
        return y

    def painel(self, x, y, w, h, cor=T.PAINEL, borda=T.BORDA, raio=12):
        rect = self.pg.Rect(x, y, w, h)
        self.pg.draw.rect(self.jogo.tela, cor, rect, border_radius=raio)
        if borda:
            self.pg.draw.rect(self.jogo.tela, borda, rect, 1, border_radius=raio)
        return rect

    def barra(self, x, y, largura, atual, maximo, cor, altura=7):
        self.painel(x, y, largura, altura, (39, 58, 60), None, 3)
        proporcao = min(1, max(0, atual) / max(1, maximo))
        if proporcao:
            self.painel(x, y, max(1, int(largura * proporcao)), altura, cor, None, 3)

    def botao(self, rotulo, acao, x, y, w, h=48, detalhe=None, primario=False, ativo=True):
        rect = self.pg.Rect(x, y, w, h)
        hover = ativo and rect.collidepoint(self.pg.mouse.get_pos())
        fundo = T.OURO if primario else T.ELEVADO
        if hover:
            fundo = (242, 204, 138) if primario else (43, 71, 72)
        if not ativo:
            fundo = (22, 36, 39)
        cor = T.FUNDO if primario and ativo else T.TEXTO if ativo else T.APAGADO
        self.painel(x, y, w, h, fundo, T.OURO if primario and ativo else T.BORDA, 8)
        self.texto(rotulo, x + 15, y + (10 if detalhe else (h - 19) // 2), "normal", cor)
        if detalhe:
            self.texto(detalhe, x + 15, y + 35, "micro", T.FUNDO if primario else T.SUAVE)
        if ativo:
            self.jogo.botoes.append((rect, acao))

    def selo(self, texto, x, y, cor=T.OURO):
        largura = self.fontes["micro"].size(texto)[0] + 20
        self.painel(x, y, largura, 24, T.ELEVADO, None, 5)
        self.texto(texto, x + 10, y + 5, "micro", cor)
