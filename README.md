Projeto de Mini-Compilador para Expressões MatemáticasEste repositório contém o código-fonte de um mini-compilador/interpretador desenvolvido como projeto acadêmico para a disciplina de Compiladores e Computabilidade - Ex: Teoria da Computação/Compiladores.
O compilador é capaz de analisar e calcular o resultado de expressões aritméticas que envolvem números inteiros, os quatro operadores básicos (+, -, *, /) e parênteses.
1. Arquitetura
O mini-compilador é implementado em Python e segue uma arquitetura tradicional de front-end de compilador, com a etapa de interpretação acoplada à análise sintática:

Analisador Léxico (lexer):Quebra a expressão de entrada em tokens (números, operadores, parênteses).
Analisador Sintático/Interpretador (Parser): Utiliza um Analisador Descendente Recursivo para impor a gramática e a precedência de operadores, calculando o resultado da expressão em tempo real.

2. Requisitos
Para executar o mini-compilador, você precisa apenas ter o Python 3.x instalado.
Linguagem: Python 3.x
Dependências: Nenhuma biblioteca externa necessária (apenas a biblioteca padrão re).

3. Como Executar
3.1. Execução Interativa (CLI)
Para rodar o interpretador em modo interativo (linha de comando):
Salve o código-fonte em um arquivo (ex: mini_compiler.py).
Execute o script no seu terminal:

Bash
python mini_compiler.py

O programa entrará em um loop de comandos. Digite suas expressões ou sair para encerrar.Exemplo de Sessão:

=== Mini Compilador de Expressões Matemáticas ===
Digite expressões (ex: 2 + 3 * (4 - 1)) ou 'sair' para encerrar.

>>> 5 * (2 + 3) - 1
Resultado: 24

>>> 10 / (5 - 5)
⚠️ Erro: Erro: divisão por zero

>>> 2 + 3 * 4
Resultado: 14

>>> 1.5 + 2.2
Resultado: 3.7

>>> -3 + 2
Resultado: -1

>>> sair
Encerrando compilador...

3.2. Execução de Testes Automatizados

O código-fonte inclui uma função rodar_testes() que valida o comportamento do analisador em casos de precedência, parênteses e erros conhecidos.

Para rodar os testes, localize a última linha do arquivo e descomente a chamada à função:

Python
# -----------------------------
# Testes Automáticos
# -----------------------------
# ... (código da função rodar_testes) ...

# Descomente a linha abaixo para rodar os testes direto:
rodar_testes() 

Resultado Esperado dos Testes:Ao executar o arquivo com a função de testes descomentada, o output será:=== Rodando Testes Automáticos ===

Teste: 2+3        | Esperado: 5 | Obtido: 5 | ✅ OK
Teste: 10 - 4     | Esperado: 6 | Obtido: 6 | ✅ OK
Teste: 2 * 3 + 4  | Esperado: 10 | Obtido: 10 | ✅ OK
Teste: 2 + 3 * 4  | Esperado: 14 | Obtido: 14 | ✅ OK
Teste: (2 + 3) * 4 | Esperado: 20 | Obtido: 20 | ✅ OK
Teste: 10 / 2     | Esperado: 5 | Obtido: 5.0 | ✅ OK
Teste: 10 / (5 - 5) | Esperado: Erro | Obtido: Erro | ✅ OK
Teste: 2 +        | Esperado: Erro | Obtido: Erro | ✅ OK
Teste: (2+3       | Esperado: Erro | Obtido: Erro | ✅ OK

# Um teste adicional de erro léxico pode ser incluído, como '2a + 3'

4. Tratamento de ErrosO compilador trata três classes principais de erros, garantindo a robustez do analisador:

Classe de Erro Exemplo de Erro Tipo de Exceção
Erro Léxico 2a + 3 (Erro Léxico: Caractere inesperado 'a')
Erro Sintático (2 + 3Esperado ')' mas encontrado 'Fim inesperado da expressão'
Erro Semântico 10/0 Erro: divisão por zero

