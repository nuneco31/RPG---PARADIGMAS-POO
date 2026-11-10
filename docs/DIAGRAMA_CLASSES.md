# Diagrama de classes

O [diagrama do núcleo no README](../README.md#diagrama-de-classes) mostra personagens, habilidades, inventário, batalha e contratos de persistência. Esta visão complementar mostra a composição e a apresentação que usam esse núcleo.

```mermaid
classDiagram
    class Campanha {
        +jogador
        +progresso
        +estado
        +acionar(acao)
    }
    class JogoTerminal {
        +executar()
        +explorar()
        +menu_inventario()
    }
    class JogoInterface {
        +executar()
        +acionar(acao)
    }
    class Batalha {
        +executar_acao(acao, habilidade, item)
        +encerrada
    }
    class BatalhaTerminal {
        +lutar(input_fn, output_fn)
    }
    class LeitorPartida {
        <<Protocol>>
        +carregar(jogador)
    }
    class GravadorPartida {
        <<Protocol>>
        +salvar(jogador, progresso)
    }
    class Salvamento {
        +caminho
        +salvar(jogador, progresso)
        +carregar(jogador)
    }
    JogoTerminal *-- Campanha
    JogoInterface *-- Campanha
    JogoInterface *-- EventosInterface
    JogoInterface *-- InterfaceRenderizador
    InterfaceRenderizador *-- Componentes
    InterfaceRenderizador *-- Ilustracoes
    InterfaceRenderizador ..> Tema
    JogoTerminal ..> BatalhaTerminal : cria no console
    Batalha <|-- BatalhaTerminal
    Campanha *-- Batalha
    Campanha --> LeitorPartida : recebe no construtor
    Campanha --> GravadorPartida : recebe no construtor
    LeitorPartida <|.. Salvamento : estrutural
    GravadorPartida <|.. Salvamento : estrutural
```

`BatalhaTerminal` é o nome usado no diagrama para distinguir `jogo.batalha_terminal.Batalha` de `jogo.batalha.Batalha`. No código, ambas se chamam `Batalha`; a primeira importa a segunda como `RegrasBatalha` e acrescenta a interação textual.

`criar_campanha`, em `jogo/montagem.py`, é uma função, portanto não aparece como classe. Ela instancia `Salvamento` e injeta a mesma instância nas portas de leitura e gravação. Nos testes, essas portas também recebem objetos diferentes.

## Inventário e configurações

```mermaid
classDiagram
    class Jogador
    class Inventario {
        -itens
        -equipamentos
        +adicionar(nome, quantidade)
        +usar(nome, jogador)
        +equipar(nome, jogador)
    }
    class Item {
        <<immutable>>
        +nome
        +tipo
        +valor
    }
    class Vocacao {
        <<immutable>>
        +nome
        +vida
        +ataque
        +defesa
        +mana
        +esquiva
        +habilidades
    }
    class Habilidade {
        <<immutable>>
        +nome
        +custo_mana
        +poder
        +tipo
        +fator_ataque
        +chance_critico
        +calcular_poder(ataque)
        +aplicar(usuario, alvo, multiplicador)
    }
    Jogador *-- Inventario
    Inventario ..> Item : consulta catalogo
    Jogador o-- Vocacao
    Vocacao o-- Habilidade
    Jogador o-- Habilidade
    Habilidade <|-- HabilidadeCura
```

`Inventario` guarda nomes e quantidades, consultando o catálogo de `Item`; não possui uma instância mutável por unidade. As configurações Guerreiro, Mago e Arqueiro são objetos `Vocacao` compartilhados e imutáveis. A composição aqui representa a relação de domínio “tem um”; a agregação com losango vazio destaca os objetos compartilhados.

Os módulos de protótipo preservados por compatibilidade não fazem parte do fluxo atual e foram omitidos. As relações representam o programa iniciado por `main.py`.
