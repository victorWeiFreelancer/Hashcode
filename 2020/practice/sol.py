import sys
sys.dont_write_bytecode = True

# the real DP with memo

def Accum(M, memo, arr):
    gclosest = 0
    gbestPath = []
    for i in range(len(arr) - 1, -1, -1):
        memoLen = len(memo)
        closest = arr[i]
        bestPath = [i]
        for m in memo:
            if arr[i] + m[0] < M:
                if closest < arr[i] + m[0]:
                    closest = arr[i] + m[0]
                    bestPath = [i] + m[1]
            elif arr[i] + m[0] == M:
                return [i] + m[1]
        memo.insert(0, (closest, bestPath.copy()))
        if gclosest < closest:
            gclosest = closest
            gbestPath = bestPath.copy()
        del bestPath
    return gbestPath

def main():
    M, N = list(map(int, input().split()))
    pizzaList = list(map(int, input().split()))
    memo = []
    optimalList = Accum(M, memo, pizzaList)
    print(len(optimalList))
    print(*optimalList, sep=' ')



if __name__ == '__main__':
    main()