import argparse

def compare(Ai, Bj):
    if Ai == Bj:
        return m
    else:
        return d

def NeedlemanWunsch(A, B):
    nA = len(A)
    nB = len(B)
    F = [[_ * g for _ in range(0, nA + 1)]]
    for _ in range(1, nB + 1):
        row = [0] * (nA + 1)
        row[0] = _ * g
        F.append(row)

    for j in range(nB + 1):
        for i in range(nA + 1):
            if i == 0 and j == 0:
                F[j][i] = 0
            elif j == 0:
                F[j][i] = g * i
            elif i == 0:
                F[j][i] = g * j
            else:
                dm = F[j - 1][i - 1] + m if A[i - 1] == B[j - 1] else F[j - 1][i - 1] + d
                F[j][i] = max(F[j - 1][i] + g, F[j][i - 1] + g, dm)
    F = F
    WWtemp=[]
    ZZtemp=[]
    EnumerateAlignments(A, B, F, WWtemp, ZZtemp, W='', Z='')
    return WWtemp, ZZtemp

def EnumerateAlignments(A, B, F, WWtemp, ZZtemp, W, Z):
    i = len(A)
    j = len(B)
    if i == 0 and j == 0:
        WWtemp.append(W)
        ZZtemp.append(Z)
    elif i > 0 and j > 0:
        mm = compare(A[i - 1], B[j - 1])

        if F[j][i] == F[j - 1][i - 1] + mm:
            EnumerateAlignments(A[:i - 1], B[:j - 1], F, WWtemp, ZZtemp, A[i-1] + W, B[j-1] + Z)
    if i > 0 and F[j][i] == F[j][i - 1] + g:
        EnumerateAlignments(A[:i - 1], B, F, WWtemp, ZZtemp, A[i-1] + W, '-' + Z)
    if j > 0 and F[j][i] == F[j - 1][i] + g:
        EnumerateAlignments(A, B[:j - 1], F, WWtemp, ZZtemp, '-' + W, B[j-1] + Z)

def ComputeAlignmentScore(A, B):
    L = [0] * (len(B) + 1)
    for j in range(len(L)):
        L[j] = j * g
    K = [0] * (len(B) + 1)
    for i in range(1, len(A) + 1):
        L, K = K, L
        L[0] = i * g
        for j in range(1, len(B) + 1):
            md = compare(A[i - 1], B[j - 1])
            L[j] = max(L[j - 1] + g, K[j] + g, K[j - 1] + md)
    return L

def UpdateAlignments(WW, ZZ, WWl, WWr, ZZl, ZZr):
    l = []
    for i in range(len(WWl)):
        for j in range(len(WWr)):
            l.append((WWl[i] + WWr[j], ZZl[i] + ZZr[j]))

    l_no_duplicates = list(set(l))
    for i in range(len(l_no_duplicates)):
        WW.append(l[i][0])
        ZZ.append(l[i][1])

def Hirschberg(A, B):
    if len(A) == 0:
        WW = ['-'] * len(B)
        ZZ = [B]
    elif len(B) == 0:
        WW = [A]
        ZZ = ['-'] * len(A)
    elif len(A) == 1 or len(B) == 1:
        WW, ZZ = NeedlemanWunsch(A, B)
    else:
        i = len(A) // 2
        Sl = ComputeAlignmentScore(A[:i], B)
        Sr = ComputeAlignmentScore(A[i:][::-1], B[::-1])
        Sr.reverse()
        S = [Sl[i] + Sr[i] for i in range(len(Sl))]
        J = [i for i, _ in enumerate(S) if _ == max(S)]
        ZZ = []
        WW = []
        for j in J:
            if(args.t):
                print('(', i,',',  j, ')')
            WWl, ZZl = Hirschberg(A[:i], B[:j])
            WWr, ZZr = Hirschberg(A[i:], B[j:])

            UpdateAlignments(WW, ZZ, WWl, WWr, ZZl, ZZr)

    return WW, ZZ



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action = 'store_true')
    parser.add_argument('-f', action = 'store_true')
    parser.add_argument('-l', action = 'store_true')
    parser.add_argument('gap', type=int)
    parser.add_argument('match', type=int)
    parser.add_argument('differ', type=int)
    parser.add_argument('sequenceA')
    parser.add_argument('sequenceB')

    args = parser.parse_args()
    F = None

    if(not args.f):
        m = args.match
        d = args.differ
        g = args.gap
        A = args.sequenceA
        B = args.sequenceB
        WW, ZZ = Hirschberg(A, B)
        for i in range(len(WW)):
            print(WW[i])
            print(ZZ[i])
            print("\n")
    elif(args.f and not args.l):
        m = args.match
        d = args.differ
        g = args.gap
        with open(args.sequenceA, 'r') as file:
            A = file.read().replace('\n', '')
        with open(args.sequenceB, 'r') as file:
            B = file.read().replace('\n', '')
        WW, ZZ = Hirschberg(A, B)
        for i in range(len(WW)):
            print(WW[i])
            print(ZZ[i])
            print("\n")
    elif(args.f and args.l):
        print("-------------\nFEATURE NOT IMPLEMENTED YET.\n-------------")
        '''with open(args.sequenceA, 'r') as file:
            A = file.readlines()
        with open(args.sequenceB, 'r') as file:
            B = file.readlines()'''



