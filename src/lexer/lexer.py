from lexer.token import Token
from lexer.tokenType import TokenType

class Lexer:
    def __init__(self):
        self.text: str = ""
        self.ptr: int = 0

    datatypes = ["integer", "real", "boolean", "string", "gameObject"]

    keyword = [
        "initGame", "endGame", "if", "else", "while", "break", "continue",
        "setBackgroudColor", "initWindow", "setWindowTitle", "show", "setWindowSize"
    ]

    arithmeticOperators = ['+', '-', '/', '*', '%']
    openParenthesis = ['(', '{']
    closeParenthesis = [')', '}']
    specialCharacters = [',']
    skippables = ['\n', ' ', '\t']
    escape_map = {'n': '\n', 't': '\t', '\\': '\\', '"': '"'}

    def isDigit(self, char) -> bool:
        return char.isdigit()

    def isAlpha(self, char) -> bool:
        return char.isalpha()

    def tokenize(self, text: str):
        self.text = text
        self.ptr = 0

    def getNextToken(self) -> Token:
        while self.ptr < len(self.text) and self.text[self.ptr] in self.skippables:
            self.ptr += 1

        if self.ptr < len(self.text) and self.text[self.ptr] == '#':
            self.ptr += 1
            while self.ptr < len(self.text) and self.text[self.ptr] != '\n':
                self.ptr += 1
            self.ptr += 1

        if self.ptr >= len(self.text):
            return Token("", TokenType.ENDOFFILE)

        if self.text[self.ptr] == ';':
            self.ptr += 1
            return Token(";", TokenType.ENDOFLINE)

        if self.text[self.ptr] == '"':
            self.ptr += 1
            value = ""
            buffer = False
            while self.ptr < len(self.text) and (buffer or self.text[self.ptr] != '"'):
                if buffer:
                    if self.text[self.ptr] in self.escape_map:
                        value += self.escape_map[self.text[self.ptr]]
                        buffer = False
                    else:
                        raise Exception(f"Unrecognized escape sequence \\{self.text[self.ptr]}")
                else:
                    if self.text[self.ptr] == '\\':
                        buffer = True
                    else:
                        value += self.text[self.ptr]
                self.ptr += 1
            if buffer or (self.ptr >= len(self.text) or self.text[self.ptr] != '"'):
                raise Exception(f"Expected closing quote!")
            self.ptr += 1
            return Token(value, TokenType.STRINGLITERAL)

        if self.text[self.ptr] in self.specialCharacters:
            ch = self.text[self.ptr]
            self.ptr += 1
            return Token(ch, TokenType.SPECIALCHARACTER)

        if self.text[self.ptr] in self.openParenthesis:
            ch = self.text[self.ptr]
            self.ptr += 1
            return Token(ch, TokenType.OPENPARENTHESIS)

        if self.text[self.ptr] in self.closeParenthesis:
            ch = self.text[self.ptr]
            self.ptr += 1
            return Token(ch, TokenType.CLOSEPARENTHESIS)

        if self.text[self.ptr] in self.arithmeticOperators:
            ch = self.text[self.ptr]
            self.ptr += 1
            return Token(ch, TokenType.ARITHMETICOPERATOR)

        if self.text[self.ptr] == '=':
            self.ptr += 1
            if self.ptr < len(self.text) and self.text[self.ptr] == '=':
                self.ptr += 1
                return Token("==", TokenType.RELATIONALOPERATOR)
            return Token("=", TokenType.ASSIGNMENT)

        if self.text[self.ptr] in ['<', '>']:
            op = self.text[self.ptr]
            self.ptr += 1
            if self.ptr < len(self.text) and self.text[self.ptr] == '=':
                op += '='
                self.ptr += 1
            return Token(op, TokenType.RELATIONALOPERATOR)

        if self.text[self.ptr] == '!':
            self.ptr += 1
            if self.ptr >= len(self.text) or self.text[self.ptr] != '=':
                raise Exception(f"Unrecognized token '!'")
            self.ptr += 1
            return Token("!=", TokenType.RELATIONALOPERATOR)

        if self.isDigit(self.text[self.ptr]):
            value = ""
            while self.ptr < len(self.text) and self.isDigit(self.text[self.ptr]):
                value += self.text[self.ptr]
                self.ptr += 1
            return Token(value,TokenType.NUMERICLITERAL)

        if self.isAlpha(self.text[self.ptr]):
            value = ""
            while self.ptr < len(self.text) and (self.isAlpha(self.text[self.ptr]) or self.isDigit(self.text[self.ptr])):
                value += self.text[self.ptr]
                self.ptr += 1
            if value in self.keyword:
                return Token(value, TokenType.KEYWORD)
            elif value in self.datatypes:
                return Token(value, TokenType.KEYWORD)
            else:
                return Token(value, TokenType.IDENTIFIER)

        raise Exception(f"Unrecognized token {self.text[self.ptr]}")
