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
        """ for i in range(10):
            print('Group', i + 1)
            print([student.school for student in value if student.group == i + 1], end='\n\n') """
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

def closest_gpa(group, target):
    return min(group, key=lambda x: abs(float(x.CGPA) - target))

#assign students to groups based on their cgpa
def assign_groups(stud_TG, group_size: int):
    for key, value in stud_TG.items():
        #sort the students in the tutorial group based on their cgpa
        #from highest to lowest
        #value = sortfunction(value, cgpa)
        value.sort(key=lambda x: x.CGPA, reverse=True)
        avg_cgpa = sum([float(student.CGPA) for student in value]) / len(value)
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
                """ target_student = closest_gpa(gender_group, avg_cgpa)
                groups[min_index].append(target_student)
                group_cgpas[min_index] += float(target_student.CGPA)
                #print(target_student.Name)
                gender_group.remove(target_student) """
                groups[min_index].append(student)
                #update the cgpa and count of the group
                group_cgpas[min_index] += float(student.CGPA)
                group_counts[min_index] += 1
        #make sure each group has at most 2 students from the same school
        """ for student in groups:
            for i in range(len(student)):
                if student[i].school == student[i - 1].school:
                    if i + 1 < len(student):
                        if student[i].school == student[i + 1].school:
                            student[i], student[i + 1] = student[i + 1], student[i]
 """

        for i, group in enumerate(groups):
            for student in group:
                student.group = i + 1

    return stud_TG





def calculate_gpa_differences(groups):
    highest_diff = []
    lowest_diff = []

    for tg, studentList in groups.items():
        
    
        avg_cgpa = sum([float(student.CGPA) for student in studentList]) / len(studentList)
        #find the average cgpa of each group
        avg_group_cgpa = sorted([sum([float(student.CGPA) for student in studentList if student.group == i + 1]) / 5 for i in range(10)])
        print(avg_group_cgpa)
        highest_avg_gpa = avg_group_cgpa[-1]
        lowest_avg_gpa = avg_group_cgpa[0]
        highest_diff.append(float(highest_avg_gpa) - float(avg_cgpa))
        lowest_diff.append(float(avg_cgpa) - float(lowest_avg_gpa))
        
        print(f"Tutorial Group: {tg} | Average CGPA: {avg_cgpa:.3f} | Highest CGPA: {float(highest_avg_gpa):.3f} | Lowest CGPA: {float(lowest_avg_gpa):.3f}")

    print(f"Highest GPA difference: {max(highest_diff):}")
    print(f"Lowest GPA difference: {max(lowest_diff):}")

# Example usage
records = read_records()
grouped_records = group_students(records)
grouped_students = assign_groups(grouped_records, group_size=5)
print_grouped_records(grouped_students)
