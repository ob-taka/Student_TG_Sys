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

# a binary tree where lowest cgpa is left most node and highest cgpa is right most node
def cgpa_tree(stud_list, stud):
    # node is a empty, add student as leaf
    if stud_list == []:
        return [stud]
    # node is a leaf, promote leaf to branch and add new student as leaf .. [left leaf, branch, right leaf]
    elif len(stud_list) == 1:
        # compare cgpa of student, if cgpa higher, add new student as right leaf, else (equal/lower) add new student as left leaf
        if stud.CGPA > stud_list[0].CGPA:
            return [[], stud_list[0], [stud]] 
        else:
            return [[stud], stud_list[0], []]
    # node is a branch ## more chim explaination: node is a branch/subtree/tree no one knows, thats why we go deeper (call cgpa_tree recursively) ##
    elif len(stud_list) == 3:
        # compare cgpa with the branch/parent .. [[left child],[parent],[right child]], if cgpa higher, go right, else (equal/lower) go left
        if stud.CGPA > stud_list[1].CGPA:
            stud_list[2] = cgpa_tree(stud_list[2], stud)
            return stud_list
        else:
            stud_list[0] = cgpa_tree(stud_list[0], stud)
            return stud_list
    
    # sort cgpa by highest to lowest .. only 'if' statements are changed ## cgpa diff across teams/tg 0.20199999, ~0.03 more than sorting lowest to highest ##
    # if stud_list == []:
    #     return [stud]
    # elif len(stud_list) == 1:
    #     if stud.CGPA < stud_list[0].CGPA: # only the > sign is changed to < sign
    #         return [[], stud_list[0], [stud]]
    #     else:
    #         return [[stud], stud_list[0], []]
    # elif len(stud_list) == 3:
    #     if stud.CGPA < stud_list[1].CGPA: # only the > sign is changed to < sign
    #         stud_list[2] = cgpa_tree(stud_list[2], stud)
    #         return stud_list
    #     else:
    #         stud_list[0] = cgpa_tree(stud_list[0], stud)
    #         return stud_list

# read a tree of students and return a list from left to right [lowestCGPA, ..., highestCGPA]
def read_tree(tree, list):
    # go through each node in tree [node, student, node] or a leaf [student]
    for i in tree:
        if i == []: # empty node, ignore
            continue
        elif type(i) == student.Student: # node is a student, add to list
            list.append(i)
        else: # node is unknown, go deeper ## node could be another tree [node, student, node] or a leaf [student], can add elif to check if u want ##
            read_tree(i, list)

    return list

# take a list of students and return it sorted by lowest cgpa (first in list) to highest cgpa (last in list)
def sort_by_cgpa(tg):
    # initialize
    cgpa_sorted_tree = []

    # add each student into the tree (the tree gets bigger as more students are added)
    for stud in tg:
        cgpa_sorted_tree = cgpa_tree(cgpa_sorted_tree, stud)

    # turn tree into list [lowestCGPA, ..., highestCGPA] then return the result
    return read_tree(cgpa_sorted_tree, [])

# return a dictionary of list {"Male": [student, ...], "Female":[student, ...]}
def split_by_gender(tg):
    # initialize
    gender_dict = {}

    # add each student into list by gender
    for stud in tg:
        if stud.Gender not in gender_dict.keys(): # only used to initialize the key "Male" / "Female", and value as list [student] ## by all means we can init gender_dict = {"Male": [], "Female": []} then we can delete this if statement, im just being safe, incase got "others" as gender ##
            gender_dict[stud.Gender] = [stud]
        else:
            gender_dict[stud.Gender].append(stud) 

    # since we are using cgpa_sorted_tg, the list is already sorted by cgpa, so we don't need to sort it again
    # from this for loop, we can see that the students are still sorted by CGPA after splitting into gender groups
    # for gender in gender_dict.keys():
    #     print(gender, ":", end=" [ ")
    #     for stud in gender_dict[gender]:
    #         print(stud.CGPA, end=", ")
    #     print("]")

    return gender_dict

# split students into teams as evenly as possible by gender
# ideal team [avg_CGPA(male/female), high_CGPA_male, low_CGPA_male, high_CGPA_female, low_CGPA_female] ## the intention is for high and low to avg out their own cgpa, (5.0 + 3.0) / 2 = 4.0cgpa ##
# flaw is when gender ratio is around 1:4, [avg_CGPA(male), high_CGPA_female, low_CGPA_female, high_CGPA_female, low_CGPA_female] ## the last few teams will have either highest cgpa male or lowest cgpa male ##
# flaw 2, code does not work if number of students is not divisible by team_size, e.g. 50 students, team_size is 6, 2 students will have no team
# flaw 3, code does not work if team_size is even number, e.g. 6
def create_teams_by_gender(tg, team_size = 5):
    # initialize
    gender_dict = split_by_gender(tg) # {"Male": [male students], "Female": [female students]}
    number_of_teams = len(tg)//team_size ## if team_size = 6, 50//6 = 8, 50%6 = 2, 8 teams with 6 students, 2 students will have no team ##
    should_take_from_top = True # top as in top of the list, in this case, first in list ## no need to reinitalize for every team, since i take the odd male/female (during take avg), so we are left with even numbers in both male to take and female to take, each pair will auto reset this var to true ##
    
    # atleast x number of males in each team, e.g. 16 males, 10 teams, 16//10 = 2, at least 1 males per team
    base_males = len(gender_dict['Male']) // number_of_teams
    # number of teams with 1 extra male, e.g. 16 males, 10 teams, 16 % 10 = 6, add 1 more male to first 6 teams
    extra_males = len(gender_dict['Male']) % number_of_teams

    # note that loop start with 1, meaning first team is team 1
    for team in range(1, number_of_teams + 1):
        male_taken = 0
        # we take avg from odd gender, so the remaining gender to add to teams are multiples of 2, which then we take 1 top CGPA and 1 bottom CGPA.
        should_take_avg = True

        # assign i students to team. ## A flaw in this is that the last team may have less students in than team_size (e.g. 50 / 6, the loop will run out of range on last team) ##
        for i in range(team_size):
            # first student in team has avg cgpa
            if should_take_avg:
                # take avg cgpa male when number of males that should be in this team are odd, else take avg cgpa female
                ## this if statement does a few things, explaination below ##
                ## first few teams has extra male .. if (team <= extra_males), base male + 1 extra .. does not add 1 if no need extra male ##
                ## check if there is an odd number of males in this team .. (base_male + 1) % 2 == 1 .. does not add 1 if no need extra male ##
                ## else, there is an even number of males in this team, we take from female ... flaw is that if team_size is even number e.g. 6, then both gender in team are odd or even, to which we either take or dont take avg at all .. 3male 3female or 2male 4female .. check if females in team is odd ##
                if (team <= extra_males and (base_males + 1) % 2 == 1) or (team > extra_males and base_males % 2 == 1):
                    gender_dict['Male'][len(gender_dict['Male'])//2].Group = team # assign team to avg cgpa male student in list
                    gender_dict['Male'] = gender_dict['Male'][:len(gender_dict['Male'])//2] + gender_dict['Male'][len(gender_dict['Male'])//2 + 1:] # remove avg male student from list
                    male_taken += 1
                else:
                    gender_dict['Female'][len(gender_dict['Female'])//2].Group = team # assign team to avg cgpa female student
                    gender_dict['Female'] = gender_dict['Female'][:len(gender_dict['Female'])//2] + gender_dict['Female'][len(gender_dict['Female'])//2 + 1:] # remove avg female student from list

                should_take_avg = False
                continue # student taken, skip rest of code and move to next loop

            # take males first, then females
            if  male_taken < base_males or (team <= extra_males and male_taken < base_males + 1):
                if should_take_from_top: # remember that first in list is lowest cgpa ## the naming of this variable is abit weird, take from top means top of the list and not top ranking cgpa student, feel free to change to var name ##
                    gender_dict['Male'][0].Group = team # assign team to first male student
                    gender_dict['Male'] = gender_dict['Male'][1:] # remove first male student from list
                    should_take_from_top = False
                else:
                    gender_dict['Male'][-1].Group = team # assign team to last male student
                    gender_dict['Male'] = gender_dict['Male'][:-1] # remove last male student from list
                    should_take_from_top = True
                male_taken += 1
            else:
                if should_take_from_top:
                    gender_dict['Female'][0].Group = team # assign team to first female student
                    gender_dict['Female'] = gender_dict['Female'][1:] # remove first female student from list
                    should_take_from_top = False
                else:
                    gender_dict['Female'][-1].Group = team # assign team to last female student
                    gender_dict['Female'] = gender_dict['Female'][:-1] # remove last female student from list
                    should_take_from_top = True
    ## no return of anything as we update the student object directly. if we were using a dictionary to store student details instead of student object, then we would need to update and return the dict/list/updated tg ##

# return a dictionary of list {team: [list of students], ...}
## team (key) in dict is not in order, if a cgpa_sorted_tg is thrown here, for each team, the student (value) in the list will be in order of cgpa (lowest to highest) ##
def get_dict_of_teams(tg):
    team_dict = {}
    
    for stud in tg:
        if stud.Group not in team_dict.keys():
            team_dict[stud.Group] = [stud]
        else:
            team_dict[stud.Group].append(stud)

    return team_dict

# see if can swap students (similar cgpa and same gender)
## can just throw this if statement in the code since i only used it once, the code was getting too complex with alot of loops and ifs so i took this out ##
def is_swappable(stud1, stud2, allowed_cgpa_diff):
    # if gender is same, cgpa diff is within allowed_cgpa_diff, and school is different, then return true / it is swappable
    ## abs() just make the diff a positive number, cuz negative number (-0.xxx)) is always smaller than allowed_cgpa_diff (0.1) ##
    if stud1.Gender == stud2.Gender and abs(float(stud1.CGPA) - float(stud2.CGPA)) < allowed_cgpa_diff and stud1.school != stud2.school:
        return True
    else:
        return False

# swap teams for 2 students
## can just throw this code back since i only used it once, the code was getting too complex with alot of loops and ifs so i took this out ##
def swap_group(stud1, stud2, team_dict):
    # swap team in team_dict
    team_dict[stud1.Group].append(stud2)
    team_dict[stud2.Group].append(stud1)
    team_dict[stud1.Group].remove(stud1)
    team_dict[stud2.Group].remove(stud2)

    # swap team in student object
    temp_group = stud1.Group
    stud1.Group = stud2.Group
    stud2.Group = temp_group

    return team_dict

# check if selected school has reached allowed_school_per_team in this team
def is_school_limit_reached(team, selected_school, allowed_schools_per_team):
    school_count = 0

    for stud in team:
        if stud.school == selected_school:
            school_count += 1
            if school_count == allowed_schools_per_team: # school limit is reached ## no need >= since it instantly exit/end function via return ##
                return True
    # school limit is not reached, have space to add more student of same school
    return False

# try to swap students so their teams does not consist of students with same schools more than allowed_schools_per_team, allow swapping if student cgpa is within allow_cgpa_diff
def diversify_teams_by_school(tg, allowed_schools_per_team = 2, allowed_cgpa_diff = 0.1):
    # allowed_schools_per_team = max(allowed_schools_per_team, 2) # hell no am i trusting the user. at least 2 schools per team!
    team_dict = get_dict_of_teams(tg)
    swap_overlap_dict = {}

    # record teams with excess students from same school to swap out
    for team in team_dict.keys():
        school_list = []
        swap_counter = {}

        for stud in team_dict[team]:
            school_list.append(stud.school)

            # when school limit is reached, record number of students that should swap out
            if school_list.count(stud.school) > allowed_schools_per_team:
                if stud.school not in swap_counter.keys():
                    swap_counter[stud.school] = 1
                else:
                    swap_counter[stud.school] = swap_counter[stud.school] + 1

        # only record when students in this team need swapping
        if swap_counter != {}:
            swap_overlap_dict[team] = swap_counter

    # deversify schools in teams that have excess students from same school
    for team in swap_overlap_dict.keys():
        swappable_students = {} # {school: [list of swappable students]}

        # get list of swappable students in teams that should swap ## possible swap candidates for teams with overlap ##
        for stud in team_dict[team]:
            if stud.school in swap_overlap_dict[team].keys():
                if stud.school not in swappable_students.keys():
                    swappable_students[stud.school] = [stud]
                else:
                    swappable_students[stud.school].append(stud)
        
        # for each school in team that should swap
        for school in swap_overlap_dict[team].keys():
            number_to_swap = swap_overlap_dict[team][school]
            number_swapped = 0

            # for each student in selected school that can swap ## possible swap candidates, not all students in list need to swap ##
            for stud in swappable_students[school]:
                has_swapped = False

                # check with other teams
                for other_team in team_dict.keys():
                    if other_team == team: # same team, no need to check ## if statement may not be nescessary ##
                        continue
                    if is_school_limit_reached(team_dict[other_team], school, allowed_schools_per_team): # current student will exceed school limit in other team, skip this team
                        continue
                    
                    # check with other students in other team
                    for other_stud in team_dict[other_team]:
                        if is_school_limit_reached(team_dict[team], other_stud.school, allowed_schools_per_team): # check if other student will exceed school limit of current team, skip this student
                            continue
                        if is_swappable(stud, other_stud, allowed_cgpa_diff):
                            team_dict = swap_group(stud, other_stud, team_dict) # update team_dict, very important, or else teams may get duplicate students / corrupted
                            number_swapped += 1
                            has_swapped = True
                            break # student has been swapped, no need to check with other students in other team

                    if has_swapped: # student has been swapped, no need to check with other teams
                        break

                if number_swapped == number_to_swap: # team is now within school limit for selected school, no need to swap remaining candidates
                    break
            ## nothing happens if fail to swap ##
        ## nothing happens if no team need swapping ##
    
    # look at school distribution
    # team_school_dict = {}
    # for team in team_dict.keys():
    #     stud_school_list = []
    #     for stud in team_dict[team]:
    #         stud_school_list.append(stud.school)
    #     team_school_dict[team] = stud_school_list
    # print(team_school_dict)
    ## no return of anything as we update the student object directly. since team_dict is updated, we can choose to return it, but it is not nescessary ##

# check diversity among all tg
def check_results(stud_TG):
    print("Checking results:")
    cgpa_diff_across_tg = []
    types_of_gender_teams = []
    max_school_across_tg = []

    # go through all tutorial groups
    for tg in stud_TG.keys():
        # print(tg, ":")

        # get dict of teams
        # cgpa_sorted_tg = sort_by_cgpa(stud_TG[tg])
        # team_dict = get_dict_of_teams(cgpa_sorted_tg)
        team_dict = get_dict_of_teams(stud_TG[tg])

        # check avg cgpa across all teams
        team_cgpa_list = []
        for team in team_dict.keys():
            total_cgpa = 0.0
            for stud in team_dict[team]:
                total_cgpa += float(stud.CGPA)
            team_cgpa_list.append(total_cgpa / len(team_dict[team]))
        # print(team_cgpa_list)
        cgpa_diff_across_tg.append(max(team_cgpa_list) - min(team_cgpa_list)) # record team cgpa diff in tg

        # check gender distribution
        gender_dict = {} # {"gender mixture": int(number of teams with same gender cocktail), ...} .. should be 2 or less keys
        for team in team_dict.keys():
            male_count = 0
            female_count = 0
            for stud in team_dict[team]: # count number of males and females in team
                if stud.Gender == "Male":
                    male_count += 1
                else:
                    female_count += 1
            gender_key = "M" + str(male_count) + "F" + str(female_count) # dictionary key is gender mixture e.g. M3F2, M2F3, etc
            if gender_key not in gender_dict.keys():
                gender_dict[gender_key] = 1
            else:
                gender_dict[gender_key] = gender_dict[gender_key] + 1
        # print(gender_dict)
        types_of_gender_teams.append(len(gender_dict.keys())) # record number of different gender mixtures in tg  .. should be 2 or less

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
        # print(max_school_in_team)
        max_school_across_tg.append(max(max_school_in_team)) # record highest number of same school in a tg

    print("max (cgpa diff) across tg: ", max(cgpa_diff_across_tg), "min cgpa diff across tg: ", min(cgpa_diff_across_tg)) # less = better
    print("max (type of gender distribution) across tg: ", max(types_of_gender_teams)) # should be 2 or less
    print("max (number of same school in a team) across tg: ", max(max_school_across_tg)) # as close as x stated in diversify_teams_by_school ([], x, cgpa_tolerance) # if more than x, less = better
    print("number of tg with", max(max_school_across_tg), "same school in a team: ", max_school_across_tg.count(max(max_school_across_tg))) # if more than x (shown above), less = better, else (same/less than x) ignore this


# only import and create functions outside. Don't initialize variables outside, as they will become global variables and 
# may mess up codes due to having similar var names in the 'def'/function u coding, the name could confuse u too.
def main():
    # initialize variables
    stud_records = read_records()
    stud_TG = group_students(stud_records)
    allowed_schools_per_team = 2
    allowed_cgpa_diff = 0.05

    # diversify the teams in tg
    for tg in stud_TG.keys():
        cgpa_sorted_tg = [] # its a habit of mine to initialize variables before using it, but not necessary in python
        cgpa_sorted_tg = sort_by_cgpa(stud_TG[tg])
        create_teams_by_gender(cgpa_sorted_tg)
        diversify_teams_by_school(cgpa_sorted_tg, allowed_schools_per_team, allowed_cgpa_diff) # highly recommend at least 2 schools per team, or else the code will be too hesitant to swap students

    #TODO: update results into students.csv


    # show how diverse the teams are
    check_results(stud_TG)


# start the whole program
main()

# i prioritize gender, then cgpa, then school
# this is so as the first most notable difference in teams is the gender ratio, we need to convince the students that the teams are balanced, so i decided to tackle what they can see / what is most obvious
# then cgpa to ensure that the teams are balanced in terms of cgpa, if students compare cgpa within the group they will realise that each high cgpa student is paired with a low cgpa student
# lastly is the school/course they are in, i do not see much merit in this, but i understand that each school focus on different things, which results in students tracking different things, and the different perspectives from tracking dfferent things may be useful in their team/project. so here u go.