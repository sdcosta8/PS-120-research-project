import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
from scipy import stats

def generate_diversity_dic(schools):
    f = open("schooldistrict_ethnicity_info.txt", "r")
    school_dic = {}
    for x in f:
        lst = x.split()
        dist_index = lst.index("DISTRICT")
        ethn_index = lst.index("ETHNIC")
        stud_index = lst.index("ENR_TOTAL")
        break

    for x in f:
        lst = x.split('\t')
        if lst[dist_index] not in school_dic:
            school_dic[lst[dist_index]] = {lst[ethn_index] : int(lst[stud_index])}
        else:
            if lst[ethn_index] not in school_dic[lst[dist_index]]:
                school_dic[lst[dist_index]][lst[ethn_index]] = int(lst[stud_index])
            else:
                school_dic[lst[dist_index]][lst[ethn_index]] += int(lst[stud_index])

    for key in sorted(list(school_dic.keys())):
        school_dic[key]["total_enrollment"] = sum(school_dic[key].values())
    dic = {}
    for school in schools:
        per_minority = 0
        school_name = school.school_name
        if '5' in school_dic[school_name]:
            per_minority += school_dic[school_name]["5"] 
        if '6' in school_dic[school_name]:
            per_minority +=  school_dic[school_name]["6"] 
        if '2' in school_dic[school_name]:
            per_minority +=  school_dic[school_name]["2"] 
        if '3' in school_dic[school_name]:
            per_minority += school_dic[school_name]["3"] 
        if '4' in school_dic[school_name]:
            per_minority += school_dic[school_name]["4"]
        dic[school_name] = per_minority/school_dic[school_name]["total_enrollment"] * 100
    return dic


def plot_1 (schools, diversity_dic):
    for school in schools:
        if school.before_aver < school.after_aver:
            c = "green"
        elif school.before_aver == school.after_aver:
            c = "yellow"
        else:
            c = "red"
        per_minority = diversity_dic[school.school_name]
        plt.plot([per_minority, per_minority], [school.before_aver * 100, school.after_aver * 100], marker="o", color = c)
    red_patch = mpatches.Patch(color='red', label='Negative change in (%) of minority board members')
    green_patch = mpatches.Patch(color='green', label='Positive change in (%) of minority board members')
    yellow_patch = mpatches.Patch(color='yellow', label='No change in (%) of minority board members')
    plt.legend(handles=[red_patch, green_patch, yellow_patch])
    plt.xlabel("Percent of school enrollment that are minorities")
    plt.ylabel("Percent of board members that are a minority (%)")
    plt.xticks(rotation=90)
    plt.show()

def plot_1_gender (schools, diversity_dic):
    for school in schools:
        if school.before_aver_gender < school.after_aver_gender:
            c = "green"
        elif school.before_aver_gender == school.after_aver_gender:
            c = "yellow"
        else:
            c = "red"
        per_minority = diversity_dic[school.school_name]
        plt.plot([per_minority, per_minority], [school.before_aver_gender * 100, school.after_aver_gender * 100], marker="o", color = c)
    red_patch = mpatches.Patch(color='red', label='Negative change in (%) of female board members')
    green_patch = mpatches.Patch(color='green', label='Positive change in (%) of female board members')
    yellow_patch = mpatches.Patch(color='yellow', label='No change in (%) of female board members')
    plt.legend(handles=[red_patch, green_patch, yellow_patch])
    plt.xlabel("Percent of school enrollment that are minorities (%)")
    plt.ylabel("Percent change of board members that are female (%)")
    plt.xticks(rotation=90)
    plt.show()
        
        
def plot_2 (schools, diversity_dic):
    x = []
    y = []
    for school in schools:
        per_minority = diversity_dic[school.school_name]
        if school.before_aver < school.after_aver:
            c = "green"
        elif school.before_aver == school.after_aver:
            c = "yellow"
        else:
            c = "red"
        x.append(per_minority)
        y.append(school.after_aver * 100 - school.before_aver * 100)
        plt.plot([per_minority], [school.after_aver * 100 - school.before_aver * 100], marker="o", color = c)
    red_patch = mpatches.Patch(color='red', label='Negative change in (%) of minority board members')
    green_patch = mpatches.Patch(color='green', label='Positive change in (%) of minority board members')
    yellow_patch = mpatches.Patch(color='yellow', label='No change in (%) of minority board members')
    plt.legend(handles=[red_patch, green_patch, yellow_patch])
    
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    print("r = " +  str(r_value) + " p = " + str(p_value) + " std_error = "  + str(std_err) )
    x1=np.linspace(0,100,500)
    y1=gradient*x1+intercept
    plt.plot(x1,y1,'--k')
    plt.xlabel("Percent of school enrollment that are minorities (%)")
    plt.ylabel("Percent change of board members that are a minority (%)")
    plt.xticks(rotation=90)
    plt.show()

def plot_2_gender (schools, diversity_dic):
    x = []
    y = []
    for school in schools:
        per_minority = diversity_dic[school.school_name]
        if school.before_aver_gender < school.after_aver_gender:
            c = "green"
        elif school.before_aver_gender == school.after_aver_gender:
            c = "yellow"
        else:
            c = "red"
        x.append(per_minority)
        y.append(school.after_aver_gender * 100 - school.before_aver_gender * 100)
        plt.plot([per_minority], [school.after_aver * 100 - school.before_aver * 100], marker="o", color = c)
    red_patch = mpatches.Patch(color='red', label='Negative change in (%) of female board members')
    green_patch = mpatches.Patch(color='green', label='Positive change in (%) of female board members')
    yellow_patch = mpatches.Patch(color='yellow', label='No change in (%) of female board members')
    plt.legend(handles=[red_patch, green_patch, yellow_patch])
    
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    print("r = " +  str(r_value) + " p = " + str(p_value) + " std_error = "  + str(std_err) )
    x1=np.linspace(0,100,500)
    y1=gradient*x1+intercept
    plt.plot(x1,y1,'--k')
    plt.xlabel("Percent of school enrollment that are minorities")
    plt.ylabel("Percent of board members that are female (%)")
    plt.xticks(rotation=90)
    plt.show()

def plot_3 (schools, diversity_dic):
    for school in schools:
        per_minority = diversity_dic[school.school_name]
        plt.plot([per_minority], [school.after_aver * 100], marker="o", color = 'b')
    plt.xlabel("Percent of school enrollment that are minorities")
    plt.ylabel("Percent of board members that are a minority (%)")
    plt.title("Percent After")
    plt.xticks(rotation=90)
    plt.show()


def plot_3_gender (schools, diversity_dic):
    for school in schools:
        per_minority = diversity_dic[school.school_name]
        plt.plot([per_minority], [school.after_aver_gender * 100], marker="o", color = 'b')
    plt.xlabel("Percent of school enrollment that are minorities")
    plt.ylabel("Percent of board members that are female (%)")
    plt.xticks(rotation=90)
    plt.title("Percent After")
    plt.show()

def plot_4 (schools, diversity_dic):
    for school in schools:
        per_minority = diversity_dic[school.school_name]
        plt.plot([per_minority], [school.before_aver * 100], marker="o", color = 'b')
    plt.xlabel("Percent of school enrollment that are minorities")
    plt.ylabel("Percent of board members that are a minority (%)")
    plt.xticks(rotation=90)
    plt.title("Percent BEFORE")
    plt.show()

def plot_4_gender (schools, diversity_dic):
    for school in schools:
        per_minority = diversity_dic[school.school_name]
        plt.plot([per_minority], [school.before_aver_gender * 100], marker="o", color = 'b')
    plt.xlabel("Percent of school enrollment that are minorities")
    plt.ylabel("Percent of board members that are female (%)")
    plt.title("Percent BEFORE")
    plt.xticks(rotation=90)
    plt.show()


def plot_individual_schools (school):
    plt.xlabel("School District Name")
    plt.ylabel("Percent of board members that are a minority (%)")
    plt.plot(school.years, school.percent_minority)
    plt.plot(school.year_of_change, school.percent_minority[6], marker="o")
    plt.title(school.school_name)
    plt.show()

def plot_individual_schools_gender (school):
    plt.xlabel("School District Name")
    plt.ylabel("Percent of board members that are female (%)")
    plt.plot(school.years, school.percent_gender)
    plt.plot(school.year_of_change, school.percent_gender[6], marker="o")
    plt.title(school.school_name)
    plt.show()

def plot_all_schools (schools):
    for x in schools:
        if x.before_aver < x.after_aver:
            c = "green"
        else:
            c = "red"
        plt.plot([x.school_name, x.school_name], [x.before_aver * 100, x.after_aver * 100], marker="o", color = c)
    plt.xlabel("School District Name")
    plt.ylabel("Percent of board members that are a minority (%)")
    plt.xticks(rotation=90)
    plt.show()

def plot_all_schools_gender (schools):
    for x in schools:
        if x.before_aver < x.after_aver:
            c = "green"
        else:
            c = "red"
        plt.plot([x.school_name, x.school_name], [x.before_aver_gender * 100, x.after_aver_gender * 100], marker="o", color = c)
    plt.xlabel("School District Name")
    plt.ylabel("Percent of board members that are female (%)")
    plt.xticks(rotation=90)
    plt.show()



def t_test(school):
    t2, p2 = stats.ttest_ind(school.after_aver_lst, school.before_aver_lst)
    print(school.school_name, t2, p2)

def t_test_gender(school):
    t2, p2 = stats.ttest_ind(school.after_aver_gender_lst, school.before_aver_gender_lst)
    print(school.school_name, t2, p2)

def year_graph(schools):
    dic = {}
    for school in schools:
        i = 0
        for percentage in school.after_aver_lst:
            if i in dic:
                dic[i].append(percentage * 100)
            else:
                dic[i] = [percentage * 100]
            i += 1
    i = 0
    j = 0
    for key in dic.keys():
        # print(j + 1, np.average(dic[key]), np.std(dic[key]), len(dic[key]))
        j += 1
        if len((dic[key])) > 4:
            i += 1
            plt.errorbar(key + 1, np.average(dic[key]), yerr=np.std(dic[key]), marker="o", color= "b", ecolor='r', capsize=2)
    plt.xlim([0, i + 1])
    plt.ylim([0, 100])
    plt.xlabel("Years after change from At-large elections")
    plt.ylabel("Average percent of board that identify as a minority (%)")
    plt.show()

def year_graph_gender(schools):
    dic = {}
    for school in schools:
        i = 0
        for percentage in school.after_aver_gender_lst:
            if i in dic:
                dic[i].append(percentage * 100)
            else:
                dic[i] = [percentage * 100]
            i += 1
    i = 0
    j = 0
    for key in dic.keys():
        # print(j + 1, np.average(dic[key]), np.std(dic[key]), len(dic[key]))
        j += 1
        if len((dic[key])) > 4:
            i += 1
            plt.errorbar(key + 1, np.average(dic[key]), yerr=np.std(dic[key]), marker="o", color= "b", ecolor='r', capsize=2)
    plt.xlim([0, i + 1])
    plt.ylim([0, 100])
    plt.xlabel("Years after change from At-large elections")
    plt.ylabel("Average percent of board that are female (%)")
    plt.show()

def generate_all_gender_plots(schools):
    diversity_dic = generate_diversity_dic(schools)
    year_graph_gender(schools)
    plot_all_schools_gender(schools)
    plot_all_schools_gender(schools[:(int(len(schools)/2))])
    plot_all_schools_gender(schools[(int(len(schools)/2)):]) 
    plot_1_gender(schools, diversity_dic)
    plot_2_gender(schools, diversity_dic)
    plot_3_gender(schools, diversity_dic)
    plot_4_gender(schools, diversity_dic)

def generate_all_minority_plots(schools):
    diversity_dic = generate_diversity_dic(schools)
    year_graph(schools)
    plot_all_schools(schools)
    plot_all_schools(schools[:(int(len(schools)/2))])
    plot_all_schools(schools[(int(len(schools)/2)):]) 
    plot_1(schools, diversity_dic)
    plot_2(schools, diversity_dic)
    plot_3(schools, diversity_dic)
    plot_4(schools, diversity_dic)