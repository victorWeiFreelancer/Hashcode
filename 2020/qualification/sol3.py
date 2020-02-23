import sys
import math
import copy
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
        self.score = 0
        self.hasNumValuebook = 0

    def __repr__(self):
        return " ".join([ "id", str(self.id), "signUpTime", str(self.signTime), "cap", str(self.cap) ])  +  "\n" \
            + " ".join([ str(id) for id in self.bIDs])
    
    def __str__(self):
        return " ".join([ "id", str(self.id), "signUpTime", str(self.signTime), "cap", str(self.cap) ])  +  "\n" \
            + " ".join([ str(id) for id in self.bIDs])
        
    def computeScore(self, remainDays, books):
        if self.signTime >= remainDays:
            return 0
        return sum( [ books[id].score for id in self.bIDs[0: min( (remainDays- self.signTime)*self.cap, self.numB ) ] ] )


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
                # lib.bScores = sum([ books[bookId].score for bookId in lib.bIDs ])
                lib.bIDs.sort( key= lambda id:books[id].score, reverse=True)
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
    sol = []
    remainDays = D
    bookisScanned = [ 0 ]*len(books)
    # bact to the greedy algo and with trim of already scanned books in candidate libraries
    while(remainDays > 0):
        maxScore = 0
        bestLib = None
        for lib in libs:
            bookIds = lib.bIDs[:]
            for id in bookIds:
                if bookisScanned[id] == 1:
                    lib.bIDs.remove(id)
                    lib.numB -= 1
            libScore = lib.computeScore(remainDays, books)/lib.signTime
            if maxScore < libScore:
                maxScore = libScore
                bestLib = lib
                continue
            if maxScore == libScore:
                if bestLib is not None:
                    if bestLib.numB/bestLib.cap > lib.numB/lib.cap:
                        bestLib = lib
                        continue
        # print(bestLib)
        if bestLib is not None:
            bestLib.bIDs = bestLib.bIDs[0: min( (remainDays- bestLib.signTime)*bestLib.cap, bestLib.numB) ]
            bestLib.numB = len(bestLib.bIDs)
            for id in bestLib.bIDs:
                bookisScanned[id] = 1
            print(bestLib)
            sol.append(copy.deepcopy(bestLib))
            libs.remove(bestLib)
            remainDays -= bestLib.signTime
        else:
            remainDays = 0
    return sol
        

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
            # sortOnBookScoreSumDivSignTime(libs)
            sol = sortE(libs, books, D)
        elif sys.argv[1] == "d_tough_choices.txt":
            sortD(libs, books)
        elif sys.argv[1] == "e_so_many_books.txt":
            sol = sortE(libs, books, D)
        elif sys.argv[1] == "f_libraries_of_the_world.txt":
            sol = sortE(libs, books, D)

    finishT = strftime("%H:%M:%S")
    fw = open(" ".join([sys.argv[1].split('.')[0], startT, finishT, ".out"]),'w')
    if sys.argv[1] == "e_so_many_books.txt" or sys.argv[1] == "f_libraries_of_the_world.txt" \
        or sys.argv[1] == "c_incunabula.txt":
        fw.write( str(len(sol))+ '\n')
        for lib in sol:
            fw.write( " ".join( map(str, [lib.id, len(lib.bIDs)]))  + '\n')
            fw.write( " ".join( map(str, lib.bIDs) )  + '\n')
    else:
        fw.write( str(len(libs))+ '\n')
        for lib in libs:
            fw.write( " ".join( map(str, [lib.id, len(lib.bIDs)]))  + '\n')
            fw.write( " ".join( map(str, lib.bIDs) )  + '\n')

if __name__ == '__main__':
    main()