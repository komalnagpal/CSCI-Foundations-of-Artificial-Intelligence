import resolver.Unifier as Unifier

from preprocessor.Parser import Sentence,Utilities
from preprocessor.CNFConverter import CNFConverter

str1 = Utilities.parse_expr("D(y)")
str2 = Utilities.parse_expr("D(x)")
# print(Unifier.unify_clause({},str1,str2))
# if Utilities.is_not_a_variable(str1):
#     print("ckds")

# a = Utilities.parse_expr('~Coyote(x)|~Roadrunner(y)|~Chase(x,y)|Catch(x,y)|Frustrated(x)')
# a = Utilities.parse_expr('~A(x) | ~B(x) | ~C(x)')
a= Utilities.parse_expr("~B(Bob, v_4)")
b= Utilities.parse_expr("B(John, Alice)| K(v,u) & O(u,i)")
cf = CNFConverter()
# print(cf.get_cnf(a))
print(Utilities.fetch_conjunction_clauses(b))
print(Unifier.unify_clause({},a,b))

def subst(s, x):
    """Substitute the substitution s into the expression x.
    >>> subst({x: 42, y:0}, F(x) + y)
    (F(42) + 0)
    """
    if isinstance(x, list):
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([subst(s, xi) for xi in x])
    elif not isinstance(x, Sentence):
        return x
    elif Utilities.is_logic_variable_symbol(x.operator):
        return s.get(x, x)
    else:
        return Sentence(x.operator, *[subst(s, arg) for arg in x.sub_expr])


t = subst({'v_4':'Alice'},a)
# print(t)

