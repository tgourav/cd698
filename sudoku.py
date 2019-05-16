from __future__ import print_function

import ckt
import adapter

from solver import Solver

from simulator import simulate

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


def main():
    test1()
    print ('Tests PASSED.')

if __name__ == '__main__':
    main()
