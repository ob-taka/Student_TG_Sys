def sortingFunc(list, attr):
    lengthList = len(list)
    if lengthList < 5:
        for again in range(0, lengthList):
            for i in range(0, lengthList):
                if list[i] > list[i+1]:
                    list[i], list[i+1] = list [i+1], list[i]
            again +=1
        
    else:
        halfLen = lengthList // 2
        halfList1 = []
        halfList2 = []
        for i in list:
            if getattr(i, attr) > getattr(list[halfLen], attr):
                halfList2.append(i)
            elif getattr(i, attr) < getattr(list[halfLen], attr):
                halfList1.append(i)
            elif getattr(i, attr) == getattr(list[halfLen], attr):
                halfList1.append(i)
        halfList1 = sortingFunc(halfList1, attr)
        halfList2 = sortingFunc(halfList2, attr)
        finalList = halfList1 + halfList2
    return finalList
            


