import ckt
from aoi import gateToCNF as f
import aoi
def circuitToCNF(root_node, node2literal_map, newVar):
    """Convert a circuit into a set of clauses. node2literal_map is a map
    from nodes to literals. newVar is a function that returns a new literal.
    This could just be the solver object's newVar method."""

    def getLiteral(n):
        """Helper function that returns a literal corresponding to a node.
        It creates a new literal using newVar if one doesn't already exist."""
        if n not in node2literal_map:
            node2literal_map[n] = newVar(n)
        return node2literal_map[n]

    queue = [root_node] # queue for BFS.
    visited = set() # empty set.
    clauses = []
    while len(queue) > 0:
        n = queue.pop(0)
        if n in visited:
            continue
        visited.add(n)
        # get the literal for the output node.
        output_lit = getLiteral(n)
        input_lits = [getLiteral(fi) for fi in n.fanins]
        for cl in gateToCNF(n, output_lit, input_lits):
            clauses.append(cl)
        for fi in n.fanins:
            queue.append(fi)
    return clauses

def gateToCNF(g, lOut, lFanins):
    """Return a list of clauses that encode the functionality of this gate.
    lOut is the literal corresponding to the output of the gate, while lFanins
    is a list of literals that corresponds to each of the inputs of this
    gate."""
    #print "g ", g
    if g.is_const0():
        return [[-lOut]]
    elif g.is_const1():
        return [[lOut]]
    elif g.is_input():
        return []
    elif g.is_not_gate():
        # Clauses for a NOT gate.
        return [[lFanins[0], lOut], [-lFanins[0], -lOut]]
    elif g.is_buf_gate():
        # Clauses for a buffer. (A buffer is a gate whose output = input.)
        return [[lFanins[0], -lOut], [-lFanins[0], lOut]]
    elif g.is_and_gate():
        #TODO: Fill in the clauses for an AND gate HERE
        #print "and gate"
        #print lFanins
        clauses = [[-f for f in lFanins]]
        #print clauses
        clauses[0].extend([lOut])
        #print lFanins
        #print clauses
        for f in lFanins:
            clauses.append([f,-lOut])
        #print clauses
        return clauses

    elif g.is_or_gate():
        #TODO: Fill in the clauses for an OR gate HERE
        clauses = [list(lFanins)]
        clauses[0].extend([-lOut])
        #print clauses
        #print lFanins
        for f in lFanins:
            clauses.append([-f,lOut])
        return clauses

    elif g.is_xor_gate():
        #TODO: Fill in the clauses for an XOR gate HERE
        return [[-lFanins[0],-lFanins[1],-lOut],[lFanins[0],lFanins[1],-lOut],[lFanins[0],-lFanins[1],lOut],[-lFanins[0],lFanins[1],lOut]]
    elif g.is_xnor_gate():
        #TODO: Fill in the clauses for an XNOR gate HERE
        return [[lFanins[0],lFanins[1],lOut],[-lFanins[0],lFanins[1],-lOut],[lFanins[0],-lFanins[1],-lOut],[-lFanins[0],-lFanins[1],lOut]]
    elif g.is_nand_gate():
        #TODO: Fill in the clauses for an NAND gate HERE
        clauses = [[-f for f in lFanins]]
        clauses[0].extend([-lOut])
        for f in lFanins:
            clauses.append([f,lOut])
        return clauses
    elif g.is_nor_gate():
        #TODO: Fill in the clauses for an NOR gate HERE
        clauses = [list(lFanins)]
        clauses[0].extend([lOut])
        for f in lFanins:
            clauses.append([-f,-lOut])
        return clauses
    elif g.is_aoi_gate():
        return aoi.gateToCNF(g, lOut, lFanins)
    else:
        # You DO NOT need to change this.
        raise NotImplementedError("Unknown gate: %s" % str(g))
