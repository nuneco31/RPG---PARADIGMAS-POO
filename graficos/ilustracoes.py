"""Arte vetorial autoral: árvores, ruínas e personagens, sem assets externos.

As superfícies são calculadas uma vez e reutilizadas em cada desenho.
"""

from graficos.tema import Tema as T


class Ilustracoes:
    def __init__(self, pygame):
        self.pg = pygame
        self._cache = {}

    def floresta(self, largura, altura):
        chave = ("floresta", largura, altura)
        if chave in self._cache:
            return self._cache[chave]
        pg = self.pg
        tela = pg.Surface((largura, altura))
        for y in range(altura):
            fracao = y / max(1, altura)
            cor = (int(23 - 6 * fracao), int(49 - 14 * fracao), int(54 - 15 * fracao))
            pg.draw.line(tela, cor, (0, y), (largura, y))
        lua = (int(largura * .73), int(altura * .25))
        pg.draw.circle(tela, (49, 77, 76), lua, int(altura * .23))
        pg.draw.circle(tela, (192, 191, 147), lua, int(altura * .12))
        for camada, cor in enumerate(((39, 70, 68), (27, 58, 56), (13, 35, 37))):
            base = int(altura * (.73 + camada * .1))
            passo = max(36, largura // 10)
            for indice, x in enumerate(range(-passo, largura + passo, passo)):
                x += (camada * 23) % passo
                h = int(altura * (.35 + ((indice * 7 + camada) % 5) * .055))
                w = int(h * .34)
                pg.draw.rect(tela, cor, (x - 3, base - h // 2, 6, h // 2 + 20))
                for nivel in range(3):
                    topo = base - h + nivel * h * .2
                    pg.draw.polygon(tela, cor, [(x, topo), (x - w, topo + h * .6), (x + w, topo + h * .6)])
        pg.draw.polygon(tela, (72, 81, 64), [(largura*.53, altura*.65), (largura*.59, altura*.65), (largura*.78, altura), (largura*.34, altura)])
        pg.draw.polygon(tela, (115, 111, 77), [(largura*.55, altura*.65), (largura*.57, altura*.65), (largura*.65, altura), (largura*.48, altura)])
        cx, cy = int(largura * .56), int(altura * .66)
        rw, rh = max(18, int(altura*.12)), max(30, int(altura*.21))
        pg.draw.rect(tela, (83, 103, 91), (cx-rw, cy-rh, rw*2, rh), border_radius=rw)
        pg.draw.rect(tela, (13, 35, 37), (cx-rw+7, cy-rh+8, rw*2-14, rh), border_radius=max(2,rw-7))
        for i in range(15):
            x = int((i * 97 + 31) % largura)
            y = int(altura*.5 + (i*31) % max(1,int(altura*.45)))
            pg.draw.circle(tela, T.OURO, (x, y), 1 if i % 3 else 2)
        self._cache[chave] = tela
        return tela

    def retrato(self, tipo, largura=112, altura=132):
        chave = (tipo, largura, altura)
        if chave in self._cache:
            return self._cache[chave]
        pg = self.pg
        tela = pg.Surface((160, 180), pg.SRCALPHA)
        d = pg.draw
        d.ellipse(tela, (11, 22, 25, 110), (23, 157, 116, 16))
        if tipo == "heroi":
            d.polygon(tela, (47, 92, 82), [(80,70),(45,91),(26,158),(128,158),(114,91)])
            d.polygon(tela, (92, 138, 116), [(80,72),(54,94),(55,149),(106,149),(108,94)])
            d.polygon(tela, (37, 66, 66), [(54,92),(34,145),(55,149)])
            d.circle(tela, (213, 182, 133), (80,58), 25)
            d.polygon(tela, (58, 55, 45), [(53,58),(56,32),(82,23),(104,37),(107,61),(91,40),(71,48)])
            d.rect(tela, (53,61,53), (59,79,43,14), border_radius=4)
            d.rect(tela, (42, 57, 54), (57,136,47,9))
            d.circle(tela, T.OURO, (81,140), 5)
            d.polygon(tela, (195,206,183), [(120,47),(125,54),(113,130),(105,130)])
            d.line(tela, T.OURO, (99,125),(124,130),4)
            d.line(tela, (69,47,35), (111,130),(108,149),6)
            d.circle(tela, (31,41,40), (72,59), 2)
            d.circle(tela, (31,41,40), (89,59), 2)
        elif "Mago" in tipo:
            d.polygon(tela, (84,74,117), [(80,65),(48,93),(30,158),(130,158),(108,93)])
            d.circle(tela, (168,155,159), (80,63), 23)
            d.polygon(tela, (101,87,139), [(80,15),(43,60),(117,60)])
            d.line(tela, (155,128,77), (127,52),(123,158),6)
            d.circle(tela, (137,172,200), (128,48),11)
            d.line(tela, T.OURO, (64,65),(76,65),3)
            d.line(tela, T.OURO, (86,65),(98,65),3)
        else:
            chefe = "Rei" in tipo
            pele = (133,148,100) if "Orc" in tipo else (113,160,112)
            d.polygon(tela, (92,61,51) if chefe else (65,80,65), [(80,77),(43,94),(29,158),(130,158),(114,94)])
            d.polygon(tela, pele, [(56,48),(32,43),(50,73),(60,79),(101,79),(111,69),(130,43),(105,47)])
            d.circle(tela, pele, (80,61), 30)
            d.polygon(tela, (60,78,54), [(51,52),(60,31),(92,27),(110,47),(99,42),(65,46)])
            d.line(tela, T.FUNDO,(60,60),(72,64),3)
            d.line(tela, T.FUNDO,(87,64),(100,60),3)
            d.polygon(tela, T.TEXTO, [(62,79),(65,67),(70,81)])
            d.polygon(tela, T.TEXTO, [(90,81),(96,67),(99,79)])
            d.line(tela, (116,91,57), (127,86),(127,156),7)
            d.polygon(tela, (155,169,145),[(126,85),(115,65),(140,69),(149,93),(130,95)])
            if chefe:
                d.polygon(tela, T.OURO,[(53,39),(49,16),(67,27),(80,10),(94,27),(112,16),(107,39)])
                d.rect(tela, T.OURO, (52,36,56,7))
                d.circle(tela, T.VERMELHO, (80,33),4)
        resultado = pg.transform.smoothscale(tela, (largura, altura))
        self._cache[chave] = resultado
        return resultado
