from __future__ import print_function
import math
import numpy as np
from solver import Solver
import ckt
import itertools
import adapter

def box_value(S,node2literal , i,j):
    count = 1
    for k in range(3):
        if S.modelValue(node2literal[i][j][k]):
            return count
        count = count + 1
def createVariables(n):
    return [ckt.InputNode('x%d' %i) for i in range(n)]

def test1():
    # Create a bunch of simple circuits.
    S = Solver()
    node2literal = [[[0 for k in range(3)] for j in range(3)] for i in range(3)]
    #print(node2literal[0][0][0])
    for i in range(3):
        for j in range(3):
            for k in range(3):
                #print(node2literal[i][j][k])
                node2literal[i][j][k] = S.newVar()
    clause = []
    clause2 = []
    temp = []
    print(temp)
    # Rows and columns should have unique numbers
    for i in range(3):
        for j in range(0,2,1):
            for k in range(j+1,3,1):
                for l in range(3):
                    clause = (-node2literal[i][j][l], -node2literal[i][k][l])  # for row
                    clause2 = (-node2literal[j][i][l], -node2literal[k][i][l]) # for column
                    S.addClause(*clause)
                    S.addClause(*clause2)
                    temp.append(clause)
                    clause = []
                    clause2 = []


    # each box should have only one variable as one
    for i in range(3):
        for j in range(3):
            clause = [node2literal[i][j][0], node2literal[i][j][1], node2literal[i][j][2]]
            S.addClause(*clause)
            clause = [-node2literal[i][j][0], -node2literal[i][j][1], node2literal[i][j][2]]
            S.addClause(*clause)
            clause = [-node2literal[i][j][0], node2literal[i][j][1], -node2literal[i][j][2]]
            S.addClause(*clause)
            clause = [node2literal[i][j][0], -node2literal[i][j][1], -node2literal[i][j][2]]
            S.addClause(*clause)
    print(temp)
    r = S.solve()
    print(r)
    for i in range(3):
        for j in range(3):
            print(S.modelValue(node2literal[i][j][0]),S.modelValue(node2literal[i][j][1]),S.modelValue(node2literal[i][j][2]))
    print(box_value(S,node2literal,0,0),box_value(S,node2literal,0,1),box_value(S,node2literal,0,2))
    print(box_value(S,node2literal,1,0),box_value(S,node2literal,1,1),box_value(S,node2literal,1,2))
    print(box_value(S,node2literal,2,0),box_value(S,node2literal,2,1),box_value(S,node2literal,2,2))







def testn(n):
    if n!=(n**0.5)**2:
        print("n should be square of an integer")
    num_boxes = int(n**(0.5))
    S = Solver()
    bn = int(math.ceil(math.log(n,2)))
    print(bn)
    variables = createVariables(bn*n*n)
    node2literal_map = {}
    node2literal = [[[0 for k in range(bn)] for j in range(n)] for i in range(n)]
    #print(node2literal[0][0][0])
    for i in range(n):
        for j in range(n):
            for k in range(bn):
                #print(node2literal[i][j][k])
                node2literal[i][j][k] = S.newVar()
                node2literal_map[variables[i*n*bn + j*bn + k]] = node2literal[i][j][k]
    assumptions = []
    clause = []
    clause2 = []
    temp = []
    # Rows and columns should have unique numbers
    for i in range(n):
        for j in range(0,n-1,1):
            for k in range(j+1,n,1):
                ckt1 = ckt.Const0Node()
                ckt2 = ckt.Const0Node()
                for l in range(bn):
                    ckt0 = variables[i*n*bn + j*bn + l] ^ variables[i*n*bn + k*bn+ l]
                    ckt1 = ckt1 | ckt0
                    ckt0 = variables[j*n*bn + i*bn + l] ^ variables[k*n*bn + i*bn+ l]
                    ckt2 = ckt2 | ckt0
#                    clause = [node2literal[i][j][l], -node2literal[i][k][l]]  # for row
#                    S.addClause(*clause)
#                    print(clause)
#                    clause = [-node2literal[i][j][l], node2literal[i][k][l] ]
#                    S.addClause(*clause)
#                    print(clause)
#                    clause2 = [node2literal[j][i][l], -node2literal[k][i][l]] # for column
#                    S.addClause(*clause2)
#                    print(clause2)
#                    clause2 = [-node2literal[j][i][l], node2literal[k][i][l]]
#                    S.addClause(*clause2)
#                    print(clause2)
                ckt1 = ckt1 & ckt2
                def newVar(p):
                    return S.newVar()
                clauses = adapter.circuitToCNF(ckt1,node2literal_map,newVar)
                assumptions.append(node2literal_map[ckt1])
                #print(ckt1)
                for c in clauses:
                    S.addClause(*c)
    #r = S.solve(*assumptions)
    #print(r)
    #PrintSudoku(S,node2literal,n,bn)
    #  limit each element in range 1 to n if math.ceil(math.log(n,2)) != math.floor(math.log(n,2))
    if (n != 2**bn):
        #print("in if condition")
        for i in range(n):
            for j in range(n):
                clause =[]
                for l in range(n, 2**bn, 1):
                    binary = bin(l)
                    for k in range(bn):
                        if (binary[k+2] == '0'):
                            clause.append(node2literal[i][j][k])
                        else:
                            clause.append(-node2literal[i][j][k])
                    S.addClause(*clause)
                    #print(clause)
                    clause = []


    # for each box in matrix every element should be unique
    nparray = np.array(node2literal)
    for b1 in range(num_boxes):
        for b2 in range(num_boxes):
            #temp stores elements of each box in sudoku to have unique numbers
            temp = nparray[b1*num_boxes:(b1+1)*num_boxes, b2*num_boxes:(b2+1)*num_boxes]
            # all possibel combinations of elements to check their uniqueness
            for i in range(b1*num_boxes,(b1+1)*num_boxes ,1):
                for j in range(b2*num_boxes,(b2+1)*num_boxes ,1):
                    for k  in range(b1*num_boxes,(b1+1)*num_boxes,1):
                        if k ==i :
                            continue
                        for l in range(b2*num_boxes,(b2+1)*num_boxes,1):
                            if l == j:
                                continue
                            ckt1 = ckt.Const0Node()
                            for m in range(bn):
                                ckt0 = variables[i*n*bn + j*bn + m] ^ variables[k*n*bn + l*bn +m]
                                ckt1 = ckt1 | ckt0
                            def newVar(p):
                                return S.newVar()
                            clauses = adapter.circuitToCNF(ckt1,node2literal_map,newVar)
                            assumptions.append(node2literal_map[ckt1])
                            for c in clauses:
                                S.addClause(*c)







    #print(nparray)

    while True:
        print("Pleasr enter entries of sudoku puzzle in format \"row col value\" OR enter anyhing else to start sudoku solver")
        input = raw_input()
        input = input.split()
        if len(input)!=3:
            print("solving sudoku please wait")
            break
        row = int(input[0])-1
        col = int(input[1])-1
        value = int(input[2]) -1
        print(row,col,value)
        #limit checking of entered values
        assert (row>=0 & row<n)
        assert (col>=0 & col<n)
        assert (value >=0 & value<n)
        bin_value = bin(value)
        l = len(bin_value) - 1
        for k in range(bn):
            if l<=1:
                assumptions.append(-node2literal[row][col][bn-k-1])
            else:
                if bin_value[l]=='0':
                    assumptions.append(-node2literal[row][col][bn-k-1])
                elif bin_value[l]=='1':
                    assumptions.append(node2literal[row][col][bn-k-1])
                else:
                    assert 0
                l = l-1

    print("length of assumptions ",len(assumptions))
    print("length of node2literal_map ",len(node2literal_map))
    r = S.solve(*assumptions)
    if not r:
        print("No solution found")
        return

    #print(r)
    #print(assumptions)
    PrintSudoku(S,node2literal,n,bn)

def PrintSudoku(S,map,n,bn):
    out = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            for k in range(bn):
                #print(S.modelValue(map[i][j][k]))
                if S.modelValue(map[i][j][k]):
                    out[i][j] += 2**(bn-k-1)
    out += 1
    print("solution to sudoku puzzle")
    print(out)
    unique, counts = np.unique(out, return_counts=True)
    print(dict(zip(unique, counts)))
def main():
    #uncomment test1() to run 3x3 and comment testn()
    #for 3x3 matrix
    #test1()
    # for nxn matrix
    n = input("Enter size (square of an integer) of sudoku puzzle: ")
    n = int(n)
    testn(n)
    print ('Tests PASSED.')

if __name__ == '__main__':
    main()
