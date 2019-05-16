from __future__ import print_function

from ckt import ASTNode

def _simulate(node, input_assignment, memo):
    if node in memo:
        return memo[node]

    vins = [_simulate(fi, input_assignment, memo) for fi in node.fanins]
    if node.node_type == ASTNode.CONST0:
        v = 0
    elif node.node_type == ASTNode.CONST1:
        v = 1
    elif node.node_type == ASTNode.INPUT:
        if node not in input_assignment:
            raise ValueError("Model doesn't assign value to input: %s" % str(node))
        v = input_assignment[node]
    elif node.node_type == ASTNode.AND_GATE:
        v = reduce(lambda x,y: x and y, vins, 1)
    elif node.node_type == ASTNode.NOT_GATE:
        v = not vins[0]
    elif node.node_type == ASTNode.BUF_GATE:
        v = vins[0]
    elif node.node_type == ASTNode.OR_GATE:
        v = reduce(lambda x,y: x or y, vins, 0)
    elif node.node_type == ASTNode.XOR_GATE:
        v = vins[0] != vins[1]
    elif node.node_type == ASTNode.XNOR_GATE:
        v = vins[0] == vins[1]
    elif node.node_type == ASTNode.NAND_GATE:
        v = not reduce(lambda x,y: x and y, vins, 1)
    elif node.node_type == ASTNode.NOR_GATE:
        v = not reduce(lambda x,y: x or y, vins, 0)
    else:
        assert False, node.node_type

    assert v == 0 or v == 1
    memo[node] = v
    return v

def simulate(node, input_assignment):
    memo = {}
    return _simulate(node, input_assignment, memo)

