import sys
import networkx as nx
from timeit import default_timer as timer
sys.dont_write_bytecode = True

def score(p1, p2):
    s1 = p1 & p2
    # print(s1)
    s2 = p1 - s1
    # print(s2)
    s3 = p2 - s1
    # print(s3)
    return min( len(s1), len(s2), len(s3))

# def orderSlides(slides, N, sol):
#     memo = []
#     maxScoreGlobal = 0
#     maxOrderGlobal = ([], 0)
#     for s in range(1, N):
#         maxScore = 0
#         maxOrder = ([], 0)
#         for p in range(s):
#             if score(slides[p][0], slides[s][0]) > 0:
#                 for m in memo:



def main():
    N = int(input())
    photoList = []
    for i in range(N):
        photo = list(input().split())
        photoList.append([ photo[0], int( photo[1] ), set(photo[2:]), i])
    photoH = [ p for p in photoList if p[0]=='H']
    photoV = [ p for p in photoList if p[0]=='V']
    slides = [ p[2:] for p in photoH]
    for i in range(0, len(photoV), 2):
        photoVV = [ photoV[i][2] | photoV[i+1][2], [photoV[i][3], photoV[i+1][3]] ]
        slides.append( photoVV )
    # print(slides)
    G = nx.Graph()
    start = timer()
    for i in range(N):
        for j in range(i+1, N):
            s = score(slides[i][0], slides[j][0])
            if s > 0:
                G.add_edge(i, j, weight=s)
    end = timer()
    print(f"time spent {end-start:0.4f}")
    nx.write_adjlist(G,"G.adjlist")
    nx.write_edgelist(G, "G.edgelist")
    sol = []
    # orderSlides(slides, N, sol )
    # print(slides)

if __name__ == '__main__':
    main()