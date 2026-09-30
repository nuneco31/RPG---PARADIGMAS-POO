# RPG em Python - Paradigmas da Programação / POO

Este projeto é um pequeno jogo de RPG desenvolvido em Python com foco em conceitos de Programação Orientada a Objetos (POO) e organização por responsabilidades.

## Objetivo

O jogo simula uma batalha entre um jogador e inimigos, com:
- atributos de personagem (vida, ataque, defesa)
- sistema de XP e nível
- combate entre personagens
- movimentação do personagem em tela
- renderização visual com Pygame

## Estrutura do projeto

```text
rpg-c/
├── main.py
├── README.md
├── .gitignore
├── .venv/
├── jogo/
│   ├── __init__.py
│   ├── jogo.py
│   ├── eventos.py
│   └── combate.py
├── personagens/
│   ├── __init__.py
│   ├── personagem.py
│   ├── jogador.py
│   └── inimigo.py
└── graficos/
    ├── __init__.py
    └── renderizador.py
```

## Responsabilidade de cada pasta

- `main.py`: inicia o jogo
- `jogo/`: regras do jogo, eventos e combate
- `personagens/`: classes base, jogador e inimigos
- `graficos/`: renderização da tela e elementos visuais

## Requisitos

- Python 3.10+
- Pygame

## Como executar

1. Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

2. Execute o jogo:

```powershell
python main.py
```

## Controles

- `W`, `A`, `S`, `D`: movimentar o personagem
- `Espaço`: atacar o Goblin 1
- `H`: atacar o Goblin 2

## Observações

Este projeto foi organizado em módulos para facilitar a compreensão dos conceitos de POO e da divisão de responsabilidades, algo muito útil para apresentação em disciplinas de Paradigmas da Programação.
