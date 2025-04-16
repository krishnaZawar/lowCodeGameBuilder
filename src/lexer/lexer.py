from lexer.token import Token
from lexer.tokenType import TokenType

class Lexer:
    datatypes = ["integer", "string", "gameObject"]

    keyword = [
        "initGame", "endGame", "if", "else", "while", "break", "continue", "and", "or"
    ]

    functions = [
        "setBackgroundColor", "initWindow", "setWindowTitle", "GameObject", "draw" , "moveX" , "moveY" , "getX" , "getY" , "keyDown"
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

    def __init__(self):
        self.text: str = ""
        self.ptr: int = 0

    def tokenize(self, text: str):
        self.text = text
        self.ptr = 0

    def getNextToken(self) -> Token:
        curToken : Token
        while self.ptr < len(self.text) and self.text[self.ptr] in self.skippables:
            self.ptr += 1

        if self.ptr < len(self.text) and self.text[self.ptr] == '#':
            self.ptr += 1
            while self.ptr < len(self.text) and self.text[self.ptr] != '\n':
                self.ptr += 1
            self.ptr += 1

        if self.ptr >= len(self.text):
            curToken = Token("", TokenType.ENDOFFILE)
            return curToken

        if self.text[self.ptr] == ';':
            self.ptr += 1
            curToken =  Token(";", TokenType.ENDOFLINE)

        elif self.text[self.ptr] == '"':
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
            curToken = Token(value, TokenType.STRINGLITERAL)

        elif self.text[self.ptr] in self.specialCharacters:
            ch = self.text[self.ptr]
            self.ptr += 1
            curToken = Token(ch, TokenType.SPECIALCHARACTER)

        elif self.text[self.ptr] in self.openParenthesis:
            ch = self.text[self.ptr]
            self.ptr += 1
            curToken = Token(ch, TokenType.OPENPARENTHESIS)

        elif self.text[self.ptr] in self.closeParenthesis:
            ch = self.text[self.ptr]
            self.ptr += 1
            curToken = Token(ch, TokenType.CLOSEPARENTHESIS)

        elif self.text[self.ptr] in self.arithmeticOperators:
            ch = self.text[self.ptr]
            self.ptr += 1
            curToken = Token(ch, TokenType.ARITHMETICOPERATOR)

        elif self.text[self.ptr] == '=':
            self.ptr += 1
            if self.ptr < len(self.text) and self.text[self.ptr] == '=':
                self.ptr += 1
                curToken = Token("==", TokenType.RELATIONALOPERATOR)
            else:
                curToken = Token("=", TokenType.ASSIGNMENT)

        elif self.text[self.ptr] == '<' or self.text[self.ptr] == '>':
            op = self.text[self.ptr]
            self.ptr += 1
            if self.ptr < len(self.text) and self.text[self.ptr] == '=':
                op += '='
                self.ptr += 1
            curToken = Token(op, TokenType.RELATIONALOPERATOR)

        elif self.text[self.ptr] == '!':
            self.ptr += 1
            if self.ptr >= len(self.text) or self.text[self.ptr] != '=':
                raise Exception(f"Unrecognized token '!'")
            self.ptr += 1
            curToken = Token("!=", TokenType.RELATIONALOPERATOR)

        elif self.isDigit(self.text[self.ptr]):
            value = ""
            while self.ptr < len(self.text) and self.isDigit(self.text[self.ptr]):
                value += self.text[self.ptr]
                self.ptr += 1
            curToken = Token(value,TokenType.NUMERICLITERAL)

        elif self.isAlpha(self.text[self.ptr]):
            value = ""
            while self.ptr < len(self.text) and (self.isAlpha(self.text[self.ptr]) or self.isDigit(self.text[self.ptr])):
                value += self.text[self.ptr]
                self.ptr += 1
            if value in self.keyword or value in self.datatypes or value in self.functions:
                curToken = Token(value, TokenType.KEYWORD)
            else:
                curToken = Token(value, TokenType.IDENTIFIER)
        else:
            raise Exception(f"Unrecognized token {self.text[self.ptr]}")
    
        return curToken
