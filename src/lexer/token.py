from lexer.tokenType import TokenType
class Token:
    def __init__(self, value : str = "", type : TokenType = None) -> None:
        self.type : TokenType= type
        self.value : str = value

    def equals(self, token : 'Token') -> bool:
        return self.type == token.type and self.value == token.value