from __future__ import print_function

import sys
import ckt
import adapter
from solver import Solver
from ckteq import areEquivalent

def createVariables():
    "Return 32 Boolean variables that represent an IPv4 address."
    return [ckt.InputNode('x%d' % i) for i in range(32)]

def rulesToIndicatorFn(rules, xs):
    """Convert a set of firewall rules into an indicator function for the
    set of packets accepted by the firewall."""
    sop = ckt.Const0Node()
    for (A, B, C, D, n) in rules:
        W = D + C*256 + B*(256**2) + A*(256**3)
        cube = ruleToIndicatorFn(W, xs, n).simplify()
        sop = sop | cube
    return sop.simplify()

def ruleToIndicatorFn(W, xs, n):
    """Helper function that converts CIDR A.B.C.D/n tuple into a Boolean
    function that matches the set of addresses represented by the CIDR
    notation."""
    cube = ckt.Const1Node()
    for i in xrange(n):
        bit_index = 31 - i
        if (W >> bit_index) & 1:
            cube = cube & xs[bit_index]
        else:
            cube = cube & ~xs[bit_index]
    return cube

def firewallDifference(f1, f2):
    """Find the difference of two firewalls."""
    ########################################################################
    # TODO: Add your code here. You might find it helpful to create a few  #
    # helper functions.                                                    #
    ########################################################################
    variables = createVariables()
    rule1 = rulesToIndicatorFn(f1,variables)
    rule2 = rulesToIndicatorFn(f2,variables)
    root_node = rule1 & ~rule2

    S = Solver()
    So = Solver()

    node2literal_map = {}
    for v in variables:
        v1 = S.newVar()
        v2 = So.newVar()
        if v1==v2:
            node2literal_map[v] = v1
        else:
            print("error")
    def newVar(n):
        So.newVar()
        return S.newVar()
    clauses = adapter.circuitToCNF(root_node,node2literal_map, newVar)
    for c in clauses:
        S.addClause(*c)
        So.addClause(*c)
    liter_of_s = node2literal_map[root_node]
    diff = []
    while S.solve(liter_of_s):
        clause = []
        for v in variables:
            liter_of_v = node2literal_map[v]
            if S.modelValue(liter_of_v):
                clause.append(liter_of_v)
            else:
                clause.append(-liter_of_v)
        # How to find n
        i = 1
        while True:
            new_cnf = [-liter_of_s] + clause[i:]
            #print(new_cnf)
            r1 = So.solve(*new_cnf)
            if r1 ==True or i == len(clause)+1:
                i = i-1
                break
            i = i+1
        cube = clause[i:]
        n = len(clause) - i
        if len(cube)>0:
            clauses = [-c for c in cube]
            S.addClause(*clauses)
        # How to get A B C D
        i=0
        w =0
        for c in clause:
            if c >0:
                w = w | (2**(i))
            i = i+1
        A = (w >> 24) & 0xff
        B = (w >> 16) & 0xff
        C = (w >> 8) & 0xff
        D = (w) & 0xff
        diff.append((A,B,C,D,n))
    #print(diff)

    return diff

def areFirewallsEquivalent(f1, f2):
    """Utility function that uses ckteq.areEquivalent to check if two
    firewalls are equivalent."""
    xs = createVariables()
    a1 = rulesToIndicatorFn(f1, xs)
    a2 = rulesToIndicatorFn(f2, xs)
    (r, _) = areEquivalent(a1, a2)
    return r

def printRules(rules, f=sys.stdout):
    """Utility function that pretty-prints a firewall."""
    for (A, B, C, D, n) in rules:
        print ('%d.%d.%d.%d/%d' % (A, B, C, D, n), file=f)
    f.flush()

def test1():
    f1 = [(14, 110, 0, 0, 15), (15, 110, 0, 0, 15), (30, 216, 0, 0, 13),
          (31, 208, 0, 0, 12), (94, 83, 236, 144, 30), (95, 82, 236, 144, 30),
          (112, 0, 0, 0, 5), (128, 0, 0, 0, 5), (136, 10, 0, 0, 15),
          (136, 12, 0, 0, 16), (163, 217, 224, 0, 20), (173, 211, 0, 0, 17),
          (174, 210, 0, 0, 17), (176, 56, 0, 0, 15), (176, 58, 0, 0, 17),
          (176, 128, 0, 0, 9), (177, 58, 0, 0, 15), (184, 0, 0, 0, 6),
          (213, 184, 0, 0, 14), (214, 180, 0, 0, 14), (241, 31, 223, 104, 29),
          (241, 31, 224, 104, 30), (245, 171, 224, 0, 19), (245, 172, 224, 0, 19)]

    f2 = [(14, 110, 0, 0, 15), (31, 208, 0, 0, 12), (94, 83, 235, 144, 31),
          (94, 83, 236, 144, 30), (95, 82, 236, 144, 30), (112, 0, 0, 0, 5),
          (128, 0, 0, 0, 4), (163, 216, 224, 0, 19), (163, 217, 224, 0, 19),
          (174, 210, 0, 0, 17), (176, 58, 0, 0, 17), (176, 128, 0, 0, 9),
          (177, 0, 0, 0, 8), (184, 0, 0, 0, 6), (213, 182, 0, 0, 15),
          (213, 184, 0, 0, 14), (241, 31, 223, 104, 29), (241, 31, 224, 104, 30),
          (245, 172, 240, 0, 20), (249, 82, 96, 0, 20), (249, 83, 96, 0, 20)]

    d12 = [(30, 216, 0, 0, 13), (15, 110, 0, 0, 15), (245, 172, 224, 0, 20),
           (245, 171, 224, 0, 19), (176, 56, 0, 0, 15), (173, 211, 0, 0, 17),
           (214, 180, 0, 0, 14)]

    e12 = firewallDifference(f1, f2)
    assert areFirewallsEquivalent(e12, d12)

    f1 = [(5, 176, 176, 168, 31), (6, 176, 176, 168, 31), (10, 0, 0, 0, 7),
          (14, 19, 32, 0, 20), (19, 164, 203, 68, 30), (19, 165, 202, 70, 31),
          (20, 165, 202, 70, 31), (53, 209, 0, 0, 16), (54, 210, 0, 0, 16),
          (56, 214, 174, 96, 27), (56, 214, 175, 96, 27), (57, 213, 174, 96, 27),
          (68, 0, 0, 0, 6), (99, 71, 242, 160, 28), (112, 102, 185, 0, 24),
          (112, 103, 184, 0, 22), (113, 102, 184, 0, 22), (128, 0, 0, 0, 1)]

    f2 = [(5, 176, 176, 168, 31), (6, 176, 176, 168, 31), (6, 176, 177, 168, 31),
          (10, 0, 0, 0, 7), (14, 19, 32, 0, 19), (14, 20, 32, 0, 20),
          (19, 164, 203, 68, 30), (19, 165, 202, 70, 31), (54, 209, 0, 0, 16),
          (56, 213, 175, 96, 27), (56, 214, 174, 96, 27), (69, 0, 0, 0, 8),
          (76, 52, 32, 0, 21), (77, 52, 40, 0, 21), (77, 53, 32, 0, 20),
          (98, 72, 242, 160, 30), (99, 71, 242, 160, 28), (112, 102, 185, 0, 24),
          (112, 103, 184, 0, 22), (113, 102, 184, 0, 22), (128, 0, 0, 0, 1)]

    d12 = [(70, 0, 0, 0, 7), (68, 0, 0, 0, 8), (53, 209, 0, 0, 16),
           (57, 213, 174, 96, 27), (54, 210, 0, 0, 16), (20, 165, 202, 70, 31),
           (56, 214, 175, 96, 27)]

    e12 = firewallDifference(f1, f2)
    assert areFirewallsEquivalent(e12, d12)

if __name__ == '__main__':
    test1()
