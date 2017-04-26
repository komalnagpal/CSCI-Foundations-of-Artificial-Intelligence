from preprocessor import Parser
import sys

def unify_variable(input_var, clause, substitution):
    """
    :param input_var: variable to be unified
    :param clause: Sentence
    :param substitution: Existing set of substitution
    :return: subsitution given input_var and sentence x
    """
    if input_var in substitution.keys():
        return unify_clause(substitution[input_var], clause,
                              substitution)
    else:
        substitution[input_var] = clause
        return substitution


def unify_clause(substitution, input_clause, given_clause):
    """
    :param input_clause: Sentence to be unified
    :param given_clause: Sentence that will be used for unification
    :param substitution: Existing set of substitutions
    :return: substitution which modify the input_clause exactly like given_clause
    """
    if input_clause == given_clause:
        return substitution
    elif Parser.Utilities.is_a_variable(input_clause):
        return unify_variable(input_clause, given_clause,
                              substitution)
    elif Parser.Utilities.is_a_variable(given_clause):
        return unify_variable(given_clause, input_clause,
                              substitution)
    elif Parser.Utilities.is_object_of(given_clause,
                                       Parser.Sentence) and \
            Parser.Utilities.is_object_of(
                input_clause, Parser.Sentence):
        if input_clause.operator != given_clause.operator:
            raise Exception
        return unify_clause(
            unify_clause(input_clause.operator, given_clause.operator,
                         substitution), input_clause.sub_expr,
            given_clause.sub_expr)
    elif input_clause.__class__.__name__ in (
            'list', 'tuple') and given_clause.__class__.__name__ in (
            'list',
            'tuple' and len(given_clause) == len(input_clause)):
        if (len(input_clause) != len(given_clause)) or  not input_clause or not given_clause:
            return {}
        return unify_clause(
            unify_clause(substitution, input_clause[0],
                         given_clause[0]), input_clause[1:],
            given_clause[1:])
    else:
        return {}

