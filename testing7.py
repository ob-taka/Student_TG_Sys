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
    #debugging code here can be removed
    # lengthList = len(list) 
    # print(lengthList)
    if len(list) <= 1: #if list is empty or only contains 1 element (most likely due to all values being the same for the prev recursion and thus being kicked to middle list), just return the empty list
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
        #input()

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


#assign students to groups based on their cgpa
def assign_groups(stud_TG, group_size: int):
    for key, value in stud_TG.items():
        #sort the students in the tutorial group based on their cgpa
        #from highest to lowest
        #value.sort(key=lambda x: x.CGPA, reverse=True)
        value = sortingFunc(value, "CGPA")[::-1]
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
        diversify_teams_by_school(value, allowed_schools_per_team = 2, allowed_cgpa_diff = 0.1)
        
    return stud_TG




def get_dict_of_teams(tg):
    team_dict = {}
    
    # print(tg[0].Tutorial_group)

    for stud in tg:
        if stud.group not in team_dict.keys():
            team_dict[stud.group] = [stud]
        else:
            team_dict[stud.group].append(stud)
    return team_dict # {team: [list of students sorted by cgpa from lowest to highest]}


# see if can swap students (similar cgpa and same gender) to make teams more diverse
def is_swappable(stud1, stud2, allowed_cgpa_diff):
    if stud1.Gender == stud2.Gender and abs(float(stud1.CGPA) - float(stud2.CGPA)) < allowed_cgpa_diff and stud1.school != stud2.school:
        # print(abs(float(stud1.CGPA) - float(stud2.CGPA))) # abs() just make the diff a positive number, cuz -0.xxx is always smaller than allowed_cgpa_diff (0.1)
        return True
    else:
        return False

# swap teams for 2 students
def swap_group(stud1, stud2, team_dict):
    #update team_dict
    team_dict[stud1.group].append(stud2)
    team_dict[stud2.group].append(stud1)
    team_dict[stud1.group].remove(stud1)
    team_dict[stud2.group].remove(stud2)

    # officially swap
    temp_group = stud1.group
    stud1.group = stud2.group
    stud2.group = temp_group

    return team_dict

# check with other teams
def is_school_limit_reached(team, school, allowed_schools_per_team):
    school_count = 0
    for stud in team:
        if stud.school == school:
            school_count += 1
            if school_count == allowed_schools_per_team: # no need >= since it instantly exit/end function
                return True
    return False

# STEM: ['EEE', 'CoE', 'SBS', 'CCDS', 'MAE', 'MSE', 'SPMS', 'CCEB', 'ASE', 'CEE']
# non-STEM: ['SSS', 'CoB (NBS)', 'SoH', 'WKW SCI', 'ADM', 'HASS']
# uncertain: ['NIE', 'LKCMedicine']
def diversify_teams_by_school(tg, allowed_schools_per_team = 2, allowed_cgpa_diff = 0.1):
    # stem_list = ['EEE', 'CoE', 'SBS', 'CCDS', 'MAE', 'MSE', 'SPMS', 'CCEB', 'ASE', 'CEE']
    # non_stem_list = ['SSS', 'CoB (NBS)', 'SoH', 'WKW SCI', 'ADM', 'HASS']
    team_dict = get_dict_of_teams(tg) #dictionary of a single TG where key is group number and value is list of students
    # allowed_schools_per_team = max(allowed_schools_per_team, 2) # hell no am i trusting the user. at least 2 schools per team!


    # school_dict = {}
    swap_overlap_dict = {}

    # record teams with excess students from same school to swap out
    for team in team_dict.keys(): #team is team number
        school_list = []
        swap_counter = {}

        for stud in team_dict[team]:
            school_list.append(stud.school)
            # when school limit is reached, record number of students to swap out
            if school_list.count(stud.school) > allowed_schools_per_team:
                if stud.school not in swap_counter.keys():
                    swap_counter[stud.school] = 1
                else:
                    swap_counter[stud.school] = swap_counter[stud.school] + 1
        # only record when students need swapping

        if swap_counter != {}:
            swap_overlap_dict[team] = swap_counter

    # print("old team: ", swap_overlap_dict) # {team: {school: number of students to swap out}}
    
    # deversify
    for team in swap_overlap_dict.keys():
        swappable_students = {} # {school: [list of swappable students]}
        
        # get list of swappable students in teams that must swap
        for stud in team_dict[team]:
            if stud.school in swap_overlap_dict[team].keys():
                if stud.school not in swappable_students.keys():
                    swappable_students[stud.school] = [stud]
                else:
                    swappable_students[stud.school].append(stud)
        # time to swap for each school in team
        for school in swap_overlap_dict[team].keys():
            number_to_swap = swap_overlap_dict[team][school]
            number_swapped = 0

            for stud in swappable_students[school]:
                has_swapped = False

                # check with other teams
                for other_team in team_dict.keys():
                    if other_team == team: # same team, no need to check
                        continue

                    for other_stud in team_dict[other_team]:
                        if is_school_limit_reached(team_dict[other_team], school, allowed_schools_per_team): # go next team
                            break
                        if is_school_limit_reached(team_dict[team], other_stud.school, allowed_schools_per_team): # check if new student will exceed school limit of current team
                            continue
                        if is_swappable(stud, other_stud, allowed_cgpa_diff):
                            team_dict = swap_group(stud, other_stud, team_dict) # update team_dict, very important, or else other team may get dups
                            number_swapped += 1
                            has_swapped = True
                            break

                    if has_swapped: # student has been swapped, no need to check with other teams
                        break

                if number_swapped == number_to_swap: # team is balanced, no need to swap more
                    break





stud_records = read_records()
stud_TG = group_students(stud_records)
grouped_tg = assign_groups(stud_TG, 10)
print_grouped_records(grouped_tg)




                