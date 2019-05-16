import itertools

class ASTNode(object):
    CONST0      = 0
    CONST1      = 1
    INPUT       = 2
    AND_GATE    = 3
    NOT_GATE    = 4
    BUF_GATE    = 5
    OR_GATE     = 6
    XOR_GATE    = 7
    # The following may not be implemented.
    XNOR_GATE   = 8
    NAND_GATE   = 9
    NOR_GATE    = 10
    AOI_GATE    = 11

    # Constructor.
    def __init__(self, t):
        "Construct an abstract ASTNode. Should never be called directly."
        self.node_type = t
        self.fanins = ()
        self.name = None
        self.value = None
        self.hash_code = None

    # Matching functions for node types.

    def is_aoi_gate(self):
        "check if the gate is aoi gate or not"
        return self.node_type == ASTNode.AOI_GATE
    def is_const0(self):
        "Is this a constant 0?"
        return self.node_type == ASTNode.CONST0
    def is_const1(self):
        "Is this a constant 1?"
        return self.node_type == ASTNode.CONST1
    def is_const(self):
        "Is this any type of constant?"
        return self.is_const0() or self.is_const1()
    def is_input(self):
        "Is this an input node?"
        return self.node_type == ASTNode.INPUT
    def is_and_gate(self):
        "Is this an and gate?"
        return self.node_type == ASTNode.AND_GATE
    def is_not_gate(self):
        "Is this a not gate?"
        return self.node_type == ASTNode.NOT_GATE
    def is_buf_gate(self):
        "Is this a buffer? (output = input)?"
        return self.node_type == ASTNode.BUF_GATE
    def is_or_gate(self):
        "Is this an or gate?"
        return self.node_type == ASTNode.OR_GATE
    def is_xor_gate(self):
        "Is this an eXclusive or gate?"
        return self.node_type == ASTNode.XOR_GATE
    def is_xnor_gate(self):
        "Is this an eXclusive nor gate?"
        return self.node_type == ASTNode.XNOR_GATE
    def is_nand_gate(self):
        "Is this a nand gate?"
        return self.node_type == ASTNode.NAND_GATE
    def is_nor_gate(self):
        "Is this a nor gate?"
        return self.node_type == ASTNode.NOR_GATE

    # Operator overloading.
    def __and__(self, other):
        "Overload a & b"
        return AndGate(self, other)
    def __or__(self, other):
        "Overload a | b"
        return OrGate(self, other)
    def __invert__(self):
        "Overload ~a"
        return NotGate(self)
    def __xor__(self, other):
        "Overload a ^ b"
        return XorGate(self, other)
    def __ne__(self, other):
        "Overload a != b. Just delegates to __eq__ in subclasses."
        return not self.__eq__(other)
    def __eq__(self, other):
        "Is this node equal to 'other'?"
        return other.node_type == self.node_type and other.fanins == self.fanins
    def __hash__(self):
        "Hashcode for this node."
        if self.hash_code is None:
            self.hash_code = hash((self.node_type, self.fanins))
        return self.hash_code
    def __repr__(self):
        "repr just defaults to str."
        return str(self)

    # Utility methods.
    def simplify(self):
        "Simplifier. Just constant propagation for now."
        return self

    def support(self):
        stack = [self]
        support = set() # Track list of support nodes.
        visited = set() # Track visited nodes.
        # This is pretty standard DFS.
        while len(stack) > 0:
            n = stack.pop()
            if n in visited: continue
            visited.add(n)
            # Add to support?
            if n.is_input(): support.add(n)
            # Visit child nodes.
            for f in n.fanins: stack.append(f)
        return support

class Const0Node(ASTNode):
    def __init__(self):
        "Construct a constant 0 node."
        ASTNode.__init__(self, ASTNode.CONST0)
        self.value = 0

    def __str__(self):
        "Return a string representation of this node."
        return '0'


class Const1Node(ASTNode):
    def __init__(self):
        "Construct a constant 1 node."
        ASTNode.__init__(self, ASTNode.CONST1)
        self.value = 1
    def __str__(self):
        "Return a string representation of this node."
        return '1'

class InputNode(ASTNode):
    def __init__(self, name):
        "Construct an input node."
        ASTNode.__init__(self, ASTNode.INPUT)
        self.name = name
    def __str__(self):
        "Return a string representation of this node."
        return self.name
    def __hash__(self):
        "Hashcode for this node."
        if self.hash_code is None:
            self.hash_code = hash((self.node_type, self.fanins, self.name))
        return self.hash_code
    def __eq__(self, other):
        "Is this node equal to 'other'?"
        return other.node_type == self.node_type and other.name == self.name

class AndGate(ASTNode):
    def __init__(self, *fanins):
        "Construct an and gate."
        ASTNode.__init__(self, ASTNode.AND_GATE)
        assert len(fanins) >= 2
        self.fanins = tuple(fanins[:])
    def __str__(self):
        "Return a string representation of this node."
        return '(%s)' % (' & '.join('%s' % str(gi) for gi in self.fanins))
    def simplify(self):
        fanins = [f.simplify() for f in self.fanins]
        fanins0 = [f for f in fanins if f.is_const0()]
        faninsP = [f for f in fanins if not f.is_const1()]
        if len(fanins0) > 0: return Const0Node()
        elif len(faninsP) == 0: return Const1Node()
        elif len(faninsP) == 1: return faninsP[0]
        else: return AndGate(*faninsP)

class NotGate(ASTNode):
    def __init__(self, *fanins):
        "Construct a not gate."
        ASTNode.__init__(self, ASTNode.NOT_GATE)
        assert len(fanins) == 1
        self.fanins = tuple(fanins[:])
    def __str__(self):
        "Return a string representation of this node."
        return '~(%s)' % str(self.fanins[0])
    def simplify(self):
        assert len(self.fanins) == 1
        f0 = self.fanins[0].simplify()
        if f0.is_const0(): return Const1Node()
        elif f0.is_const1(): return Const0Node()
        else: return NotGate(f0)

class BufGate(ASTNode):
    def __init__(self, *fanins):
        "Construct a not gate."
        ASTNode.__init__(self, ASTNode.BUF_GATE)
        assert len(fanins) == 1
        self.fanins = tuple(fanins[:])
    def __str__(self):
        "Return a string representation of this node."
        return '~(%s)' % str(self.fanins[0])
    def simplify(self):
        assert len(self.fanins) == 1
        f0 = self.fanins[0].simplify()
        if f0.is_const0(): return Const0Node()
        elif f0.is_const1(): return Const1Node()
        else: return BufGate(f0)

class OrGate(ASTNode):
    def __init__(self, *fanins):
        "Construct an or gate."
        ASTNode.__init__(self, ASTNode.OR_GATE)
        assert len(fanins) >= 2
        self.fanins = fanins[:]
    def __str__(self):
        "Return a string representation of this node."
        return '(%s)' % (' | '.join('%s' % str(gi) for gi in self.fanins))
    def simplify(self):
        fanins = [f.simplify() for f in self.fanins]
        fanins1 = [f for f in fanins if f.is_const1()]
        faninsP = [f for f in fanins if not f.is_const0()]
        if len(fanins1) > 0: return Const1Node()
        elif len(faninsP) == 0: return Const0Node()
        elif len(faninsP) == 1: return faninsP[0]
        else: return OrGate(*faninsP)


class XorGate(ASTNode):
    def __init__(self, *fanins):
        "Construct a eXclusive or gate."
        ASTNode.__init__(self, ASTNode.XOR_GATE)
        assert len(fanins) == 2
        self.fanins = tuple(fanins[:])
    def __str__(self):
        "Return a string representation of this node."
        s0 = str(self.fanins[0])
        s1 = str(self.fanins[1])
        return '(%s ^ %s)' % (s0, s1)
    def simplify(self):
        assert len(self.fanins) == 2
        f0 = self.fanins[0].simplify()
        f1 = self.fanins[1].simplify()
        if f0.is_const() and f1.is_const():
            r = self.f0.value ^ self.f1.value
            if r == 0: return Const0Node()
            elif r == 1: return Const1Node()
            else: assert False
        elif f0.is_const():
            if f0.value == 0: return f1
            elif f0.value == 1: return NotGate(f1)
            else: assert False
        elif f1.is_const():
            if f1.value == 0: return f0
            elif f1.value == 1: return NotGate(f0)
            else: assert False
        else:
            return XorGate(f0, f1)

class XnorGate(ASTNode):
    def __init__(self, *fanins):
        "Construct an eXclusive nor gate."
        ASTNode.__init__(self, ASTNode.XNOR_GATE)
        assert len(fanins) == 2
        self.fanins = tuple(fanins[:])
    def __str__(self):
        fanin_str = ', '.join(str(fi) for fi in self.fanins)
        return "xnor(%s)" % (fanin_str)

class NandGate(ASTNode):
    def __init__(self, *fanins):
        "Construct a nand gate."
        ASTNode.__init__(self, ASTNode.NAND_GATE)
        assert len(fanins) >= 2
        self.fanins = tuple(fanins[:])
    def __str__(self):
        fanin_str = ', '.join(str(fi) for fi in self.fanins)
        return "nand(%s)" % (fanin_str)

class NorGate(ASTNode):
    def __init__(self, *fanins):
        "Construct a nor gate."
        ASTNode.__init__(self, ASTNode.NOR_GATE)
        assert len(fanins) >= 2
        self.fanins = tuple(fanins[:])
    def __str__(self):
        fanin_str = ', '.join(str(fi) for fi in self.fanins)
        return "nor(%s)" % (fanin_str)

def notEqual(n1, n2):
    return XorGate(n1, n2)

def xnor(n1, n2):
    return XnorGate(n1, n2)

def equal(n1, n2):
    return xnor(n1, n2)

def nand(*ns):
    return NandGate(*ns)

def nor(*ns):
    return NorGate(*ns)
