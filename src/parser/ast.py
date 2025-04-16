from lexer.token import Token

class AST:
    def __init__(self, token : Token = Token()) -> None:
        self.token : Token = token
        self.children : list['AST'] = []