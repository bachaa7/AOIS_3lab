import itertools

from expression_validator import ExpressionValidator
from logic_evaluator import LogicEvaluator
from rpn_converter import RPNConverter

class TruthTableWithSubexpressions:
    def __init__(self, expression):
        self.expression = expression
        self.variables = sorted(ExpressionValidator.VARIABLES & set(expression))
        self.converter = RPNConverter(expression)
        self.subexpressions = []
        self.subexpression_strs = []

    def extract_subexpressions(self):
        stack = []
        rpn_expression = self.converter.to_rpn()

        for token in rpn_expression:
            if token in self.converter.variables:
                stack.append([token])
            elif token in self.converter.operators:
                if token == '!':
                    operand = stack.pop()
                    subexpression = operand + [token]
                else:
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    subexpression = operand1 + operand2 + [token]

                stack.append(subexpression)
                self.subexpressions.append(subexpression)

        for subexpr in self.subexpressions:
            self.subexpression_strs.append(self.convert_to_string(subexpr))

    def convert_to_string(self, rpn_expression):
        stack = []
        for token in rpn_expression:
            if token in self.converter.variables:
                stack.append(token)
            elif token == '!':
                operand = stack.pop()
                stack.append(f"!{operand}")
            elif token in {'&', '|', '->', '~'}:
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '&':
                    stack.append(f"({operand1} & {operand2})")
                elif token == '|':
                    stack.append(f"({operand1} | {operand2})")
                elif token == '->':
                    stack.append(f"({operand1} -> {operand2})")
                elif token == '~':
                    stack.append(f"({operand1} ~ {operand2})")
        return stack[0]

    def evaluate_subexpressions(self, variable_values):
        evaluator = LogicEvaluator(self.converter.to_rpn())
        results = []

        for subexpression in self.subexpressions:
            evaluator = LogicEvaluator(subexpression)
            result = evaluator.evaluate(variable_values)
            results.append(result)

        final_result = evaluator.evaluate(variable_values)  # Финальное выражение
        return results, final_result

    def generate_table(self):
        self.extract_subexpressions()
        table = []

        for values in itertools.product([False, True], repeat=len(self.variables)):
            variable_values = dict(zip(self.variables, values))
            subformula_results, final_result = self.evaluate_subexpressions(variable_values)

            table.append((variable_values, subformula_results, final_result))

        return table

    def display_table(self):
        table = self.generate_table()

        subexpressions = self.subexpression_strs[:-1]

        col_width = max(len(col) for col in (self.variables + subexpressions + ["Result"])) + 2

        headers = self.variables + subexpressions + ["Result"]
        header_row = " | ".join(f"{header:<{col_width}}" for header in headers)
        print(header_row)
        print("-" * len(header_row))

        for row in table:
            variable_values, subformula_results, final_result = row

            variable_str = " | ".join(f"{int(variable_values[var]):<{col_width}}" for var in self.variables)

            subformula_str = " | ".join(f"{int(result):<{col_width}}" for result in subformula_results[:-1])

            result_str = f"{int(final_result):<{col_width}}"

            print(f"{variable_str} | {subformula_str} | {result_str}")


    def to_index_form(self):
        truth_table = self.generate_table()

        binary_representation = "".join(str(int(final_result)) for _, _, final_result in truth_table)

        decimal_value = int(binary_representation, 2)

        return {
            "binary": binary_representation,
            "decimal": decimal_value
        }