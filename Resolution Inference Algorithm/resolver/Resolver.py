import resolver.Unifier as Unifier
from preprocessor.KnowledgeBase import KBStorageUnit
import time


class Resolver:
    def __init__(self, knowledge_base, queries):
        self.knowledge_base = knowledge_base
        self.queries = queries

    def fetch_conjugate_predicates(self, query, clause):
        conjugate_list = []
        query_predicates = query.predicates
        clause_predicates = clause.predicates
        existing_conjugates = set()
        common_predicates = query_predicates.keys() & clause_predicates.keys()
        for pred in common_predicates:
            for x in clause_predicates[pred]:
                for y in query_predicates[pred]:
                    if x.operator != y.operator and x not in \
                            existing_conjugates and y not in existing_conjugates:
                        existing_conjugates.add(x)
                        existing_conjugates.add(y)
                        conjugate_list.append([x, y])
        return conjugate_list

    def result_output(self):
        raise TrueQuery

    def resolve_clause(self, sub_dicts, clauses, query, query_start_time,
                       depth=0):
        output = "TRUE"
        check_flag = False
        query_elapsed_time = int(time.time())
        if depth >= 800: # or query_elapsed_time >= query_start_time:
            raise MaxDepthLimit
        for kb_clause in clauses:
            print(kb_clause.predicates.keys() & query.predicates.keys())
            if kb_clause.predicates.keys() & query.predicates.keys():
                conjugates = self.fetch_conjugate_predicates(query,
                                                             kb_clause)
                for conjugate in conjugates:
                    check_flag = False
                    resolution_step_output = self.resolve_query(query,
                                                                conjugate,
                                                                kb_clause)
                    if resolution_step_output:
                        new_clause, sub_dict = resolution_step_output
                        if new_clause.disjunct_clauses == set():
                            self.result_output()
                        else:
                            if len(
                                    sub_dict) == 0 and new_clause in self.knowledge_base:
                                continue
                            if len(sub_dict) != 0:
                                new_clause = new_clause.substitute_unified_values(
                                    sub_dict)
                                for k in clauses:
                                    if new_clause.disjunct_clauses == k.disjunct_clauses:
                                        check_flag = True
                                        break

                                if check_flag:
                                    continue
                            output = self.resolve_clause(
                                (sub_dict, sub_dicts), clauses + [query],
                                new_clause, query_start_time, depth + 1)
        return "FALSE"

    def resolve_query(self, query, conjugate, clause):
        var1 = conjugate[0]
        var2 = conjugate[1]
        unified_predicates = set()
        if var1.operator == "~":
            clause1 = var1.sub_expr[0]
            clause2 = var2
        else:
            clause1 = var1
            clause2 = var2.sub_expr[0]
        try:
            unified_dict = Unifier.unify_clause({}, clause1, clause2)
        except Exception:
            pass
        else:
            if not unified_dict and self.check_constants(clause1.sub_expr,
                                                         clause2.sub_expr):
                return False
            else:
                if unified_dict or (
                    not unified_dict and not self.check_constants(clause1,
                                                                  clause2)):
                    unified_predicates.add(var1)
                    unified_predicates.add(var2)
        if unified_predicates:
            return KBStorageUnit(clause.disjunct_clauses.union(
                query.disjunct_clauses) - unified_predicates), unified_dict
        return False

    def check_constants(self, expr1, expr2):
        if expr1 != expr2:
            return True
        else:
            return False

    def resolve_all_queries(self):
        output_list = []
        for query in self.queries:
            try:
                query_start_time = time.time()
                result = self.resolve_clause(None, self.knowledge_base,
                                             query,
                                             (int(query_start_time) + 60))
                output_list.append(result)
            except TrueQuery:
                output_list.append("TRUE")
                pass
            except MaxDepthLimit:
                output_list.append("FALSE")
        print("Output File Result: ", output_list)
        return output_list


class TrueQuery(Exception):
    pass


class MaxDepthLimit(Exception):
    pass
