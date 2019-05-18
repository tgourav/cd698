from __future__ import print_function
import math
import numpy as np
from solver import Solver

def box_value(S,node2literal , i,j):
    count = 1
    for k in range(3):
        if S.modelValue(node2literal[i][j][k]):
            return count
        count = count + 1


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

def testn():
    n = 4
    num_boxes = int(n**(0.5))
    S = Solver()
    bn = int(math.ceil(math.log(n,2)))
    print(bn)
    node2literal = [[[0 for k in range(bn)] for j in range(n)] for i in range(n)]
    #print(node2literal[0][0][0])
    for i in range(n):
        for j in range(n):
            for k in range(bn):
                #print(node2literal[i][j][k])
                node2literal[i][j][k] = S.newVar()
    clause = []
    clause2 = []
    temp = []
    # Rows and columns should have unique numbers
    for i in range(n):
        for j in range(0,n-1,1):
            for k in range(j+1,n,1):
                for l in range(bn):
                    clause = [node2literal[i][j][l], -node2literal[i][k][l]]  # for row
                    S.addClause(*clause)
                    print(clause)
                    clause = [-node2literal[i][j][l], node2literal[i][k][l] ]
                    S.addClause(*clause)
                    print(clause)
                    clause2 = [node2literal[j][i][l], -node2literal[k][i][l]] # for column
                    S.addClause(*clause2)
                    print(clause2)
                    clause2 = [-node2literal[j][i][l], node2literal[k][i][l]]
                    S.addClause(*clause2)
                    print(clause2)
    for i in range(n):
        for j in range(0,n-1,1):
            clause = []
            for l in range(bn):
                clause.append(node2literal[i][j][l])
            S.addClause(*clause)

    #  limit each element in range 1 to n if math.ceil(math.log(n,2)) != math.floor(math.log(n,2))
    if (n != 2**bn):
        for i in range(n):
            for j in range(n):
                clause =[]
                for l in range(n, 2**bn, 1):
                    binary = bin(l)
                    for k in range(bn):
                        if (binary[k+2] == '0'):
                            clause.append(-node2literal[i][j][k])
                        else:
                            clause.append(node2literal[i][j][k])
                    S.addClause(*clause)
                    print(clause)
                    clause = []

    # Currently working
    r = S.solve()
    print(r)
    PrintSudoku(S,node2literal,n,bn)
    # for each box in matrix
    nparray = np.array(node2literal)
    for b1 in range(num_boxes):
        for b2 in range(num_boxes):
            temp = nparray[b1*num_boxes:(b1+1)*num_boxes, b2*num_boxes:(b2+1)*num_boxes]

            #print(b1*num_boxes, (b1+1)*num_boxes, b2*num_boxes,(b2+1)*num_boxes)
            #print(temp)
            #print(np.reshape(temp,(9,4)).tolist())
            temp = np.reshape(temp,(4,2)).tolist()
            for j in range(0,len(temp)-1,1):
                for k in range(i,len(temp),1):
                    for l in range(bn):
                        clause = [temp[j][l], temp[k][l]]  # for row
                        S.addClause(*clause)
                        print(clause)
                        clause = [-temp[j][l], -temp[k][l] ]
                        S.addClause(*clause)
                        print(clause)


    #print(nparray)

    # ToDo limit each element in range 1 to n if math.ceil(math.log(n,2)) != math.floor(math.log(n,2))
    r = S.solve()
    print(r)
    PrintSudoku(S,node2literal,n,bn)

def PrintSudoku(S,map,n,bn):
    out = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            for k in range(bn):
                #print(S.modelValue(map[i][j][k]))
                if S.modelValue(map[i][j][k]):
                    out[i][j] += 2**(bn-k-1)
    print(out)
def main():
    #uncomment test1() to run 3x3 and comment testn()
    #for 3x3 matrix
    #test1()
    # for nxn matrix
    testn()
    print ('Tests PASSED.')

if __name__ == '__main__':
    main()
