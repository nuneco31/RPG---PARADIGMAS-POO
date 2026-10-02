# RPG Aventura — Paradigmas da Programação / POO

RPG didático em Python com uma interface gráfica Pygame e uma campanha alternativa por terminal. O projeto demonstra POO por meio de personagens, inimigos com comportamentos próprios, combate em turnos, inventário composto e progressão.

## Requisitos e instalação

- Python 3.10 ou superior.
- O modo Pygame requer Pygame Community Edition:

```powershell
python -m pip install -r requirements.txt
```

## Como executar

Na pasta do projeto:

```powershell
python main.py
```

Isso abre a campanha completa em uma janela Pygame. Para iniciar a versão alternativa de terminal:

```powershell
python main.py --terminal
```

No Pygame, jogue clicando nos botões de explorar, inventário, status, habilidades e salvar. Durante a batalha, clique em ataque, habilidade, poção, defender ou fugir. O modo gráfico agora apresenta a campanha, os eventos e o chefe; a alternativa de terminal segue disponível pelo comando acima.

## Como jogar

No menu principal, clique em **Explorar**, **Inventário**, **Status**, **Habilidades**, **Salvar jogo** ou **Carregar jogo**. Na exploração, escolha a estrada, entre na floresta ou procure itens. Eventos incluem combates, tesouros, NPCs, armadilhas e achados raros. Vença três encontros para chegar ao Rei Goblin, chefe com 250 HP e um golpe especial periódico.

Durante o combate, clique em **Atacar**, **Habilidade**, **Usar poção**, **Defender** ou **Fugir**. Habilidades usam mana; defesa reduz o próximo dano e poções são consumidas do inventário. O progresso pode ser salvo em `save.json` na pasta atual. Pressione `Esc` para voltar de uma tela ou fechar o jogo no menu principal.

## Estrutura e classes principais

```text
main.py                    Entrada; inicia a campanha Pygame ou modo terminal
jogo/interface.py          Fluxo da campanha gráfica
jogo/interface_eventos.py  Cliques e teclas da interface
jogo/interface_renderizador.py Desenho das telas e botões
jogo/terminal.py           Menus, exploração e eventos
jogo/batalha_terminal.py   Turnos e regras da batalha terminal
jogo/salvamento.py         Persistência JSON
jogo/jogo.py               Protótipo gráfico anterior preservado
jogo/combate.py            Combate do protótipo gráfico anterior
graficos/renderizador.py   Renderização do protótipo gráfico anterior
personagens/personagem.py  Classe base abstrata e regras comuns
personagens/jogador.py     Jogador, habilidades e progressão
personagens/inimigo.py     Inimigo, Goblin, Orc, Mago e Chefe
personagens/inventario.py  Itens, quantidades e equipamentos
personagens/habilidade.py  Definições de habilidades
tests/                     Testes automatizados
```

## Conceitos de POO utilizados

- **Abstração:** `Personagem` é uma classe abstrata que define dados e operações comuns e exige a implementação de `acao_turno`.
- **Herança:** `Jogador` e `Inimigo` especializam `Personagem`; Goblin, Orc, Mago e Chefe especializam `Inimigo`.
- **Polimorfismo:** a batalha chama `acao_turno` sem precisar conhecer o tipo concreto. O Mago atravessa parte da defesa e o Chefe usa um golpe especial a cada três turnos.
- **Encapsulamento:** vida, ataque e defesa são armazenados em atributos protegidos; propriedades mantêm vida dentro de `0..vida_maxima` e atributos não negativos.
- **Composição:** `Jogador` possui um `Inventario` e um conjunto de `Habilidade`; `JogoInterface` coordena jogador, telas, exploração, batalha e salvamento.
- **Separação de responsabilidades:** regras de personagens, batalha, interface, exploração e JSON ficam em módulos distintos.

## Testes

```powershell
python -m unittest discover -s tests -v
```

Os testes cobrem as regras existentes de seleção/respawn da interface e as regras de vida, combate, habilidades, XP, inventário, equipamentos, chefe e save/load.
