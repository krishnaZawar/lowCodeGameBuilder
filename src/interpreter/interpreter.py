from parser.parser import Parser
from parser.ast import AST
from lexer.tokenType import TokenType

class Interpreter:
    def __init__(self) -> None:
        self.parser = Parser()

        self.variableMap = {}

# -------------------------------------------arithmetic expressions------------------------------------------------
    def evaluateArithmeticOperatorNode(self, root : AST) -> int:
        left = root.children[0]
        right = root.children[1]

        leftVal : int
        rightVal : int

        if left.token.type == TokenType.ARITHMETICOPERATOR:
            leftVal = self.evaluateArithmeticOperatorNode(left)
        elif left.token.type == TokenType.NUMERICLITERAL:
            leftVal = int(left.token.value)
        elif left.token.type == TokenType.IDENTIFIER:
            if not left.token.value in self.variableMap:
                raise Exception("undefined variable used")
            if self.variableMap[left.token.value][0] != "integer":
                raise Exception("Expected integer")
            leftVal = self.variableMap[left.token.value][1]
        else:
            raise Exception("expected a numeric value")
        
        if right.token.type == TokenType.ARITHMETICOPERATOR:
            rightVal = self.evaluateArithmeticOperatorNode(right)
        elif right.token.type == TokenType.NUMERICLITERAL:
            rightVal = int(right.token.value)
        elif right.token.type == TokenType.IDENTIFIER:
            if not right.token.value in self.variableMap:
                raise Exception("undefined variable used")
            if self.variableMap[right.token.value][0] != "integer":
                raise Exception("Expected integer")
            rightVal = self.variableMap[right.token.value][1]
        else:
            raise Exception("expected a numeric value")
        
        return int(eval(f"{leftVal} {root.token.value} {rightVal}"))
        
        
    def evaluateArithmeticExpression(self, root : AST) -> int:
        if root.token.type == TokenType.ARITHMETICOPERATOR:
            return self.evaluateArithmeticOperatorNode(root)
        
        elif root.token.type == TokenType.NUMERICLITERAL:
            return int(root.token.value)
        elif root.token.type == TokenType.IDENTIFIER:
            if not root.token.value in self.variableMap:
                raise Exception("undefined variable used")
            if self.variableMap[root.token.value][0] != "integer":
                raise Exception("Expected integer")
            return self.variableMap[root.token.value][1]    
        raise Exception("expected a numeric value")
    
# ---------------------------------------------string expression--------------------------------------------------
    def evaluateStringOperatorNode(self, root : AST) -> str:
        if root.token.value != "+":
            raise Exception("invalid string operation")

        left = root.children[0]
        right = root.children[1]

        leftVal : str = ""
        rightVal : str = ""

        if left.token.type == TokenType.ARITHMETICOPERATOR:
            leftVal = self.evaluateStringOperatorNode(left)
        elif left.token.type == TokenType.STRINGLITERAL:
            leftVal = left.token.value
        elif left.token.type == TokenType.IDENTIFIER:
            if not left.token.value in self.variableMap:
                raise Exception("undefined variable used")
            if self.variableMap[left.token.value][0] != "string":
                raise Exception("Expected string")
            leftVal = self.variableMap[left.token.value][1]
        else:
            raise Exception("expected a string value")
        
        if right.token.type == TokenType.ARITHMETICOPERATOR:
            rightVal = self.evaluateStringOperatorNode(right)
        elif right.token.type == TokenType.STRINGLITERAL:
            rightVal = right.token.value
        elif right.token.type == TokenType.IDENTIFIER:
            if not right.token.value in self.variableMap:
                raise Exception("undefined variable used")
            if self.variableMap[right.token.value][0] != "string":
                raise Exception("Expected string")
            rightVal = self.variableMap[right.token.value][1]
        else:
            raise Exception("expected a string value")
        
        return leftVal + rightVal

    def evaluateStringExpression(self, root : AST) -> None:
        if root.token.type == TokenType.ARITHMETICOPERATOR:
            return self.evaluateStringOperatorNode(root)
        elif root.token.type == TokenType.STRINGLITERAL:
            return root.token.value
        elif root.token.type == TokenType.IDENTIFIER:
            if not root.token.value in self.variableMap:
                raise Exception("undefined variable used")
            if self.variableMap[root.token.value][0] != "string":
                raise Exception("Expected string")
            return self.variableMap[root.token.value][1]
        raise Exception("expected a string value")

# --------------------------------------------assignment statement-------------------------------------------------

    def interpretAssignmentStatement(self, root : AST) -> None:
        if len(root.children) == 3:
            datatype = root.children[0].token.value
            variable = root.children[1].token.value

            if variable in self.variableMap:
                raise Exception("variable exists")
            if datatype == "integer":
                value = self.evaluateArithmeticExpression(root.children[2])
            elif datatype == "string":
                value = self.evaluateStringExpression(root.children[2])

            self.variableMap[variable] = [datatype, value]
        
        else:
            variable = root.children[0].token.value

            if not variable in self.variableMap:
                raise Exception("undeclared variable used")
            
            if self.variableMap[variable][0] == "integer":
                value = self.evaluateArithmeticExpression(root.children[1])
            elif self.variableMap[variable][0] == "string":
                value = self.evaluateStringExpression(root.children[1])

            self.variableMap[variable][1] = value

# ---------------------------------------------------program---------------------------------------------------
    def interpretStatement(self, root : AST) -> None:
        if root.token.type == TokenType.ASSIGNMENT:
            self.interpretAssignmentStatement(root)

    def interpretStatementList(self, root : AST) -> None:
        for child in root.children:
            self.interpretStatement(child)

    def interpret(self, text : str) -> None:
        ast : AST  = self.parser.parse(text)

        self.interpretStatementList(ast)