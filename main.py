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
    #print(TG)
    TGmin = 10
    TGmax = 0
    classAve = 0
    classTotal = 0
    for i in array:
       classTotal += float(i.CGPA)
    classAve = classTotal / 50
    while group < 11:
        testArray = []
        for i in array:
            if i.group == group:
                testArray.append(i)
        minGPA = float(10)
        maxGPA = float(0)
        totalGPA = 0
        for i in testArray:
            floatCGPA = float(i.CGPA)
            totalGPA += floatCGPA
        gpaAve = totalGPA / 5
        if gpaAve > TGmax:
            TGmax = gpaAve
        elif gpaAve < TGmin:
            TGmin = gpaAve
        #print(f"group {group}, gpaAve {gpaAve}")
        group += 1
    print(f"{TG} range is {round((TGmax - classAve), 2)}, or {round((classAve - TGmin), 2)}")
        

stud_records = read_records() # returns a list of Student objects
stud_TG = group_students(stud_records) # returns a dictionary where keys are tut groups and values are Student objs

#print_records(stud_records, 100)

for key, value in stud_TG.items(): #sorts students by GPA
    sortThis = value
    sortedList = sorted(sortThis, key=lambda student: student.CGPA)
    value = sortedList
finalList = []
for key, value in stud_TG.items():
    listBoys = []
    listGirls = []
    for i in value:
        if i.Gender == "Male":
            listBoys.append(i)
        else:
            listGirls.append(i)
    interleaved = []
    minLen = min(len(listGirls), len(listBoys))
    print(minLen)
    for i in range(0,minLen*2):
        if i % 2 == 0:
            interleaved.append(listBoys.pop())
        else:
            interleaved.append(listGirls.pop(0))
    interleaved = interleaved + listBoys + listGirls
    index = 0
    groupNo = 1
    for i in interleaved:
        i.group = groupNo
        index += 1
        if index == 5:
            index = 0
            groupNo += 1

    #print_records(interleaved, 50)
    finalList += interleaved
    validateStudents(interleaved, key)
#print_records(finalList, 6000)

                
