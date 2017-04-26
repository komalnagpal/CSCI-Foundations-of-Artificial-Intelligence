from preprocessor.Parser import Utilities, Sentence


class KnowledgeBase:
    def __init__(self):
        self.kb_clauses = []

    def add_clause_to_kb(self, disjuncts):
        self.kb_clauses.append(KBStorageUnit(disjuncts))

    def make_query_clause(self, input_query):
        return KBStorageUnit(input_query)


class KBStorageUnit:
    def __init__(self, input_clause):

        self.disjunct_clauses = set()
        self.predicates = {}
        self.add_clause(input_clause)

    def add_clause(self, input_clause):
        self.disjunct_clauses.update(input_clause)
        for clause in self.disjunct_clauses:
            predicate = self.fetch_predicate_name(clause)
            if predicate in self.predicates:
                self.predicates[predicate].append(clause)
            else:
                self.predicates[predicate] = [clause]

    def fetch_predicate_name(self, clause):
        if clause.operator == "~":
            return clause.sub_expr[0].operator
        else:
            return clause.operator

    def is_predicate_present(self, predicate):
        if predicate in self.predicates.keys():
            return True
        else:
            return False

    def substitute_in_predicate(self, sub_dict, pred):
        if Utilities.is_logic_variable_symbol(pred.operator):
            if pred in sub_dict.keys():
                return sub_dict[pred]
            return pred
        elif isinstance(pred, list):
            return [self.substitute_in_predicate(sub_dict, itr) for itr in
                    pred]
        elif isinstance(pred, Sentence):
            inner_substitution = [
                self.substitute_in_predicate(sub_dict, itr) for itr in
                pred.sub_expr]
            return Sentence(pred.operator, *inner_substitution)

    def substitute_unified_values(self, sub_dict):
        substituted_disjuncts = []
        for clause in self.disjunct_clauses:
            substituted_disjuncts.append(
                self.substitute_in_predicate(sub_dict, clause))
        return KBStorageUnit(substituted_disjuncts)
