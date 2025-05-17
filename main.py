from KarnaughMinimizer import KarnaughMinimizer
from min import Minimizing
from normal_forms import NormalForms
from table import TruthTableWithSubexpressions


def main():
    expression = input("Введите логическое выражение: ")
    try:
        # 2 ЛАБА
        tt = TruthTableWithSubexpressions(expression)
        tt.display_table()



        # Получаем таблицу истинности
        truth_table = tt.generate_table()
        normal_forms = NormalForms(truth_table, tt.variables)
        forms = normal_forms.compute()
        print("\nСДНФ:", forms["СДНФ"])
        print("СКНФ:", forms["СКНФ"])



        # ПЕРВЫЙ МЕТОД - РАСЧЁТНЫЙ
        print("\n============================================ МЕТОД 1 ============================================")

        variables = tt.variables  # Полагаю, что tt.variables — это список переменных

        # Для СДНФ
        expression_d = forms["СДНФ"]  # Читаем выражение для СДНФ
        result_d = Minimizing.terms_sdnf(expression_d)  # Получаем термы для СДНФ
        print("\nСДНФ ТЕРМЫ: ", result_d)

        # Минимизация через расчетный метод
        min_d = Minimizing.minimize_sdnf(result_d, variables)  # Используем обновленный метод минимизации

        # Выводим результат минимизации
        print("\nМинимизированная СДНФ:", " | ".join([Minimizing.term_to_expression_sdnf(t, variables) for t in min_d]))


        # Для СКНФ
        expression_k = forms["СКНФ"]  # Читаем выражение для СКНФ
        result_k = Minimizing.terms_sknf(expression_k)  # Получаем термы для СКНФ

        # Печатаем термы СКНФ в виде дизъюнктов в скобках
        print("\nСКНФ ТЕРМЫ: ", [f"({Minimizing.term_to_expression_sknf(t, variables)})" for t in result_k])

        # Минимизация через расчетный метод для СКНФ
        min_k = Minimizing.minimize_sknf(result_k, variables)  # Используем обновленный метод минимизации

        # Выводим результат минимизации — тоже в скобках
        print("\nМинимизированная СКНФ:",
              " & ".join([f"({Minimizing.term_to_expression_sknf(t, variables)})" for t in min_k]))




        # ВТОРОЙ МЕТОД - РАСЧЁТНО-ТАБЛИЧНЫЙ
        print("\n============================================ МЕТОД 2 ============================================")
        min_d2 = Minimizing.minimize_sdnf_second(result_d, variables)
        print("\n====================== ТАБЛИЦА ======================")
        Minimizing.build_sdnf_table(result_d, min_d2)

        min_k2 = Minimizing.minimize_sknf_second(result_k, variables)
        print("\n====================== ТАБЛИЦА ======================")
        Minimizing.build_sknf_table(result_k, min_k2)

        # ТРЕТИЙ МЕТОД - КАРТА КАРНО
        print("\n============================================ МЕТОД 3 ============================================")
        # Сначала для СДНФ
        #print("\n============================================ СДНФ ============================================")
        karnaugh_minimizer = KarnaughMinimizer(expression_d)
        # karnaugh_minimizer.generate_simplified_table()
        # karnaugh_minimizer.display_simplified_table()
        # karnaugh_minimizer.display_karnaugh_map()
        # minimized_sdnf = karnaugh_minimizer.minimize_sdnf()
        # print("\nМинимизированная СДНФ:")
        # print(minimized_sdnf)
        # min_d2 = Minimizing.minimize_sdnf_second(result_d, variables)



        # Теперь для СКНФ
        # print("\n============================================ СКНФ ============================================")
        # karnaugh_minimizer = KarnaughMinimizer(expression_k)  # Используем СКНФ
        # karnaugh_minimizer.generate_simplified_table()
        # karnaugh_minimizer.display_simplified_table()
        karnaugh_minimizer.display_karnaugh_map()
        # minimized_sknf = karnaugh_minimizer.minimize_sknf()
        print("\n")
        # Вызов метода минимизации без промежуточных выводов
        min_k2 = Minimizing.minimize_sknf_second_simplified(result_k, variables)

        # Вывод только конечного результата
        minimized_sknf_final = Minimizing.minimize_sknf_second_simplified(result_k, variables)
        print("\nМинимизированная СКНФ:")
        print(minimized_sknf_final)

        print("\nМинимизированная СДНФ:")
        minimized_sdnf_final = Minimizing.minimize_sdnf_second_simplified(result_d, variables)
        print(minimized_sdnf_final)







    except ValueError as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()

# Пример: !(!a->!b) |
# (!a & !b & !c & d) | (!a & b & c & d) | (a & b & !c & d) | (a & b & c & d)






