# Crônicas da Floresta

RPG acadêmico em Python para estudar **Programação Orientada a Objetos** com uma aventura curta. Explore a floresta, equipe seu personagem e vença três encontros para enfrentar o Rei Goblin. A interface gráfica e o terminal usam o mesmo núcleo de campanha e combate.

Os personagens guardam suas regras, a campanha organiza as etapas, as interfaces recebem comandos e o renderizador desenha a tela.

![Tela inicial de Crônicas da Floresta](docs/imagens/inicio.png)

## Executar

Requer Python 3.10 ou superior. Na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

O comando padrão abre o jogo gráfico com Pygame Community Edition. Para jogar pelo terminal:

```powershell
.\.venv\Scripts\python.exe main.py --terminal
```

O terminal usa a biblioteca padrão e pode ser executado sem instalar Pygame:

```powershell
python main.py --terminal
```

Use `--seed 7` para repetir a sequência de sorteios de uma demonstração e `--save minha-partida.json` para escolher outro arquivo de salvamento. A sequência também depende das escolhas feitas durante a partida.

## Jogar

- **Explorar:** escolha a estrada ou a floresta. A floresta tem maior frequência de inimigos; ambas oferecem tesouros, encontros com uma curandeira e armadilhas.
- **Preparar o personagem:** consulte atributos e habilidades; use poções ou equipe a espada e o escudo no inventário.
- **Combater:** ataque, escolha uma habilidade, use uma poção, defenda ou tente fugir. Uma escolha inválida não consome o turno.
- **Progredir:** três vitórias comuns liberam o chefe. Fugir ou perder não conta como vitória; após uma derrota, o personagem recupera metade da vida.
- **Estudar:** abra o Caderno POO da interface gráfica para relacionar os conceitos às classes do projeto.

Na janela de 1000 × 700, use o mouse nos botões centrais e na barra lateral. A mochila mostra quatro tipos de item por página, com botões **Anterior** e **Próxima**. Habilidades sem mana suficiente ficam inativas. Durante o combate, a navegação lateral fica bloqueada; o botão **Sair** continua disponível.

`Esc` volta de telas auxiliares, fecha a seleção de habilidade ou continua após o resultado de uma batalha. Durante o turno de combate, ele não abandona o encontro. No acampamento ou na conclusão, `Esc` fecha o jogo.

O salvamento padrão fica em `save.json` **na pasta do projeto**, mesmo quando o programa é iniciado de outra pasta. Ele guarda atributos, inventário, equipamento e progresso da campanha. A batalha em andamento não é salva; salvar e carregar ficam disponíveis fora dela.

## Entender o código

```text
main.py                        Escolhe interface gráfica ou terminal
jogo/campanha.py                Fluxo compartilhado da aventura
jogo/batalha.py                 Motor de turnos, usado pelos dois modos
jogo/batalha_terminal.py        Adaptador textual para o motor de turnos
jogo/interface.py               Adaptador Pygame e ciclo da janela
jogo/interface_eventos.py       Entrada de mouse e teclado
jogo/terminal.py                Entrada e saída de texto
jogo/salvamento.py              Persistência JSON validada
graficos/interface_renderizador.py  Telas, tema e desenho procedural
graficos/componentes.py         Painéis, textos e botões reutilizáveis
graficos/ilustracoes.py          Personagens e cenário desenhados por código
graficos/tema.py                 Paleta e estilos compartilhados
personagens/personagem.py       Contrato abstrato e atributos comuns
personagens/jogador.py          Jogador, mana, defesa e progressão
personagens/inimigo.py          Inimigos e ações especializadas
personagens/inventario.py       Itens e equipamentos por composição
personagens/habilidade.py       Catálogo de habilidades
tests/                         Regressões de regras e interfaces
docs/                          Arquitetura e roteiro de apresentação
```

O motor em `jogo/batalha.py` executa uma ação sem ler entrada nem desenhar uma janela. O adaptador `batalha_terminal.py` acrescenta o método `lutar`, com perguntas e mensagens do console. Os arquivos de protótipo preservados são explicados na [arquitetura](docs/ARQUITETURA.md).

### POO no projeto

| Conceito | Exemplo concreto |
| --- | --- |
| Abstração | `Personagem` exige a implementação de `acao_turno`. |
| Herança | `Jogador` e `Inimigo` herdam de `Personagem`; os tipos de inimigo especializam `Inimigo`. |
| Polimorfismo | `Batalha` chama `inimigo.acao_turno(jogador)`; Mago e Chefe executam comportamentos próprios. |
| Encapsulamento | Propriedades limitam vida e atributos; o inventário entrega cópias de seus dicionários. |
| Composição | `Jogador` possui `Inventario`; a interface gráfica possui uma `Campanha`. |

O paradigma principal é POO. Há também fluxo imperativo para turnos e menus, além de dados imutáveis nos catálogos de itens e habilidades. Isso não torna o projeto uma implementação completa de todos os paradigmas.

Leia a [explicação da arquitetura](docs/ARQUITETURA.md) e use o [roteiro de apresentação](docs/APRESENTACAO.md) para preparar a demonstração.

## Verificar

Com as dependências gráficas instaladas:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes gráficos usam os drivers `dummy` do SDL e não precisam abrir uma janela visível. A suíte verifica combate, habilidades, inventário, progressão, salvamento, transições de campanha e integração básica com cliques. A aparência da interface também deve ser conferida visualmente; testes automatizados não garantem toda a experiência de uso.

Para executar apenas os novos testes do núcleo, sem Pygame:

```powershell
python -m unittest discover -s tests -p test_campanha.py -v
python -m unittest discover -s tests -p test_persistencia.py -v
```
