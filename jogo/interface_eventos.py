"""Converte eventos do Pygame em intenções, sem aplicar regras de combate."""


class EventosInterface:
    def __init__(self, jogo):
        self.jogo = jogo
        self.pygame = jogo.pygame

    def processar(self):
        eventos = self.pygame.event.get()
        entrada_processada = False
        for evento in eventos:
            if evento.type == self.pygame.QUIT:
                self.jogo.acionar("sair")
            elif entrada_processada:
                continue
            elif evento.type == self.pygame.KEYDOWN:
                if evento.key == self.pygame.K_ESCAPE:
                    self._voltar()
                    entrada_processada = True
            elif evento.type == self.pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for retangulo, acao in reversed(self.jogo.botoes):
                    if retangulo.collidepoint(evento.pos):
                        self.jogo.acionar(acao)
                        # Cliques restantes podem usar retângulos da tela anterior.
                        entrada_processada = True
                        break
        # A aventura é por turnos: sem entrada ou exposição da janela, a tela
        # permanece igual e não precisa gastar trabalho de desenho.
        return bool(eventos)

    def _voltar(self):
        estado = self.jogo.estado
        if estado in ("menu", "conclusao"):
            self.jogo.acionar("sair")
        elif estado == "selecionar_habilidade":
            self.jogo.acionar("voltar_combate")
        elif estado == "combate":
            return
        elif estado == "fim_batalha":
            self.jogo.acionar("continuar")
        elif estado in ("inventario", "status", "habilidades", "caderno"):
            self.jogo.acionar("voltar_anterior")
        elif estado in ("evento", "npc"):
            self.jogo.acionar("voltar_exploracao")
        else:
            self.jogo.acionar("voltar_menu")
