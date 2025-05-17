import itertools
import re

class Minimizing:

    def build_sdnf_table(self,expression_d, min_d):
        def term_to_str(term):
            return [f"!{chr(97 + idx)}" if var == 0 else f"{chr(97 + idx)}" for idx, var in enumerate(term) if
                    var != "X"]
        header_terms = [" & ".join(term_to_str(term)) for term in expression_d]

        minimized_terms = [" & ".join(term_to_str(term)) for term in min_d]

        table = [["" for _ in range(len(header_terms) + 1)] for _ in range(len(minimized_terms) + 1)]

        table[0][0] = ""
        for j, term in enumerate(header_terms, start=1):
            table[0][j] = f"({term})"

        for i, min_term in enumerate(minimized_terms, start=1):
            table[i][0] = f"({min_term})"
            for j, expr_term in enumerate(expression_d, start=1):
                min_term_parts = term_to_str(min_d[i - 1])
                expr_term_parts = term_to_str(expr_term)

                if all(item in expr_term_parts for item in min_term_parts):
                    table[i][j] = "X"

        col_widths = [max(len(row[i]) for row in table) for i in range(len(table[0]))]
        for row in table:
            print(" | ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))))

    @staticmethod
    def remove_redundant_implicants_with_logic_d(term_expression, variables):
        result = term_expression[:]
        for term in term_expression:
            term_vars = Minimizing._parse_implicant_d(term, variables)
            temp_result = [t for t in result if t != term]
            remaining_expression = " | ".join(temp_result)
            true_sets = Minimizing._generate_true_sets_d(term_vars, variables)
            is_redundant = True
            for var_values in true_sets:
                if not Minimizing._evaluate_expression_d(remaining_expression, var_values):
                    is_redundant = False
                    break
            if is_redundant:
                result.remove(term)

        return result

    @staticmethod
    def _generate_true_sets_d(term_vars, variables):
        fixed_vars = {var: val for var, val in term_vars.items() if val != "X"}
        free_vars = [var for var in variables if var not in fixed_vars]

        combinations = list(itertools.product([0, 1], repeat=len(free_vars)))

        true_sets = []
        for comb in combinations:
            var_values = fixed_vars.copy()
            var_values.update(dict(zip(free_vars, comb)))
            true_sets.append(var_values)

        return true_sets


    @staticmethod
    def _parse_implicant_d(term, variables):
        term = term.strip('()')
        components = term.split(" & ")
        term_vars = {}
        for comp in components:
            if comp.startswith('!'):
                term_vars[comp[1:]] = 0
            else:
                term_vars[comp] = 1
        for var in variables:
            if var not in term_vars:
                term_vars[var] = "X"
        return term_vars

    @staticmethod
    def _evaluate_expression_d(expression, values):
        # Сначала заменить отрицания переменных
        for var, val in values.items():
            expression = expression.replace(f"!{var}", str(int(not val)))

        # Затем заменить сами переменные
        for var, val in values.items():
            expression = expression.replace(var, str(val))

        # Заменить логические операторы на Python-эквиваленты
        expression = expression.replace("&", " and ")
        expression = expression.replace("|", " or ")

        # Если выражение пустое — безопасно вернуть False
        if not expression.strip():
            return False

        return eval(expression)

    #---------------------------------

    @staticmethod
    def terms_sdnf(expression):
        expression = expression.replace(" ", "")
        groups = re.findall(r'\((.*?)\)', expression)
        result = []

        for group in groups:
            term = []
            variables = group.split("&")
            for var in variables:
                if var.startswith("!"):
                    term.append(0)
                else:
                    term.append(1)
            result.append(term)

        return result

    @staticmethod
    def term_to_expression_sdnf(term, variables):
        expression = []
        for value, var in zip(term, variables):
            if value == 1:
                expression.append(var)
            elif value == 0:
                expression.append(f'!{var}')
            elif value == "X":
                continue
        return " & ".join(expression)


    @staticmethod
    def compare_terms_sdnf(terms, variables, verbose=False):
        n = len(terms[0])
        step_result = []
        used = [False] * len(terms)

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                diff_positions = []

                for k in range(n):
                    if terms[i][k] != terms[j][k]:
                        diff_positions.append(k)

                if len(diff_positions) == 1:
                    new_term = terms[i][:]  # создаём копию термина
                    new_term[diff_positions[0]] = "X"  # заменяем на X

                    # Если verbose включён, выводим промежуточный результат
                    if verbose:
                        term_i_expr = Minimizing.term_to_expression_sdnf(terms[i], variables)
                        term_j_expr = Minimizing.term_to_expression_sdnf(terms[j], variables)
                        new_term_expr = Minimizing.term_to_expression_sdnf(new_term, variables)
                        print(f"({term_i_expr}) | ({term_j_expr}) => ({new_term_expr})")

                    step_result.append(new_term)
                    used[i] = True
                    used[j] = True

        # Добавляем те термины, которые не были использованы
        for idx in range(len(terms)):
            if not used[idx]:
                step_result.append(terms[idx])

        return step_result


    @staticmethod
    def second_step_sdnf(terms, variables):
        print("\n=== ВТОРОЙ ШАГ СКЛЕЙКИ ===")
        return Minimizing.compare_terms_sdnf(terms, variables)

    @staticmethod
    def minimize_sdnf(expression, variables):
        print("\n=== РАСЧЁТНЫЙ МЕТОД СДНФ ===")

        if isinstance(expression, str):
            terms = Minimizing.terms_sdnf(expression)
        else:
            terms = expression
        step = 0
        while True:
            print(f"\n=== ШАГ {step + 1} СКЛЕЙКИ ===")

            next_terms = Minimizing.compare_terms_sdnf(terms, variables)

            unique_terms = []
            for term in next_terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            # Выводим термы ДО склейки в виде логических выражений
            term_expressions_before = [f"({Minimizing.term_to_expression_sdnf(term, variables)})" for term in terms]
            print(f"ТЕРМЫ ДО СКЛЕЙКИ: ", " | ".join(term_expressions_before))

            # Выводим термы ПОСЛЕ склейки в виде логических выражений
            term_expressions_after = [f"({Minimizing.term_to_expression_sdnf(term, variables)})" for term in
                                      unique_terms]
            print(f"\nТЕРМЫ ПОСЛЕ СКЛЕЙКИ: ", " | ".join(term_expressions_after))

            # Теперь выводим какие термы были склеены
            for i, term_i in enumerate(terms):
                for j, term_j in enumerate(terms):
                    if i < j:
                        # Проверяем, можно ли склеить термы (если отличие только в одной позиции)
                        diff_positions = []
                        for k in range(len(term_i)):
                            if term_i[k] != term_j[k]:
                                diff_positions.append(k)
                        if len(diff_positions) == 1:
                            # Если термы можно склеить, создаём новый термин
                            new_term = term_i[:]
                            new_term[diff_positions[0]] = "X"

                            term_i_expr = Minimizing.term_to_expression_sdnf(term_i, variables)
                            term_j_expr = Minimizing.term_to_expression_sdnf(term_j, variables)
                            new_term_expr = Minimizing.term_to_expression_sdnf(new_term, variables)

                            # Печатаем склеенные термы в формате: "ТЕРМЫ 1 и 5 склеены: (!a & c) | (a & c) => (!a & b)"
                            print(
                                f"ТЕРМЫ {i + 1} и {j + 1} склеены: ({term_i_expr}) | ({term_j_expr}) => ({new_term_expr})")

            # Выводим финальный результат после склеивания
            print("\nВЫВОД:", " | ".join(term_expressions_after))

            if not unique_terms:
                print("\nБольше нечего склеивать, минимизация завершена.")
                result = Minimizing.remove_redundant_implicants_with_logic_d(term_expressions_after, variables)
                print("ВЫВОД:", " | ".join(result))
                break
            if unique_terms == terms:
                print("\nБольше нечего склеивать, минимизация завершена.")
                term_expressions_after = [f"{Minimizing.term_to_expression_sdnf(term, variables)}" for term in
                                          unique_terms]
                print("ВЫВОД:", " | ".join(term_expressions_after))
                break

            terms = unique_terms
            step += 1

        return terms

    #-------------------------------------2 ----------------------------2 ----------------------------------------
    @staticmethod
    def minimize_sdnf_second(expression, variables):
        print("\n=== РАСЧЁТНО-ТАБЛИЧНЫЙ МЕТОД СДНФ ===")

        if isinstance(expression, str):
            terms = Minimizing.terms_sdnf(expression)
        else:
            terms = expression

        step = 1
        while True:
            print(f"\n=== ШАГ {step} СКЛЕЙКИ ===")

            # ВАЖНО: verbose=True включит логгирование склеек
            next_terms = Minimizing.compare_terms_sdnf(terms, variables, verbose=True)

            # Убираем дубликаты
            unique_terms = []
            for term in next_terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            # Проверка: если ничего не поменялось — завершаем
            if set(map(tuple, unique_terms)) == set(map(tuple, terms)):
                print("\nБольше нечего склеивать, минимизация завершена.")
                term_expressions = [f"({Minimizing.term_to_expression_sdnf(t, variables)})" for t in unique_terms]
                print("\nВЫВОД:", " | ".join(term_expressions))
                break

            # Отображаем термы после склейки
            print("\nТЕРМЫ:", unique_terms)

            # Таблица соответствий
            print("\nТаблица соответствий после склейки:")
            Minimizing.build_sdnf_table(terms, unique_terms)

            print("\n")
            term_expressions = [f"({Minimizing.term_to_expression_sdnf(term, variables)})" for term in unique_terms]
            print("ВЫВОД:", " | ".join(term_expressions))

            terms = unique_terms
            step += 1

        return terms

    #--------------------------------------------------------------------------------------------------------------------------------------------------

    def build_sknf_table(expression_k, min_k):
        def term_to_str(term):
            return [f"!{chr(97 + idx)}" if var == 0 else f"{chr(97 + idx)}" for idx, var in enumerate(term) if
                    var != "X"]

        header_terms = [" | ".join(term_to_str(term)) for term in expression_k]

        minimized_terms = [" | ".join(term_to_str(term)) for term in min_k]

        table = [["" for _ in range(len(header_terms) + 1)] for _ in range(len(minimized_terms) + 1)]

        table[0][0] = ""
        for j, term in enumerate(header_terms, start=1):
            table[0][j] = f"({term})"

        for i, min_term in enumerate(minimized_terms, start=1):
            table[i][0] = f"({min_term})"
            for j, expr_term in enumerate(expression_k, start=1):
                min_term_parts = term_to_str(min_k[i - 1])
                expr_term_parts = term_to_str(expr_term)

                if all(item in expr_term_parts for item in min_term_parts):
                    table[i][j] = "X"

        col_widths = [max(len(row[i]) for row in table) for i in range(len(table[0]))]
        for row in table:
            print(" | ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))))


    @staticmethod
    def remove_redundant_implicants_with_logic_k(term_expression, variables):
        result = term_expression[:]  # copy
        for term in term_expression:
            term_vars = Minimizing._parse_implicant_k(term, variables)
            temp_result = [t for t in result if t != term]
            remaining_expression = " & ".join(temp_result)
            false_sets = Minimizing._generate_false_sets_k(term_vars, variables)
            is_redundant = True
            for var_values in false_sets:
                if Minimizing._evaluate_expression_k(remaining_expression, var_values):
                    is_redundant = False
                    break
            if is_redundant:
                result.remove(term)

        return result

    @staticmethod
    def _generate_false_sets_k(term_vars, variables):
        fixed_vars = {var: (1 - val) for var, val in term_vars.items() if val != "X"}
        free_vars = [var for var in variables if var not in fixed_vars]

        combinations = list(itertools.product([0, 1], repeat=len(free_vars)))

        false_sets = []
        for comb in combinations:
            var_values = fixed_vars.copy()
            var_values.update(dict(zip(free_vars, comb)))
            false_sets.append(var_values)

        return false_sets

    @staticmethod
    def _parse_implicant_k(term, variables):
        term = term.strip('()')
        components = term.split(" | ")
        term_vars = {}
        for comp in components:
            if comp.startswith('!'):
                term_vars[comp[1:]] = 0
            else:
                term_vars[comp] = 1
        for var in variables:
            if var not in term_vars:
                term_vars[var] = "X"
        return term_vars

    @staticmethod
    def _evaluate_expression_k(expression, values):
        # Сначала заменить отрицания переменных
        for var, val in values.items():
            expression = expression.replace(f"!{var}", str(int(not val)))

        # Затем заменить сами переменные
        for var, val in values.items():
            expression = expression.replace(var, str(val))

        # Заменить логические операторы на Python-эквиваленты
        expression = expression.replace("&", " and ")
        expression = expression.replace("|", " or ")

        # Если выражение пустое — безопасно вернуть False
        if not expression.strip():
            return False

        return eval(expression)

    @staticmethod
    def terms_sknf (expression):
        expression = expression.replace(" ", "")
        groups = re.findall(r'\((.*?)\)', expression)
        result = []

        for group in groups:
            term = []
            variables = group.split("|")
            for var in variables:
                if var.startswith("!"):
                    term.append(0)
                else:
                    term.append(1)
            result.append(term)

        return result

    @staticmethod
    def term_to_expression_sknf(term, variables):
        expression = []
        for value, var in zip(term, variables):
            if value == 1:
                expression.append(var)
            elif value == 0:
                expression.append(f'!{var}')
            elif value == "X":
                continue
        return " | ".join(expression)


    @staticmethod
    def compare_terms_sknf(terms, variables, verbose=False):
        n = len(terms[0])
        step_result = []
        used = [False] * len(terms)

        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                diff_positions = []

                for k in range(n):
                    if terms[i][k] != terms[j][k]:
                        diff_positions.append(k)

                if len(diff_positions) == 1:
                    new_term = terms[i][:]  # копия терма
                    new_term[diff_positions[0]] = "X"  # заменяем различие на X

                    if verbose:
                        term_i_expr = Minimizing.term_to_expression_sknf(terms[i], variables)
                        term_j_expr = Minimizing.term_to_expression_sknf(terms[j], variables)
                        new_term_expr = Minimizing.term_to_expression_sknf(new_term, variables)
                        print(f"({term_i_expr}) & ({term_j_expr}) => ({new_term_expr})")

                    step_result.append(new_term)
                    used[i] = True
                    used[j] = True

        # Добавляем неиспользованные термы
        for idx in range(len(terms)):
            if not used[idx]:
                step_result.append(terms[idx])

        return step_result

    @staticmethod
    def second_step_sknf(terms, variables):
        print("\n=== ВТОРОЙ ШАГ СКЛЕЙКИ ===")
        return Minimizing.compare_terms_sknf(terms, variables)

    @staticmethod
    def minimize_sknf(expression, variables):
        print("\n=== РАСЧЁТНЫЙ МЕТОД СКНФ ===")

        if isinstance(expression, str):
            terms = Minimizing.terms_sknf(expression)  # Получаем термы из строки СКНФ
        else:
            terms = expression  # Если термы уже переданы в виде списка

        step = 0
        while True:
            print(f"\n=== ШАГ {step + 1} СКЛЕЙКИ ===")

            next_terms = Minimizing.compare_terms_sknf(terms, variables)  # Получаем термы после склейки

            unique_terms = []
            for term in next_terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            # Выводим термы ДО склейки в виде логических выражений в скобках
            term_expressions_before = [f"({Minimizing.term_to_expression_sknf(term, variables)})" for term in terms]
            print(f"ТЕРМЫ ДО СКЛЕЙКИ: ", " & ".join(term_expressions_before))

            # Выводим термы ПОСЛЕ склейки в виде логических выражений в скобках
            term_expressions_after = [f"({Minimizing.term_to_expression_sknf(term, variables)})" for term in
                                      unique_terms]
            print(f"\nТЕРМЫ ПОСЛЕ СКЛЕЙКИ: ", " & ".join(term_expressions_after))

            # Печатаем, какие термы были склеены
            for i, term_i in enumerate(terms):
                for j, term_j in enumerate(terms):
                    if i < j:
                        # Проверяем, можно ли склеить термы (если отличие только в одной позиции)
                        diff_positions = []
                        for k in range(len(term_i)):
                            if term_i[k] != term_j[k]:
                                diff_positions.append(k)
                        if len(diff_positions) == 1:
                            # Если термы можно склеить, создаём новый термин
                            new_term = term_i[:]
                            new_term[diff_positions[0]] = "X"

                            term_i_expr = Minimizing.term_to_expression_sknf(term_i, variables)
                            term_j_expr = Minimizing.term_to_expression_sknf(term_j, variables)
                            new_term_expr = Minimizing.term_to_expression_sknf(new_term, variables)

                            # Печатаем склеенные термы в формате: "ТЕРМЫ 1 и 5 склеены: (a & b) | (!a & b) => (b & c)"
                            print(
                                f"ТЕРМЫ {i + 1} и {j + 1} склеены: ({term_i_expr}) & ({term_j_expr}) => ({new_term_expr})")

            # Выводим финальный результат после склеивания
            print("\nВЫВОД:", " & ".join(term_expressions_after))

            if not unique_terms:
                print("\nБольше нечего склеивать, минимизация завершена.")
                result = Minimizing.remove_redundant_implicants_with_logic_k(term_expressions_after, variables)
                print("ВЫВОД:", " & ".join(result))
                break
            if unique_terms == terms:
                print("\nБольше нечего склеивать, минимизация завершена.")
                term_expressions_after = [f"({Minimizing.term_to_expression_sknf(term, variables)})" for term in
                                          unique_terms]
                print("ВЫВОД:", " & ".join(term_expressions_after))
                break

            terms = unique_terms
            step += 1

        return terms

    @staticmethod
    def minimize_sknf_second(expression, variables):
        print("\n=== РАСЧЁТНО-ТАБЛИЧНЫЙ МЕТОД СКНФ ===")

        if isinstance(expression, str):
            terms = Minimizing.terms_sknf(expression)
        else:
            terms = expression
        step = 0
        while True:
            print(f"\n=== ШАГ {step + 1} СКЛЕЙКИ ===")

            next_terms = Minimizing.compare_terms_sknf(terms, variables,verbose=True)

            unique_terms = []
            for term in next_terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            print("\nТаблица соответствий после склейки:")
            Minimizing.build_sknf_table(terms, unique_terms)

            print("\n")
            term_expressions = [f"({Minimizing.term_to_expression_sknf(term, variables)})" for term in
                                unique_terms]
            print("ВЫВОД:", " & ".join(term_expressions))

            if not unique_terms:
                print("\nБольше нечего склеивать, минимизация завершена.")
                result = Minimizing.remove_redundant_implicants_with_logic_k(term_expressions, variables)
                print("\nВЫВОД:", " & ".join(result))
                break
            if unique_terms == terms:
                print("\nБольше нечего склеивать, минимизация завершена.")
                print("\nВЫВОД:", " & ".join(term_expressions))
                break

            terms = unique_terms
            step += 1

        return terms

    @staticmethod
    def minimize_sknf_second_simplified(expression, variables):
        if isinstance(expression, str):
            terms = Minimizing.terms_sknf(expression)
        else:
            terms = expression

        def transform_expression_to_python(expr):
            return expr.replace('!', 'not ').replace('&', 'and').replace('|', 'or')

        def transform_expression_to_original(expr):
            return expr.replace('not ', '!').replace('and', '&').replace('or', '|')

        while True:
            next_terms = Minimizing.compare_terms_sknf(terms, variables)

            unique_terms = []
            for term in next_terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            if not unique_terms or unique_terms == terms:
                term_expressions = [f"({Minimizing.term_to_expression_sknf(term, variables)})" for term in unique_terms]
                python_expressions = [transform_expression_to_python(expr) for expr in term_expressions]
                result = Minimizing.remove_redundant_implicants_with_logic_k(python_expressions, variables)
                result_in_original_format = [transform_expression_to_original(expr) for expr in result]
                return " & ".join(result_in_original_format)

            terms = unique_terms

    @staticmethod
    def minimize_sdnf_second_simplified(expression, variables, verbose=False):
        if isinstance(expression, str):
            terms = Minimizing.terms_sdnf(expression)
        else:
            terms = expression

        def transform_expression_to_python(expr):
            return expr.replace('!', 'not ').replace('&', 'and').replace('|', 'or')

        def transform_expression_to_original(expr):
            return expr.replace('not ', '!').replace('and', '&').replace('or', '|')

        step = 0
        while True:
            next_terms = Minimizing.compare_terms_sdnf(terms, variables, verbose)

            unique_terms = []
            for term in next_terms:
                if term not in unique_terms:
                    unique_terms.append(term)

            term_expressions = [f"({Minimizing.term_to_expression_sdnf(term, variables)})" for term in unique_terms]

            if not unique_terms:
                result = Minimizing.remove_redundant_implicants_with_logic_d(term_expressions, variables)
                return " | ".join(result)

            if unique_terms == terms:
                return " | ".join(term_expressions)

            terms = unique_terms
            step += 1

