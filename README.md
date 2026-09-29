# Biblioteca Pessoal — projeto integrador de Python

Este projeto é uma aplicação de terminal para cadastrar e administrar livros. Ele foi pensado para ser estudado de ponta a ponta: comece executando, depois leia cada função e faça pequenas mudanças.

## Como executar

No terminal, entre nesta pasta e execute:

```powershell
python biblioteca.py
```

O arquivo `biblioteca.json` será criado automaticamente quando você sair pelo menu. Ele guarda os livros cadastrados.

## O que o sistema faz

1. Cadastra livros.
2. Lista livros e sua situação.
3. Busca por título ou autor.
4. Registra empréstimos e devoluções.
5. Exibe estatísticas.
6. Sugere aleatoriamente uma leitura disponível.
7. Salva os dados para a próxima execução.

## Mapa dos conceitos usados

|          Conceito           |                       Onde observar no código                          |
|-----------------------------|------------------------------------------------------------------------|
| Variáveis e tipos           | parâmetros, `ano`, `total`, `disponivel` e textos das mensagens        |
| Entrada e saída             | `input()` e `print()` em todo o programa                               |
| Operadores                  | cálculos, comparações e condições em `ler_ano`, `estatisticas` e menus |
| Condicionais                | regras de empréstimo, devolução e escolha do menu                      |
| `while`, `for` e `range`    | validação de entradas, menu e listagens                                |
| Strings                     | `.strip()`, `.lower()` e f-strings                                     |
| Listas                      | `self.livros`, resultados de busca e livros disponíveis                |
| Tuplas                      | `OPCOES_MENU` e o retorno de `estatisticas()`                          |
| Dicionários                 | `acoes` e os dados que são gravados no JSON                            |
| Funções                     | cada ação do menu possui uma função própria                            |
| Tratamento de erros         | `try/except ValueError` nas leituras numéricas                         |
| Módulos                     | `json`, `datetime`, `pathlib` e `random`                               |
| Arquivos                    | `with open()` nos métodos `salvar` e `carregar`                        |
| POO                         | classes `Livro` e `Biblioteca`, atributos, métodos e `__init__`        |

## Roteiro de estudo

1. Execute o programa e cadastre dois livros.
2. Empreste um deles e confirme as estatísticas.
3. Feche o programa pela opção 8 e abra novamente para confirmar que os dados foram salvos.
4. Localize a classe `Livro` e explique cada atributo com palavras próprias.
5. Localize a função `ler_ano` e force um erro digitando letras em vez de números.
6. Adicione uma nova opção ao menu: remover um livro.
7. Como desafio, registre também o gênero e uma nota de avaliação para cada livro.

## Perguntas para a apresentação do projeto

- Por que `input()` precisa de conversão para `int()` em algumas situações?
- Por que `livros` é uma lista?
- Por que cada livro é um objeto, e não apenas uma string?
- Qual é a diferença entre `print()` e `return`?
- Por que os dados continuam existindo depois que o programa termina?
- O que aconteceria se o programa não usasse `try/except` ao ler um número?
