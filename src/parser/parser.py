from lexer.lexer import Lexer
from lexer.token import Token
from lexer.tokenType import TokenType
from parser.ast import AST
class Parser:
    def __init__(self) -> None:
        self.lexer : Lexer = Lexer()
        self.curToken : Token | None = None

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
        
    def parseFunction(self) -> AST:
        root : AST = AST(self.curToken)

        self.eat(TokenType.KEYWORD)

        self.parseParenthesis("(")
        
        if self.curTokenValue(")"):
            self.parseParenthesis(")")
            return root
        
        root.children.append(self.parseArithmeticExpression())
        while self.curTokenValue(","):
            self.eat(TokenType.SPECIALCHARACTER)
            root.children.append(self.parseArithmeticExpression())
        self.parseParenthesis(")")

        return root

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
            root.children.append(AST(Token("0", TokenType.NUMERICLITERAL)))
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
        if self.peek(TokenType.RELATIONALOPERATOR):
            root = AST(self.curToken)
            self.eat(TokenType.RELATIONALOPERATOR)
        else:
            raise Exception('relational operator  token not recognised')
    
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

# -------------------------------------------------------------------parse while loop---------------------------------------------------
    def parseWhileLoop(self) -> AST: 
        root : AST = AST(self.curToken)

        self.eat(TokenType.KEYWORD)

        self.parseParenthesis("(")
        root.children.append(self.parseBooleanExpression())
        self.parseParenthesis(")")

        self.parseParenthesis("{")
        root.children.append(self.parseStatementList(Token("}", TokenType.CLOSEPARENTHESIS)))
        self.parseParenthesis("}")

        return root

    def parseBreak(self) -> AST:
        root : AST = AST(self.curToken)

        self.eat(TokenType.KEYWORD)
        self.eat(TokenType.ENDOFLINE)

        return root
    
    def parseContinue(self) -> AST:
        root : AST = AST(self.curToken)

        self.eat(TokenType.KEYWORD)
        self.eat(TokenType.ENDOFLINE)

        return root
    
# -------------------------------------------------------------------parse program---------------------------------------------------

    def parseStatement(self) -> AST:
        root : AST | None = AST()
        # assignment
        if self.curTokenValueIn(self.lexer.datatypes) or self.peek(TokenType.IDENTIFIER):
            root = self.parseAssignmentStatement()

        elif self.curTokenValue("if"):
            root = self.parseIfElseIfBlock()

        elif self.curTokenValue("break"):
            root = self.parseBreak()

        elif self.curTokenValue("continue"):
            root = self.parseContinue()

        elif self.curTokenValue("while"):
            root = self.parseWhileLoop()

        elif self.curTokenValueIn(self.lexer.functions):
            root = self.parseFunction()

        return root

    def parseStatementList(self, endToken : Token) -> AST:
        root : AST | None = AST()
        while not self.curToken.equals(endToken):
            root.children.append(self.parseStatement())
        return root

    def parse(self, text : str) -> AST:
        self.lexer.tokenize(text)

        ast : AST = AST()

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