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

Isso abre o jogo em Pygame. Para iniciar a campanha de terminal, sem dependências externas:

```powershell
python main.py --terminal
```

No Pygame, use `W`, `A`, `S`, `D` para mover, `1` ou `2` para selecionar um Goblin e `Espaço` para atacar.

## Como jogar

No menu principal:

```text
1 - Explorar
2 - Inventário
3 - Status
4 - Habilidades
5 - Salvar jogo
6 - Carregar jogo
7 - Sair
```

Na Floresta Sombria, escolha a estrada, entre na floresta ou procure itens. Eventos incluem combates, tesouros, NPCs, armadilhas e achados raros. Vença três encontros para chegar ao Rei Goblin, chefe com 250 HP e um golpe especial periódico.

Durante o combate:

```text
1 - Ataque
2 - Habilidade
3 - Usar poção
4 - Defender
5 - Fugir
```

Entradas inválidas não consomem o turno. Habilidades usam mana; defesa reduz o próximo dano e poções são consumidas do inventário. O progresso pode ser salvo em `save.json` na pasta atual.

## Estrutura e classes principais

```text
main.py                    Entrada; modo terminal ou Pygame
jogo/terminal.py           Menus, exploração e eventos
jogo/batalha_terminal.py   Turnos e regras da batalha terminal
jogo/salvamento.py         Persistência JSON
jogo/jogo.py               Interface Pygame original
jogo/combate.py            Combate da interface Pygame
jogo/eventos.py            Teclado da interface Pygame
graficos/renderizador.py   Desenho da interface Pygame
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
- **Composição:** `Jogador` possui um `Inventario` e um conjunto de `Habilidade`; `JogoTerminal` coordena jogador, exploração, batalha e salvamento.
- **Separação de responsabilidades:** regras de personagens, batalha, interface, exploração e JSON ficam em módulos distintos.

## Testes

```powershell
python -m unittest discover -s tests -v
```

Os testes cobrem as regras existentes de seleção/respawn da interface e as regras de vida, combate, habilidades, XP, inventário, equipamentos, chefe e save/load.
