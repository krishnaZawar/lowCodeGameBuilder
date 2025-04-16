from parser.parser import Parser
from parser.ast import AST
from lexer.tokenType import TokenType
from interpreter.loopControl import LoopControl
import pygame

pygame.init()

class Interpreter:
    def __init__(self) -> None:
        self.parser = Parser()

        self.variableMap = {}
        
        self.window = None
        self.isWindowRunning = False
        
    
    def isArithmeticExpression(self,root : AST) -> bool:
        if root.token.type == TokenType.NUMERICLITERAL:
            return True
        if root.token.type == TokenType.STRINGLITERAL:
            return False
        if root.token.type == TokenType.IDENTIFIER:
            variable = root.token.value
            if not variable in self.variableMap:
                raise Exception('Undeclared variable is used!')             
            return True if self.variableMap[variable][0] == "integer" else False
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

# --------------------------------------------Boolean expression-------------------------------------------------
    def evaluateBooleanCondition(self, root: AST) -> bool:
        leftExpr = root.children[0]
        rightExpr = root.children[1]

        isLeftArithmetic = self.isArithmeticExpression(leftExpr)
        isRightArithmetic = self.isArithmeticExpression(rightExpr)

        if isLeftArithmetic != isRightArithmetic:
            self.throwTypeError("Values of different datatypes cannot be compared", root.token.line)

        if isLeftArithmetic:
            leftVal = self.evaluateArithmeticExpression(leftExpr)
            rightVal = self.evaluateArithmeticExpression(rightExpr)
        else:
            leftVal = str(self.evaluateStringExpression(leftExpr))
            rightVal = str(self.evaluateStringExpression(rightExpr))

        op = root.token.value
        if op == ">":
            return leftVal > rightVal
        elif op == "<":
            return leftVal < rightVal
        elif op == ">=":
            return leftVal >= rightVal
        elif op == "<=":
            return leftVal <= rightVal
        elif op == "!=":
            return leftVal != rightVal
        else:  # assumes '=='
            return leftVal == rightVal



    def evaluateBooleanOperator(self, root: AST) -> bool:
        leftExpr = root.children[0]
        rightExpr = root.children[1]

        # Evaluate left side
        if leftExpr.token.type == TokenType.RELATIONALOPERATOR:
            leftVal = self.evaluateBooleanCondition(leftExpr)
        else:
            leftVal = self.evaluateBooleanOperator(leftExpr)

        # Evaluate right side
        if rightExpr.token.type == TokenType.RELATIONALOPERATOR:
            rightVal = self.evaluateBooleanCondition(rightExpr)
        else:
            rightVal = self.evaluateBooleanOperator(rightExpr)

        return (leftVal and rightVal) if root.token.value == "and" else (leftVal or rightVal)


    def evaluateBooleanExpression(self, root: AST) -> bool:
        if root.token.type == TokenType.RELATIONALOPERATOR:
            return self.evaluateBooleanCondition(root)
        return self.evaluateBooleanOperator(root)

# ---------------------------------------------gameobject----------------------------------------------------------
    def interpretGameObjectCall(self, root : AST) -> list:
        if len(root.children) != 7:
            raise Exception("GameObject expects four arguments: x, y, width and height, r, g, b")
        
        x = self.evaluateArithmeticExpression(root.children[0])
        y = self.evaluateArithmeticExpression(root.children[1])
        w = self.evaluateArithmeticExpression(root.children[2])
        h = self.evaluateArithmeticExpression(root.children[3])
        r = self.evaluateArithmeticExpression(root.children[4])
        g = self.evaluateArithmeticExpression(root.children[5])
        b = self.evaluateArithmeticExpression(root.children[6])

        return [[x, y, w, h], [r, g, b]]
    
    def draw(self, root : AST) -> None:
        if len(root.children) != 1:
            raise Exception("draw expects one argument: gameObject")
        
        variable = root.children[0].token.value

        if not variable in self.variableMap:
            raise Exception("undeclared variable used")
        
        if self.variableMap[variable][0] != "gameObject":
            raise Exception("Draw expects gameObject parameter")
        
        if self.window:
            color, dimensions = self.variableMap[variable][1][1], self.variableMap[variable][1][0]
            pygame.draw.rect(self.window, color, dimensions)

        


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
            elif datatype == "gameObject":
                value = self.interpretGameObjectCall(root.children[2])

            self.variableMap[variable] = [datatype, value]
        
        else:
            variable = root.children[0].token.value

            if not variable in self.variableMap:
                raise Exception("undeclared variable used")
            
            if self.variableMap[variable][0] == "integer":
                value = self.evaluateArithmeticExpression(root.children[1])
            elif self.variableMap[variable][0] == "string":
                value = self.evaluateStringExpression(root.children[1])
            elif self.variableMap[variable][0] == "gameObject":
                value = self.interpretGameObjectCall(root.children[1])

            self.variableMap[variable][1] = value
            
# ---------------------------------------------------interpret if else if block---------------------------------------------------

    def interpretIfElseIfBlock(self,root : AST) -> None:
        if root.token.value == "if":
            condition_node = root.children[0]
            if self.evaluateBooleanExpression(condition_node):
                self.interpretStatementList(root.children[1])
            elif len(root.children) == 3:
                if root.children[2].token.value == "if":
                    self.interpretIfElseIfBlock(root.children[2])
                else:
                    self.interpretStatementList(root.children[2])
                    
# ---------------------------------------------------interpret while block---------------------------------------------------
            
    def interpretWhileBlock(self,root : AST) -> None:
        cond = root.children[0]
        while self.evaluateBooleanExpression(cond):
            try:
                self.interpretStatementList(root.children[1])
            except LoopControl as e:
                if e.value == "break":
                    break
                
# ---------------------------------------------------Screen Function---------------------------------------------------

    def initWindow(self, root : AST) -> None:
        if len(root.children) != 2:
            raise Exception("initWindow expects two arguments: width and height")

        width_node = root.children[0]
        height_node = root.children[1]

        width = self.evaluateArithmeticExpression(width_node)
        height = self.evaluateArithmeticExpression(height_node)

        if not isinstance(width, int) or not isinstance(height, int):
            raise Exception("Width and height must be integers")
 
        self.window = pygame.display.set_mode((width, height))
        
        self.isWindowRunning = True
        
        # self.window.fill((255, 255, 255))
        pygame.display.update()


    def setWindowTitle(self,root : AST):
        if len(root.children) != 1:
            raise Exception('setWindowTitle expects one argument: title')
        
        title = self.evaluateStringExpression(root.children[0])
        
        if self.window:
            pygame.display.set_caption(title)
        
    
    
    def setBackgroundColor(self,root : AST):
        if len(root.children) != 3:
            raise Exception('setBackgroundColor expects four argument: red , blue , green')    
        
        r = self.evaluateArithmeticExpression(root.children[0])
        g = self.evaluateArithmeticExpression(root.children[1])
        b = self.evaluateArithmeticExpression(root.children[2])
        
        if self.window:
            self.window.fill((r,g,b))
        
        
# ---------------------------------------------------program---------------------------------------------------
    def interpretStatement(self, root : AST) -> None:
        if root.token.type == TokenType.ASSIGNMENT:
            self.interpretAssignmentStatement(root)
        elif root.token.value == "if":
            self.interpretIfElseIfBlock(root)
        elif root.token.value == "while":
            self.interpretWhileBlock(root)
        elif root.token.value in ['break' , 'continue']:
            raise  LoopControl(root.token.value)
        elif root.token.value == 'initWindow':
            self.initWindow(root)
        elif root.token.value == 'setWindowTitle':
            self.setWindowTitle(root)
        elif root.token.value == 'setBackgroundColor':
            self.setBackgroundColor(root)
        elif root.token.value == 'draw':
            self.draw(root)

    def interpretStatementList(self, root : AST) -> None:
        for child in root.children:
            self.interpretStatement(child)
        if self.window:
            if self.isWindowRunning:
                self.updateWindow()
            else:
                pygame.quit()

    def interpret(self, text : str) -> None:
        ast : AST  = self.parser.parse(text)

        self.interpretStatementList(ast)
        
        for var in self.variableMap:
            print(f"{var} : {self.variableMap[var]}")
            
    def printAst(self, ast : AST,spaces = 0):
        if not ast: 
            return
        print(f"{' '*spaces}{ast.token.value}")
        for child in ast.children:
            self.printAst(child, spaces+2)
        



# -------------------------------------------------------Window----------------------------------------------------------

    def updateWindow(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isWindowRunning = False

        pygame.display.flip()