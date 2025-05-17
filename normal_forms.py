class NormalForms:
    def __init__(self, truth_table, variables):
        self.truth_table = truth_table
        self.variables = variables

    def compute(self):
        sknf, sdnf = [], []
        sknf_indices, sdnf_indices = [], []

        for index, (variable_values, _, final_result) in enumerate(self.truth_table):
            term = []
            if final_result:
                sdnf_indices.append(index)
                for var in self.variables:
                    term.append(var if variable_values[var] else f'!{var}')
                sdnf.append(f"({' & '.join(term)})")
            else:
                sknf_indices.append(index)
                for var in self.variables:
                    term.append(f'!{var}' if variable_values[var] else var)
                sknf.append(f"({' | '.join(term)})")

        return {
            "СКНФ": " & ".join(sknf),
            "СДНФ": " | ".join(sdnf),
            "СКНФ Индексы": sknf_indices,
            "СДНФ Индексы": sdnf_indices
        }