# Roteiro de apresentação

Priorize o console, como pede o trabalho. Reserve a interface gráfica para uma demonstração extra. Execute os testes antes da apresentação e leia os trechos indicados para conseguir explicar as decisões.

## Demonstração de 6 a 8 minutos

| Tempo | Mostrar | Explicar |
| --- | --- | --- |
| 1 min | `python main.py`, escolha de classe e nome | Guerreiro, Mago e Arqueiro usam composição com `Vocacao`. |
| 1 min | Inventário: equipar espada e consultar status | Encapsulamento de quantidades; composição e bônus de equipamento. |
| 2 min | Combate no console, habilidade, resposta inimiga e vitória | Motor de turnos compartilhado, mana, dano e XP. |
| 2 min | `Personagem`, `HabilidadeCura` e protocolos | Herança, polimorfismo e exemplos de SOLID. |
| 1 min | Diagrama e `jogo/montagem.py` | Relações entre classes e injeção do adaptador JSON. |
| 1 min | Testes e salvar/carregar | Evidências de extensão, substituição, segregação e persistência segura. |

## Combate reproduzível

Execute:

```sh
python main.py --classe mago --nome Lia --seed 7
```

Escolha `1` (explorar), `2` (floresta), `2` (habilidade), `Enter` (Bola de Fogo) e `1` (ataque). O Mago enfrenta um Goblin: a magia gasta mana, o inimigo responde e a vitória concede 30 XP. Use `5` para salvar, `6` para carregar e `7` para sair.

A semente controla o sorteio, mas as escolhas também influenciam a sequência. Não é preciso alterar atributos ou simular uma vitória para fazer essa demonstração.

## Onde mostrar SOLID

- **SRP:** compare `Batalha.executar_acao`, `JogoTerminal.executar` e `Salvamento.salvar`. Regras, apresentação e armazenamento têm responsabilidades distintas.
- **OCP:** mostre `Jogador.aplicar_habilidade` delegando a `Habilidade.aplicar`. O teste de Dreno adiciona um comportamento sem editar o motor.
- **LSP:** explique a chamada `inimigo.acao_turno(jogador)`. Mago e Chefe mudam a ação e preservam o retorno de dano real e os limites de vida.
- **ISP:** mostre os protocolos separados de um método cada. No teste, um objeto somente lê e outro somente grava.
- **DIP:** `Campanha` recebe as duas portas no construtor; `criar_campanha` escolhe `Salvamento`. A regra de jogo não importa o adaptador JSON.

## Perguntas para preparar

**Por que Guerreiro, Mago e Arqueiro não são subclasses?** As diferenças atuais são atributos e habilidades, representadas por uma vocação imutável. Composição evita repetir métodos. Herança continua presente nos personagens, inimigos e habilidades.

**Onde está o polimorfismo de fato?** Nas chamadas a `acao_turno` e `aplicar`. Não basta ter subclasses: o chamador precisa usar o mesmo contrato com comportamentos diferentes.

**O que significa o prefixo `_`?** Acesso não público por convenção em Python. Os limites de vida e mana são aplicados pelas propriedades; não se trata de privacidade absoluta.

**Protocol garante os tipos em execução?** Não. É um contrato estrutural para documentação e análise estática. Os testes verificam o comportamento dos adaptadores.

**Por que a imagem do console é um registro renderizado?** O script executa o programa e converte sua saída real em PNG. Os arquivos TXT completos e o roteiro permitem reproduzir a sessão. Não são capturas da janela do sistema.

**O save antigo ainda funciona?** Sim. A versão 1 sem classe usa Aventureiro; a versão 2 guarda a classe escolhida. Dados inválidos são recusados antes de alterar a partida ativa.

## Comandos de apoio

```sh
python main.py
python main.py --classe mago --nome Lia --seed 7
python -m unittest discover -s tests -p test_solid_e_classes.py -v
python -m unittest discover -s tests -v
python main.py --grafico --classe arqueiro
```

A suíte completa e o modo gráfico precisam de `pygame-ce`; o console e os testes específicos de classes/SOLID usam a biblioteca padrão. Consulte o README para instalar a dependência opcional.

O escopo é uma campanha curta com armazenamento local. Balanceamento, missões e arte podem evoluir. Os testes cobrem comportamentos concretos, sem prometer cobertura total.
