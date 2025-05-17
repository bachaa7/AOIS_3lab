from expression_validator import ExpressionValidator
from table import TruthTableWithSubexpressions


class KarnaughMinimizer:
    def __init__(self, expression):
        self.expression = expression
        self.variables = sorted(ExpressionValidator.VARIABLES & set(expression))
        self.truth_table_generator = TruthTableWithSubexpressions(expression)
        self.truth_table = []

    def generate_table(self):
        self.truth_table = self.truth_table_generator.generate_table()

    def display_simplified_table(self):
        simplified_table = self.generate_simplified_table()

        headers = self.variables + ["Result"]
        header_row = " | ".join(headers)
        print(header_row)
        print("-" * len(header_row))

        for row in simplified_table:
            print(" | ".join(map(str, row)))

    def generate_simplified_table(self):
        table = self.truth_table_generator.generate_table()

        simplified_table = []
        for variable_values, _, final_result in table:
            combination = [int(variable_values[var]) for var in self.variables]
            simplified_table.append(combination + [int(final_result)])

        return simplified_table

    def generate_karnaugh_map(self):
        simplified_table = self.generate_simplified_table()
        num_vars = len(self.variables)

        if num_vars < 2 or num_vars > 5:
            raise ValueError("Таблицы Карно поддерживаются только для 2-5 переменных.")

        # Разделение переменных на группы
        if num_vars <= 4:
            group_1_vars = self.variables[:num_vars // 2]
            group_2_vars = self.variables[num_vars // 2:]
        else:
            group_1_vars = self.variables[:2]
            group_2_vars = self.variables[2:]

        row_headers = self._generate_gray_code(len(group_1_vars))
        col_headers = self._generate_gray_code(len(group_2_vars))

        # Карно-таблица
        karnaugh_map = [
            [None for _ in col_headers]
            for _ in row_headers
        ]

        # Заполнение Карно-таблицы
        for row_header in range(len(row_headers)):
            for col_header in range(len(col_headers)):
                combination = row_headers[row_header] + col_headers[col_header]
                for entry in simplified_table:
                    if entry[:num_vars] == combination:
                        karnaugh_map[row_header][col_header] = entry[-1]

        return {
            "rows": row_headers,
            "columns": col_headers,
            "map": karnaugh_map
        }

    def display_karnaugh_map(self):
        kmap = self.generate_karnaugh_map()

        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        num_vars = len(self.variables)
        if num_vars <= 4:
            row_vars = self.variables[:num_vars // 2]
            col_vars = self.variables[num_vars // 2:]
        else:
            row_vars = self.variables[:2]
            col_vars = self.variables[2:]

        print(f"Строки ({','.join(row_vars)})")
        print(f"Столбцы ({','.join(col_vars)})")
        print()

        cell_width = max(
            len("".join(map(str, col))) for col in (columns + rows)
        ) + 2

        col_header = " " * (len(row_vars) + 3)
        col_header += " | ".join(f"{''.join(map(str, col)):^{cell_width}}" for col in columns)
        print(col_header)
        print(" " * (len(row_vars) + 3) + "-" * (len(col_header) - (len(row_vars) + 3)))

        for row, values in zip(rows, karnaugh_map):
            row_header = "".join(map(str, row)).ljust(3)
            row_values = " | ".join(f"{str(v) if v is not None else '-':^{cell_width}}" for v in values)
            print(f"{row_header}{row_values}")

    @staticmethod
    def _generate_gray_code(num_bits):
        if num_bits == 0:
            return [[]]
        smaller = KarnaughMinimizer._generate_gray_code(num_bits - 1)
        return [[0] + code for code in smaller] + [[1] + code for code in reversed(smaller)]

    def find_groups(self, for_sdnf=True):
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        target_value = 1 if for_sdnf else 0
        groups = []

        # Поиск групп в Карно-таблице
        for size in [32, 16, 8, 4, 2, 1]:
            for row in range(len(rows)):
                for col in range(len(columns)):
                    group = self._find_group(row, col, size, karnaugh_map, rows, columns, target_value)
                    if group:
                        groups.append(group)
        return groups

    def _find_group(self, row, col, size, kmap, rows, columns, target_value):
        group = []
        # Для поиска групп — уточните правила группировки для Karnaugh map
        if kmap[row][col] == target_value:
            group.append((row, col))
        # Логика для обработки групп по размерам
        return group

    def minimize_sdnf(self):
        groups = self.find_groups(for_sdnf=True)
        implicants = []
        for group in groups:
            implicant = self._group_to_implicant(group, for_sdnf=True)
            implicants.append(implicant)
        return " ∨ ".join(implicants)

    def minimize_sknf(self):
        groups = self.find_groups(for_sdnf=False)
        implicants = []
        for group in groups:
            implicant = self._group_to_implicant(group, for_sdnf=False)
            implicants.append(implicant)
        return " ∧ ".join(implicants)

    def _group_to_implicant(self, group, for_sdnf=True):
        implicant = []

        # Проверка на пустоту группы
        if not group:
            return implicant

        # Проверяем, что все элементы группы имеют одинаковую длину
        group_length = len(group[0])
        for code in group:
            if len(code) != group_length:
                raise ValueError(f"Элементы группы имеют разную длину: {group}")


