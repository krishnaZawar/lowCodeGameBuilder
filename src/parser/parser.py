from lexer.lexer import Lexer
from lexer.token import Token
from lexer.tokenType import TokenType
from parser.ast import AST
class Parser:
# ------------------------------------------------------------------generics--------------------------------------------------------
    def eat(self, type : TokenType) -> None:
        if self.peek(type):
            self.curToken = self.lexer.getNextToken()
        else:
            raise Exception("parsing error")

    def curTokenValue(self, value : str) -> bool:
        return value == self.curToken.value
    
    def curTokenValueIn(self, values : list[str]) -> bool:
        return self.curToken.value in values
    
    def peek(self, type : TokenType) -> bool:
        return self.curToken.type == type

    def parseParenthesis(self, value : str) -> None:
        if self.curToken.value == value:
            self.eat(self.curToken.type)
        else:
            raise Exception("parsing error")

    def __init__(self) -> None:
        self.lexer : Lexer = Lexer()
        self.curToken : Token | None = None

# -------------------------------------------------------------------parse arithmetic expression------------------------------------
    def parseArithmeticSubExpr(self) -> AST:
        root : AST | None
        if self.curTokenValue("("):
            self.parseParenthesis("(")
            root = self.parseAddSubExpr()
            self.parseParenthesis(")")
        elif self.curTokenValue("-"):
            root = AST(self.curToken)
            self.eat(TokenType.ARITHMETICOPERATOR)
            root.children.append(Token("0", TokenType.NUMERICLITERAL))
            root.children.append(self.parseArithmeticSubExpr())
        elif self.peek(TokenType.IDENTIFIER) or self.peek(TokenType.NUMERICLITERAL) or self.peek(TokenType.STRINGLITERAL):
            root = AST(self.curToken)
            self.eat(self.curToken.type)
        else:
            raise Exception("parsing error")
        
        return root

    def parseMulDivModExpr(self) -> AST:
        root = self.parseArithmeticSubExpr()

        while self.curTokenValueIn(["*", "/", "%"]):
            newRoot = AST(self.curToken)
            self.eat(TokenType.ARITHMETICOPERATOR)
            newRoot.children.append(root)
            newRoot.children.append(self.parseMulDivModExpr())
            root = newRoot

        return root
    
    def parseAddSubExpr(self) -> AST:
        root = self.parseMulDivModExpr()

        while self.curTokenValueIn(["+", "-"]):
            newRoot = AST(self.curToken)
            self.eat(TokenType.ARITHMETICOPERATOR)
            newRoot.children.append(root)
            newRoot.children.append(self.parseAddSubExpr())
            root = newRoot

        return root

    def parseArithmeticExpression(self) -> AST:
        return self.parseAddSubExpr()
    
# -------------------------------------------------------------------parse boolean expressions-------------------------------------
    def parseBooleanSubExpr(self) -> AST:
        root : AST | None = None
        if self.curTokenValue("("):
            self.parseParenthesis("(")
            root = self.parseOrExpr()
            self.parseParenthesis(")")
            return root
        left = self.parseArithmeticExpression()
        if self.curTokenValueIn(["and", "or"]):
            root = AST(self.curToken)
            self.eat(TokenType.KEYWORD)
        right = self.parseArithmeticExpression()

        root.children.append(left)
        root.children.append(right)

        return root
    
    def parseAndExpr(self) -> AST:
        root = self.parseBooleanSubExpr()

        while self.curTokenValue("and"):
            newRoot = AST(self.curToken)
            self.eat(TokenType.KEYWORD)
            newRoot.children.append(root)
            newRoot.children.append(self.parseAndExpr())
            root = newRoot

        return root
    
    def parseOrExpr(self) -> AST:
        root = self.parseAndExpr()

        while self.curTokenValue("or"):
            newRoot = AST(self.curToken)
            self.eat(TokenType.KEYWORD)
            newRoot.children.append(root)
            newRoot.children.append(self.parseOrExpr())
            root = newRoot

        return root

    def parseBooleanExpression(self) -> AST:
        return self.parseOrExpr()

# -------------------------------------------------------------------parse assignment statement-------------------------------------

    def parseAssignmentStatement(self) -> AST:
        root : AST = AST()
        if self.peek(TokenType.KEYWORD):
            root.children.append(AST(self.curToken))
            self.eat(TokenType.KEYWORD)
            
        root.children.append(AST(self.curToken))
        self.eat(TokenType.IDENTIFIER)

        root.token = self.curToken
        self.eat(TokenType.ASSIGNMENT)

        root.children.append(self.parseArithmeticExpression())

        self.eat(TokenType.ENDOFLINE)

        return root
    
# ----------------------------------------------------------------parse if else if block---------------------------------------------

    def parseIfElseIfBlock(self) -> AST:
        root : AST = AST(self.curToken)

        self.eat(TokenType.KEYWORD)

        self.parseParenthesis("(")
        root.children.append(self.parseBooleanExpression())
        self.parseParenthesis(")")

        self.parseParenthesis("{")
        root.children.append(self.parseStatementList(Token("}", TokenType.CLOSEPARENTHESIS)))
        self.parseParenthesis("}")

        if self.curTokenValue("else"):
            self.eat(TokenType.KEYWORD)
            if self.curTokenValue("if"):
                root.children.append(self.parseIfElseIfBlock())
            else:
                self.parseParenthesis("{")
                root.children.append(self.parseStatementList(Token("}", TokenType.CLOSEPARENTHESIS)))
                self.parseParenthesis("}")

        return root

            
    
# -------------------------------------------------------------------parse program---------------------------------------------------

    def parseStatement(self) -> AST:
        root : AST | None = None
        # assignment
        if self.curTokenValueIn(self.lexer.datatypes) or self.peek(TokenType.IDENTIFIER):
            root = self.parseAssignmentStatement()

        return root

    def parseStatementList(self, endToken : Token) -> AST:
        root : AST | None = AST()
        while not self.curToken.equals(endToken):
            root.children.append(self.parseStatement())
        return root

    def parse(self, text : str) -> AST:
        self.lexer.tokenize(text)

        ast : AST = None

        self.curToken = self.lexer.getNextToken()

        if not self.curTokenValue("initGame"):
            raise Exception("parsing error")
        
        self.eat(TokenType.KEYWORD)
        self.eat(TokenType.ENDOFLINE)

        ast = self.parseStatementList(Token("endGame", TokenType.KEYWORD))

        if not self.curTokenValue("endGame"):
            raise Exception("parsing error")
        
        
        self.eat(TokenType.KEYWORD)
        self.eat(TokenType.ENDOFLINE)

        if not self.peek(TokenType.ENDOFFILE):
            raise Exception("parsing error")

        return ast