# RPG em Python - Paradigmas da Programação / POO

## Visão geral

Este projeto foi desenvolvido como uma aplicação didática de Programação Orientada a Objetos (POO), utilizando Python e a biblioteca Pygame para representar um pequeno jogo de RPG em 2D. A proposta principal é demonstrar os princípios de encapsulamento, herança, abstração e organização por responsabilidades em um sistema simples e funcional.

O jogo simula uma batalha entre o jogador e inimigos, com movimentação, seleção de alvo, combate, sistema de XP e evolução de nível. A estrutura foi organizada em módulos para facilitar a compreensão e a apresentação do projeto em uma disciplina acadêmica.

## Objetivos do projeto

- aplicar conceitos de POO em um cenário prático
- demonstrar a separação de responsabilidades em classes e pacotes
- implementar um sistema de combate simples e interativo
- desenvolver uma arquitetura organizada para facilitar manutenção e leitura

## Conceitos de POO aplicados

- Herança: a classe `Jogador` e a classe `Inimigo` herdam de `Personagem`
- Encapsulamento: atributos como vida, ataque e defesa ficam dentro das classes
- Abstração: o código usa classes e métodos com funções bem definidas
- Modularização: o projeto foi dividido em diretórios conforme a responsabilidade de cada parte

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
├── graficos/
│   ├── __init__.py
│   └── renderizador.py
└── tests/
    └── test_combate.py
```

## Responsabilidade de cada pasta

- `main.py`: ponto de entrada do programa
- `jogo/`: lógica principal do jogo, processamento de ações e regras de combate
- `personagens/`: classes do jogador, inimigos e personagem base
- `graficos/`: renderização da interface visual em tela
- `tests/`: testes automatizados para validar o comportamento do combate

## Requisitos

- Python 3.10 ou superior
- Biblioteca Pygame
- Ambiente virtual recomendado

## Como executar

1. Acesse a pasta do projeto.
2. Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

3. Execute o jogo:

```powershell
python main.py
```

## Controles

- `W`, `A`, `S`, `D`: movimentação do personagem
- `1`: selecionar o Goblin 1
- `2`: selecionar o Goblin 2
- `Espaço`: atacar o goblin selecionado

## Sistema de combate

O sistema de combate funciona da seguinte forma:

1. o jogador seleciona um inimigo usando as teclas `1` ou `2`
2. o personagem ataca com `Espaço`
3. o goblin selecionado reage atacando o jogador na sequência
4. se o inimigo for derrotado, o jogador recebe XP
5. quando a XP acumulada atinge o valor necessário, o personagem sobe de nível

## Observações finais

Esse projeto foi organizado para demonstrar de forma clara a aplicação dos paradigmas de programação, especialmente em relação à montagem de classes e à separação de responsabilidades. A estrutura modular facilita a explicação para o professor, pois cada diretório representa uma camada funcional do sistema.

A proposta não é apenas criar um jogo funcional, mas também apresentar uma solução bem organizada e coerente com os princípios da Programação Orientada a Objetos.
