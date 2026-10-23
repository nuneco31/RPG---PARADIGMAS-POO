"""Telas da campanha. O renderizador lê o estado e registra áreas clicáveis.

Ele não modifica personagens nem decide resultados: ações seguem para a
campanha. A única informação local é a página visível da mochila.
"""

from graficos.componentes import Componentes
from graficos.ilustracoes import Ilustracoes
from graficos.tema import Tema as T


class InterfaceRenderizador:
    TITULOS = {
        "menu": "O chamado da floresta",
        "exploracao": "Escolha seu caminho",
        "inventario": "Sua mochila",
        "status": "O aventureiro",
        "habilidades": "Artes do aventureiro",
        "selecionar_habilidade": "Prepare sua habilidade",
        "combate": "Um encontro na trilha",
        "evento": "A floresta tem histórias",
        "npc": "Uma presença amiga",
        "fim_batalha": "O desfecho do encontro",
        "conclusao": "Uma nova crônica começa",
        "caderno": "O código por trás da aventura",
    }

    def __init__(self, jogo):
        self.jogo = jogo
        self.pygame = jogo.pygame
        self.ui = Componentes(jogo)
        self.arte = Ilustracoes(self.pygame)
        self.pagina_inventario = 0

    def desenhar(self):
        jogo = self.jogo
        jogo.tela.fill(T.FUNDO)
        jogo.botoes.clear()
        self._lateral()
        self.ui.texto("CAPÍTULO 01  /  FLORESTA SOMBRIA", 248, 25, "micro", T.OURO)
        self.ui.texto(self.TITULOS.get(jogo.estado, "Sua aventura"), 246, 48, "titulo")
        self._status_compacto()
        telas = {
            "menu": self._menu, "exploracao": self._exploracao,
            "inventario": self._inventario, "status": self._status,
            "habilidades": self._habilidades,
            "selecionar_habilidade": self._selecionar_habilidade,
            "combate": self._combate, "evento": self._evento,
            "npc": self._npc, "fim_batalha": self._fim_batalha,
            "conclusao": self._conclusao, "caderno": self._caderno,
        }
        telas.get(jogo.estado, self._menu)()
        self._rodape()
        self.pygame.display.flip()

    def _lateral(self):
        u = self.ui
        u.painel(0, 0, 222, 700, T.LATERAL, None, 0)
        self.pygame.draw.line(self.jogo.tela, T.BORDA, (221, 0), (221, 700))
        # Emblema: um pinheiro dentro de uma moldura em losango.
        self.pygame.draw.polygon(self.jogo.tela, T.OURO, [(42,22),(62,42),(42,62),(22,42)], 1)
        self.pygame.draw.polygon(self.jogo.tela, T.OURO, [(42,30),(32,47),(52,47)])
        self.pygame.draw.line(self.jogo.tela, T.OURO, (42,42), (42,54), 2)
        u.texto("CRÔNICAS", 23, 79, "grande")
        u.texto("DA FLORESTA", 24, 109, "pequena", T.OURO)
        u.texto("Uma aventura sobre escolhas.", 24, 141, "micro", T.SUAVE)
        bloqueado = self.jogo.estado in ("combate", "selecionar_habilidade", "fim_batalha")
        navegacao = [
            ("01", "Acampamento", "voltar_menu", "menu"),
            ("02", "Explorar", "explorar", "exploracao"),
            ("03", "Mochila", "inventario", "inventario"),
            ("04", "Habilidades", "habilidades", "habilidades"),
            ("05", "Personagem", "status", "status"),
            ("06", "Caderno POO", "caderno", "caderno"),
        ]
        for indice, (numero, rotulo, acao, estado) in enumerate(navegacao):
            y = 191 + indice * 42
            selecionado = self.jogo.estado == estado
            rect = self.pygame.Rect(15, y, 192, 36)
            hover = rect.collidepoint(self.pygame.mouse.get_pos()) and not bloqueado
            if selecionado or hover:
                u.painel(15, y, 192, 36, T.ELEVADO, None, 7)
            if selecionado:
                u.painel(15, y + 8, 3, 20, T.OURO, None, 1)
            u.texto(numero, 29, y + 11, "micro", T.OURO if selecionado else T.APAGADO)
            u.texto(rotulo, 58, y + 9, "pequena", T.APAGADO if bloqueado else T.TEXTO)
            if not bloqueado:
                self.jogo.botoes.append((rect, acao))
        u.painel(20, 466, 182, 126, T.PAINEL, None)
        u.texto("SUA JORNADA", 34, 481, "micro", T.OURO)
        vencidos = min(3, self.jogo.progresso["encontros"])
        u.paragrafo("Liberte a floresta do Rei Goblin.", 34, 507, 150, limite=2)
        for i in range(3):
            cor = T.VERDE if i < vencidos else T.BORDA
            u.painel(35 + i * 47, 556, 37, 5, cor, None, 2)
        legenda = "Chefe derrotado" if self.jogo.progresso["chefe_derrotado"] else f"{vencidos}/3 encontros vencidos"
        u.texto(legenda, 34, 572, "micro", T.SUAVE)
        u.botao("Sair da aventura", "sair", 20, 627, 182, 36)
        u.texto("PYTHON  /  POO  /  RPG", 32, 680, "micro", T.APAGADO)

    def _status_compacto(self):
        u = self.ui
        j = self.jogo.jogador
        u.painel(246, 102, 730, 77)
        u.texto(j.nome, 265, 118, "normal")
        u.texto(f"AVENTUREIRO  ·  NV {j.nivel}", 265, 146, "micro", T.OURO)
        dados = [
            (410, "VIDA", j.vida, j.vida_maxima, T.VERDE),
            (603, "MANA", j.mana, j.mana_maxima, T.AZUL),
            (797, "EXPERIÊNCIA", j.xp, j.xp_necessaria, T.OURO),
        ]
        for x, nome, atual, maximo, cor in dados:
            u.texto(nome, x, 117, "micro", T.SUAVE)
            u.texto(f"{atual}/{maximo}", x + 91, 117, "micro", cor)
            u.barra(x, 149, 153, atual, maximo, cor)

    def _cena(self, x, y, w, h):
        self.jogo.tela.blit(self.arte.floresta(w, h), (x, y))
        self.pygame.draw.rect(self.jogo.tela, T.BORDA, (x,y,w,h), 1, border_radius=10)

    def _menu(self):
        u = self.ui
        self._cena(246, 201, 730, 218)
        u.painel(247, 202, 365, 216, T.PAINEL, None, 0)
        u.selo("UMA FLORESTA. MUITAS ESCOLHAS.", 266, 221)
        u.texto("Toda jornada", 267, 263, "titulo")
        u.texto("começa com um passo.", 267, 298, "grande")
        u.paragrafo("Prepare seus equipamentos, escolha uma trilha e descubra o que vive além das ruínas.", 268, 349, 315, limite=3)
        self.jogo.tela.blit(self.arte.retrato("heroi", 132, 154), (793, 262))
        u.botao("Começar a explorar", "explorar", 246, 436, 238, 61, "Escolha sua próxima trilha", True)
        u.botao("Preparar mochila", "inventario", 496, 436, 234, 61, "Itens e equipamentos")
        u.botao("Abrir o caderno", "caderno", 742, 436, 234, 61, "Entenda os conceitos de POO")
        u.botao("Salvar progresso", "salvar", 246, 514, 238, 43)
        u.botao("Carregar jornada", "carregar", 496, 514, 234, 43)
        u.texto("SEU RITMO. SUAS ESCOLHAS.", 754, 530, "micro", T.APAGADO)

    def _exploracao(self):
        u = self.ui
        self._cena(648, 202, 328, 354)
        u.texto("A trilha se divide.", 248, 208, "grande")
        u.paragrafo("O caminho muda os encontros. Prepare-se antes de seguir adiante.", 249, 245, 370, limite=2)
        pronto = self.jogo.progresso["encontros"] >= 3 and not self.jogo.progresso["chefe_derrotado"]
        u.botao("Seguir pela estrada", "estrada", 246, 311, 380, 66,
                "Caminho tranquilo · mais encontros amigáveis")
        u.botao("Entrar na floresta", "floresta", 246, 389, 380, 66,
                "Caminho perigoso · mais combates", True)
        u.botao("Procurar suprimentos", "procurar", 246, 470, 380, 48)
        if pronto:
            u.selo("O REI GOBLIN ESPERA ADIANTE", 261, 531)
        else:
            u.texto("Dica: equipe sua espada antes do primeiro combate.", 249, 538, "micro", T.SUAVE)

    def _inventario(self):
        u = self.ui
        jogador = self.jogo.jogador
        itens = list(jogador.inventario.itens.items())
        paginas = max(1, (len(itens) + 3) // 4)
        self.pagina_inventario = max(0, min(self.pagina_inventario, paginas - 1))
        u.texto("Tudo pronto para a próxima trilha?", 248, 203, "normal")
        u.texto("POÇÕES RESTAURAM RECURSOS. EQUIPAMENTOS MELHORAM ATRIBUTOS.", 249, 233, "micro", T.SUAVE)
        inicio = self.pagina_inventario * 4
        for i, (nome, quantidade) in enumerate(itens[inicio:inicio + 4]):
            y = 263 + i * 58
            u.painel(246, y, 730, 49)
            u.painel(259, y + 12, 27, 25, T.ELEVADO, None, 5)
            u.texto(str(quantidade), 268, y + 17, "micro", T.OURO)
            u.texto(nome, 303, y + 14, "normal")
            pocao = nome.startswith("Poção")
            acao = f"usar:{nome}" if pocao else f"equipar:{nome}"
            u.botao("Usar" if pocao else "Equipar", acao, 833, y + 6, 129, 37)
        if not itens:
            u.paragrafo("A mochila está vazia. Explore para encontrar itens e equipamentos.", 267, 293, 640, limite=2)
        equipados = ", ".join(jogador.inventario.equipamentos.values()) or "nenhum equipamento"
        u.paragrafo("Equipados: " + equipados, 249, 503, 720, "micro", limite=1)
        u.botao("Anterior", "pagina:anterior", 246, 530, 128, 35, ativo=self.pagina_inventario > 0)
        u.texto(f"Página {self.pagina_inventario + 1} de {paginas}", 395, 541, "micro", T.SUAVE)
        u.botao("Próxima", "pagina:proxima", 522, 530, 128, 35, ativo=self.pagina_inventario + 1 < paginas)
        u.botao("Voltar", "voltar_anterior", 846, 530, 130, 35)

    def _status(self):
        u = self.ui
        j = self.jogo.jogador
        self._cena(246, 201, 251, 356)
        self.jogo.tela.blit(self.arte.retrato("heroi", 210, 245), (266, 290))
        u.selo("GUARDIÃO DA TRILHA", 276, 223)
        dados = [
            ("ATAQUE", str(j.ataque), "Força usada nos seus golpes."),
            ("DEFESA", str(j.defesa), "Reduz o dano dos inimigos."),
            ("NÍVEL", str(j.nivel), "A experiência fortalece o aventureiro."),
        ]
        for i, (rotulo, valor, descricao) in enumerate(dados):
            y = 201 + i * 100
            u.painel(515, y, 461, 85)
            u.texto(rotulo, 533, y + 15, "micro", T.OURO)
            u.texto(valor, 897, y + 19, "titulo")
            u.texto(descricao, 533, y + 46, "pequena", T.SUAVE)
        u.botao("Voltar à jornada", "voltar_anterior", 515, 517, 461, 40)

    def _lista_habilidades(self, em_combate):
        u = self.ui
        j = self.jogo.jogador
        u.texto("Escolha com atenção: habilidades consomem mana.", 248, 204, "pequena", T.SUAVE)
        for i, h in enumerate(j.habilidades.values()):
            y = 245 + i * 88
            u.painel(246, y, 730, 76)
            u.texto(h.nome, 264, y + 14, "normal")
            efeito = f"Restaura {h.poder} de vida" if h.tipo == "cura" else f"Ataque + {h.poder} de poder"
            u.texto(f"{efeito}  ·  {h.custo_mana} de mana", 264, y + 46, "pequena", T.SUAVE)
            permitida = em_combate or h.tipo == "cura"
            mana = j.mana >= h.custo_mana
            rotulo = "Usar" if permitida and mana else "Sem mana" if permitida else "Em combate"
            u.botao(rotulo, f"habilidade:{h.nome}", 803, y + 16, 154, 42, ativo=permitida and mana)
        u.botao("Cancelar" if em_combate else "Voltar", "voltar_combate" if em_combate else "voltar_anterior", 246, 523, 230, 38)

    def _habilidades(self):
        self._lista_habilidades(False)

    def _selecionar_habilidade(self):
        self._lista_habilidades(True)

    def _combatente(self, personagem, x, heroi=False):
        u = self.ui
        cor = T.VERDE if heroi else T.VERMELHO
        u.painel(x, 202, 348, 188)
        u.texto("SEU AVENTUREIRO" if heroi else "ADVERSÁRIO", x + 18, 217, "micro", cor)
        self.jogo.tela.blit(self.arte.retrato("heroi" if heroi else personagem.nome), (x + 6, 248))
        u.texto(personagem.nome, x + 120, 251, "normal")
        u.texto(f"{personagem.vida}/{personagem.vida_maxima} de vida", x + 120, 281, "pequena", T.SUAVE)
        u.barra(x + 120, 310, 206, personagem.vida, personagem.vida_maxima, cor)
        u.texto(f"ATQ {personagem.ataque}   ·   DEF {personagem.defesa}", x + 120, 334, "micro", T.SUAVE)
        if not heroi and "Rei" in personagem.nome:
            u.texto("Golpe especial a cada 3 turnos", x + 120, 359, "micro", T.OURO)

    def _combate(self):
        u = self.ui
        self._combatente(self.jogo.jogador, 246, True)
        self._combatente(self.jogo.inimigo, 628)
        u.selo("SEU TURNO  /  ESCOLHA UMA AÇÃO", 246, 405)
        acoes = [
            ("Atacar", "combate:1", "Golpe sem custo de mana", True),
            ("Habilidade", "abrir_habilidades_combate", "Ataques especiais ou cura", False),
            ("Usar poção", "combate:3", "Use uma poção da mochila", False),
            ("Defender", "combate:4", "Reduz o próximo dano", False),
            ("Fugir", "combate:5", "Tente voltar para a trilha", False),
        ]
        for i, (rotulo, acao, detalhe, primario) in enumerate(acoes):
            if i < 3:
                x, y, w = 246 + i * 248, 441, 234
            else:
                x, y, w = 246 + (i - 3) * 371, 508, 359
            ativo = acao != "combate:3" or any(
                self.jogo.jogador.inventario.quantidade(nome) > 0
                for nome in ("Poção de Vida", "Poção de Mana")
            )
            u.botao(rotulo, acao, x, y, w, 57, detalhe, primario, ativo)

    def _narrativa(self, titulo, selo, cor=T.OURO):
        u = self.ui
        self._cena(746, 202, 230, 356)
        u.painel(246, 202, 481, 356)
        u.selo(selo, 267, 222, cor)
        u.texto(titulo, 267, 266, "grande", cor)
        u.paragrafo(self.jogo.mensagem, 268, 312, 435, "normal", T.TEXTO, limite=5)

    def _evento(self):
        self._narrativa("Uma descoberta na trilha", "DIÁRIO DA FLORESTA")
        self.ui.botao("Continuar", "voltar_exploracao", 267, 493, 210, 44, primario=True)
        self.ui.botao("Ver mochila", "inventario", 490, 493, 216, 44)

    def _npc(self):
        self._narrativa("Uma ajuda inesperada", "ENCONTRO AMIGÁVEL", T.VERDE)
        self.ui.botao("Aceitar poção", "aceitar_pocao", 267, 483, 210, 54, primario=True)
        self.ui.botao("Agradecer e seguir", "recusar_npc", 490, 483, 216, 54)

    def _fim_batalha(self):
        resultado = self.jogo.resultado_batalha
        titulo = {"vitoria": "A trilha está livre!", "derrota": "É hora de se recuperar.", "fuga": "Um passo de cada vez."}.get(resultado, "O encontro terminou.")
        self._narrativa(titulo, "ENCONTRO CONCLUÍDO", T.VERDE if resultado == "vitoria" else T.OURO)
        self.ui.botao("Seguir a jornada", "continuar", 267, 489, 439, 48, primario=True)

    def _conclusao(self):
        self._narrativa("A floresta respira outra vez.", "CAPÍTULO CONCLUÍDO", T.VERDE)
        self.ui.botao("Voltar ao acampamento", "voltar_menu", 267, 489, 439, 48, primario=True)

    def _caderno(self):
        u = self.ui
        u.texto("Cinco ideias de POO que você acabou de colocar em prática.", 248, 204, "pequena", T.SUAVE)
        conceitos = [
            ("01", "Abstração", "Personagem define a base comum de quem participa da aventura."),
            ("02", "Herança", "Jogador e Inimigo especializam Personagem com novos comportamentos."),
            ("03", "Polimorfismo", "acao_turno funciona para Goblin, Mago e Chefe; cada um age à sua maneira."),
            ("04", "Encapsulamento", "As propriedades de vida mantêm o valor entre zero e o máximo permitido."),
            ("05", "Composição", "Um Jogador possui um Inventario e várias Habilidades. Objetos colaboram."),
        ]
        for i, (numero, nome, explicacao) in enumerate(conceitos):
            y = 240 + i * 61
            u.painel(246, y, 730, 54)
            u.texto(numero, 260, y + 18, "pequena", T.OURO)
            u.texto(nome, 296, y + 17, "normal")
            u.paragrafo(explicacao, 470, y + 9, 485, "pequena", limite=2)

    def _rodape(self):
        u = self.ui
        u.painel(246, 584, 730, 98)
        narrativo = self.jogo.estado in ("combate", "selecionar_habilidade", "menu", "inventario", "habilidades", "status", "exploracao")
        titulo = "DIÁRIO DA JORNADA" if narrativo else "NOTAS DE VIAGEM"
        u.texto(titulo, 263, 598, "micro", T.OURO)
        mensagem = self.jogo.mensagem if narrativo else "Explore no seu ritmo. Cada escolha abre um novo encontro; o Caderno POO conecta a aventura ao código."
        u.paragrafo(mensagem, 263, 622, 694, "pequena", limite=3)
