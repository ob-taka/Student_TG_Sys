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


def sort_by_cgpa(tg):
    cgpa_sorted_tree = []
    # cgpa_sorted_list = []

    for stud in tg:
        cgpa_sorted_tree = cgpa_tree(cgpa_sorted_tree, stud)

    return read_tree(cgpa_sorted_tree, [])

def split_by_gender(tg):
    gender_dict = {}

    for stud in tg:
        if stud.Gender not in gender_dict.keys():
            gender_dict[stud.Gender] = [stud]
        else:
            gender_dict[stud.Gender].append(stud)

    return gender_dict


# assumming only 2 gender "Male" and "Female" (caps sensitive), which is true, but i ignoring the possiblity of 'others' in the future
def put_into_teams_by_gender(tg, team_size = 5):
    gender_dict = split_by_gender(tg) # {"Male": [a list of male obj], "Female": [a list of female obj]}
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

    # for stud in tg:
    #     print(stud.Gender, stud.Group, stud.CGPA, end=", ")
    # print(" end")
    
    # return tg  # not needed since we updated the object directly

def get_dict_of_teams(tg):
    team_dict = {}
    print(tg)
    input()
    # print(tg[0].Tutorial_group)

    for stud in tg:
        if stud.Group not in team_dict.keys():
            team_dict[stud.Group] = [stud]
        else:
            team_dict[stud.Group].append(stud)
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
    team_dict[stud1.Group].append(stud2)
    team_dict[stud2.Group].append(stud1)
    team_dict[stud1.Group].remove(stud1)
    team_dict[stud2.Group].remove(stud2)

    # officially swap
    temp_group = stud1.Group
    stud1.Group = stud2.Group
    stud2.Group = temp_group

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
    


def check_results(stud_TG):
    print("Checking results:")
    cgpa_diff_across_tg = []
    types_of_gender_teams = []
    max_school_acroos_tg = []

    # go through all tutorial groups
    for tg in stud_TG.keys():
        print("Tutorial Group:", tg, " number of students:", len(stud_TG[tg]))
        team_dict = get_dict_of_teams(stud_TG[tg])

        # check avg cgpa across all teams
        team_cgpa_list = []
        for team in team_dict.keys():
            total_cgpa = 0.0
            for stud in team_dict[team]:
                total_cgpa += float(stud.CGPA)
            team_cgpa_list.append(total_cgpa / len(team_dict[team]))
        # print("max avg cgpa: ", max(team_cgpa_list), "min avg cgpa: ", min(team_cgpa_list), "avg cgpa diff across team:", max(team_cgpa_list) - min(team_cgpa_list))
        print("avg cgpa diff across team:", max(team_cgpa_list) - min(team_cgpa_list))
        cgpa_diff_across_tg.append(max(team_cgpa_list) - min(team_cgpa_list))

        # check gender distribution
        gender_dict = {}
        for team in team_dict.keys():
            male_count = 0
            female_count = 0
            for stud in team_dict[team]:
                if stud.Gender == "Male":
                    male_count += 1
                else:
                    female_count += 1
            gender_key = "M" + str(male_count) + "F" + str(female_count)
            if gender_key not in gender_dict.keys():
                gender_dict[gender_key] = 1
            else:
                gender_dict[gender_key] = gender_dict[gender_key] + 1
        print(gender_dict)
        types_of_gender_teams.append(len(gender_dict.keys()))

        # check school distribution

        # max number of same school in a team
        max_school_in_team = []
        for team in team_dict.keys():
            school_count = {}
            for stud in team_dict[team]:
                if stud.school not in school_count.keys():
                    school_count[stud.school] = 1
                else:
                    school_count[stud.school] = school_count[stud.school] + 1
            max_school_in_team.append(max(school_count.values()))
        print("max number of same school in a team: ", max(max_school_in_team))
        max_school_acroos_tg.append(max(max_school_in_team))

    print("max cgpa diff across tg: ", max(cgpa_diff_across_tg), "min cgpa diff across tg: ", min(cgpa_diff_across_tg))
    print("max type of gender mixture: ", max(types_of_gender_teams))
    print("max number of same school in a team across tg: ", max(max_school_acroos_tg))
    print("number of tg with", max(max_school_acroos_tg), "same school in a team: ", max_school_acroos_tg.count(max(max_school_acroos_tg)))



# stud_records = read_records()
# stud_TG = group_students(stud_records)
#sort_by_cgpa(stud_TG['G-1'])

# only import and create functions outside. Don't initialize variables outside, as they will become global variables and 
# may mess up codes due to having similar var names in the 'def' / function u coding, the name could confuse u too.
def main():
    stud_records = read_records()
    stud_TG = group_students(stud_records)
    # schools = []

    for tg in stud_TG.keys():
        # print(tg,":")
        tg_sorted_list = []

        # print("Tutorial Group: ", tg, "number of students: ", len(stud_TG[tg]))
        # print_records(sort_by_cgpa(stud_TG[tg]), 6000) # I'm not sure why u want n, but I know n should not be less than students in tutorial group if i want to print the whole tutorial group, i put 6000 cuz maybe got more than 50 in a tutorial group and max is 6000 students so just for fun i put 6000
        # print("Tutorial Group: ", tg, "number of students: ", len(sort_by_cgpa(stud_TG[tg])))
        tg_sorted_list = sort_by_cgpa(stud_TG[tg]) #//sorting algo
        # gender_dict = split_by_gender(tg_sorted_list)
        # print(gender_dict)
        put_into_teams_by_gender(tg_sorted_list)
        # get_dict_of_teams(stud_TG[tg])
        diversify_teams_by_school(tg_sorted_list, 2, 0.1) # highly recommend at least 2 schools per team
        # diversify_teams_by_school(tg_sorted_list) # just run 2x and it fix itself? idk why
    #     for stud in tg_sorted_list:
    #         if stud.school not in schools:
    #             schools.append(stud.school)
    # print(schools)

    check_results(stud_TG)



# start the whole program
main()

