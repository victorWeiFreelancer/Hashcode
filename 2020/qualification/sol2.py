import sys
import math
from time import gmtime, strftime
sys.dont_write_bytecode = True

class B:
    def __init__(self, id, score):
        super().__init__()
        self.id, self.score = id, score
        self.libId = []

class L:
    def __init__(self, id, numB, signTime, cap):
        super().__init__()
        self.id, self.numB, self.signTime, self.cap = id, numB, signTime, cap
        self.bIDs = []
        self.bScores = 0
        self.hasNumValuebook = 0

def readInput(books, libs):
    if(len(sys.argv)==1):
        nB, nL, D = list(map(int, input().split()))
        bookScoreList = list(map(int, input().split()))
        # print("bookScoreList", bookScoreList)
        for i in range(nB):
            b = B(i, bookScoreList[i])
            books.append(b)
        for i in range(nL):
            libInfo = list(map(int, input().split()))
            lib = L(id, libInfo[0], libInfo[1], libInfo[2])
            bIDs = list(map(int, input().split()))
            # print(libInfo)
            lib.bIDs.extend( bIDs )
    else:
        with open(sys.argv[1], 'r') as fo:
            nB, nL, D = list(map(int, fo.readline().split()))
            bookScoreList = list(map(int, fo.readline().split()))
            # print("bookScoreList", bookScoreList)
            for i in range(nB):
                b = B(i, bookScoreList[i])
                books.append(b)
            for i in range(nL):
                libInfo = list(map(int, fo.readline().split()))
                lib = L(i, libInfo[0], libInfo[1], libInfo[2])
                bIDs = list(map(int, fo.readline().split()))
                lib.bIDs.extend( bIDs )
                lib.bScores = sum([ books[bookId].score for bookId in lib.bIDs ])
                libs.append(lib)
                # print(lib.bIDs)
    # print(nB, nL, D)
    return nB, nL, D

def sortOnSignUpTime(libs):
    libs.sort(key = lambda l:l.signTime)

def sortOnBookScoreSumDivSignTime(libs):
    libs.sort(key = lambda l:l.bScores/l.signTime, reverse=True)

def sortD(libs, books):
    bookIsStored = [ 0 ] * len(books)
    libs.sort(key = lambda l:l.numB, reverse = True)
    for i in range(len(libs)-1):
        for bookId in libs[i].bIDs:
            bookIsStored[bookId]=1
        for lib in libs[i+1:]:
            libBookList = [ b for b in lib.bIDs]
            for id in libBookList:
                if bookIsStored[id]==1:
                    lib.bIDs.remove(id)
                    lib.numB -= 1
        libs.sort(key = lambda l:l.numB, reverse = True)
        if libs[i+1].numB == 0:
            break;
    # libs.sort(key = lambda l:l.numB, reverse = True)
    for i in range(len(libs)):
        if libs[i].numB == 0:
            del libs[i:]
            break

def sortE(libs, books, D):
    # libs.sort(key = lambda l:l.cap, reverse = True)
    averageSignTime = 0
    for lib in libs:
        lib.bIDs.sort( key= lambda id:books[id].score, reverse=True)
        averageSignTime += lib.signTime
    averageSignTime /= len(libs)*2
    print("averageSignTime", averageSignTime)
    avgBooksCanbeScanned = math.floor(D / averageSignTime)
    print("avgBooksCanbeScanned", avgBooksCanbeScanned)
    print("avgBooksCanbeScanned", math.floor(D - averageSignTime))
    for lib in libs:
        lib.bScores = sum( [ books[id].score for id in lib.bIDs[ 0: avgBooksCanbeScanned*lib.cap ]])
    libs.sort(key = lambda l:l.bScores/(l.signTime**1), reverse=True)
    # for lib in libs:
    #     print(lib.bScores)
    # firstL1Cap = next(l for l in libs if l.cap==1)
    # firstL1CapIndex = libs.index(firstL1Cap)


def sortF(libs, books, D):
    sortedBooks = sorted(books, key = lambda book: book.score, reverse=True)
    for lib in libs:
        for book in sortedBooks[0:10000]:
            if book.id in lib.bIDs:
                lib.hasNumValuebook += book.score

    averageSignTime = 0
    for lib in libs:
        lib.bIDs.sort( key= lambda id:books[id].score, reverse=True)
        averageSignTime += lib.signTime
        # print("max", books[lib.bIDs[0]].score, "pmedian", books[math.floor(len(lib.bIDs)/2)].score, "numbooks", lib.numB)
    averageSignTime /= len(libs)
    avgBooksCanbeScanned = math.floor(D/averageSignTime)
    print("avgBooksCanbeScanned", avgBooksCanbeScanned)
    print("averageSignTime", averageSignTime)
    for lib in libs:
        lib.bScores = sum( [ books[id].score + lib.hasNumValuebook*2 for id in lib.bIDs[ 0: avgBooksCanbeScanned*lib.cap ]])
    libs.sort(key = lambda l:l.bScores/(l.signTime), reverse=True)
    for i, lib in enumerate(libs):
        for bookId in lib.bIDs[ 0: avgBooksCanbeScanned*lib.cap]:
            for l in range(i+1, len(libs)):
                if bookId in libs[l].bIDs:
                    libs[l].bIDs.remove(bookId)
    for lib in libs:
        lib.bScores = sum( [ books[id].score + lib.hasNumValuebook*2 for id in lib.bIDs[ 0: avgBooksCanbeScanned*lib.cap ]])
    libs.sort(key = lambda l:l.bScores/(l.signTime), reverse=True)


def sortOnNumBooks(libs):
    libs.sort(key = lambda l:l.numB, reverse = True)
    

def main():
    books = []
    libs = []
    startT = strftime("%H:%M:%S")
    nB, nL, D = readInput(books, libs)
    startT = strftime("%H:%M:%S")
    # print()
    if len(sys.argv)>1:
        if(sys.argv[1] == "b_read_on.txt"):
            sortOnSignUpTime(libs)
        elif sys.argv[1] == "c_incunabula.txt":
            sortOnBookScoreSumDivSignTime(libs)
        elif sys.argv[1] == "d_tough_choices.txt":
            sortD(libs, books)
        elif sys.argv[1] == "e_so_many_books.txt":
            sortE(libs, books, D)
        elif sys.argv[1] == "f_libraries_of_the_world.txt":
            sortF(libs, books, D)

    finishT = strftime("%H:%M:%S")
    fw = open(" ".join([sys.argv[1].split('.')[0], startT, finishT, ".out"]),'w')
    fw.write( str(len(libs))+ '\n')
    for lib in libs:
        fw.write( " ".join( map(str, [lib.id, len(lib.bIDs)]))  + '\n')
        fw.write( " ".join( map(str, lib.bIDs) )  + '\n')

if __name__ == '__main__':
    main()