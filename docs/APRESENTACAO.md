# Roteiro para apresentar o projeto

Use este roteiro como apoio e adapte a duração ao tempo da disciplina. Antes da apresentação, instale as dependências, rode os testes e confira a janela no computador que será usado.

## Demonstração sugerida: 6 a 8 minutos

| Tempo aproximado | Mostrar | Explicar |
| --- | --- | --- |
| 1 minuto | Tela inicial e Caderno POO | Objetivo acadêmico e visão geral da aventura. |
| 1 minuto | Inventário, equipamento e atributos | O jogador possui um inventário; equipar altera atributos com regras próprias. |
| 2 minutos | Exploração e uma batalha | A interface envia comandos; campanha e batalha decidem o resultado. |
| 2 minutos | `Personagem`, `Inimigo` e `acao_turno` | Abstração, herança, encapsulamento e polimorfismo em código real. |
| 1 minuto | `Campanha` e testes | Regras independentes de Pygame, sorteador previsível e transições verificadas. |
| 1 minuto | Salvar/carregar ou modo terminal | A mesma lógica pode ser apresentada de duas maneiras. |

Não dependa de encontrar um inimigo específico ao acaso durante a fala. Use `--seed 7` e repita as mesmas escolhas para reproduzir os sorteios. Tenha o arquivo de código correspondente aberto para mostrar o comportamento do Mago e do Chefe. Não altere resultados ou atributos ao vivo sem explicar que se trata de preparação da demonstração.

## Uma explicação curta para começar

> Crônicas da Floresta é um RPG em turnos usado para demonstrar POO. O jogador explora, organiza itens e enfrenta inimigos com comportamentos diferentes. Separamos as regras das interfaces para jogar tanto em uma janela quanto pelo terminal e testar a campanha sem abrir a parte gráfica.

## Perguntas que o código ajuda a responder

**Onde está o polimorfismo?** Na chamada `inimigo.acao_turno(jogador)`. A batalha usa o contrato comum; a classe concreta determina o comportamento. Ter subclasses, por si só, não é toda a demonstração: mostre também a chamada compartilhada.

**Por que usar uma classe abstrata?** Ela representa as regras comuns e exige uma ação de turno. Criar um personagem incompleto diretamente deixa de fazer sentido.

**O que protege a vida do personagem?** A propriedade `vida` restringe o valor. Explique que atributos com `_` são protegidos por convenção em Python, sem prometer privacidade absoluta.

**Por que composição no inventário?** Um jogador tem uma mochila; ele não é uma mochila. O inventário controla quantidade e equipamentos enquanto o jogador controla experiência e combate.

**O terminal e a janela são jogos diferentes?** São duas interfaces para o mesmo núcleo. Entrada e saída mudam; personagens, batalha, progresso e persistência são compartilhados.

**Onde aparecem outros paradigmas?** Os ciclos e condicionais são imperativos; os catálogos de itens e habilidades usam dados imutáveis. O projeto permanece principalmente orientado a objetos.

**Como demonstrar testes úteis?** Mostre que escolher uma ação inválida não consome o turno, vencer não concede XP duas vezes e carregar um arquivo inválido não modifica parcialmente o personagem. Esses testes descrevem comportamentos observáveis.

## Comandos de apoio

```powershell
python main.py --seed 7
python main.py --terminal --seed 7
python -m unittest discover -s tests -v
```

Se estiver usando um ambiente virtual sem ativá-lo, substitua `python` por `.\.venv\Scripts\python.exe`.

## O que reconhecer na conclusão

O projeto demonstra uma pequena campanha, com interfaces gráfica e textual, e uma separação de responsabilidades adequada ao seu tamanho. O salvamento é local e cobre o estado entre encontros. A arte é procedural e a experiência ainda pode evoluir com novas missões, acessibilidade e balanceamento. Evite alegar “100% de cobertura”, perfeição ou originalidade absoluta; apresente as escolhas que consegue justificar no código.
