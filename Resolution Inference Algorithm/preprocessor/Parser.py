import re


class Sentence:
    def __init__(self, operator, *sub_expr):
        self.operator = str(operator).strip()
        self.sub_expr = [expr for expr in
                         map(Utilities.parse_expr, sub_expr)]

    def __eq__(self, arg2):
        return (arg2 is self) or (isinstance(arg2, Sentence)
                                  and self.operator == arg2.operator
                                  and self.sub_expr == arg2.sub_expr)

    def __and__(self, arg2):
        obj = Sentence('&', self, arg2)
        return obj

    def __or__(self, arg2):
        obj = Sentence('|', self, arg2)
        return obj

    def __invert__(self):
        obj = Sentence('~', self)
        return obj

    def __rshift__(self, arg2):
        obj = Sentence('>>', self, arg2)
        return obj

    def __hash__(self):
        hash_val = hash(tuple(self.sub_expr)) ^ hash(self.operator)
        return hash_val

    def negate_unit_clause(self):
        if self.operator == "~":
            return self.sub_expr[0]
        else:
            return ~self

    def __call__(self, *args):
        return Sentence(self.operator, *args)


class Utilities:
    itr_var = 0

    def __init__(self):
        pass

    @staticmethod
    def is_object_of(var, obj_type):
        return isinstance(var, obj_type)

    @staticmethod
    def parse_expr(clause):
        if Utilities.is_object_of(clause, Sentence):
            return clause
        clause = clause.replace('=>', '>>')
        input_clause = re.sub(r'([\w]+)', r'Sentence("\1")', clause)
        return eval(input_clause)

    @staticmethod
    def is_string_symbol(expr):
        if Utilities.is_object_of(expr, str) and expr[0].isalpha():
            return True
        else:
            return False

    @staticmethod
    def is_logic_variable_symbol(input_str):
        return input_str[0].islower() and Utilities.is_string_symbol(
            input_str)

    @staticmethod
    def is_logic_variable_constant(input_str):
        return input_str[0].isupper() and Utilities.is_string_symbol(
            input_str)

    @staticmethod
    def check_conjunctions(input_seq):
        for clause in input_seq:
            if clause.operator == "&":
                return clause
            else:
                return None

    @staticmethod
    def is_a_variable(expr):
        if Utilities.is_object_of(expr, Sentence) and len(
                expr.sub_expr) == 0 and \
                Utilities.is_logic_variable_symbol(expr.operator):
            return True
        else:
            return False

    @staticmethod
    def standardize_variables(clause, variable_map):
        if Utilities.is_logic_variable_symbol(clause.operator):
            if clause in variable_map.keys():
                return variable_map[clause]
            else:
                variable_map[clause] = Sentence(
                    'x_%d' % Utilities.itr_var)
                Utilities.itr_var += 1
                return variable_map[clause]
        else:
            return Sentence(clause.operator,
                            *[Utilities.standardize_variables(a,
                                                              variable_map)
                              for a in clause.sub_expr])

    @staticmethod
    def fetch_conjunction_clauses(input_clause):
        return Utilities.segregate_clauses('&', [input_clause])

    @staticmethod
    def fetch_disjunction_clauses(input_clause):
        return Utilities.segregate_clauses('|', [input_clause])

    @staticmethod
    def segregate_clauses(operator, clause_list):
        dissociated_clauses = []

        def collate_subclauses(expr):
            for expresion in expr:
                if expresion.operator != operator:
                    dissociated_clauses.append(expresion)
                else:
                    collate_subclauses(expresion.sub_expr)

        collate_subclauses(clause_list)
        return dissociated_clauses

    @staticmethod
    def is_not_a_variable(expr):
        if Utilities.is_object_of(expr, Sentence) and len(
                expr.sub_expr) == 0 and \
                Utilities.is_logic_variable_constant(expr.operator):
            return False
        else:
            return True
