# Como a aventura está organizada

## Um caminho para ler o código

Comece em `main.py`, siga para `Campanha` e depois leia `Batalha`, `Jogador` e `Inventario`. Deixe o renderizador por último: ele apresenta o estado que o núcleo já calculou.

```text
Mouse/teclado → EventosInterface → JogoInterface → Campanha
Entrada de texto              → JogoTerminal   → Campanha
                                                   ↓
                                                Batalha
                                                   ↓
                                      Jogador / Inimigo / Inventario

Campanha → Salvamento → arquivo JSON
JogoInterface → InterfaceRenderizador → janela Pygame
```

As setas indicam chamadas e coordenação. Os módulos de campanha, personagens e persistência não importam Pygame. Isso permite executar regras e testes sem inicializar uma janela.

## Responsabilidades

| Parte | O que resolve | O que a outra parte recebe |
| --- | --- | --- |
| `Personagem` e subclasses | Dano, vida e comportamento de cada personagem | Valores de dano e estado atualizado |
| `Inventario` | Quantidades, consumo e bônus de equipamento | Resultado da operação e cópias dos itens |
| `Batalha` | Ação do jogador, resposta inimiga, fim e recompensa | Mensagem e estado da batalha |
| `Campanha` | Exploração, eventos, transições e progresso | Estado de tela e mensagem |
| `Salvamento` | Ler, validar e gravar a partida | Progresso restaurado ou erro |
| `JogoInterface` | Inicializar Pygame e coordenar o ciclo gráfico | Comandos para a campanha e dados para desenho |
| `JogoTerminal` | Perguntar escolhas e mostrar mensagens | Comandos para as mesmas regras |
| `InterfaceRenderizador` | Compor painéis, personagens e botões | Pixels na janela |

O domínio não imprime mensagens durante ataques ou progressão. O retorno de uma operação permite que cada interface escolha como apresentar o resultado. O motor está em `jogo/batalha.py`; `batalha_terminal.py` acrescenta o laço de perguntas do console por herança.

## Uma ação, passo a passo

1. O jogador escolhe **Atacar**.
2. A interface encaminha `combate:1` à campanha.
3. A campanha pede a `Batalha` para executar a ação `1`.
4. A batalha calcula o ataque e pede ao inimigo para receber dano.
5. Se ele sobreviver, a batalha chama `acao_turno` do inimigo. Se morrer, concede XP uma única vez.
6. A campanha identifica vitória, derrota ou fuga e prepara a tela de resultado.
7. Ao continuar, a campanha registra o encontro e libera a exploração.

Essa divisão impede que o botão de voltar interrompa um combate e evite a resposta inimiga. Durante a batalha, apenas suas ações e telas relacionadas ficam disponíveis. No resultado, continuar finaliza a transição uma única vez.

## Pilares de POO com exemplos reais

**Abstração.** `Personagem(ABC)` reúne aquilo que jogador e inimigo têm em comum. O método abstrato `acao_turno` obriga cada classe concreta a oferecer uma ação.

**Herança.** `Jogador` reaproveita vida, ataque e defesa de `Personagem`, acrescentando mana, experiência e inventário. `Goblin`, `Orc`, `Mago` e `Chefe` aproveitam a estrutura de `Inimigo`.

**Polimorfismo.** A batalha chama a mesma operação `acao_turno` em diferentes inimigos. O Mago atravessa parte da defesa; o Rei Goblin alterna seu ataque com um golpe especial. A escolha do comportamento acontece no objeto, sem a batalha precisar conter uma condição para cada espécie.

**Encapsulamento.** A propriedade `vida` mantém o valor entre zero e a vida máxima. `Inventario.itens` e `equipamentos` retornam cópias: mudar o dicionário recebido não altera a mochila internamente. O prefixo `_` expressa uma convenção de acesso protegido em Python, não uma proibição absoluta da linguagem.

**Composição.** O jogador possui um inventário. A interface gráfica possui uma campanha. Uma relação “tem um” permite que cada objeto concentre uma responsabilidade sem precisar herdar de tudo que usa.

## Outros elementos de paradigmas

- **Imperativo:** o ciclo do jogo e as decisões de turnos descrevem uma sequência de operações.
- **Orientado a objetos:** estado e comportamento ficam associados a personagens, batalha, campanha e inventário.
- **Imutabilidade localizada:** as definições de `Item` e `Habilidade` usam `dataclass(frozen=True)`. Seus valores não mudam durante a partida; a quantidade de itens e a mana pertencem a outros objetos.

Há decisões e cálculos que poderiam ser funções puras, mas o jogo é principalmente orientado a objetos. O roteiro de apresentação deve mostrar o código existente e explicar essa escolha.

## Persistência e segurança de estado

O JSON guarda uma fotografia do personagem e do progresso. O carregamento valida os dados antes de aplicá-los ao jogador ativo, evitando deixar nome, atributos e inventário parcialmente modificados por um arquivo inválido. Armas e escudos ainda na mochila também são restaurados.

Os atributos salvos já incluem os bônus dos equipamentos. Ao carregar, o inventário restaura quais itens estão equipados e não soma esses bônus novamente. Esse detalhe preserva a compatibilidade com as partidas do projeto anterior.

O caminho padrão é calculado a partir do módulo do projeto. Um caminho explicitamente fornecido ao construtor continua útil para testes e partidas alternativas.

A gravação escreve primeiro em um arquivo temporário no mesmo diretório e depois substitui o destino. Isso reduz o risco de truncar uma partida existente caso a escrita seja interrompida antes da substituição.

## Leveza e limites

O jogo usa a biblioteca padrão e uma dependência gráfica, `pygame-ce`. O cenário e os personagens são desenhados por código; não é necessário carregar pacotes de imagens ou fontes externos. `Tema` concentra a paleta, `Componentes` desenha elementos reutilizáveis e `Ilustracoes` cuida da arte. Textos e ilustrações calculados são reutilizados em cache. A janela redesenha após eventos, com limite de 30 quadros por segundo, e permanece sem trabalho de desenho quando está ociosa. Inicializa apenas vídeo e fontes, sem subsistema de áudio. A campanha é pequena e o inventário usa paginação para conservar a legibilidade.

Os módulos `jogo/jogo.py`, `jogo/combate.py`, `jogo/eventos.py` e `graficos/renderizador.py` pertencem ao protótipo anterior. Eles não são a entrada da campanha atual. Foram mantidos para preservar compatibilidade e testes antigos; novas funcionalidades devem seguir `Campanha` e `Batalha`, evitando ampliar o fluxo antigo.

A arquitetura foi mantida proporcional a um trabalho acadêmico: não há contêiner de injeção, servidor, banco de dados ou uma hierarquia de padrões de projeto. O sorteador pode ser substituído nos testes para obter resultados previsíveis. Os testes cobrem regressões importantes, sem alegar cobertura total de cenários.
