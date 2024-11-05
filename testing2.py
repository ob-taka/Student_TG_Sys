list1 = [5,3,6,2,7,6,3,7,8,1]
for again in range(0, len(list1)):
    for i in range(0, len(list1)-1):
        if list1[i] > list1[i+1]:
            list1[i], list1[i+1] = list1[i+1], list1[i]
    again +=1
print(list1)