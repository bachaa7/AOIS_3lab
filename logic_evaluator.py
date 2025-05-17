from expression_validator import ExpressionValidator

class LogicEvaluator:
    def __init__(self, rpn_expression):
        self.rpn = rpn_expression

    def evaluate(self, values):
        stack = []
        for token in self.rpn:
            if token in ExpressionValidator.VARIABLES:
                stack.append(values[token])
            elif token == '!':
                stack.append(not stack.pop())
            elif token == '&':
                b, a = stack.pop(), stack.pop()
                result = True if a == True and b == True else False
                stack.append(result)
            elif token == '|':
                b, a = stack.pop(), stack.pop()
                stack.append(True if a is True or b is True else False)
            elif token == '->':
                b, a = stack.pop(), stack.pop()
                stack.append(True if (not a or b) else False)
            elif token == '~':
                b, a = stack.pop(), stack.pop()
                stack.append(True if a == b else False)
        return stack[0]