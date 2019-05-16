from __future__ import print_function
import math
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
    n = 9
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
    print(temp)
    # Rows and columns should have unique numbers
    for i in range(n):
        for j in range(0,n-1,1):
            for k in range(j+1,n,1):
                for l in range(bn):
                    clause = [-node2literal[i][j][l], -node2literal[i][k][l]]  # for row
                    clause2 = [-node2literal[j][i][l], -node2literal[k][i][l]] # for column
                    S.addClause(*clause)
                    S.addClause(*clause2)
                    clause = []
                    clause2 = []


    # each element of matrix should have only one variable as one
    for i in range(n):
        for j in range(n):
            clause =[]
            for k in range(bn):
                clause.append(node2literal[i][j][k])
            S.addClause(*clause)
            clause *= -1
            for k in range(bn):
                clause[k] *= -1
                S.addClause(*clause)
                clause[k] *= -1
            
    # for each box in matrix
    for i in range(num_boxes):
        for j in range(num_boxes):
            clause =[]
    r = S.solve()
    print(r)
    for i in range(3):
        for j in range(3):
            print(S.modelValue(node2literal[i][j][0]),S.modelValue(node2literal[i][j][1]),S.modelValue(node2literal[i][j][2]))
    print(box_value(S,node2literal,0,0),box_value(S,node2literal,0,1),box_value(S,node2literal,0,2))
    print(box_value(S,node2literal,1,0),box_value(S,node2literal,1,1),box_value(S,node2literal,1,2))
    print(box_value(S,node2literal,2,0),box_value(S,node2literal,2,1),box_value(S,node2literal,2,2))


def main():
    #uncomment test1() to run 3x3 and comment testn()
    #for 3x3 matrix
    #test1()
    # for nxn matrix
    testn()
    print ('Tests PASSED.')

if __name__ == '__main__':
    main()
