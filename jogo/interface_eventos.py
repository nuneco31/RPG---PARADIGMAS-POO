class EventosInterface:
    """Converte cliques do mouse e teclas em ações da interface do jogo."""

    def __init__(self, jogo):
        self.jogo = jogo
        self.pygame = jogo.pygame

    def processar(self):
        for evento in self.pygame.event.get():
            if evento.type == self.pygame.QUIT:
                self.jogo.rodando = False
            elif evento.type == self.pygame.KEYDOWN:
                if evento.key == self.pygame.K_ESCAPE:
                    if self.jogo.estado in ("menu", "conclusao"):
                        self.jogo.rodando = False
                    elif self.jogo.estado == "selecionar_habilidade":
                        self.jogo.estado = "combate"
                    elif self.jogo.estado == "combate":
                        continue
                    elif self.jogo.estado == "fim_batalha":
                        self.jogo.acionar("continuar")
                    else:
                        self.jogo.estado = "menu"
            elif evento.type == self.pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for retangulo, acao in reversed(self.jogo.botoes):
                    if retangulo.collidepoint(evento.pos):
                        self.jogo.acionar(acao)
                        break
