import sys
import numpy as np
import math
sys.dont_write_bytecode = True

# impossibe to solve because the memory consumption can be 2^N

def Accum(M, memo, arr):
    closest = 0
    bestList = []
    for i, p in enumerate(arr):
        memoLen = len(memo)
        for m in range(memoLen):
            if not memo[m][0]==0:
                if memo[m][1] + p < M:
                    memo.append( (memo[m][0]+[i], memo[m][1]+p) )
                elif memo[m][1] + p == M:
                    return memo[m][0]+[i]
                else:
                    if closest < memo[m][1]:
                        closest = memo[m][1]
                        print(memo[m])
                        del bestList
                        bestList = memo[m][0].copy()
                        del memo[m][0]
                        memo[m] = (0, 0)
        memo.append( ([i], p) )
        for j, m in enumerate(memo):
            if m[0]==0:
                memo.pop(j)
        print("i %d memolen %d" %(i, memoLen))
    return bestList    

def main():
    M, N = list(map(int, input().split()))
    pizzaList = list(map(int, input().split()))
    # print(sum(pizzaArray[0:45]))
    memo = []
    optimalList = Accum(M, memo, pizzaList)
    # print( "minRes %d, minSubOpt %s" %(minRes, optimalList))
    print(len(optimalList))
    print(*optimalList, sep=' ')



if __name__ == '__main__':
    main()