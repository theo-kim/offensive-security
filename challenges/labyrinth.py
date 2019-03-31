A = [None, None, 227]
B = [None, None, 505]
C = [None, None, 1128]
D = [None, None, 531]
E = [None, None, 289]
F = [None, None, 937]
G = [None, None, 410]
H = [None, None, 314]
I = [None, None, 866]
J = [None, None, 710]

A[0] = C
A[1] = G
B[0] = E
B[1] = D
C[0] = D
C[1] = G
D[0] = I
D[1] = D
E[0] = F
E[1] = H
F[0] = A
F[1] = F
G[0] = J
G[1] = A
H[0] = A
H[1] = J
I[0] = J
I[1] = B
J[0] = J
J[1] = D

instr = ["L"]
target = 9595

def solve(moves) :
    start = A
    curr = start
    summed = 0

    for i in moves :
        summed += curr[2]
        if i == "L" :
            curr = curr[0]
        elif i == "R" :
            curr = curr[1]

    return summed

def recursemaze (moves) :
    if (len(moves) > 17) :
        return -1
    else :
        mine = solve(moves)

        if (mine == target) :
            print("Found it")
            print("".join(moves))
            exit()
        
        recursemaze(moves + ["L"])
        recursemaze(moves + ["R"])
        

recursemaze(["L"])
recursemaze(["R"])