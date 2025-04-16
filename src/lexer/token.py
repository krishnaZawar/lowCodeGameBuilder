from src.lexer.tokenType import TokenType
class Token:
    def __init__(self, type : TokenType, value : str) -> None:
        self.type : TokenType= type
        self.value : str = value

    def equals(self, token : 'Token') -> bool:
        return self.type == token.type and self.value == token.value