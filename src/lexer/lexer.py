from lexer.token import Token

class Lexer:
    def __init__(self) -> None:
        self.text : str = ""
        self.ptr : int = 0

    def tokenize(self, text : str) -> None:
        self.text = text
        self.ptr = 0

    def getNextToken(self) -> Token:
        pass