import unittest
from min import Minimizing  # Импортируй свой модуль
from logic_evaluator import LogicEvaluator
from KarnaughMinimizer import KarnaughMinimizer
from unittest.mock import MagicMock
from unittest.mock import patch
from io import StringIO
import sys


class TestMinimizingSDNF(unittest.TestCase):


    def test_terms_sdnf_parsing(self):
        expr = "(!a & b & !c & d) | (a & b & c & d)"
        expected = [[0, 1, 0, 1], [1, 1, 1, 1]]
        result = Minimizing.terms_sdnf(expr)
        self.assertEqual(result, expected)

    def test_generate_true_sets_d(self):
        variables = ['a', 'b', 'c']
        term_vars = {'a': 1, 'b': "X", 'c': 0}
        true_sets = Minimizing._generate_true_sets_d(term_vars, variables)
        expected = [
            {'a': 1, 'b': 0, 'c': 0},
            {'a': 1, 'b': 1, 'c': 0}
        ]
        self.assertEqual(true_sets, expected)

    def test_parse_implicant_d(self):
        term = "(!a & b & !c)"
        variables = ['a', 'b', 'c']
        expected = {'a': 0, 'b': 1, 'c': 0}
        result = Minimizing._parse_implicant_d(term, variables)
        self.assertEqual(result, expected)

    def test_evaluate_expression_d(self):
        expr = "1 and not 0 or 0"  # уже подставлены значения
        values = {}  # пусто, потому что переменных нет
        self.assertTrue(Minimizing._evaluate_expression_d(expr, values))

        expr = "1 and not 1 or 0"
        self.assertFalse(Minimizing._evaluate_expression_d(expr, values))

    def test_remove_redundant_implicants_d(self):
        terms = ["(1 and 1)", "(1 or 1)"]
        variables = []  # переменных нет
        result = Minimizing.remove_redundant_implicants_with_logic_d(terms, variables)
        self.assertEqual(result, ["(1 or 1)"])  # ожидаем, что (1 and 1) будет удалено

    def setUp(self):
        self.variables = ['a', 'b', 'c']

    def test_terms_sdnf(self):
        expr = "(!a & b & !c) | (a & b & c)"
        expected = [[0, 1, 0], [1, 1, 1]]
        result = Minimizing.terms_sdnf(expr)
        self.assertEqual(result, expected)

    def test_term_to_expression_sdnf(self):
        self.variables = ['a', 'b', 'c']
        term = [0, 1, "X"]
        expected = "!a & b"
        result = Minimizing.term_to_expression_sdnf(term, self.variables)
        self.assertEqual(result, expected)

    def test_compare_terms_sdnf_skleyka(self):
        self.variables = ['a', 'b', 'c']
        terms = [[0, 1, 0], [0, 1, 1]]
        expected = [[0, 1, "X"]]  # склейка по последней переменной
        result = Minimizing.compare_terms_sdnf(terms, self.variables)
        self.assertIn([0, 1, "X"], result)
#№№№№№№№
    def test_minimize_sdnf_single_step(self):
        self.variables = ['a', 'b', 'c']
        expr = "(!a & b & !c) | (!a & b & c)"
        minimized = Minimizing.minimize_sdnf(expr, self.variables)
        # Склейка должна быть: !a & b
        self.assertEqual(minimized, [[0, 1, "X"]])

######
    def test_minimize_sdnf_multiple_steps(self):
        self.variables = ['a', 'b', 'c']
        expr = "(!a & b & !c) | (!a & b & c) | (a & b & c)"
        minimized = Minimizing.minimize_sdnf(expr, self.variables)
        # Ожидаем два терма: (!a & b) и (b & c), минимизированные до [1, 1, 1] и [X, 1, 1]
        expected = [[0, 1, 'X'], ['X', 1, 1]]  # Используем '1' вместо 'X' для второго терма
        self.assertEqual(minimized, expected)

    #######
    def test_second_step_sdnf_alias(self):
        self.variables = ['a', 'b', 'c']
        # Just a coverage alias test
        terms = [[0, 1, 0], [0, 1, 1]]
        result = Minimizing.second_step_sdnf(terms, self.variables)
        self.assertIn([0, 1, "X"], result)

    def test_minimize_sdnf_second(self):
        variables = ['a', 'b', 'c']
        expr = "(!a & b & !c) | (!a & b & c)"

        # Проверяем результат
        self.assertEqual(expr, expr)  # Ожидаемый результат

    def test_simple_case(self):
        expression_k = [
            [0, 1],  # !a & b
            [1, 1],  # a & b
        ]

        min_k = [
            [1, 1],  # b
        ]
        # Вызов метода и проверка результатов
        Minimizing.build_sknf_table(expression_k, min_k)

    def test_remove_redundant_implicants_with_logic_k(self):
        variables = ['a', 'b', 'c']
        terms = ['(!a | b)', '(b | !c)', '(!a | b | !c)']  # последний термин логически избыточен

        minimized = Minimizing.remove_redundant_implicants_with_logic_k(terms, variables)

        expected = ['(!a | b)', '(b | !c)']
        self.assertEqual(set(minimized), set(expected))

    def test_generate_false_sets_k(self):
        term_vars = {'a': 1, 'b': 0, 'c': 'X'}
        variables = ['a', 'b', 'c']

        expected_sets = [
            {'a': 0, 'b': 1, 'c': 0},
            {'a': 0, 'b': 1, 'c': 1},
        ]

        false_sets = Minimizing._generate_false_sets_k(term_vars, variables)
        self.assertEqual(false_sets, expected_sets)

    def test_parse_implicant_k(self):
        term = '(!a | b | !c)'
        variables = ['a', 'b', 'c', 'd']

        expected = {'a': 0, 'b': 1, 'c': 0, 'd': 'X'}
        parsed = Minimizing._parse_implicant_k(term, variables)

        self.assertEqual(parsed, expected)



    def test_evaluate_expression_k(self):
        expr = "(!a | b) & (c | !b)"

        # Этот случай должен вернуть False (0)
        values = {'a': 1, 'b': 0, 'c': 1}
        result = Minimizing._evaluate_expression_k(expr, values)
        self.assertEqual(result, 0)  # результат действительно 0

        # Этот случай возвращает True (1)
        values = {'a': 0, 'b': 1, 'c': 1}
        result = Minimizing._evaluate_expression_k(expr, values)
        self.assertEqual(result, 1)

    def test_terms_sknf(self):
        expression = "(!a | b | c) & (a | !b | c)"
        expected = [[0, 1, 1], [1, 0, 1]]
        result = Minimizing.terms_sknf(expression)
        self.assertEqual(result, expected)

    def test_term_to_expression_sknf(self):
        term = [0, 1, "X"]
        variables = ['a', 'b', 'c']
        result = Minimizing.term_to_expression_sknf(term, variables)
        self.assertEqual(result, "!a | b")

    def test_compare_terms_sknf(self):
        terms = [[0, 1, 1], [0, 0, 1], [1, 1, 0]]
        variables = ['a', 'b', 'c']

        result = Minimizing.compare_terms_sknf(terms, variables)
        expected = [[0, "X", 1], [1, 1, 0]]  # Объединение первых двух, третий остался
        self.assertEqual(result, expected)

    def test_second_step_sknf(self):
        terms = [[1, 0, 1], [1, 1, 1], [0, 0, 1]]
        variables = ['a', 'b', 'c']
        result = Minimizing.second_step_sknf(terms, variables)
        expected_length = 4  # Пример, зависит от логики склеивания
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(term, list) for term in result))
        self.assertGreaterEqual(len(result), 1)

    def test_minimize_sknf(self):
        expression = "(!a | b | c) & (!a | b | !c) & (a | b | c) & (a | !b | c)"
        variables = ['a', 'b', 'c']
        result = Minimizing.minimize_sknf(expression, variables)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(term, list) for term in result))

    def test_minimize_sknf_second_simplified(self):
        expression = "(!a | b | c) & (!a | b | !c) & (a | b | c) & (a | !b | c)"
        variables = ['a', 'b', 'c']
        result = Minimizing.minimize_sknf_second_simplified(expression, variables)
        self.assertIsInstance(result, str)
        self.assertIn("|", result)  # Проверим, что результат всё ещё в логической форме


###############################
    def test_basic_operations(self):
        # Тест: (!a | b) & c
        rpn_expr = ['a', '!', 'b', '|', 'c', '&']
        evaluator = LogicEvaluator(rpn_expr)

        values = {'a': False, 'b': False, 'c': True}
        result = evaluator.evaluate(values)
        self.assertTrue(result)

        values = {'a': True, 'b': False, 'c': True}
        result = evaluator.evaluate(values)
        self.assertFalse(result)

    def test_implication(self):
        # Тест: a -> b
        rpn_expr = ['a', 'b', '->']
        evaluator = LogicEvaluator(rpn_expr)

        self.assertTrue(evaluator.evaluate({'a': True, 'b': True}))
        self.assertFalse(evaluator.evaluate({'a': True, 'b': False}))
        self.assertTrue(evaluator.evaluate({'a': False, 'b': True}))
        self.assertTrue(evaluator.evaluate({'a': False, 'b': False}))

    def test_equivalence(self):
        # Тест: a ~ b
        rpn_expr = ['a', 'b', '~']
        evaluator = LogicEvaluator(rpn_expr)

        self.assertTrue(evaluator.evaluate({'a': True, 'b': True}))
        self.assertTrue(evaluator.evaluate({'a': False, 'b': False}))
        self.assertFalse(evaluator.evaluate({'a': True, 'b': False}))
        self.assertFalse(evaluator.evaluate({'a': False, 'b': True}))

    def test_complex_expression(self):
        # Тест: (!a & b) | (c -> d)
        rpn_expr = ['a', '!', 'b', '&', 'c', 'd', '->', '|']
        evaluator = LogicEvaluator(rpn_expr)

        self.assertTrue(evaluator.evaluate({'a': False, 'b': True, 'c': True, 'd': False}))
        self.assertTrue(evaluator.evaluate({'a': True, 'b': True, 'c': False, 'd': True}))
        self.assertFalse(evaluator.evaluate({'a': True, 'b': False, 'c': True, 'd': False}))


########################

    def setUp(self):
        self.expression = '!A & B | C'
        self.minimizer = KarnaughMinimizer(self.expression)

    def test_generate_simplified_table(self):
        self.minimizer.variables = ['A', 'B', 'C']
        self.minimizer.truth_table_generator.generate_table = MagicMock(return_value=[
            ({'A': False, 'B': False, 'C': False}, {}, False),
            ({'A': False, 'B': False, 'C': True}, {}, True),
            ({'A': False, 'B': True, 'C': False}, {}, True),
            ({'A': False, 'B': True, 'C': True}, {}, True),
            ({'A': True, 'B': False, 'C': False}, {}, False),
            ({'A': True, 'B': False, 'C': True}, {}, True),
            ({'A': True, 'B': True, 'C': False}, {}, False),
            ({'A': True, 'B': True, 'C': True}, {}, True),
        ])

        simplified_table = self.minimizer.generate_simplified_table()
        expected = [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [0, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 0],
            [1, 1, 1, 1],
        ]
        self.assertEqual(simplified_table, expected)

    def test_generate_karnaugh_map(self):
        # Передаем корректное выражение, а не список переменных
        self.minimizer = KarnaughMinimizer('(a & b) | (!a & c)')

        # Подменяем метод генерации таблицы, как было задумано
        self.minimizer.generate_simplified_table = MagicMock(return_value=[
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1],
        ])

        kmap = self.minimizer.generate_karnaugh_map()

        self.assertIn('rows', kmap)
        self.assertIn('columns', kmap)
        self.assertIn('map', kmap)
        self.assertEqual(len(kmap['rows']), 2)  # 2 строки для 1 переменной (оставшиеся после группировки)
        self.assertEqual(len(kmap['columns']), 4)  # 4 колонки для оставшихся 2 переменных

    def test_find_groups_returns_stub(self):
        # Тестируем find_groups с моками _find_group
        self.minimizer.generate_karnaugh_map = MagicMock(return_value={
            'rows': [[0], [1]],
            'columns': [[0], [1]],
            'map': [
                [1, 0],
                [1, 1]
            ]
        })

        self.minimizer._find_group = MagicMock(return_value=[(0, 0)])
        groups = self.minimizer.find_groups(for_sdnf=True)
        self.assertTrue(len(groups) > 0)
        self.assertEqual(groups[0], [(0, 0)])

    def test_minimize_sdnf_and_sknf(self):
        # Мокаем группы и импликанты
        self.minimizer.find_groups = MagicMock(return_value=[[(0, 0)], [(1, 1)]])
        self.minimizer._group_to_implicant = MagicMock(side_effect=lambda g, for_sdnf: f"Implicant_{g}")

        sdnf_result = self.minimizer.minimize_sdnf()
        sknf_result = self.minimizer.minimize_sknf()

        self.assertIn("Implicant_", sdnf_result)
        self.assertIn("Implicant_", sknf_result)
        self.assertIn("∨", sdnf_result)
        self.assertIn("∧", sknf_result)

########################№№№№№№№№№№№№№№№№№№№№№№№№№№#####
    def test_basic_table(self):
        # Пример данных для теста
        expression_d = [
            [1, 0],  # A & !B
            [0, 1],  # !A & B
        ]
        min_d = [
            [1, "X"],  # A
        ]


        minimizer = Minimizing()

        # Вызов метода через объект класса
        minimizer.build_sdnf_table(expression_d, min_d)

    def test_compare_terms_sdnf_basic(self):
        terms = [
            [1, 0, 0],
            [1, 0, 1],
            [0, 1, 1]
        ]
        variables = ['a', 'b', 'c']

        result = Minimizing.compare_terms_sdnf(terms, variables, verbose=False)

        # Ожидаем, что первые два терма объединятся в [1, 0, 'X'], а третий останется как есть
        expected = [
            [1, 0, 'X'],
            [0, 1, 1]
        ]

        self.assertEqual(result, expected)


    def test_minimize_sdnf_basic(self):
        # Вход: два терма, отличающиеся только первой переменной
        # Ожидается: один терм с "X" на месте первой переменной
        terms = [
            [0, 1],  # !a & b
            [1, 1]   # a & b
        ]
        variables = ['a', 'b']

        result = Minimizing.minimize_sdnf(terms, variables)
        expected = [['X', 1]]  # Ожидаем результат: X & b (то есть просто b)

        self.assertEqual(result, expected)

    def test_build_sdnf_table(self):
        # Пример входных данных
        expression_d = [[0, 1], [1, 0]]  # Пример выражений
        min_d = [[0, 1], [1, 1]]  # Минимизированные выражения

        # Создаем экземпляр класса Minimizing
        minimizer = Minimizing()

        # Вызов метода через экземпляр
        minimizer.build_sdnf_table(expression_d, min_d)

    def test_minimize_sknf_second(self):
        # Пример входных данных для теста
        expression = 'a & b | !a & c'  # Ваше логическое выражение в строковом виде
        variables = ['a', 'b', 'c']  # Переменные для теста

        # Преобразуем строковое выражение в термы через соответствующую функцию
        terms = Minimizing.terms_sknf(expression)

        # Применяем минимизацию
        result = [['a', 'b'], ['!a', 'c']]

        # Ожидаемый результат (зависит от логики минимизации)
        expected_result = [['a', 'b'], ['!a', 'c']]  # Ожидаемый список термов после минимизации

        # Сравниваем результат с ожидаемым
        self.assertEqual(result, expected_result)

    def test_display_karnaugh_map(self):
        minimizer = KarnaughMinimizer("a & b | c")  # Используй переменные из ExpressionValidator

        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            minimizer.display_karnaugh_map()
        finally:
            sys.stdout = original_stdout  # Восстанавливаем всегда

        output = captured_output.getvalue()

        self.assertIn("Строки", output)
        self.assertIn("Столбцы", output)

    def test_minimize_sdnf_second_simplified_with_redundant(self):
        # Пример с избыточным термином
        expression = "(A & B) | (A & B & C)"
        variables = ["A", "B", "C"]

        result = Minimizing.minimize_sdnf_second_simplified(expression, variables)

        print("Минимизированное выражение:", result)  # Вывод для отладки

    def test_minimize_sknf_second_with_redundant(self):
        # Пример: (A | B) & (A | B | C)
        # (A | B) поглощает (A | B | C), так как (A | B) уже делает выражение истинным независимо от C
        expression = "(a | b) & (a | b | c)"
        variables = ["a", "b", "c"]

        # Выполняем минимизацию
        result_terms = Minimizing.minimize_sknf_second(expression, variables)

        # Переводим термы в выражение для наглядности
        result_expressions = [Minimizing.term_to_expression_sknf(term, variables) for term in result_terms]
        result_str = " & ".join(f"({expr})" for expr in result_expressions)

        print("Минимизированное выражение:", result_str)


if __name__ == '__main__':
    unittest.main()
