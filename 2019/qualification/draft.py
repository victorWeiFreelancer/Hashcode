# print(slides)
    slideLen = len(slides)
    # score2DList = [[0 for x in range(slideLen)] for y in range(slideLen)]
    positiveScoresList = []
    outputList = []
    for i in range(slideLen):
        max = 0
        maxJ = 0
        for j in range(i+1, slideLen):
            s = score(slides[i][0], slides[j][0])
            # score2DList[i][j] = s
            # score2DList[j][i] = s
            if s > max:
                positiveScoresList.append((i, j, s))
                max = s
                maxJ = j
        
        if max == 0:
            outputList.append(slideLen[i][1])
                # print( "i %d, j %d: score %d" %(i, j, s)) 
    # for row in score2DList:
    #     print(' '.join([str(elem) for elem in row]))
    print(len(positiveScoresList))
    # print(len(photoH))
    # print(len(photoV))
    # print(score(photoList[1], photoList[2]))