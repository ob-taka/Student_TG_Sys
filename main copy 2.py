import student as student
import csv

#read records.csv file and map the records to the student class
def read_records():
    records = []
    with open('records.csv') as file:
        next(file)  # Skip the header
        for line in file:
            tutorial_group, student_id, school, name, gender, cgpa = line.strip().split(',')
            records.append(student.Student(tutorial_group, student_id, school, name, gender, cgpa, int(0)))
    return records

#write a def that prints the records 1 at a time
def print_records(records, n):
    for i in range(min(n, len(records))):
        record = records[i]
        print(record.Tutorial_group, record.Student_ID, record.school, record.Name, record.Gender, record.CGPA, record.group)

#write a def that create a temporary list of students with the same tutorial group
def group_students(stud_records):
    t_groups = {}
    for stud in stud_records:
        if stud.Tutorial_group not in t_groups:
            t_groups[stud.Tutorial_group] = []
        t_groups[stud.Tutorial_group].append(stud)
    return t_groups

def validateStudents(array, TG):
    group = 1
    TGmin = 10
    TGmax = 0
    classAve = 0
    classTotal = 0
    for i in array:                  #this bit finds the class GPA average for comparison
       classTotal += float(i.CGPA)
    classAve = classTotal / 50
    while group < 11:
        testArray = []
        boyCount = 0
        girlCount = 0
        for i in array:                 #gender balance within the group
            if i.group == group:
                testArray.append(i)
                if i.Gender == "Male":
                    boyCount += 1
                if i.Gender == "Female":
                    girlCount += 1
        minGPA = float(10)
        maxGPA = float(0)
        totalGPA = 0
        for i in testArray:               #finds average GPA of the group
            floatCGPA = float(i.CGPA)
            totalGPA += floatCGPA
        gpaAve = totalGPA / 5
        if gpaAve > TGmax:  #compares the average GPA of the group to the class average
            TGmax = gpaAve
        elif gpaAve < TGmin:
            TGmin = gpaAve
        print(f"{TG}, Group {group} Male:Female = {boyCount}:{girlCount}") #validation print output for group
        group += 1
    
    print(f"{TG} range is {round((TGmax - classAve), 2)}, or {round((classAve - TGmin), 2)}. \n") #validation print output for the whole group

def print_attr(list, attr):
    for i in list:
        print(getattr(i, attr))

def findAverage(list, attr):
    total = 0
    ave = 0
    for i in list:
        total += float(getattr(i, attr))
    ave = total / len(list)
    return ave


def sortingFunc(list, attr):
    lengthList = len(list)
    # if lengthList <= 5: #if length of list is below a certain value, use bubble sort to sort it
    #     for again in range(0, lengthList*2):
    #         for i in range(0, lengthList-1):
    #             if float(getattr(list[i], attr)) > float(getattr(list[i+1], attr)):
    #                 list[i], list[i+1] = list [i+1], list[i]
    #         again +=1
    #     finalList = list
    if len(list) == 0: #if list is empty (most likely due to all values being the same for the prev recursion and thus being kicked to middle list), just return the empty list
        return list
    else:
        valence = float(list[(len(list)//2)].CGPA)
        #valence = round(findAverage(list, "CGPA"), 2) #round was added because floating point math of 4.1499999999995 was resulting in an infinite recursion where everything in the list was 4.15 but the average was 4.14999999995 so yea
        halfList1 = []
        halfList2 = []
        meanList = []
        for i in list:
            if float(getattr(i, attr)) > valence: #if more than average, goes to right list 
                halfList2.append(i)
            elif float(getattr(i, attr)) < valence: #if less than average, goes to left list
                halfList1.append(i)
            elif float(getattr(i, attr)) == valence: #if equal to average, goes to center list (this was implemented because the prev version had recursion depth issues where all values in the list were the same and kept getting kicked to the left list infinitely)
                meanList.append(i)
        halfList1 = sortingFunc(halfList1, attr) #recursively sorting left list
        halfList2 = sortingFunc(halfList2, attr) #recursively sorting right list
        finalList = halfList1 + meanList + halfList2 #recombines the lists
    return finalList
                   

stud_records = read_records() # returns a list of Student objects
stud_TG = group_students(stud_records) # returns a dictionary where keys are tut groups and values are Student objs


for key, value in stud_TG.items(): #sorts students by GPA
    sortThis = value
    sortedList = sortingFunc(value, "CGPA")
    value = sortedList
    # print_records(value, 50) #testing code
    # input("next")
    
finalList = []
for key, value in stud_TG.items(): #this part takes the males and females and interleaves them with one in ascending GPA order and the other in decending GPA order
    listBoys = []
    listGirls = []
    for i in value:
        if i.Gender == "Male":
            listBoys.append(i)
        else:
            listGirls.append(i)
    interleaved = []
    minLen = min(len(listGirls), len(listBoys)) #this is here so the program doesnt try to pop from an empty list and run into an out of bounds error
    for i in range(0,minLen*2):
        if i % 2 == 0:
            interleaved.append(listBoys.pop())
        else:
            interleaved.append(listGirls.pop(0))
    interleaved = interleaved + listBoys + listGirls #combines the remaining ppl in the lists to the main list
    index = 0
    groupNo = 1
    for i in interleaved: #making the small groups
        i.group = groupNo
        index += 1
        if index == 5:
            index = 0
            groupNo += 1

    finalList += interleaved #appends the sorted list to the final big list of students. can be changed to edit a dictionary
    validateStudents(interleaved, key)

#input("print final list") #this is so you can actually read the validation before getting 6000 lines in your terminal
#print_records(finalList, 6000) 


                
