import ckt
import ckteq
from ckt import ASTNode

class AOIGate(ASTNode):
    def __init__(self, *fanins):
        "Construct an AOI gate"
        ASTNode.__init__(self, ASTNode.AOI_GATE)
        assert len(fanins) == 3
        self.fanins = tuple(fanins[:])
    def __str__(self):
        "Return a string represntation of this node"
        return '(%s)' % (' &|~ '.join('%s' % str(gi) for gi in self.fanins))
    def simplify(self):
        fanins = [f.simplify() for f in self.fanins]
        if fanins[0].is_const0() or fanins[1].is_const0():
            if fanins[2].is_const0():
                return ckt.Const1Node()
            elif fanins[2].is_const1():
                return ckt.Const0Node()
            else:
                return ckt.NotGate(fanins[2])
        elif fanins[0].is_const1() and fanins[1].is_const1():
            return ckt.Const0Node()
        elif fanins[2].is_const1():
            return ckt.Const0Node()
        elif fanins[2].is_const0():
            return ckt.NotGate(ckt.AndGate(fanins[0], fanins[1]))
        else:
            return AOIGate(*fanins)

def gateToCNF(g, lOut, lFanins):
    if g.is_aoi_gate():
        #TODO: Fill in the clauses for an AOI gate here
        return [[-lFanins[2],-lOut],[lFanins[1],lFanins[2],lOut],[lFanins[0],lFanins[2],lOut],[-lFanins[0],-lFanins[1],-lOut]]

    else:
        raise NotImplementedError("Should be unreachable")

# Assume that the circuit is made of AND, OR, NOT and Input nodes
oneAOI = ckt.Const1Node()
zeroAOI = AOIGate(ckt.Const1Node(),ckt.Const1Node(),ckt.Const1Node())
def aoi_and_gate(ck):
    #return aoi_not_gate(AOIGate(convertToAOI(ck.fanins[0]),convertToAOI(ck.fanins[1]),zeroAOI))
    temp = oneAOI
    for fanin in ck.fanins:
        nand = AOIGate(temp, fanin, zeroAOI)
        temp = aoi_not_gate(nand)
    return temp
    #temp1 = AOIGate(ck.fanins[0], ck.fanins[1],zeroAOI)
    #temp2 = ckt.NotGate(temp1.fanins)
    #return aoi_not_gate(temp2)


def aoi_or_gate(ck):
#    print "or gate ", ck.fanins
    #return aoi_not_gate(AOIGate(convertToAOI(ck.fanins[0]),oneAOI,convertToAOI(ck.fanins[1])))
    temp = zeroAOI
    for fanin in ck.fanins:
        nand = AOIGate(temp, temp, fanin)
        temp = aoi_not_gate(nand)
    return temp
    #temp2 = AOIGate(ck.fanins[0],oneAOI, ck.fanins[1])
    #temp3 = ckt.NotGate(temp2.fanins)
    #return aoi_not_gate(temp3)


def aoi_not_gate(ck):
    #print "not gate ", ck
    #return AOIGate(zeroAOI,zeroAOI,convertToAOI(ck.fanins[0]))
    return AOIGate(zeroAOI,zeroAOI, ck)

def convertToAOI(ck):
    # TODO: Convert the circuit ck into an equivalent circuit
    # consisting only of AOIGate() and Const1Node()

    if ck.is_const0():
        #print "const0"
        return  zeroAOI
    elif ck.is_const1():
        #print "const1"
        return  oneAOI
    elif ck.is_input():
        #print "input", ck
        return  ck
    elif ck.is_or_gate():
        #print "or", ck
        fanins = [convertToAOI(f) for f in ck.fanins]
        #print "to aoi fanins", fanins, len(fanins)
        ck1 = ckt.OrGate(*fanins)
        return  aoi_or_gate(ck1)
    elif ck.is_and_gate():
        #print "and", ck
        fanins = [convertToAOI(f) for f in ck.fanins]
        #print "to aoi fanins", fanins, len(fanins)
        ck1 = ckt.AndGate(*fanins)
        return  aoi_and_gate(ck1)
    elif ck.is_not_gate():
        #print "not", ck
        fanins = [convertToAOI(f) for f in ck.fanins]
        #print "to aoi fanins", fanins, len(fanins)
        ck1 = ckt.NotGate(*fanins)
        return  aoi_not_gate(ck1.fanins[0])
    else:
        #print "something is wrong"
        assert 0





def tests():
    def check_aoi_ckt(ck):
        stack = [ck]
        visited = set()
        while len(stack) > 0:
            n = stack.pop()
            #print n
            if n in visited: continue
            visited.add(n)
            #print "n ", n


            if not n.is_input():
                if not n.is_aoi_gate() and not n.is_const1():
                    return False
            for f in n.fanins: stack.append(f)
        return True

    a = ckt.InputNode('a')
    b = ckt.InputNode('b')
    f1 = (~a & b) | (a & ~b)
    #print "start "
    c = convertToAOI(f1)
    #print "End"
    #print "c", c




    #assert 0
    assert check_aoi_ckt(c)
    #print "simplify c ", c.simplify()
    assert ckteq.areEquivalent(f1, c.simplify())[0]

    f3 = f1 | ckt.Const0Node()
    c = convertToAOI(f3)
    assert check_aoi_ckt(c)
    assert ckteq.areEquivalent(f3, c.simplify())[0]

    f4 = f3 & ckt.Const1Node()
    c = convertToAOI(f4)
    assert check_aoi_ckt(c)
    assert ckteq.areEquivalent(f4, c.simplify())[0]


if __name__ == '__main__':
    tests()
    print ("TESTS PASSED")
