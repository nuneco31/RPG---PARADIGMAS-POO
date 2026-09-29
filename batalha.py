class Batalha:

    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo

    def iniciar(self):

        print("\n==============================")
        print("       INÍCIO DA BATALHA")
        print("==============================")

        print(f"\n{self.jogador.nome} encontrou um {self.inimigo.nome}!")

        while self.jogador.esta_vivo() and self.inimigo.esta_vivo():

            self.mostrar_status()
            self.menu()

            escolha = input("\nEscolha uma opção: ")

            if escolha == "1":
                self.jogador.atacar(self.inimigo)

            elif escolha == "2":
                self.jogador.usar_habilidade(self.inimigo)

            elif escolha == "3":
                print("\nVocê fugiu da batalha!")
                return

            else:
                print("\nOpção inválida!")
                continue

            # Verifica se o inimigo morreu
            if not self.inimigo.esta_vivo():

                print(f"\n{self.inimigo.nome} foi derrotado!")

                self.jogador.ganhar_xp(
                    self.inimigo.xp_recompensa
                )

                break

            # Turno do inimigo
            print("\n--- Turno do inimigo ---")

            self.inimigo.atacar(self.jogador)

            # Verifica se o jogador morreu
            if not self.jogador.esta_vivo():

                print(f"\n{self.jogador.nome} foi derrotado!")

        print("\n==============================")
        print("        FIM DA BATALHA")
        print("==============================")

    def mostrar_status(self):

        print("\n------------------------------")
        print(f"{self.jogador.nome}: {self.jogador.vida} HP")
        print(f"{self.inimigo.nome}: {self.inimigo.vida} HP")
        print("------------------------------")

    def menu(self):

        print("\nO que deseja fazer?")
        print("1 - Atacar")
        print("2 - Usar habilidade")
        print("3 - Fugir")