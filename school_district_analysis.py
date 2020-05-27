import pandas as pd
import numpy as np
f = open("schooldistrict_demo_info.txt", "r")
dic = {}
for x in f:
    lst = x.split()
    dist_index = lst.index("DISTRICT")
    ethn_index = lst.index("ETHNIC")
    stud_index = lst.index("ENR_TOTAL")
    break

for x in f:
    lst = x.split('\t')
    if lst[dist_index] not in dic:
        dic[lst[dist_index]] = {lst[ethn_index] : int(lst[stud_index])}
    else:
        if lst[ethn_index] not in dic[lst[dist_index]]:
            dic[lst[dist_index]][lst[ethn_index]] = int(lst[stud_index])
        else:
            dic[lst[dist_index]][lst[ethn_index]] += int(lst[stud_index])

for key in dic.keys():
    dic[key]["total_enrollment"] = sum(dic[key].values())
    #print(dic[key]['5']/dic[key]["total_enrollment"])



df = pd.read_excel('District info.xlsx')
district = []
at_large = []
pre_dist = []
unclear = []
for index, row in df.iterrows():
    if row["District or At-large"] == 'At-large/But changing' or row["District or At-large"] == 'At-large':
        at_large.append(row['Districts'])
    elif  row["District or At-large"] == 'Post-CVRA Elections' or row["District or At-large"] == 'Pre-CVRA Elections'  :
        district.append(row['Districts'])
    else:
        unclear.append(row['Districts'])
    if row["District or At-large"] == 'Post-CVRA Elections':
        pre_dist.append(row['Districts'])

district = np.array(district)
at_large = np.array(at_large)
pre_dist = np.array(pre_dist)

total = 0
total_latino = np.array([])
total_black = np.array([])
total_asian = np.array([])
for school in district:
    asian = 0
    total += dic[school]["total_enrollment"]
    if '5' in dic[school]:
        total_latino = np.append(total_latino, dic[school]["5"] /  dic[school]["total_enrollment"])
    if '6' in dic[school]:
        total_black = np.append(total_black, dic[school]["6"] /  dic[school]["total_enrollment"])
    if '2' in dic[school]:
        asian +=  dic[school]["2"] 
    if '3' in dic[school]:
        asian += dic[school]["3"]
    if '4' in dic[school]:
        asian +=  dic[school]["4"]
    if asian != 0:
        total_asian = np.append(total_asian, asian / dic[school]["total_enrollment"])

students_dis = total  
latino_dis = total_latino
black_dis = total_black
asian_dis = total_asian

total = 0
total_latino = np.array([])
total_black = np.array([])
total_asian = np.array([])

for school in at_large:
    asian = 0
    total += dic[school]["total_enrollment"]
    if '5' in dic[school]:
        total_latino = np.append(total_latino, dic[school]["5"] /  dic[school]["total_enrollment"])
    if '6' in dic[school]:
        total_black = np.append(total_black, dic[school]["6"] /  dic[school]["total_enrollment"])
    if '2' in dic[school]:
        asian +=  dic[school]["2"] 
    if '3' in dic[school]:
        asian += dic[school]["3"]
    if '4' in dic[school]:
        asian +=  dic[school]["4"]
    if asian != 0:
        total_asian = np.append(total_asian, asian / dic[school]["total_enrollment"])

students_at_large = total  
latino_at_large = total_latino
black_at_large = total_black
asian_at_large = total_asian

total = 0
total_latino = np.array([])
total_black = np.array([])
total_asian = np.array([])
for school in pre_dist:
    asian = 0
    total += dic[school]["total_enrollment"]
    if '5' in dic[school]:
        total_latino = np.append(total_latino, dic[school]["5"] /  dic[school]["total_enrollment"])
    if '6' in dic[school]:
        total_black = np.append(total_black, dic[school]["6"] /  dic[school]["total_enrollment"])
    if '2' in dic[school]:
        asian +=  dic[school]["2"] 
    if '3' in dic[school]:
        asian += dic[school]["3"]
    if '4' in dic[school]:
        asian +=  dic[school]["4"]
    if asian != 0:
        total_asian = np.append(total_asian, asian / dic[school]["total_enrollment"])


students_pre_dist = total  
latino_pre_dist = total_latino
black_pre_dist = total_black
asian_pre_dist = total_asian

df_financial = pd.read_excel('expense data.xlsx')
total_money_at_large = []
total_money_district = []
for index, row in df_financial.iterrows():
    if row["DISTRICT"].upper() in map(str.upper, at_large):
        total_money_at_large.append(row["Current\nExpense Per ADA"])

    elif row["DISTRICT"].upper() in map(str.upper, district):
        total_money_district.append(row["Current\nExpense Per ADA"])

calculated_financial_stats = {"Average Current Expense Per ADA for district schools" :
                            np.average(total_money_district), "Average Current Expense Per ADA for at-large schools" :
                            np.average(total_money_at_large), "Median Current Expense Per ADA for district schools" :
                            np.median(total_money_district), "Median Current Expense Per ADA for at-large schools" :
                            np.median(total_money_at_large), "STD Current Expense Per ADA for district schools" :
                            np.std(total_money_district), "STD Current Expense Per ADA for at-large schools" :
                            np.std(total_money_at_large)}

calculated_stats_dist = {"Number School Dist" : len(district), "Total enrollment" : students_dis,
                             "Average enrollment" : students_dis/len(district), "enrollment std": np.std(np.array([dic[school]["total_enrollment"] for school in district])),  "Latino std students" : np.std(latino_dis),
                             "Average percent Latino students" : np.average(latino_dis), "Black std students" : np.std(black_dis),
                             "Average  percent Black students" : np.average(black_dis), "Asian std students" : np.std(asian_dis),
                             "Average percent Asian students" : np.average(asian_dis), "enrollment median" : np.median(np.array([dic[school]["total_enrollment"] for school in district])),
                             "Median Latino Students" : np.median(latino_dis), "Median Black Students" : np.median(black_dis), "Median Asian Students" : np.median(asian_dis) }

calculated_stats_pre_dist = {"Number School Dist" : len(pre_dist), "Total enrollment" : students_pre_dist,
                             "Average enrollment" : students_pre_dist/len(pre_dist), "enrollment std": np.std(np.array([dic[school]["total_enrollment"] for school in pre_dist])),  "Latino std students" : np.std(latino_pre_dist),
                             "Average percent Latino students" : np.average(latino_pre_dist), "Black std students" : np.std(black_pre_dist),
                             "Average  percent Black students" : np.average(black_pre_dist), "Asian std students" : np.std(asian_pre_dist),
                             "Average percent Asian students" : np.average(asian_pre_dist), "enrollment median" : np.median(np.array([dic[school]["total_enrollment"] for school in pre_dist])),
                             "Median Latino Students" : np.median(latino_pre_dist), "Median Black Students" : np.median(black_pre_dist), "Median Asian Students" : np.median(asian_pre_dist) }


calculated_stats_at_large = {"Number School Dist" : len(at_large), "Total enrollment" : students_at_large,
                             "Average enrollment" : students_at_large/len(at_large), "enrollment std": np.std(np.array([dic[school]["total_enrollment"] for school in at_large])), "Latino std students" : np.std(latino_at_large),
                             "Average percent Latino students" : np.average(latino_at_large), "Black std students" : np.std(black_at_large),
                             "Average percent Black students" : np.average(black_at_large), "Asian std students" : np.std(asian_at_large),
                             "Average percent Asian students" : np.average(asian_at_large), "enrollment median" : np.median(np.array([dic[school]["total_enrollment"] for school in at_large])),
                             "Median Latino Students" : np.median(latino_at_large), "Median Black Students" : np.median(black_at_large), "Median Asian Students" : np.median(asian_at_large) }

dic_school_pre_dist = {}
for school in pre_dist:
    dic_school_pre_dist[school] = dic[school] 

dic_school_dist = {}
for school in district:
    dic_school_dist[school] = dic[school]

dic_school_atlarge = {}
for school in at_large:
    dic_school_atlarge[school] = dic[school] 

writer = pd.ExcelWriter('school_district_enroll.xlsx', engine='xlsxwriter')

enrollment_info = pd.DataFrame(data=dic_school_dist)
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1')  

enrollment_info = pd.DataFrame(data=dic_school_atlarge)
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1',  startrow=13)  

enrollment_info = pd.DataFrame(data=pd.DataFrame.from_records([calculated_stats_dist]))
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1',  startrow=26) 

enrollment_info = pd.DataFrame(data=pd.DataFrame.from_records([calculated_stats_at_large]))
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1',  startrow=29)

enrollment_info = pd.DataFrame(data=pd.DataFrame.from_records([calculated_stats_pre_dist]))
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1',  startrow=32)

enrollment_info = pd.DataFrame(data=pd.DataFrame.from_records([calculated_financial_stats]))
enrollment_info = enrollment_info.fillna(0)
enrollment_info.to_excel(writer, sheet_name='sheet1',  startrow=35)


writer.save()
