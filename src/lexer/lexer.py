from lexer.token import Token

class Lexer:
    datatypes = ["integer", "real", "boolean", "string", "gameObject"]

    keyword = [
            "initGame",
            "endGame",
            "if",
            "else", 
            "while",
            "break",
            "continue",
            "setBackgroudColor",
            "initWindow",
            "setWindowTitle",
            "show",
            "setWindowSize"
    ]
    
    arithmeticOperators = [
        '+', '-', '/', '*', '%' 
    ]
    
    openParenthesis = [
        '(', '{'
    ]

    closeParenthesis = [
        ')', '}'
    ]

    specialCharacters = [
        ','
    ]

    skippables = [
        '\n', ' ', '\t'
    ]          
            

    def __init__(self) -> None:
        self.text : str = ""
        self.ptr : int = 0


    def tokenize(self, text : str) -> None:
        self.text = text
        self.ptr = 0

    def getNextToken(self) -> Token:
        curToken : Token

        if value in self.dataTypes:
            pass
        