def findAverage(list):
    total = 0
    ave = 0
    for i in list:
        total += float(i)
    ave = total / len(list)
    return ave




def sortingFunc(list, recursionNo):
    lengthList = len(list)
    #print_records(list, lengthList)
    if lengthList <= 5:
        for again in range(0, lengthList*2):
            for i in range(0, lengthList-1):
                if list[i] > list[i+1]:
                    list[i], list[i+1] = list [i+1], list[i]
            again +=1
        finalList = list
        print(list, lengthList)
    elif recursionNo > 50:
        return list, recursionNo  
    else:
        valence = findAverage(list)
        halfLen = lengthList // 2
        print(halfLen, lengthList)
        #print_records(list, lengthList)
        halfList1 = []
        halfList2 = []
        print("recursion", recursionNo)
        for i in list:
            if float(i) > valence:
                #print(getattr(i, attr), valence, "more")
                halfList2.append(i)
            elif float(i) < valence:
                #print(getattr(i, attr), valence, "less")
                halfList1.append(i)
            elif float(i) == valence:
                #print(getattr(i, attr), valence, "same")
                halfList1.append(i)
        #print("half1")
        #print_records(halfList1, len(halfList1))
        #print("half2")
        #print_records(halfList2, len(halfList2))
        halfList1, recursionNo = sortingFunc(halfList1, recursionNo+1)
        print("half1 done")
        halfList2, recursionNo = sortingFunc(halfList2, recursionNo+1)
        print("half2 done")
        #print(type(halfList1), type(halfList2))
        finalList = halfList1 + halfList2
    return finalList, recursionNo

listTest = [4,3,6,1,7,9,2,6,6,4,3,4.5,3.5,2.7,4.2,3.1,5.6,9.3,11,5.6,3.4,3.5,3.3,3.3]
listSorted, recursionDepth = sortingFunc(listTest, 0)
print(listSorted)