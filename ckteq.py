from __future__ import print_function

import ckt
import adapter

from solver import Solver

from simulator import simulate

def areEquivalent(n1, n2):
    """This function should check whether the circuits represented by n1 and n2
    (both of which must be subclass of ASTNode) are equivalent.

    The function should return a tuple (eq, model). eq is a Boolean variable
    which is true when n1 and n2 are equivalent and false otherwise. 'model' is
    a dictionary that maps from InputNodes to {0, 1}.

    Note you can use the support() of a circuit node to get all of the InputNodes
    that the circuit "depends" on."""

    S = Solver()
    support1 = n1.support()
    support2 = n2.support()
    support = support1.union(support2)

    #########################################
    # TODO: FILL IN YOUR CODE HERE.
    root_node = n1 ^ n2
    #print (root_node)
    node2literal_map = {}
    def newVar(n):
        return S.newVar()
    clauses = adapter.circuitToCNF(root_node, node2literal_map, newVar)
    for clause in clauses:
        S.addClause(*clause)
    #########################################
    # Result is that everything is equivalent!
    literal = node2literal_map[root_node]
    # FIX this.
    r = S.solve(literal)
    # 'model' is None.
    #model = None
    if r == True:
        model = {}
        for s in support:
            literal_of_s = node2literal_map[s]
            model[s] = S.modelValue(literal_of_s)
    else:
        model = None
    return (not r, model)
    #########################################
    # Do not modify anything below this line.
    #########################################

def test1():
    # Create a bunch of simple circuits.
    a = ckt.InputNode('a')
    b = ckt.InputNode('b')
    f1 = (~a & b) | (a & ~b)
    f2 = (a ^ b)
    f3 = f2 | ckt.Const0Node()
    f4 = f3 & ckt.Const1Node()
    g2 = f2 | ckt.Const1Node()
    g3 = g2 & ckt.Const0Node()

    # A bunch of simple tests. All of these are equivalent.
    assert (areEquivalent(f1, f2))[0]
    assert (areEquivalent(f1, f3))[0]
    assert (areEquivalent(f1, f4))[0]
    assert (areEquivalent(f1, f3.simplify()))[0]
    assert (areEquivalent(f1, f4.simplify()))[0]
    assert (areEquivalent(g2.simplify(), ~g3.simplify()))[0]

    # the following tests are not.
    # but first we need a helper function.
    def checkNotEquivalent(f, g):
        (r, model) = areEquivalent(f, g)
        assert not r
        # simulate the inputs from the model
        f_s = simulate(f, model)
        g_s = simulate(g, model)
        # and ensure the circuits do in fact produce different outputs.
        assert f_s != g_s

    checkNotEquivalent(f1, g2)
    checkNotEquivalent(f1, g2.simplify())
    checkNotEquivalent(f2, g3.simplify())

def main():
    test1()
    print ('Tests PASSED.')

if __name__ == '__main__':
    main()
