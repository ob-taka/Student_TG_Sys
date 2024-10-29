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

# let me flex my programming skills using recursion
def cgpa_tree(stud_list, stud):
    if stud_list == []:
        return [stud]
    elif len(stud_list) == 1:
        if stud.CGPA > stud_list[0].CGPA:
            return [[], stud_list[0], [stud]]
        else: # CGPA same or less than current student
            return [[stud], stud_list[0], []]
    elif len(stud_list) == 3:
        if stud.CGPA > stud_list[1].CGPA:
            stud_list[2] = cgpa_tree(stud_list[2], stud)
            return stud_list
        else:
            stud_list[0] = cgpa_tree(stud_list[0], stud)
            return stud_list
    # else: # list not empty and not 1 or 3 items in list, should not happen cause i designed it to always have 0, 1 or 3 items in list, most likely user call function with a stud_list that is not empty
    #     print("HUH?!? ", stud_list)
    #     return [stud]

# read_tree is universal, it can read any tree u throw in it and return a list of items in the tree from left most leaf? branch? element to right most element
def read_tree(tree, list):
    for i in tree:
        if i == []:
            continue
        # need the tree to be tree of class/object 'student' tho, or else it is useless
        elif type(i) == student.Student:
            list.append(i)
        else: # i is a tree
            read_tree(i, list)
            
    # print(list)
    return list

# def avg_cgpa(tg):
#     total_cgpa = 0
#     for stud in tg:
#         total_cgpa += float(stud.CGPA)
#     print(total_cgpa / len(tg))
#     return total_cgpa / len(tg)

def sort_by_cgpa(tg):
    cgpa_sorted_tree = []
    # cgpa_sorted_list = []

    for stud in tg:
        cgpa_sorted_tree = cgpa_tree(cgpa_sorted_tree, stud)
    # print(cgpa_sorted_tree)

    # cgpa_sorted_list = read_tree(cgpa_sorted_tree, [])
    # for i in cgpa_sorted_list:
    #     print(i.CGPA, end=" ")
    # print("") # next line so future print statements are on a new line

    # avg_cgpa(read_tree(cgpa_sorted_tree, []))

    return read_tree(cgpa_sorted_tree, [])

def split_by_gender(tg):
    gender_dict = {}

    for stud in tg:
        if stud.Gender not in gender_dict.keys():
            gender_dict[stud.Gender] = [stud]
        else:
            gender_dict[stud.Gender].append(stud)

    # from this for loop, we can see that the students are still sorted by CGPA after splitting into gender groups
    # for gender in gender_dict.keys():
    #     for stud in gender_dict[gender]:
    #         print(gender, ":", stud.CGPA, end=", ")
    #     print(" end")

    return gender_dict


# assumming only 2 gender "Male" and "Female" (caps sensitive), which is true, but i ignoring the possiblity of 'others' in the future
def put_into_teams_by_gender(tg, team_size = 5):
    gender_dict = split_by_gender(tg)
    number_of_teams = len(tg)//team_size
    should_take_from_top = True
    # student_taken = 0 # team * team_size + i

    # atleast y number of males in each team
    base_males = len(gender_dict['Male']) // number_of_teams
    # number of teams with 1 extra male
    extra_males = len(gender_dict['Male']) % number_of_teams

    for team in range(1, number_of_teams + 1):
        male_taken = 0
        should_take_avg = True

        for i in range(team_size):
            if should_take_avg:
                # if team_size % 2 == 0:
                    # if male_taken == 0:
                    #     gender_dict['Male'][len(gender_dict['Male'])//2].Group = team
                    #     gender_dict['Male'] = gender_dict['Male'][:len(gender_dict['Male'])//2] + gender_dict['Male'][len(gender_dict['Male'])//2 + 1:] # remove avg male student
                    #     male_taken += 1
                    #     continue
                    # else:
                    #     gender_dict['Female'][len(gender_dict['Female'])//2].Group = team
                    #     gender_dict['Female'] = gender_dict['Female'][:len(gender_dict['Female'])//2] + gender_dict['Female'][len(gender_dict['Female'])//2 + 1:] # remove avg female student
                # VVV change to elif when using code above ... # check if need odd number of males in group then take avg cgpa male
                if (team <= extra_males and (base_males + 1) % 2 == 1) or (team > extra_males and base_males % 2 == 1):
                    gender_dict['Male'][len(gender_dict['Male'])//2].Group = team
                    gender_dict['Male'] = gender_dict['Male'][:len(gender_dict['Male'])//2] + gender_dict['Male'][len(gender_dict['Male'])//2 + 1:] # remove avg male student
                    male_taken += 1
                else:
                    gender_dict['Female'][len(gender_dict['Female'])//2].Group = team
                    gender_dict['Female'] = gender_dict['Female'][:len(gender_dict['Female'])//2] + gender_dict['Female'][len(gender_dict['Female'])//2 + 1:] # remove avg female student

                should_take_avg = False
                continue

            if  male_taken < base_males or (team <= extra_males and male_taken < base_males + 1):
                if should_take_from_top:
                    gender_dict['Male'][0].Group = team
                    gender_dict['Male'] = gender_dict['Male'][1:] # remove top male student
                    should_take_from_top = False
                else:
                    gender_dict['Male'][-1].Group = team
                    gender_dict['Male'] = gender_dict['Male'][:-1] # remove bottom male student
                    should_take_from_top = True
                male_taken += 1
            else:
                if should_take_from_top:
                    gender_dict['Female'][0].Group = team
                    gender_dict['Female'] = gender_dict['Female'][1:] # remove top female student
                    should_take_from_top = False
                else:
                    gender_dict['Female'][-1].Group = team
                    gender_dict['Female'] = gender_dict['Female'][:-1] # remove bottom female student
                    should_take_from_top = True

    for stud in tg:
        print(stud.Gender, stud.Group, stud.CGPA, end=", ")
    print(" end")
    
    # return tg  # not needed since we updated the object directly

def split_by_school(tg):
    school_dict = {}

    for stud in tg:
        if stud.school not in school_dict.keys():
            school_dict[stud.school] = [stud]
        else:
            school_dict[stud.school].append(stud)

    # some tg have 13 student from same school... good luck
    # for school in school_dict.keys():
    #     print(school, ":", len(school_dict[school]), end=" ")
    # print(" end")

    return school_dict

# stud_records = read_records()
# stud_TG = group_students(stud_records)
#sort_by_cgpa(stud_TG['G-1'])

# only import and create functions outside. Don't initialize variables outside, as they will become global variables and 
# may mess up codes due to having similar var names in the 'def' / function u coding, the name could confuse u too.
def main():
    stud_records = read_records()
    stud_TG = group_students(stud_records)

    for tg in stud_TG.keys():
        print(tg,":")
        tg_sorted_list = []
        gender_dict = {}
        # print("Tutorial Group: ", tg, "number of students: ", len(stud_TG[tg]))
        # print_records(sort_by_cgpa(stud_TG[tg]), 6000) # I'm not sure why u want n, but I know n should not be less than students in tutorial group if i want to print the whole tutorial group, i put 6000 cuz maybe got more than 50 in a tutorial group and max is 6000 students so just for fun i put 6000
        # print("Tutorial Group: ", tg, "number of students: ", len(sort_by_cgpa(stud_TG[tg])))
        tg_sorted_list = sort_by_cgpa(stud_TG[tg])
        # gender_dict = split_by_gender(tg_sorted_list)
        # print(gender_dict)
        put_into_teams_by_gender(tg_sorted_list)



# start the whole program
main()