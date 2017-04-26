from itertools import islice
import linecache
from preprocessor.Parser import Utilities
from preprocessor.CNFConverter import CNFConverter
from preprocessor.KnowledgeBase import KnowledgeBase, KBStorageUnit
from resolver.Resolver import Resolver


class Executor:
    def __init__(self, PATH):
        self.number_of_queries = 0
        self.number_of_sentences = 0
        self.knowledge_base = KnowledgeBase()
        self.queries = []
        cnf_converter_obj = CNFConverter()
        with open(PATH, "r") as inputfile:
            self.number_of_queries = int(inputfile.readline())
            self.number_of_sentences = int(linecache.getline(PATH,
                                                             self.number_of_queries + 2).rstrip(
                '\n'))
            for line in islice(inputfile, 0, self.number_of_queries):
                query_obj = Utilities.parse_expr(line)
                self.queries.append(
                    KBStorageUnit([query_obj.negate_unit_clause()]))
            for line in islice(inputfile, 1, None):
                cnf_clause = cnf_converter_obj.get_cnf(
                    Utilities.standardize_variables(
                        Utilities.parse_expr(line), {}))
                for each_conj in Utilities.fetch_conjunction_clauses(
                        cnf_clause):
                    self.knowledge_base.add_clause_to_kb(
                        Utilities.fetch_disjunction_clauses(each_conj))


def mainfortesting(PATH):
    executor_obj = Executor(PATH)
    resolution_obj = Resolver(executor_obj.knowledge_base.kb_clauses,
                              [query for query in executor_obj.queries])
    query_result = resolution_obj.resolve_all_queries()
    file_obj = open("output.txt", 'w')
    for x in query_result:
        file_obj.write('{}'.format(x))
        file_obj.write('\n')
    file_obj.truncate(file_obj.tell() - 2)
    file_obj.close()


if __name__ == "__main__":
    PATH = 'input.txt'
    executor_obj = Executor(PATH)
    resolution_obj = Resolver(executor_obj.knowledge_base.kb_clauses,
                              [query for query in executor_obj.queries])
    query_result = resolution_obj.resolve_all_queries()
    file_obj = open("output.txt", 'w')
    for x in query_result:
        file_obj.write('{}\n'.format(x))
    file_obj.truncate(file_obj.tell() - 1)
    file_obj.close()
