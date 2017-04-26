from preprocessor import Parser


class CNFConverter:
    associative_op = dict(zip(['&', '|'], [True, False]))

    def __init__(self):
        pass

    def get_cnf(self, sentence):
        temp_clause = self.remove_implies_operator(sentence)
        temp_clause = self.propogate_negation_operator(temp_clause)
        return self.distribute_and_operator(temp_clause)

    def remove_implies_operator(self, sentence):
        if Parser.Utilities.is_string_symbol(sentence):
            return sentence
        sub_args = [self.remove_implies_operator(element) for element in
                    sentence.sub_expr]
        if sentence.operator == ">>":
            return ~sub_args[0] | sub_args[1]
        else:
            return Parser.Sentence(sentence.operator, *sub_args)

    def propogate_negation_operator(self, sentence):
        if sentence.operator == "~":
            expr = sentence.sub_expr[0]
            if expr.operator == "|":
                expr_itr = map(self.negate, expr.sub_expr)
                return self.associate_clauses("&", *expr_itr)
            if expr.operator == "~":
                return self.propogate_negation_operator(expr.sub_expr[0])
            if expr.operator == "&":
                expr_itr = map(self.negate, expr.sub_expr)
                return self.associate_clauses("|", *expr_itr)
            return sentence
        elif Parser.Utilities.is_string_symbol(
                sentence.operator) or not sentence.sub_expr:
            return sentence
        else:
            expr_itr = map(self.propogate_negation_operator,
                           sentence.sub_expr)
            return Parser.Sentence(sentence.operator, *expr_itr)

    def check_method_callable(self, seq):
        func = lambda arg: arg.operator == '&'
        for x in seq:
            if func(x):
                return x
        return None

    def distribute_and_operator(self, input_sentence):
        if input_sentence.operator == "&":
            expr_itr = map(self.distribute_and_operator,
                           input_sentence.sub_expr)
            return self.associate_clauses("&", *expr_itr)
        elif input_sentence.operator == "|":
            sub_clauses = self.associate_clauses("|",
                                                 *input_sentence.sub_expr)
            if not sub_clauses.sub_expr:
                return False
            elif len(sub_clauses.sub_expr) == 1:
                return self.distribute_and_operator(
                    sub_clauses.sub_expr[0])
            else:
                conjunct_clauses = self.check_method_callable(
                    sub_clauses.sub_expr)
                if conjunct_clauses is None:
                    return self.associate_clauses(sub_clauses.operator,
                                                  *sub_clauses.sub_expr)
                non_conjunct_clauses = [clause for clause in
                                        sub_clauses.sub_expr if
                                        clause is not conjunct_clauses]
                if len(non_conjunct_clauses) == 1:
                    remaining_non_conjuncts = non_conjunct_clauses[0]
                else:
                    remaining_non_conjuncts = self.associate_clauses("|",
                                                                     *non_conjunct_clauses)
                expr_itr = map(self.distribute_and_operator,
                               [(conjunct | remaining_non_conjuncts) for
                                conjunct in conjunct_clauses.sub_expr])
                return self.associate_clauses("&", *expr_itr)

        else:
            return input_sentence

    def negate(self, sentence):
        return self.propogate_negation_operator(~sentence)

    @staticmethod
    def associate_clauses(join_op, *expr):
        sub_clauses_list = []
        for arg in expr:
            if arg.operator == join_op:
                sub_clauses_list.extend(arg.sub_expr)
            else:
                sub_clauses_list.append(arg)
        if not sub_clauses_list:
            return CNFConverter.associative_op[join_op]
        elif len(sub_clauses_list) == 1:
            return expr[0]
        else:
            return Parser.Sentence(join_op, *sub_clauses_list)
