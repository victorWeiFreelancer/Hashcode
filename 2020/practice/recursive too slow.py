import sys
import numpy as np
import math
sys.dont_write_bytecode = True

# recursion but way too slow

def DP(M, optimal, shift, arr):
    remainArr = arr[shift:]
    if len(remainArr):
        minRes = math.inf 
        minSubOpt = []
        for i in range(len(remainArr)):
            optCopy = optimal.copy()
            if M < remainArr[i]:
                return M, optimal
            elif M == remainArr[i]:
                optCopy.append(shift + i)
                return 0, optCopy
            else:
                optCopy.append(shift + i)
                subMin, subOptimal = DP(M - remainArr[i], optCopy, shift + i + 1, arr)
                if minRes > subMin:
                    minRes = subMin
                    minSubOpt = subOptimal
        # print( "minRes %d, minSubOpt %s" %(minRes, minSubOpt))
        # optCopy = minSubOpt
        return minRes, minSubOpt          
    else:
        return M, optimal

def main():
    M, N = list(map(int, input().split()))
    pizzaArray = np.array(list(map(int, input().split())))
    # print(sum(pizzaArray[0:45]))
    minRes, optimalList = DP(M, [], 0, pizzaArray)
    # print( "minRes %d, minSubOpt %s" %(minRes, optimalList))
    print(len(optimalList))
    print(*optimalList, sep=' ')



if __name__ == '__main__':
    main()