from lexer.token import Token

class AST:
    def __init__(self, token : Token = None) -> None:
        self.token : Token | None = token
        self.children : list['AST'] = []