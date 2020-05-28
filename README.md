# PS-120-research-project
This repo contains the datasets and python code that was used to generate the findings in our research paper for PS 120

School_district_board_racial_makeup.xlsx - This is the dataset that we collected for this project. It contains every school district in California that has countywide elections. Each school district in the dataset is catergorized by if it has at-large, pre-cvra, post-cvra, or at-large/but changing labels.

school_district_election_info.xlsx - This is the second dataset that we collected for this project. This dataset examines all the schools that we identified as post-CVRA and identifies there board members that served on the school board 6 years before the transition to district elections to the present. For each board member, we included their board tenure, ethnicity and gender.

school_district_t-test.xlsx - This excel sheet contains the t-test and p-values comparing each school district's racial makeup and gender representation on the board before and after the switch to district elections. 

expense data.xlsx - This excel sheet contains the average daily expense of each school district for the year of 2019-2020 in California. We use this excel spread sheet in our data analysis to see if there is a difference in the expenses of schools with at-large elections vs district elections.

schooldistrict_ethnicity_info.txt - This text file contains ethnicity information and enrollment size for the year of 2019-2020 for each school district in California.  We use this excel spread sheet in our data analysis to see if there is a difference in the enrollment size and racial makeup of schools with at-large elections vs district elections.

school_district_analysis.py - This python file performs the first data analysis for our project by computing the mean, median, and std of enrollment size, racial makeup, and expenses for at-large and distrct election schools.

school_district_board_analysis.py - This python file computes data analysis for seeing if the switch to district elections causes a change in the racial makeup of school boards. Also, this program is responsible for producing the plots for the project.

school_district_graphing_code.py - This python file is responsible for creating the plots in our research report.

