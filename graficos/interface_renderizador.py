class InterfaceRenderizador:
    """Desenha telas, status e botões clicáveis do RPG Pygame."""

    FUNDO = (20, 25, 38)
    PAINEL = (34, 43, 61)
    BOTAO = (57, 91, 135)
    BOTAO_HOVER = (76, 119, 169)
    TEXTO = (239, 242, 247)
    SUAVE = (177, 190, 209)
    VERDE = (85, 180, 125)
    VERMELHO = (198, 82, 82)

    def __init__(self, jogo):
        self.jogo = jogo
        self.pygame = jogo.pygame

    def desenhar(self):
        jogo = self.jogo
        tela = jogo.tela
        tela.fill(self.FUNDO)
        jogo.botoes.clear()
        self._texto("RPG AVENTURA", 48, 28, jogo.fonte, self.TEXTO)
        self._texto(self._subtitulo(), 50, 72, jogo.fonte_pequena, self.SUAVE)
        self._painel_status()

        renderizadores = {
            "menu": self._menu,
            "exploracao": self._exploracao,
            "evento": self._evento,
            "npc": self._npc,
            "inventario": self._inventario,
            "status": self._status,
            "habilidades": self._habilidades,
            "selecionar_habilidade": self._selecionar_habilidade,
            "combate": self._combate,
            "fim_batalha": self._fim_batalha,
            "conclusao": self._conclusao,
        }
        renderizadores.get(jogo.estado, self._menu)()
        self._mensagem()
        self.pygame.display.flip()

    def _subtitulo(self):
        return {
            "menu": "Sua aventura começa na Floresta Sombria.",
            "exploracao": "Floresta Sombria — escolha seu caminho.",
            "combate": "Combate por turnos — observe a vida e a mana.",
            "fim_batalha": "O combate terminou.",
            "inventario": "Itens e equipamentos do jogador.",
            "status": "Atributos e progresso do personagem.",
            "habilidades": "Habilidades disponíveis e seus custos.",
            "selecionar_habilidade": "Escolha uma habilidade para este turno.",
            "npc": "Encontro na trilha.",
            "conclusao": "A pequena aventura chegou ao fim.",
        }.get(self.jogo.estado, "Evento da floresta")

    def _painel_status(self):
        jogador = self.jogo.jogador
        self._caixa(40, 112, 920, 78, self.PAINEL)
        self._texto(f"{jogador.nome}  |  Nível {jogador.nivel}", 60, 124, self.jogo.fonte_pequena, self.TEXTO)
        self._texto(f"HP {jogador.vida}/{jogador.vida_maxima}", 60, 155, self.jogo.fonte_menor, self.TEXTO)
        self._barra(210, 160, 230, 15, jogador.vida, jogador.vida_maxima, self.VERDE)
        self._texto(f"Mana {jogador.mana}/{jogador.mana_maxima}", 475, 155, self.jogo.fonte_menor, self.TEXTO)
        self._barra(620, 160, 180, 15, jogador.mana, jogador.mana_maxima, (88, 142, 220))
        self._texto(f"XP {jogador.xp}/{jogador.xp_necessaria}", 830, 153, self.jogo.fonte_menor, self.SUAVE)

    def _menu(self):
        self._texto("O que deseja fazer?", 70, 225, self.jogo.fonte, self.TEXTO)
        itens = [
            ("Explorar", "explorar"), ("Inventário", "inventario"),
            ("Status", "status"), ("Habilidades", "habilidades"),
            ("Salvar jogo", "salvar"), ("Carregar jogo", "carregar"),
            ("Sair", "sair"),
        ]
        for indice, (rotulo, acao) in enumerate(itens):
            coluna, linha = indice % 2, indice // 2
            self._botao(rotulo, acao, 70 + coluna * 430, 290 + linha * 74, 390, 54)

    def _exploracao(self):
        self._texto("A trilha se divide entre a estrada e a parte fechada da floresta.", 70, 225, self.jogo.fonte_pequena, self.TEXTO)
        self._botao("Seguir pela estrada", "estrada", 70, 290, 390, 58)
        self._botao("Entrar na floresta", "floresta", 500, 290, 390, 58)
        self._botao("Procurar itens", "procurar", 70, 370, 390, 58)
        self._botao("Voltar ao menu", "voltar_menu", 500, 370, 390, 58)
        vencidos = self.jogo.progresso["encontros"]
        self._texto(f"Encontros vencidos: {vencidos}/3", 75, 465, self.jogo.fonte_pequena, self.SUAVE)
        if vencidos >= 3 and not self.jogo.progresso["chefe_derrotado"]:
            self._texto("Um rugido ecoa adiante: o Rei Goblin está esperando.", 75, 505, self.jogo.fonte_pequena, (238, 190, 99))

    def _evento(self):
        self._paragrafo(self.jogo.mensagem, 75, 250, self.jogo.fonte_pequena, self.TEXTO)
        self._botao("Continuar", "voltar_exploracao", 70, 350, 390, 58)
        self._botao("Abrir inventário", "inventario", 500, 350, 390, 58)

    def _npc(self):
        self._paragrafo(self.jogo.mensagem, 75, 250, self.jogo.fonte_pequena, self.TEXTO)
        self._botao("Aceitar poção", "aceitar_pocao", 70, 330, 390, 58)
        self._botao("Agradecer e seguir", "recusar_npc", 500, 330, 390, 58)

    def _inventario(self):
        jogador = self.jogo.jogador
        itens = jogador.inventario.itens
        equipamentos = jogador.inventario.equipamentos
        self._texto("Itens na mochila", 70, 215, self.jogo.fonte_pequena, self.TEXTO)
        linha = 255
        if not itens:
            self._texto("Nenhum item guardado.", 80, linha, self.jogo.fonte_menor, self.SUAVE)
        for nome, quantidade in itens.items():
            self._texto(f"{nome}  x{quantidade}", 80, linha + 10, self.jogo.fonte_pequena, self.TEXTO)
            if nome.startswith("Poção"):
                self._botao("Usar", f"usar:{nome}", 650, linha, 120, 44)
            else:
                self._botao("Equipar", f"equipar:{nome}", 790, linha, 135, 44)
            linha += 58
        self._texto("Equipados: " + (", ".join(equipamentos.values()) or "nenhum"), 80, 500, self.jogo.fonte_menor, self.SUAVE)
        self._botao("Voltar", "voltar_anterior", 70, 555, 390, 52)

    def _status(self):
        jogador = self.jogo.jogador
        linhas = [
            f"Vida: {jogador.vida}/{jogador.vida_maxima}",
            f"Ataque: {jogador.ataque}",
            f"Defesa: {jogador.defesa}",
            f"Mana: {jogador.mana}/{jogador.mana_maxima}",
            f"Nível: {jogador.nivel}  |  XP: {jogador.xp}/{jogador.xp_necessaria}",
        ]
        for indice, linha in enumerate(linhas):
            self._texto(linha, 80, 235 + indice * 48, self.jogo.fonte, self.TEXTO)
        self._botao("Voltar", "voltar_anterior", 70, 500, 390, 54)

    def _habilidades(self):
        self._texto("Ataques podem ser usados em combate; Cura também pode ser usada aqui.", 70, 220, self.jogo.fonte_menor, self.SUAVE)
        linha = 270
        for habilidade in self.jogo.jogador.habilidades.values():
            self._texto(f"{habilidade.nome}  |  custo: {habilidade.custo_mana} mana", 80, linha + 9, self.jogo.fonte_pequena, self.TEXTO)
            if habilidade.nome == "Cura":
                self._botao("Usar Cura", f"habilidade:{habilidade.nome}", 700, linha, 220, 45)
            linha += 65
        self._botao("Voltar", "voltar_anterior", 70, 500, 390, 54)

    def _selecionar_habilidade(self):
        linha = 245
        for habilidade in self.jogo.jogador.habilidades.values():
            self._botao(f"{habilidade.nome} ({habilidade.custo_mana} mana)", f"habilidade:{habilidade.nome}", 70, linha, 570, 50)
            linha += 62
        self._botao("Cancelar", "voltar_combate", 680, 245, 240, 50)

    def _combate(self):
        inimigo = self.jogo.inimigo
        self._caixa(70, 215, 850, 135, (62, 42, 49))
        self._texto(inimigo.nome, 95, 230, self.jogo.fonte, self.TEXTO)
        self._texto(f"HP {inimigo.vida}/{inimigo.vida_maxima}", 95, 280, self.jogo.fonte_pequena, self.TEXTO)
        self._barra(310, 288, 500, 19, inimigo.vida, inimigo.vida_maxima, self.VERMELHO)
        self._botao("Atacar", "combate:1", 70, 390, 250, 54)
        self._botao("Habilidade", "abrir_habilidades_combate", 350, 390, 250, 54)
        self._botao("Usar poção", "combate:3", 630, 390, 250, 54)
        self._botao("Defender", "combate:4", 210, 465, 250, 54)
        self._botao("Fugir", "combate:5", 490, 465, 250, 54)
        self._paragrafo(self.jogo.mensagem, 80, 535, self.jogo.fonte_menor, self.SUAVE, 830)

    def _fim_batalha(self):
        self._paragrafo(self.jogo.mensagem, 80, 250, self.jogo.fonte_pequena, self.TEXTO)
        rotulo = "Ver resultado" if self.jogo.resultado_batalha == "vitoria" else "Continuar"
        self._botao(rotulo, "continuar", 70, 360, 390, 58)

    def _conclusao(self):
        self._paragrafo(self.jogo.mensagem, 75, 260, self.jogo.fonte_pequena, (238, 210, 130))
        self._botao("Voltar ao menu", "voltar_menu", 70, 365, 390, 58)

    def _mensagem(self):
        if self.jogo.estado not in ("combate", "fim_batalha", "evento", "npc", "conclusao"):
            self._paragrafo(self.jogo.mensagem, 52, 625, self.jogo.fonte_menor, self.SUAVE, 900)

    def _botao(self, texto, acao, x, y, largura, altura):
        pygame = self.pygame
        retangulo = pygame.Rect(x, y, largura, altura)
        cor = self.BOTAO_HOVER if retangulo.collidepoint(pygame.mouse.get_pos()) else self.BOTAO
        pygame.draw.rect(self.jogo.tela, cor, retangulo, border_radius=9)
        pygame.draw.rect(self.jogo.tela, (110, 139, 174), retangulo, 1, border_radius=9)
        imagem = self.jogo.fonte_pequena.render(texto, True, self.TEXTO)
        self.jogo.tela.blit(imagem, imagem.get_rect(center=retangulo.center))
        self.jogo.botoes.append((retangulo, acao))

    def _texto(self, texto, x, y, fonte, cor):
        imagem = fonte.render(str(texto), True, cor)
        self.jogo.tela.blit(imagem, (x, y))

    def _paragrafo(self, texto, x, y, fonte, cor, largura=850):
        for bloco in str(texto).splitlines() or [""]:
            linha = ""
            for palavra in bloco.split():
                tentativa = f"{linha} {palavra}".strip()
                if linha and fonte.size(tentativa)[0] > largura:
                    self._texto(linha, x, y, fonte, cor)
                    y += fonte.get_linesize()
                    linha = palavra
                else:
                    linha = tentativa
            self._texto(linha, x, y, fonte, cor)
            y += fonte.get_linesize()

    def _caixa(self, x, y, largura, altura, cor):
        self.pygame.draw.rect(self.jogo.tela, cor, (x, y, largura, altura), border_radius=12)

    def _barra(self, x, y, largura, altura, atual, maximo, cor):
        self._caixa(x, y, largura, altura, (57, 64, 76))
        preenchida = int(largura * max(0, atual) / max(1, maximo))
        if preenchida:
            self.pygame.draw.rect(self.jogo.tela, cor, (x, y, preenchida, altura), border_radius=7)
