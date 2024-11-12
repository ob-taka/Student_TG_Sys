import student as student

#read records.csv file and map the records to the student class
def read_records():
    records = []
    with open('records.csv') as file:
        # Skip the header
        next(file)  
        # map record to student obj
        for line in file:
            tutorial_group, student_id, school, name, gender, cgpa = line.strip().split(',')
            records.append(student.Student(tutorial_group, student_id, school, name, gender, cgpa, int(0)))
    return records

def sortingFunc(list, attr):
    lengthList = len(list)
    if lengthList <= 5: #if length of list is below a certain value, use bubble sort to sort it
        for again in range(0, lengthList*2):
            for i in range(0, lengthList-1):
                if float(getattr(list[i], attr)) > float(getattr(list[i+1], attr)):
                    list[i], list[i+1] = list [i+1], list[i]
            again +=1
        finalList = list
    elif len(list) == 0: #if list is empty (most likely due to all values being the same for the prev recursion and thus being kicked to middle list), just return the empty list
        return list
    else:
        valence = round(findAverage(list, "CGPA"), 2) #round was added because floating point math of 4.1499999999995 was resulting in an infinite recursion where everything in the list was 4.15 but the average was 4.14999999995 so yea
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

def findAverage(list, attr):
    total = 0
    ave = 0
    for i in list:
        total += float(getattr(i, attr))
    ave = total / len(list)
    return ave

#prints the records 1 at a time
def print_records(records, n):
    for i in range(min(n, len(records))):
        record = records[i]
        print(record.Tutorial_group, record.Student_ID, record.school, record.Name, record.Gender, record.CGPA, record.group)

def print_grouped_records(grouped_records):
    for key, value in grouped_records.items():
        value.sort(key=lambda x: x.group)
        #calcualte the average cgpa of the tutorial group
        avg_cgpa = sum([float(student.CGPA) for student in value]) / len(value)
        #calculate the average cgpa of each group
        avg_group_cgpa = sorted([avg_cgpa - sum([float(student.CGPA) for student in value if student.group == i + 1]) / len([student for student in value if student.group == i + 1]) for i in range(10)])
        print(key)
        avg_cgpa = f"{avg_cgpa:.3f}"
        print(avg_cgpa)
        #print avg_group_cgpa with values rounded to 3 decimal places
        
        print("upper: " + str(f"{avg_group_cgpa[-1]:.3f}") + " " + "lower: " + str(f"{avg_group_cgpa[0]:.3f}"), end='\n\n')
        #print the gender of the students in each group
        for i in range(10):
            print('Group', i + 1)
            print([student.Gender for student in value if student.group == i + 1], end='\n\n')
        #print_records(value, 50)

#create a dictionary of students using tutorial group as key and list of students obj with the same tutorial group as value 
def group_students(stud_records):
    t_groups = {}
    for stud in stud_records:
        #check if key with the stud.tutorial_group exist in the dictionary 
        #create if doesn't exist
        if stud.Tutorial_group not in t_groups:
            t_groups[stud.Tutorial_group] = []
        t_groups[stud.Tutorial_group].append(stud)
    return t_groups

def invertList(list):
    invertedList = []
    for i in range(len(list)-1):
        invertedList.append(list.pop())
    return invertedList


#assign students to groups based on their cgpa
def assign_groups(stud_TG, group_size: int):
    for key, value in stud_TG.items():
        #sort the students in the tutorial group based on their cgpa
        #from highest to lowest
        #value.sort(key=lambda x: x.CGPA, reverse=True)
        value = sortingFunc(value, "CGPA")
        value = invertList(value)
        #divide the students into 5 groups based on their cgpa and gender
        #average cpga of each group should be as close to the average cgpa of the tutorial group as possible
        groups = [[] for i in range(group_size)] #create x groups
        #track the cgpa of each group
        group_cgpas = [0] * group_size 
        #track the number of students in each group
        group_counts = [0] * group_size

        #split students base on their gender
        #[0] => female
        #[1] => male
        gender_groups = [[], []] 
        #divide students into 2 groups based gender
        for student in value:
            if student.Gender == 'Female':
                gender_groups[0].append(student)
            else:
                gender_groups[1].append(student)

        #take students from each gender_group and assign to groups with gpa closest to the tutorial group gpa
        for gender_group in gender_groups:
            for student in gender_group:
                #get the group with the minimum cgpa
                min_index = group_cgpas.index(min(group_cgpas))
                #add the student with highest gpas to the group with the lowest cgpa
                #since the list is sorted in descending order we know the next student would have the next highest cgpa
                groups[min_index].append(student)
                #update the cgpa and count of the group
                group_cgpas[min_index] += float(student.CGPA)
                group_counts[min_index] += 1

        for i, group in enumerate(groups):
            for student in group:
                student.group = i + 1
        
    return stud_TG

stud_records = read_records()
stud_TG = group_students(stud_records)
grouped_tg = assign_groups(stud_TG, 10)
print_grouped_records(grouped_tg)




                