class ExpressionValidator:
    OPERATORS = {'!': 3, '&': 2, '|': 2, '->': 1, '~': 1}
    VARIABLES = {'a', 'b', 'c', 'd', 'e'}

    @staticmethod
    def validate(expression):
        expression = expression.replace(" ", "")
        if not expression:
            raise ValueError("Выражение не может быть пустым")
        stack = []
        last = ''
        valid_chars = ExpressionValidator.VARIABLES | {'(', ')', '!'}
        i = 0
        while i < len(expression):
            char = expression[i]
            if char in valid_chars:
                if char in ExpressionValidator.VARIABLES and last in ExpressionValidator.VARIABLES:
                    raise ValueError("Между переменными должен быть оператор")
            elif char in {'&', '|', '~'}:
                if last in ExpressionValidator.OPERATORS:
                    raise ValueError("Два оператора подряд недопустимы")
            elif char == '-':
                if i + 1 < len(expression) and expression[i + 1] == '>':
                    char = '->'
                    i += 1
                else:
                    raise ValueError("Некорректный оператор: -")
            elif char not in ExpressionValidator.OPERATORS:
                raise ValueError(f"Недопустимый символ: {char}")
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Несбалансированные скобки")
                stack.pop()
            last = char
            i += 1
        if stack:
            raise ValueError("Несбалансированные скобки")