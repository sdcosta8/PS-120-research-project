import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import school_plotting

class boardmember:
    def __init__ (self, years, name, ethnicity, gender):
        self.gender = gender
        self.name = name
        years = str(years).replace(" ", "")
        if ethnicity == 0:
            self.ethnicity = 'N'
        else:
            self.ethnicity = ethnicity
        start_year = years[:4]
        if years[4:] == "-":
            end_year = 2021
        else:
            end_year = years[5:]
        if int(start_year)+1 > int(end_year):
            print("noo")
        self.years = list(range(int(start_year)+1, int(end_year)))

class school:
    def __init__ (self, school_name, start, years, name, ethnicity, gender):
        self.start = int(start) + 1
        self.people = [boardmember(years, name, ethnicity, gender)]
        self.school_name = school_name

    def add_person(self, years, name, ethnicity, gender):
        self.people.append(boardmember(years, name, ethnicity, gender))

class school_graphing:
    def __init__ (self, school_info):
        self.school_name = school_info.school_name
        self.years = list(range(int(school_info.start) - 6, 2021))
        self.year_of_change = int(school_info.start)
        dic = {}
        for year in self.years:
            for person in school_info.people:
                if int(year) in person.years:
                    if year not in dic:
                        dic[year] = [person]
                    else:
                        dic[year].append(person)
        self.year_per_dic = dic
        percent_gender = []
        percent_minority = []
        for year in self.year_per_dic:
            total_min = 0
            total_female = 0
            total_male = 0
            for person in self.year_per_dic[year]:
                if person.ethnicity != 'N':
                    total_min += 1
                if person.gender == 'F':
                    total_female += 1
                else:
                    total_male += 1
            percent_gender.append (total_female/(len(self.year_per_dic[year])))
            percent_minority.append (total_min/(len(self.year_per_dic[year])))
        self.percent_gender = percent_gender
        self.percent_minority = percent_minority
        self.before_aver_lst = np.array(self.percent_minority[:6])
        self.after_aver_lst = np.array(self.percent_minority[6:])
        self.before_aver = np.average(np.array(self.percent_minority[:6]))
        self.after_aver = np.average(np.array(self.percent_minority[6:]))
        self.before_aver_gender = np.average(np.array(self.percent_gender[:6]))
        self.after_aver_gender = np.average(np.array(self.percent_gender[6:]))
        self.before_aver_gender_lst = np.array(self.percent_gender[:6])
        self.after_aver_gender_lst = np.array(self.percent_gender[6:])
        

df = pd.read_excel('school_dis.xlsx')
info = {}
df = df.fillna(0)
for index, row in df.iterrows():
    if row["Term Length"] == 0 or row["Date Switch"] == "can't find info":
        continue
    elif row["District"] not in info:
        info[row["District"]] = school(row["District"], row["Date Switch"], row["Term Length"], row["Name"], row["Race"], row["Gender"])
    else:
        info[row["District"]].add_person( row["Term Length"].strip(), row["Name"], row["Race"], row["Gender"])

dic = {}
before_aver = []
after_aver = []
dicts = {}
gen_dicts = {}
lst_after = []
lst_before = []
school_graph_lst = []
for x in info.values():
    school = (school_graphing(x))
    school_graph_lst.append(school)
    lst_before.append(school.before_aver)
    lst_after.append(school.after_aver)
    school_plotting.t_test(school)
    # school_plotting.t_test_gender(school)
    # school_plotting.plot_individual_schools(school)
    # school_plotting.plot_individual_schools_gender(school)

#school_plotting.generate_all_minority_plots(school_graph_lst)
school_plotting.generate_all_gender_plots(school_graph_lst)

lst_before = np.array(lst_before)
lst_after = np.array(lst_after)

writer = pd.ExcelWriter('school_district_minority.xlsx', engine='xlsxwriter')
dic_percent = {"percent of board members that were a minority before switch" : np.average(lst_before) * 100,
"median of before percentages" :  np.median(lst_before) * 100,
"std of before percentages" :  np.std(lst_before) * 100,
"percent of board members that were a minority after switch" : np.average(lst_after) * 100,
"std of after percentages" :  np.median(lst_after) * 100,
"median of after percentages" :  np.std(lst_after) * 100,
"percent change" : (np.average(lst_after) - np.average(lst_before)) * 100,
}

enrollment_info = pd.DataFrame(data=pd.DataFrame.from_records([dic]))
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1') 

enrollment_info = pd.DataFrame(data=pd.DataFrame(data=dicts))
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1',  startrow=3) 

enrollment_info = pd.DataFrame(data=pd.DataFrame(data=gen_dicts))
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1',  startrow=8) 

enrollment_info = pd.DataFrame(data=pd.DataFrame(data=pd.DataFrame.from_records([dic_percent])))
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1',  startrow=14) 


writer.save()
