import re

# ============================================================
# 🔹 Analisador Léxico (Lexer)
# ============================================================

def lexer(codigo: str):
    """
    Converte a string de entrada em uma lista de tokens válidos.
    """
    TOKEN_TYPES = [
        ('NUMBER',      r'\d+(\.\d+)?'),   # Inteiros ou decimais
        ('PLUS',        r'\+'),            # +
        ('MINUS',       r'-'),             # -
        ('MUL',         r'\*'),            # *
        ('DIV',         r'/'),             # /
        ('LPAREN',      r'\('),            # (
        ('RPAREN',      r'\)'),            # )
        ('WHITESPACE',  r'\s+'),           # Espaços em branco
        ('MISMATCH',    r'.'),             # Qualquer outro caractere
    ]

    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)
    tokens = []

    for mo in re.finditer(regex, codigo):
        tipo = mo.lastgroup
        valor = mo.group()

        if tipo == 'WHITESPACE':
            continue
        elif tipo == 'MISMATCH':
            raise Exception(f"❌ Erro Léxico: caractere inesperado '{valor}'")
        else:
            tokens.append((tipo, valor))

    return tokens


# ============================================================
# 🔹 Parser + Interpretador
# ============================================================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        """Olha o próximo token sem consumir."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, tipo_esperado=None):
        """Consome um token e retorna seu valor."""
        if self.pos >= len(self.tokens):
            raise Exception("❌ Erro Sintático: fim inesperado da expressão.")
        
        tipo, valor = self.tokens[self.pos]
        self.pos += 1

        if tipo_esperado and tipo != tipo_esperado:
            raise Exception(f"❌ Erro Sintático: esperado '{tipo_esperado}', mas encontrado '{valor}'.")

        return tipo, valor

    # -----------------------------
    # fator → ('+' | '-') fator | NUMBER | '(' expressao ')'
    # -----------------------------
    def fator(self):
        token = self.peek()

        if token is None:
            raise Exception("❌ Erro Sintático: expressão incompleta.")

        tipo, valor = token

        # Trata operadores unários
        if tipo in ('PLUS', 'MINUS'):
            self.eat()  # consome o operador
            fator = self.fator()
            return +fator if tipo == 'PLUS' else -fator

        # Números
        elif tipo == 'NUMBER':
            self.eat('NUMBER')
            return float(valor) if '.' in valor else int(valor)

        # Parênteses
        elif tipo == 'LPAREN':
            self.eat('LPAREN')
            expr = self.expressao()
            if not self.peek() or self.peek()[0] != 'RPAREN':
                raise Exception("❌ Erro Sintático: parêntese não fechado.")
            self.eat('RPAREN')
            return expr

        else:
            raise Exception(f"❌ Erro Sintático: token inesperado '{valor}'.")

    # -----------------------------
    # termo → fator (('*' | '/') fator)*
    # -----------------------------
    def termo(self):
        result = self.fator()
        while self.peek() and self.peek()[0] in ('MUL', 'DIV'):
            tipo, _ = self.eat()
            right = self.fator()
            if tipo == 'MUL':
                result *= right
            else:
                if right == 0:
                    raise Exception("❌ Erro: divisão por zero.")
                result /= right
        return result

    # -----------------------------
    # expressao → termo (('+' | '-') termo)*
    # -----------------------------
    def expressao(self):
        result = self.termo()
        while self.peek() and self.peek()[0] in ('PLUS', 'MINUS'):
            tipo, _ = self.eat()
            right = self.termo()
            if tipo == 'PLUS':
                result += right
            else:
                result -= right
        return result


# ============================================================
# 🔹 Função Principal (CLI)
# ============================================================
if __name__ == "__main__":
    print("=== 🧮 Mini Compilador Matemático (v2) ===")
    print("Digite expressões (ex: -3.5 + 2 * (4 - 1)) ou 'sair' para encerrar.")

    while True:
        codigo = input("\n>>> ")
        if codigo.lower() == "sair":
            print("Encerrando compilador...")
            break
        try:
            tokens = lexer(codigo)
            parser = Parser(tokens)
            resultado = parser.expressao()

            if parser.pos < len(tokens):
                sobrou = tokens[parser.pos:]
                raise Exception(f"❌ Tokens extras após a expressão: {sobrou}")

            print("✅ Resultado:", resultado)
        except Exception as e:
            print(e)


# ============================================================
# 🔹 Testes Automáticos
# ============================================================
def rodar_testes():
    casos = {
        "2+3": 5,
        "10 - 4": 6,
        "2 * 3 + 4": 10,
        "2 + 3 * 4": 14,
        "(2 + 3) * 4": 20,
        "10 / 2": 5,
        "10 / (5 - 5)": "Erro",
        "2 +": "Erro",
        "(2+3": "Erro",
        "-5 + 2": -3,
        "+5 * 2": 10,
        "3.5 + 1.5": 5.0,
        "-3.5 * 2": -7.0,
        "2 * (-3 + 4)": 2,
    }

    print("\n=== 🔍 Rodando Testes Automáticos ===")
    for expr, esperado in casos.items():
        try:
            tokens = lexer(expr)
            parser = Parser(tokens)
            resultado = parser.expressao()
            if parser.pos < len(tokens):
                raise Exception("Tokens extras.")
            ok = (resultado == esperado)
        except Exception:
            resultado = "Erro"
            ok = (esperado == "Erro")

        print(f"{expr:20} | Esperado: {esperado:6} | Obtido: {resultado:6} | {'✅ OK' if ok else '❌ Falhou'}")

# Descomente abaixo para testar diretamente:
# rodar_testes()
